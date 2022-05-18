import re
from rest_framework import viewsets, status
from projects.models import Project
from users.models import User, Team
from projects.api.projects.serializers import (
    ProjectListSerializer,
    ProjectCreateSerializer,
    ProjectTasksSerializer,
    ProjectUpdateSerializer,
)
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    serializer_action_classes = {
        "create": ProjectCreateSerializer,
        "update": ProjectUpdateSerializer,
    }

    def create(self, request):
        project_data = request.data
        project_data["created_by"] = request.user
        project_data["updated_by"] = request.user
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

    def update(self, request, pk=None):
        project = self.get_object()
        if request.data.get("name"):
            project.name = request.data.get("name")
        if request.data.get("description"):
            project.description = request.data.get("description")
        if request.data.get("p_start_date"):
            project.p_start_date = request.data.get("p_start_date")
        if request.data.get("p_end_date"):
            project.p_end_date = request.data.get("p_end_date")
        if request.data.get("a_start_date"):
            project.a_start_date = request.data.get("a_start_date")
        if request.data.get("a_end_date"):
            project.a_end_date = request.data.get("a_end_date")
        if request.data.get("status"):
            project.status = request.data.get("status")
        if request.data.get("progress"):
            project.progress = request.data.get("progress")
        if request.data.get("priority"):
            project.priority = request.data.get("priority")
        if request.data.get("company_name"):
            project.company_name = request.data.get("company_name")
        if request.data.get("company_email"):
            project.company_email = request.data.get("company_email")
        if request.data.get("users"):
            users = User.objects.filter(pk__in=request.data.get("users"))
            project.users.set(users)
        if request.data.get("teams"):
            teams = Team.objects.filter(pk__in=request.data.get("teams"))
            project.teams.set(teams)
        project.updated_by = request.user
        project.save()
        serializer = ProjectListSerializer(project)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

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
