from tasks.api.serializers import TaskSerializer, LessFieldsTaskSerializer, CommentSerializer
from common.actions import withTrashed, trashList, delete, restore, allItems, filterRecords
from common.permissions_scopes import TaskPermissions, CommentPermissions
from common.tasks_actions import tasksOfProject, tasksResponse, checkAttributes
from common.custom import CustomPageNumberPagination
from common.comments import commentsOfProject, checkCommnetable
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from tasks.models import Task, Comment
from projects.models import Attachment


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (TaskPermissions,)
    queryset_actions = {
        "destroy": Task.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("project_id"):
            return tasksOfProject(self, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(LessFieldsTaskSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return tasksResponse(self, serializer)

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
        if request.data.get("name"):
            task.name = request.data.get("name")
        if request.data.get("description"):
            task.description = request.data.get("description")
        if request.data.get("p_start_date"):
            task.p_start_date = request.data.get("p_start_date")
        if request.data.get("p_end_date"):
            task.p_end_date = request.data.get("p_end_date")
        if request.data.get("a_start_date"):
            task.a_start_date = request.data.get("a_start_date")
        if request.data.get("a_end_date"):
            task.a_end_date = request.data.get("a_end_date")
        if request.data.get("status"):
            task.status = request.data.get("status")
        if request.data.get("progress"):
            task.progress = request.data.get("progress")
        if request.data.get("priority"):
            task.priority = request.data.get("priority")
        task.updated_by = request.user
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Task)

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

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (CommentPermissions,)

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("id"):
            return commentsOfProject(self, request)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        commentable = checkCommnetable(request)
        if commentable:
            comment = Comment.objects.create(
                body=data['body'],
                commented_by=request.user,
                content_object=commentable
            )
            if request.data.get("attachments"):
                for attachment in data['attachments']:
                    Attachment.objects.create(
                        content_object=comment,
                        attachment=attachment['file'],
                        name=attachment['file'])
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Object id is not correct'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        comment = self.get_object()
        comment.body = request.data.get('body')
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Comment)
