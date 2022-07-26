from common.project_actions import (
    shareTo, notification, getAssignNotification, getRevokeNotification, broadcastProject, broadcastDeleteProject)
from common.actions import (delete, allItems, filterRecords,
                            countStatuses, addAttachment, deleteAttachments, getAttachments, projectsOfUser)
from projects.api.project.serializers import ProjectSerializer, ProjectTrashedSerializer
from users.api.teams.serializers import LessFieldsTeamSerializer
from projects.api.serializers import ProjectNameListSerializer
from users.api.serializers import UserWithProfileSerializer
from common.permissions_scopes import ProjectPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from users.models import User, Team
from projects.models import Project
from rest_framework import status
from tasks.models import Task


class ProjectViewSet(Repository):
    model = Project
    queryset = Project.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProjectSerializer
    permission_classes = (ProjectPermissions,)
    serializer_action_classes = {
        "trashed": ProjectTrashedSerializer,
    }
    queryset_actions = {
        "destroy": Project.objects.all(),
        "trashed": Project.objects.all(),
        "restore": Project.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Project)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ProjectNameListSerializer, queryset)
        if request.GET.get("items_per_page") == "-2":
            return allItems(self.get_serializer, queryset)

        if request.GET.get("user_id"):
            return projectsOfUser(self, request, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
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
        data = getAttachments(request, data, project.id,
                              "project_attachments_v")
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
        broadcastProject(new_project, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = self.get_object()
        data = request.data
        if request.data.get("users") is not None:
            project.users.set(request.data.get("users"))
        if request.data.get("teams") is not None:
            project.teams.set(request.data.get("teams"))
        for key, value in data.items():
            if key != "users" and key != "teams" and key != "id":
                setattr(project, key, value)
        project.updated_by = request.user
        project.save()
        serializer = ProjectSerializer(
            project, context={"request": request})
        broadcastProject(project, serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        response = delete(self, request, Project)
        ids = []
        for id in response.data['deleted_ids']:
            ids.append(str(id))
        broadcastDeleteProject({'deleted_ids': ids})
        return response

    # Custom Actions
    @ action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        project = Project.objects.only('id').get(pk=pk)
        users = User.objects.filter(project_users=project)
        if request.query_params.get('content'):
            columns = ['first_name', 'last_name', 'email']
            users = filterRecords(users, request, columns, table=User)
            serializer = UserWithProfileSerializer(
                users, many=True,  context={"request": request})
            return Response(serializer.data)

        page = self.paginate_queryset(users)
        serializer = UserWithProfileSerializer(
            page, many=True,  context={"request": request})
        return self.get_paginated_response(serializer.data)

    @ action(detail=True, methods=["get"])
    def teams(self, request, pk=None):
        project = Project.objects.only('id').get(pk=pk)
        teams = Team.objects.filter(projects=project)
        if request.query_params.get('content'):
            columns = ['name']
            teams = filterRecords(teams, request, columns, table=Team)
            serializer = LessFieldsTeamSerializer(
                teams, many=True, context={"request": request})
            return Response(serializer.data)
        page = self.paginate_queryset(teams)
        serializer = LessFieldsTeamSerializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    @ action(detail=True, methods=["post"])
    def add_users(self, request, pk=None):
        try:
            data = request.data
            project = self.get_object()
            users = User.objects.filter(pk__in=data['ids'])
            for user in data['ids']:
                project.users.add(user)
            notification(getAssignNotification, project,
                         request, 'pk__in', data['ids'])
            serializer = UserWithProfileSerializer(
                users, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["post"])
    def add_teams(self, request, pk=None):
        try:
            data = request.data
            project = self.get_object()
            teams = Team.objects.filter(pk__in=data['ids'])
            for user in data['ids']:
                project.teams.add(user)
            notification(getAssignNotification,
                         project, request, 'teams__in', data['ids'])
            serializer = LessFieldsTeamSerializer(
                teams, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["delete"])
    def delete_users(self, request, pk=None):
        try:
            project = self.get_object()
            data = request.data
            for user in data['ids']:
                project.users.remove(user)
            notification(getRevokeNotification, project,
                         request, 'pk__in', data['ids'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["delete"])
    def delete_teams(self, request, pk=None):
        try:
            project = self.get_object()
            data = request.data
            for team in data['ids']:
                project.teams.remove(team)
            notification(getRevokeNotification,
                         project, request, 'teams__in', data['ids'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        return addAttachment(self, request)

    @ action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @ action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        users = User.objects.filter(
            deleted_at__isnull=True).exclude(project_users=pk).order_by("-created_at")
        serializer = UserWithProfileSerializer(
            users, many=True,  context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @ action(detail=True, methods=["get"])
    def excluded_teams(self, request, pk=None):
        teams = Team.objects.filter(deleted_at__isnull=True).exclude(
            projects__id=pk).order_by("-created_at")
        serializer = LessFieldsTeamSerializer(
            teams, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
