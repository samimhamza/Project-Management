from common.project_actions import (
    notification, getRevokeNotification, update, retrieve, add_users, add_teams, members)
from common.actions import (allItems, filterRecords, addAttachment,
                            deleteAttachments, projectsOfUser)
from users.api.teams.serializers import LessFieldsTeamSerializer
from projects.api.project.serializers import ProjectSerializer
from projects.api.serializers import ProjectNameListSerializer
from users.api.serializers import UserWithProfileSerializer
from rest_framework.permissions import IsAuthenticated
from common.permissions import checkProjectScope
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from users.models import User, Team
from projects.models import Project
from rest_framework import status


class MyProjectViewSet(Repository):
    model = Project
    queryset = Project.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    serializer_action_classes = {}
    queryset_actions = {
        "destroy": Project.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset().filter(users=request.user)
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
        try:
            project = Project.objects.get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return retrieve(self, request, project, showPermission=True)

    def create(self, request):
        return Response({
            "detail": "You do not have permission to perform this action."
        }, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkProjectScope(request.user, project, "project_u"):
            return update(self, request, project)
        else:
            return Response({
                "detail": "You do not have permission to perform this action."
            }, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return Response({
            "detail": "You do not have permission to perform this action."
        }, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"])
    def add_users(self, request, pk=None):
        return members(add_users, request, pk)

    @action(detail=True, methods=["post"])
    def add_teams(self, request, pk=None):
        return members(add_teams, request, pk)

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
