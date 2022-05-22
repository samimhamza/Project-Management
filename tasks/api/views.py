from rest_framework import viewsets, status
from projects.models import Project
from tasks.models import Task
from tasks.api.serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskNameSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from common.custom import CustomPageNumberPagination
from django.db import transaction
import datetime


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
        data = request.data
        if data:
            Tasks = Task.objects.filter(pk__in=data["ids"])
            for Task in Tasks:
                if Task.deleted_at:
                    Task.delete()
                else:
                    Task.deleted_at = datetime.datetime.now()
                    Task.save()
        else:
            Task = self.get_object()
            if Task.deleted_at:
                Task.delete()
            else:
                Task.deleted_at = datetime.datetime.now()
                Task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def all(self, request):
        queryset = Task.objects.all().order_by("-created_at")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        queryset = self.filter_queryset(
            Task.objects.filter(deleted_at__isnull=False).order_by("-deleted_at")
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        try:
            with transaction.atomic():
                data = request.data
                Tasks = Task.objects.filter(pk__in=data["ids"])
                for Task in Tasks:
                    Task.deleted_at = None
                    Task.save()
                page = self.paginate_queryset(Tasks)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

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
