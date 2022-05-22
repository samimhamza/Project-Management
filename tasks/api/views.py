from rest_framework import viewsets, status
from projects.models import Project
from tasks.models import Task
from tasks.api.serializers import TaskCreateSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from common.custom import CustomPageNumberPagination
from common.actions import withTrashed, trashList, delete, restore


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "create": TaskCreateSerializer,
    }
    queryset_actions = {
        "delete_user": Task.objects.all(),
    }

    def create(self, request):
        data = request.data
        # data["created_by"] = request.user
        # data["updated_by"] = request.user
        new_Task = Task.objects.create(
            name=data["name"],
            description=data["description"],
            # created_by=data["created_by"],
            # updated_by=data["updated_by"],
        )
        new_Task.save()
        serializer = TaskSerializer(new_Task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        Task = self.get_object()
        if request.data.get("name"):
            Task.name = request.data.get("name")
        if request.data.get("description"):
            Task.description = request.data.get("description")
        if request.data.get("Task_projects"):
            Tasks = Project.objects.filter(pk__in=request.data.get("Task_projects"))
            Task.Task_projects.set(Tasks)
        # Task.updated_by = request.user
        Task.save()
        serializer = TaskSerializer(Task)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Task)

    @action(detail=False, methods=["get"])
    def all(self, request):
        serializer = withTrashed(self, Task, order_by="-created_at")
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Task)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Task)

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
