from projects.models import Project
from tasks.api.serializers import (
    TaskSerializer, LessFieldsTaskSerializer, CommentSerializer, TaskListSerializer, TaskTrashedSerializer)
from common.permissions_scopes import TaskPermissions, ProjectCommentPermissions, TaskCommentPermissions
from tasks.actions import (
    delete_dependencies, excluded_users, progress, tasksOfProject, tasksResponse, create, update, calculateUsersPerformance, taskProgressCalculator)
from common.comments import listComments, createComments, updateComments, broadcastDeleteComment
from common.actions import (
    delete, allItems, filterRecords, addAttachment, deleteAttachments, getAttachments)
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from common.Repository import Repository
from tasks.models import Task, Comment
from users.models import User


class TaskViewSet(Repository):
    model = Task
    queryset = Task.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TaskSerializer
    permission_classes = (TaskPermissions,)
    serializer_action_classes = {
        "retrieve": TaskListSerializer,
        "update": TaskListSerializer,
        "trashed": TaskTrashedSerializer
    }
    queryset_actions = {
        "destroy": Task.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Task)
        if request.GET.get("project_id"):
            return tasksOfProject(self, request, queryset)
        if request.GET.get("items_per_page") == "-1":
            return allItems(LessFieldsTaskSerializer, queryset)
        if request.GET.get("items_per_page") == "-2":
            return allItems(self.get_serializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return tasksResponse(self, serializer)

    def retrieve(self, request, pk=None):
        task = self.get_object()
        return Response(taskProgressCalculator(task))
        serializer = self.get_serializer(
            task, context={"request": request})
        data = serializer.data
        data = getAttachments(request, data, task.id, "task_attachments_v")
        return Response(data)

    def create(self, request):
        return create(request)

    def update(self, request, pk=None):
        task = self.get_object()
        return update(self, request, task)

    @action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        task = self.get_object()
        return excluded_users(self, task)

    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        task = self.get_object()
        return delete_dependencies(request, task)

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            task = self.get_object()
            return addAttachment(request, task)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @action(detail=True, methods=["put"])
    def progress(self, request, pk=None):
        try:
            task = self.get_object()
            return progress(request, task)
        except:
            return Response({'error': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def employee_task_report(self, request, pk=None):
        users = ''
        if request.query_params.get('project_id'):
            user_ids = Project.objects.filter(pk = request.GET['project_id']).values_list('users')
            users = User.objects.filter(deleted_at__isnull=True,pk__in=user_ids)
            return Response(calculateUsersPerformance(users,request.GET['project_id']))
        else:
            if request.query_params.get('user_id'):
                users = User.objects.filter(pk=request.GET['user_id'])  
            else:
                user_ids = Project.objects.values_list('users')
                users = User.objects.filter(deleted_at__isnull=True,pk__in=user_ids)[:10]
            return Response(calculateUsersPerformance(users))



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
