from rest_framework import viewsets
from projects.models import Project
from projects.api.projects.serializers import (
    ProjectListSerializer,
    ProjectCreateSerializer,
    ProjectTasksSerializer,
)
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    serializer_action_classes = {
        "create": ProjectCreateSerializer,
    }

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectTasksSerializer(project)
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
