from rest_framework import viewsets, status
from projects.models import Project
from users.models import User, Team
from projects.api.project.serializers import (
    ProjectListSerializer,
    ProjectCreateSerializer,
    ProjectTasksSerializer,
    ProjectTasksListSerializer,
    ProjectUpdateSerializer,
    ProjectExpensesSerializer,
)
from projects.api.serializers import ProjectNameListSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from common.custom import CustomPageNumberPagination
from common.actions import restore, delete, withTrashed, trashList

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
    queryset = Project.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProjectListSerializer
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "create": ProjectCreateSerializer,
        "update": ProjectUpdateSerializer,
    }
    queryset_actions = {
        "destroy": Project.objects.all(),
        "trashed": Project.objects.all(),
        "restore": Project.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        if request.GET.get("items_per_page") == "-1":
            serializer = ProjectNameListSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        project_data = request.data
        # project_data["created_by"] = request.user
        # project_data["updated_by"] = request.user
        new_project = Project.objects.create(
            name=project_data["name"],
            p_start_date=project_data["p_start_date"],
            p_end_date=project_data["p_end_date"],
            # created_by=project_data["created_by"],
            # updated_by=project_data["updated_by"],
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
        # project.updated_by = request.user
        project.save()
        serializer = ProjectListSerializer(project)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Project)

    @action(detail=False, methods=["get"])
    def all(self, request):
        serializer = withTrashed(self, Project, order_by="-created_at")
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Project)

    # for multi and single restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Project)

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectTasksSerializer(project)
        return self.get_paginated_response(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def tasks_list(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectTasksListSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    # testing APIS
    @action(detail=True, methods=["get"])
    def expenses(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectExpensesSerializer(project)

        return Response(serializer.data, status=status.HTTP_200_OK)
