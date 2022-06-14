from common.actions import (restore, delete, withTrashed, trashList,
                            allItems, filterRecords, countStatuses, searchRecords, addAttachment, deleteAttachments)
from projects.api.serializers import ProjectNameListSerializer, AttachmentSerializer
from users.api.teams.serializers import LessFieldsTeamSerializer
from projects.api.project.serializers import ProjectSerializer
from users.api.serializers import UserWithProfileSerializer
from common.permissions_scopes import ProjectPermissions
from common.permissions import checkCustomPermissions
from common.custom import CustomPageNumberPagination
from projects.models import Project, Attachment
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from users.models import User, Team
from tasks.models import Task
from common.notification import sendNotification


def shareTo(request, project_data, new_project):
    if project_data["share"] != "justMe":
        users = User.objects.only('id').filter(pk__in=project_data["users"])
        new_project.users.set(users)
        teams = Team.objects.only('id').filter(pk__in=project_data["teams"])
        new_project.teams.set(teams)
    if project_data["share"] == "everyone":
        users = User.objects.all()
        new_project.users.set(users)
    sendNotification(request, users, project_data, new_project)
    return new_project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProjectSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ProjectPermissions,)
    serializer_action_classes = {}
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

    def retrieve(self, request, pk=None):
        project = self.get_object()
        serializer = self.get_serializer(project)
        data = serializer.data
        countables = [
            'pendingTasksTotal', 'status', 'pending',
            'inProgressTasksTotal', 'status', 'in_progress',
            'completedTasksTotal', 'status', 'completed',
            'issuFacedTasksTotal', 'status', 'issue_faced',
            'failedTasksTotal', 'status', 'failed',
            'cancelledTasksTotal', 'status', 'cancelled'
        ]
        # custom permission checking for project_attachments
        attachments_permission = checkCustomPermissions(
            request, "project_attachments_v")
        if attachments_permission:
            attachments = Attachment.objects.filter(object_id=project.id)
            data['attachments'] = AttachmentSerializer(
                attachments, many=True, context={"request": request}).data

        data['statusTotals'] = countStatuses(Task, countables, project.id)
        return Response(data)

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
        serializer = ProjectSerializer(
            new_project, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = self.get_object()
        if request.data.get("name"):
            project.name = request.data.get("name")
        if request.data.get("description") is not None:
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
        if request.data.get("company_name") is not None:
            project.company_name = request.data.get("company_name")
        if request.data.get("company_email") is not None:
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
        serializer = ProjectSerializer(
            project, context={"request": request})
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
        if request.query_params.get('content'):
            columns = ['first_name', 'last_name', 'email']
            users = searchRecords(users, request, columns)
            serializer = UserWithProfileSerializer(users, many=True)
            return Response(serializer.data)

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
        if request.query_params.get('content'):
            columns = ['name']
            teams = searchRecords(teams, request, columns)
            serializer = LessFieldsTeamSerializer(teams, many=True)
            return Response(serializer.data)

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

    @action(detail=True, methods=["delete"])
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
        return addAttachment(self, request)

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @ action(detail=True, methods=["delete"])
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
