from rest_framework import viewsets, status
from projects.models import Project
from users.models import User, Team
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

    def create(self, request, *args, **kwargs):
        project_data = request.data
        # request.data._mutable = True
        project_data["created_by"] = request.user
        project_data["updated_by"] = request.user
        # request.data._mutable = False
        new_project = Project.objects.create(
            name=project_data["name"],
            p_start_date=project_data["p_start_date"],
            p_end_date=project_data["p_end_date"],
            created_by=project_data["created_by"],
            updated_by=project_data["updated_by"],
        )
        users = User.objects.filter(pk__in=project_data["users"])
        new_project.users.set(users)
        teams = Team.objects.filter(pk__in=project_data["teams"])
        new_project.teams.set(teams)
        new_project.save()
        serializer = ProjectListSerializer(new_project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # serializer = ProjectCreateSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data["created_by"] = request.user
        #     serializer.validated_data["updated_by"] = request.user
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectTasksSerializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def tasks(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectTasksSerializer(project)
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
