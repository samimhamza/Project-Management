from tasks.api.serializers import TaskSerializer, LessFieldsTaskSerializer
from common.actions import withTrashed, trashList, delete, restore, allItems
from common.tasks_actions import tasksOfProject, tasksResponse
from common.custom import CustomPageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from tasks.models import Task
from projects.models import Project


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination

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
        return tasksResponse(self, serializer)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        data["updated_by"] = request.user
        if data['parent']:
            parent = Task.objects.only('id').get(pk=data['parent'])
        else:
            parent = None
        if data['project']:
            project = Project.objects.only('id').get(pk=data['project'])
        else:
            project = None
        new_Task = Task.objects.create(
            parent=parent,
            name=data["name"],
            p_start_date=data["p_start_date"],
            p_end_date=data["p_end_date"],
            description=data["description"],
            project=project,
            created_by=data["created_by"],
            updated_by=data["updated_by"],
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
        Task.updated_by = request.user
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

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
