from rest_framework import serializers
from users.models import Team, User, TeamUser
from users.api.serializers import LessFieldsUserSerializer, LessFieldsTeamSerializer
from projects.api.projects.serializers import ProjectLessListSerializer


class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamUser
        fields = "__all__"


class TeamListSerializer(serializers.ModelSerializer):
    created_by = LessFieldsUserSerializer(read_only=True)
    updated_by = LessFieldsUserSerializer(read_only=True)
    team_projects = ProjectLessListSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "users",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "deleted_at",
            "team_projects",
        ]


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "name",
            "description",
        ]


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "description", "team_projects"]
