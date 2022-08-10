from common.comments import comments, destroy, listComments, createComments, updateComments
from common.actions import (
    addAttachment, deleteAttachments, getAttachments, filterRecords, unAuthorized)
from tasks.actions import (
    delete_dependencies, excluded_users, progress, tasksOfProject, create, update)
from tasks.api.serializers import (
    TaskSerializer, CommentSerializer, TaskListSerializer, TaskTrashedSerializer)
from rest_framework.permissions import IsAuthenticated
from common.custom import CustomPageNumberPagination
from common.permissions import checkProjectScope
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from common.Repository import Repository
from tasks.models import Task, Comment


class MyTaskViewSet(Repository):
    model = Task
    queryset = Task.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
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
        if request.GET.get("project_id"):
            if checkProjectScope(request.user, None, "project_tasks_v", project_id=request.GET.get("project_id")):
                queryset = filterRecords(queryset, request, table=Task)
                return tasksOfProject(self, request, queryset)
            else:
                return unAuthorized()
        return unAuthorized()

    def retrieve(self, request, pk=None):
        task = self.get_object()
        if checkProjectScope(request.user, task.project, "project_tasks_v"):
            serializer = self.get_serializer(
                task, context={"request": request})
            data = serializer.data
            data = getAttachments(request, data, task.id,
                                  "task_attachments_v", project=task.project)
            return Response(data)
        else:
            return unAuthorized()

    def create(self, request):
        if checkProjectScope(request.user, None, "project_tasks_c", project_id=request.data.get("project")):
            return create(request)
        else:
            return unAuthorized()

    def update(self, request, pk=None):
        task = self.get_object()
        if checkProjectScope(request.user, task.project, "project_tasks_u"):
            return update(self, request, task, task.project)
        else:
            return unAuthorized()

    @action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        task = self.get_object()
        if checkProjectScope(request.user, task.project, "project_tasks_v"):
            return excluded_users(self, task)
        else:
            return unAuthorized()

    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        task = self.get_object()
        if checkProjectScope(request.user, task.project, "project_tasks_u"):
            return delete_dependencies(request, task)
        else:
            return unAuthorized()

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            task = self.get_object()
            if checkProjectScope(request.user, task.project, "task_attachments_c"):
                return addAttachment(request, task)
            else:
                return unAuthorized()
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        task = self.get_object()
        if checkProjectScope(request.user, task.project, "task_attachments_d"):
            return deleteAttachments(self, request)
        else:
            return unAuthorized()

    @action(detail=True, methods=["put"])
    def progress(self, request, pk=None):
        try:
            task = self.get_object()
            if checkProjectScope(request.user, task.project, "project_tasks_u"):
                return progress(request, task)
            else:
                return unAuthorized()
        except:
            return Response({'error': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyProjectCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        return comments(self, listComments, request, "project_comments_v")

    def create(self, request):
        return comments(self, createComments, request, "project_comments_c")

    def update(self, request, pk=None):
        return updateComments(self, request, pk)

    def destroy(self, request, pk=None):
        return destroy(self, request)


class MyTaskCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return comments(self, listComments, request, "task_comments_v")

    def create(self, request):
        return comments(self, createComments, request, "task_comments_c")

    def update(self, request, pk=None):
        return updateComments(self, request, pk)

    def destroy(self, request, pk=None):
        return destroy(self, request)
