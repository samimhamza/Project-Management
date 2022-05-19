from rest_framework import serializers
from users.models import Team, User, TeamUser
from users.api.serializers import LessFieldsUserSerializer, LessFieldsTeamSerializer


class TeamUserSerializer(serializers.ModelSerializer):
    user = LessFieldsUserSerializer(read_only=True)

    class Meta:
        model = TeamUser
        fields = ["id", "type", "user"]


class TeamListSerializer(serializers.ModelSerializer):
    created_by = LessFieldsUserSerializer(read_only=True)
    updated_by = LessFieldsUserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "team_users",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "name",
            "description",
        ]
