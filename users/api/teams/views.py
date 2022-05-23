from rest_framework import viewsets, status
from projects.models import Project
from users.models import User, Team, TeamUser
from users.api.teams.serializers import (
    TeamListSerializer,
    TeamCreateSerializer,
    TeamUserSerializer,
    TeamUpdateSerializer,
    TeamNamesSerializer,
    TeamRetieveSerializer,
    ProjectTeamSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from common.custom import CustomPageNumberPagination
from common.actions import (delete, withTrashed, trashList, restore,
                            get_total_users, get_total, get_leader_by_id, get_leader)
from django.db import transaction


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = TeamListSerializer
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {
        "create": TeamCreateSerializer,
        "update": TeamUpdateSerializer,
        "retrieve": TeamRetieveSerializer,
        "add_project": ProjectTeamSerializer,
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
        if request.GET.get("items_per_page") == "-1":
            serializer = TeamNamesSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        for team in serializer.data:
            team["total_users"] = get_total_users(team["id"])
            team["leader"] = get_leader_by_id(team["id"])
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        team = self.get_object()
        serializer = self.get_serializer(team)
        data = serializer.data
        data["total_users"] = get_total(team)
        data["leader"] = get_leader(team)
        return Response(data, status=status.HTTP_200_OK)

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
        data = serializer.data
        data["total_users"] = get_total(new_team)
        data["leader"] = get_leader(new_team)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        team = self.get_object()
        if request.data.get("name"):
            team.name = request.data.get("name")
        if request.data.get("description"):
            team.description = request.data.get("description")
        if request.data.get("team_projects"):
            teams = Project.objects.filter(
                pk__in=request.data.get("team_projects"))
            team.team_projects.set(teams)
        # team.updated_by = request.user
        team.save()
        serializer = TeamListSerializer(team)
        data = serializer.data
        data["total_users"] = get_total(team)
        data["leader"] = get_leader(team)
        return Response(data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Team)

    @action(detail=False, methods=["get"])
    def all(self, request):
        serializer = withTrashed(self, Team, order_by="-created_at")
        for team in serializer.data:
            team["total_users"] = get_total_users(team["id"])
            team["leader"] = get_leader_by_id(team["id"])
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Team)

    # for multi and single restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Team)

    # Custom Actions
    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        team = self.get_object()
        users = TeamUser.objects.filter(team=team)
        page = self.paginate_queryset(users)
        serializer = TeamUserSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None):
        try:
            data = request.data
            team = self.get_object()
            user = get_object_or_404(User, pk=data["id"])
            team_user, created = TeamUser.objects.get_or_create(
                team=team, user=user)
            team_user.position = data["position"]
            team_user.save()
            serializer = TeamUserSerializer(team_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    def add_project(self, request, pk=None):
        try:
            data = request.data
            team = self.get_object()
            team.team_projects.set(data["ids"])
            serializer = self.get_serializer(team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    def delete_user(self, request, pk=None):
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

    # return different Serializers for different actions
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    # return different Querysets from different actions
    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
