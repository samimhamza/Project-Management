from rest_framework import viewsets, status
from projects.models import Project
from users.models import User, Team, TeamUser
from users.api.teams.serializers import (
    TeamListSerializer,
    TeamCreateSerializer,
    TeamUserSerializer,
    TeamUpdateSerializer,
    UserTeamUserSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from taskmanager.custom_classes.custom import CustomPageNumberPagination
import datetime


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.filter(deleted_at__isnull=True)
    serializer_class = TeamListSerializer
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "create": TeamCreateSerializer,
        "update": TeamUpdateSerializer,
    }
    queryset_actions = {
        "destroy": Team.objects.all(),
        "trashed": Team.objects.all(),
        "restore": Team.objects.all(),
    }

    def list(self, request):
        queryset = self.filter_queryset(
            Team.objects.filter(deleted_at__isnull=True).order_by("created_at")
        )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        for team in serializer.data:
            # leader = TeamUser.objects.filter(team=team, is_leader=True)
            team["total_users"] = len(team["team_users"])
            # team["leader"] = UserTeamUserSerializer(leader, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        # data["created_by"] = request.user
        # data["updated_by"] = request.user
        new_team = Team.objects.create(
            name=data["name"],
            description=data["description"],
            # created_by=data["created_by"],
            # updated_by=data["updated_by"],
        )
        if request.data.get("team_leader"):
            user = get_object_or_404(User, pk=request.data.get("team_leader"))
            TeamUser.objects.create(
                user=user, team=new_team, is_leader=True, position="Leader"
            )
        new_team.save()
        serializer = TeamListSerializer(new_team)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        team = self.get_object()
        if request.data.get("name"):
            team.name = request.data.get("name")
        if request.data.get("description"):
            team.description = request.data.get("description")
        if request.data.get("team_projects"):
            teams = Project.objects.filter(pk__in=request.data.get("team_projects"))
            team.team_projects.set(teams)
        # team.updated_by = request.user
        team.save()
        serializer = TeamListSerializer(team)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        team = self.get_object()
        if team.deleted_at:
            team.delete()
        else:
            team.deleted_at = datetime.datetime.now()
            team.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        team = self.get_object()
        team_users = TeamUser.objects.filter(team=team)
        serializer = TeamUserSerializer(team_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def user(self, request, pk=None):
        data = request.data
        team = self.get_object()
        user = get_object_or_404(User, pk=data["id"])
        team_user, created = TeamUser.objects.get_or_create(team=team, user=user)
        team_user.position = data["position"]
        team_user.save()
        serializer = TeamUserSerializer(team_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def delete_user(self, request, pk=None):
        data = request.data
        team = self.get_object()
        team_user = TeamUser.objects.get(team=team, user=data["id"])
        team_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def all(self, request):
        queryset = Team.objects.all()
        serializer = TeamListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        queryset = Team.objects.filter(deleted_at__isnull=False)
        serializer = TeamListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        data = request.data
        teams = Team.objects.filter(pk__in=data["ids"])
        for team in teams:
            team.deleted_at = None
            team.save()
        serializer = TeamListSerializer(teams, many=True)
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
