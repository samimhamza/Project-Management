from .actions import get_total_users, get_total, get_leader_by_id, get_leader
from common.actions import allItems, filterRecords, teamsOfUser
from projects.api.serializers import ProjectNameListSerializer
from users.api.serializers import UserWithProfileSerializer
from common.permissions_scopes import TeamPermissions
from rest_framework.generics import get_object_or_404
from users.models import User, Team, TeamUser
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from users.api.teams.serializers import (
    TeamListSerializer,
    TeamUserSerializer,
    TeamNamesSerializer,
    TeamRetieveSerializer,
    ProjectTeamSerializer,
    TeamTrashedSerializer,
    TeamUserDetailSerializer
)
from projects.models import Project
from django.db import transaction
from rest_framework import status


class TeamViewSet(Repository):
    model = Team
    queryset = Team.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TeamListSerializer
    permission_classes = (TeamPermissions,)
    serializer_action_classes = {
        "retrieve": TeamRetieveSerializer,
        "update": TeamRetieveSerializer,
        "add_project": ProjectTeamSerializer,
        "trashed": TeamTrashedSerializer
    }
    queryset_actions = {
        "destroy": Team.objects.all(),
        "delete_user": Team.objects.all(),
    }

    def list(self, request):
        queryset = self.filter_queryset(
            Team.objects.filter(
                deleted_at__isnull=True).order_by("-created_at")
        )
        columns = ['name']
        queryset = filterRecords(queryset, request, columns, table=Team)
        if request.GET.get("user_id"):
            return teamsOfUser(self, request, queryset)
        if request.GET.get("items_per_page") == "-1":
            return allItems(TeamNamesSerializer, queryset)
        if request.GET.get("items_per_page") == "-2":
            return allItems(self.get_serializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        for team in serializer.data:
            team["total_members"] = get_total_users(team["id"])
            team["leader"] = get_leader_by_id(team["id"], request)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        team = self.get_object()
        serializer = self.get_serializer(team)
        data = serializer.data
        data["total_members"] = get_total(team)
        data["leader"] = get_leader(team, request)
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        if "description" in data:
            description = data["description"]
        else:
            description = ""
        new_team = Team.objects.create(
            name=data["name"],
            description=description,
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        if request.data.get("team_leader"):
            user = get_object_or_404(User, pk=request.data.get("team_leader"))
            TeamUser.objects.create(
                user=user, team=new_team, is_leader=True, position="Leader"
            )
        serializer = TeamListSerializer(new_team, context={"request": request})
        data = serializer.data
        data["total_members"] = get_total(new_team)
        data["leader"] = get_leader(new_team, request)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        team = self.get_object()
        if "projects" in request.data:
            team.projects.set(request.data.get("projects"))
        for key, value in request.data.items():
            if key != "projects":
                setattr(team, key, value)
        team.updated_by = request.user
        team.save()
        serializer = self.get_serializer(team)
        data = serializer.data
        data["total_members"] = get_total(team)
        data["leader"] = get_leader(team, request)
        return Response(data, status=status.HTTP_202_ACCEPTED)

    # Custom Actions
    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        team = self.get_object()
        users = User.objects.filter(deleted_at__isnull=True, teams=team)
        page = self.paginate_queryset(users)
        serializer = UserWithProfileSerializer(
            page, many=True, context={"request": request})
        for user in serializer.data:
            team_user = TeamUser.objects.get(user=user['id'], team=team)
            team_user_serializer = TeamUserSerializer(
                team_user)
            user['is_leader'] = team_user_serializer.data['is_leader']
            user['position'] = team_user_serializer.data['position']
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None):
        try:
            data = request.data
            team = self.get_object()
            user = User.objects.get(pk=data["id"])
            userData = UserWithProfileSerializer(
                user, context={"request": request}).data
            team_user, created = TeamUser.objects.get_or_create(
                team=team, user=user)
            team_user.position = data["position"]
            team_user.save()
            team_user_serializer = TeamUserSerializer(team_user)
            userData['is_leader'] = team_user_serializer.data['is_leader']
            userData['position'] = team_user_serializer.data['position']
            return Response(userData, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        users = User.objects.filter(
            deleted_at__isnull=True).exclude(teams__id=pk).order_by("-created_at")
        serializer = UserWithProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def excluded_projects(self, request, pk=None):
        projects = Project.objects.filter(deleted_at__isnull=True).exclude(
            teams__id=pk).order_by("-created_at")

        serializer = ProjectNameListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_project(self, request, pk=None):
        try:
            data = request.data
            team = self.get_object()
            team.projects.set(data["ids"])
            serializer = self.get_serializer(team)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def delete_users(self, request, pk=None):
        try:
            with transaction.atomic():
                team = self.get_object()
                data = request.data
                if request.data.get("ids"):
                    team_users = TeamUser.objects.filter(
                        team=team, user__in=data["ids"]
                    )
                    for team_user in team_users:
                        team_user.delete()
                elif request.data.get("id"):
                    team_user = TeamUser.objects.get(
                        team=team, user=data["id"])
                    team_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )
