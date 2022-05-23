from rest_framework import viewsets, status
from tasks.models import Task
from tasks.api.serializers import TaskCreateSerializer, TaskSerializer, LessFieldsTaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from common.custom import CustomPageNumberPagination
from common.actions import withTrashed, trashList, delete, restore, allItems
from projects.models import Project


def tasksOfProject(self, request):
    queryset = Task.objects.filter(
        project=request.GET.get("project_id"))
    if request.GET.get("items_per_page") == "-1":
        return allItems(LessFieldsTaskSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "create": TaskCreateSerializer,
    }
    queryset_actions = {
        "destroy": Task.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()

        if request.GET.get("project_id"):
            return tasksOfProject(self, request)

        if request.GET.get("items_per_page") == "-1":
            return allItems(LessFieldsTaskSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        # data["created_by"] = request.user
        # data["updated_by"] = request.user
        new_Task = Task.objects.create(
            parent=data["parent"],
            name=data["name"],
            p_start_date=data["p_start_date"],
            p_end_date=data["p_end_date"],
            description=data["description"],
            # created_by=data["created_by"],
            # updated_by=data["updated_by"],
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
        # Task.updated_by = request.user
        task.save()
        serializer = TaskSerializer(Task)
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
