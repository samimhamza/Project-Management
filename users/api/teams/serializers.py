from users.api.serializers import LessFieldsUserSerializer, UserWithProfileSerializer
from projects.api.serializers import ProjectNameListSerializer
from rest_framework import serializers
from users.models import Team, TeamUser, Permission, Role, Action, SubAction


class TeamUserSerializer(serializers.ModelSerializer):
    user = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = TeamUser
        fields = ["user", "position", "is_leader"]


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
    projects = ProjectNameListSerializer(many=True, read_only=True)

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
            "projects",
        ]


class ProjectTeamSerializer(serializers.ModelSerializer):
    projects = ProjectNameListSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["projects"]


class TeamNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]
