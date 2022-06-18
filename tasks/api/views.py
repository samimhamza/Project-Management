from tasks.api.serializers import TaskSerializer, LessFieldsTaskSerializer, CommentSerializer, TaskListSerializer
from common.permissions_scopes import TaskPermissions, ProjectCommentPermissions, TaskCommentPermissions
from common.tasks_actions import tasksOfProject, tasksResponse, checkAttributes, excludedDependencies
from common.actions import (withTrashed, trashList, delete, restore,
                            allItems, filterRecords, addAttachment, deleteAttachments, getAttachments)
from common.comments import listComments, createComments, updateComments, broadcastDeleteComment
from users.api.serializers import UserWithProfileSerializer
from common.custom import CustomPageNumberPagination
from tasks.api.serializers import ProgressSerializer
from common.notification import sendNotification
from tasks.models import Task, Comment, UserTask
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from common.pusher import pusher_client
from users.models import User


def broadcastProgress(task_id, data, user_id):
    pusher_client.trigger(
        u'task.'+str(task_id), u'progress', {
            "progress": data['progress'],
            'user_id': user_id,
        })


def getNotificationData(data, request):
    data = {
        'title': 'Task Assignment',
        'description': ("Task " + str(data.name) + " has assigned to you by " +
                        str(request.user.first_name) + " " + str(request.user.last_name)),
        # 'instance_id': data.id,
        'model_name': "projects/"+str(data.project.id) + '/tasks/'
    }
    return data


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (TaskPermissions,)
    serializer_action_classes = {
        "retrieve": TaskListSerializer,
        "update": TaskListSerializer
    }
    queryset_actions = {
        "destroy": Task.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("project_id"):
            return tasksOfProject(self, request)
        if request.GET.get("items_per_page") == "-1":
            if request.GET.get("excluded_dependencies"):
                return excludedDependencies(LessFieldsTaskSerializer, queryset, request)
            return allItems(LessFieldsTaskSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return tasksResponse(self, serializer)

    def retrieve(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(
            task, context={"request": request})
        data = serializer.data
        data = getAttachments(request, data, task.id, "task_attachments_v")
        return Response(data)

    def create(self, request):
        [name, parent, project, start_date, end_date, description,
            priority, task_status, creator] = checkAttributes(request)
        new_Task = Task.objects.create(
            parent=parent,
            name=name,
            p_start_date=start_date,
            p_end_date=end_date,
            description=description,
            project=project,
            created_by=creator,
            updated_by=creator,
            priority=priority,
            status=task_status,
        )
        new_Task.save()
        serializer = TaskSerializer(new_Task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        task = self.get_object()
        if "dependencies" in request.data:
            if task.dependencies is not None:
                task.dependencies = task.dependencies + \
                    list(set(request.data.get("dependencies")) -
                         set(task.dependencies))
            else:
                task.dependencies = request.data.get("dependencies")
        if "users" in request.data:
            users = User.objects.filter(pk__in=request.data.get('users'))
            UserTask.objects.filter(task=task).delete()
            for user in users:
                userTask, created = UserTask.objects.get_or_create(
                    task=task, user=user)
                userTask.created_by = request.user
                userTask.updated_by = request.user
                userTask.save()
            if len(request.data.get('users')) > 0:
                users = User.objects.only('id').filter(
                    pk__in=request.data.get('users'))
                data = getNotificationData(
                    task, request)
                sendNotification(request, users, data)
        for key, value in request.data.items():
            if key != "users" and key != "dependencies" and key != "id":
                setattr(task, key, value)
        task.updated_by = request.user
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Task)

    @action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        task = self.get_object()
        users = User.objects.filter(
            project_users=task.project).exclude(users=task)
        serializer = UserWithProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        task = self.get_object()
        task.dependencies.remove(request.data.get('id'))
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Task, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Task)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Task)

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        return addAttachment(self, request)

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @action(detail=True, methods=["put"])
    def progress(self, request, pk=None):
        try:
            task = self.get_object()
            data = request.data
            user = User.objects.get(pk=data['user_id'])
            userTask = UserTask.objects.get(user=user, task=task)
            userTask.progress = data['progress']
            userTask.save()
            serializer = ProgressSerializer(
                userTask)
            broadcastProgress(task.id, serializer.data, data['user_id'])
            return Response(serializer.data)
        except:
            return Response({'error': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()


class ProjectCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ProjectCommentPermissions, )

    def list(self, request):
        return listComments(self, request)

    def create(self, request):
        return createComments(self, request)

    def update(self, request, pk=None):
        return updateComments(self, request, pk)

    def destroy(self, request, pk=None):
        response = delete(self, request, Comment)
        broadcastDeleteComment(response.data)
        return response


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (TaskCommentPermissions,)

    def list(self, request):
        return listComments(self, request)

    def create(self, request):
        return createComments(self, request)

    def update(self, request, pk=None):
        return updateComments(self, request, pk)

    def destroy(self, request, pk=None):
        response = delete(self, request, Comment)
        broadcastDeleteComment(response.data)
        return response
