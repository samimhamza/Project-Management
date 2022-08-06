from projects.actions import (destroy, excluded_members, excluded_teams, excluded_users, list, update,
                              retrieve, add_users, add_teams, my_project_member_actions, users, teams,
                              delete_users, delete_teams, attachments)
from common.actions import (addAttachment, deleteAttachments, unAuthorized)
from projects.api.project.serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from common.permissions import checkProjectScope
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
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
        return list(self, request, queryset, showPermissions=True)

    def retrieve(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return retrieve(self, request, project, showPermission=True)

    def create(self, request):
        return unAuthorized()

    def update(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkProjectScope(request.user, project, "projects_u"):
            return update(self, request, project)
        else:
            return unAuthorized()

    def destroy(self, request, pk=None):
        if len(request.data["ids"]) > 0:
            return unAuthorized()
        if checkProjectScope(request.user, "projects_d", pk):
            return destroy(self, request)
        else:
            return unAuthorized()

    @ action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        try:
            project = Project.objects.only('id').get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return users(self, request, project)

    @ action(detail=True, methods=["get"])
    def teams(self, request, pk=None):
        try:
            project = Project.objects.only('id').get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return teams(self, request, project)

    @action(detail=True, methods=["post"])
    def add_users(self, request, pk=None):
        return my_project_member_actions(add_users, request, pk)

    @action(detail=True, methods=["post"])
    def add_teams(self, request, pk=None):
        return my_project_member_actions(add_teams, request, pk)

    @action(detail=True, methods=["delete"])
    def delete_users(self, request, pk=None):
        return my_project_member_actions(delete_users, request, pk)

    @action(detail=True, methods=["delete"])
    def delete_teams(self, request, pk=None):
        return my_project_member_actions(delete_teams, request, pk)

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        return attachments(addAttachment, "project_attachments_c", request, pk)

    @action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        try:
            project = Project.objects.only(
                'id').get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkProjectScope(request.user, project, "project_attachments_d"):
            return deleteAttachments(self, request)
        else:
            return unAuthorized()

    @action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        return excluded_members(excluded_users, request, pk)

    @action(detail=True, methods=["get"])
    def excluded_teams(self, request, pk=None):
        return excluded_members(excluded_teams, request, pk)
