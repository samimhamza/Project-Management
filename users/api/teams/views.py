from rest_framework import viewsets, status
from projects.models import Project
from users.models import User, Team, TeamUser
from users.api.teams.serializers import (
    TeamListSerializer,
    TeamCreateSerializer,
    TeamUserSerializer,
    TeamUpdateSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import action
import datetime
from rest_framework.generics import get_object_or_404


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.filter(deleted_at__isnull=True)
    serializer_class = TeamListSerializer
    serializer_action_classes = {
        "create": TeamCreateSerializer,
        "update": TeamUpdateSerializer,
    }
    queryset_actions = {}

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

    @action(detail=True, methods=["get"])
    def team_users(self, request, pk=None):
        projects = TeamUser.objects.select_related("user", "team")
        serializer = TeamUserSerializer(projects, many=True)
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
