from projects.api.project.serializers import ProjectListSerializer, ProjectRetirieveSerializer
from common.actions import restore, delete, withTrashed, trashList, allItems, filterRecords
from projects.api.serializers import ProjectNameListSerializer, AttachmentSerializer
from users.api.teams.serializers import LessFieldsTeamSerializer
from users.api.serializers import UserWithProfileSerializer
from common.permissions_scopes import ProjectPermissions
from common.custom import CustomPageNumberPagination
from rest_framework import viewsets, status
from projects.models import Project, Attachment
from users.models import User, Team
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import User, Team
from rest_framework import viewsets, status
from projects.models import Project
import os
from pathlib import Path

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
    permission_classes = (ProjectPermissions,)

    queryset_actions = {
        "destroy": Project.objects.all(),
        "trashed": Project.objects.all(),
        "restore": Project.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ProjectNameListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        project_data = request.data
        project_data["created_by"] = request.user
        new_project = Project.objects.create(
            name=project_data["name"],
            p_start_date=project_data["p_start_date"],
            p_end_date=project_data["p_end_date"],
            created_by=project_data["created_by"],
            updated_by=project_data["created_by"],
        )
        new_project = shareTo(request, project_data, new_project)
        new_project.save()
        serializer = ProjectListSerializer(new_project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectRetirieveSerializer(project)
        # for attachment in serializer.data['attachments']:
        #     attachment['size'] = os.path.getsize(
        #         Path(__file__).resolve().parent.parent. attachment['attachment'])
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            users = User.objects.only('id').filter(
                pk__in=request.data.get("users"))
            project.users.set(users)
        if request.data.get("teams"):
            teams = Team.objects.only('id').filter(
                pk__in=request.data.get("teams"))
            project.teams.set(teams)
        project.updated_by = request.user
        project.save()
        serializer = ProjectListSerializer(project)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Project)

    @ action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Project, order_by="-created_at")

    @ action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Project)

    # for multi and single restore
    @ action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Project)

    # Custom Actions
    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        project = Project.objects.only('id').get(pk=pk)
        users = User.objects.filter(project_users=project)
        page = self.paginate_queryset(users)
        serializer = UserWithProfileSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_users(self, request, pk=None):
        try:
            data = request.data
            project = self.get_object()
            users = User.objects.filter(pk__in=data['ids'])
            for user in data['ids']:
                project.users.add(user)
            serializer = UserWithProfileSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["get"])
    def teams(self, request, pk=None):
        project = Project.objects.only('id').get(pk=pk)
        teams = Team.objects.filter(projects=project)
        page = self.paginate_queryset(teams)
        serializer = LessFieldsTeamSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_teams(self, request, pk=None):
        try:
            data = request.data
            project = self.get_object()
            teams = Team.objects.filter(pk__in=data['ids'])
            for user in data['ids']:
                project.teams.add(user)
            serializer = LessFieldsTeamSerializer(teams, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        users = User.objects.filter(
            deleted_at__isnull=True).exclude(project_users=pk).order_by("-created_at")
        serializer = UserWithProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def excluded_teams(self, request, pk=None):
        teams = Team.objects.filter(deleted_at__isnull=True).exclude(
            projects__id=pk).order_by("-created_at")
        serializer = LessFieldsTeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def delete_users(self, request, pk=None):
        try:
            project = self.get_object()
            data = request.data
            for user in data['ids']:
                project.users.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            project = self.get_object()
            data = request.data
            attachment_obj = Attachment.objects.create(
                content_object=project,
                attachment=data['file'],
                name=data['file'])
            serializer = AttachmentSerializer(attachment_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["post"])
    def delete_teams(self, request, pk=None):
        try:
            project = self.get_object()
            data = request.data
            for team in data['ids']:
                project.teams.remove(team)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
