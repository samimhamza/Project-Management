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
from rest_framework.decorators import action
import datetime

# Sharing to Teams and Users
def shareTo(request, project_data, new_project):
    if request.data.get("share"):
        if project_data["share"] != "justMe":
            users = User.objects.filter(pk__in=project_data["users"])
            new_project.users.set(users)
            teams = Team.objects.filter(pk__in=project_data["teams"])
            new_project.teams.set(teams)
        if project_data["share"] == "everyone":
            users = User.objects.all()
            new_project.users.set(users)
    else:
        users = User.objects.filter(pk__in=project_data["users"])
        new_project.users.set(users)
        teams = Team.objects.filter(pk__in=project_data["teams"])
        new_project.teams.set(teams)
    return new_project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(deleted_at__isnull=True)
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
        new_project = shareTo(request, project_data, new_project)
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

    def destroy(self, request, pk=None):
        project = self.get_object()
        if project.deleted_at:
            project.delete()
        else:
            project.deleted_at = datetime.datetime.now()
            project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectTasksSerializer(project)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def all(self, request):
        queryset = Project.objects.all()
        serializer = ProjectListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        queryset = Project.objects.filter(deleted_at__isnull=False)
        serializer = ProjectListSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
