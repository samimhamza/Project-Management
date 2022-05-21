from rest_framework import serializers
from users.models import Team, TeamUser

from users.api.serializers import LessFieldsUserSerializer, UserWithProfileSerializer

from projects.api.serializers import ProjectNameListSerializer


class TeamUserSerializer(serializers.ModelSerializer):
    user = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = TeamUser
        fields = ["position", "user"]


class LessFieldsTeamSerializer(serializers.ModelSerializer):
    users = LessFieldsUserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "description", "users"]


class TeamListSerializer(serializers.ModelSerializer):
    created_by = LessFieldsUserSerializer(read_only=True)
    updated_by = LessFieldsUserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class TeamRetieveSerializer(serializers.ModelSerializer):
    created_by = LessFieldsUserSerializer(read_only=True)
    updated_by = LessFieldsUserSerializer(read_only=True)
    team_projects = ProjectNameListSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "deleted_at",
            "team_projects",
        ]


class ProjectTeamSerializer(serializers.ModelSerializer):
    team_projects = ProjectNameListSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["team_projects"]


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


class TeamNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]
