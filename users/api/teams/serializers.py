from users.api.serializers import UserWithProfileSerializer
from projects.api.serializers import ProjectNameListSerializer
from users.models import Team, TeamUser, User
from rest_framework import serializers


class TeamUserSerializer(serializers.ModelSerializer):
    # user = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = TeamUser
        fields = ["position", "is_leader"]


class TeamUserDetailSerializer(serializers.ModelSerializer):
    user = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = TeamUser
        fields = "__all__"


class LessFieldsTeamSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, team):
        qs = User.objects.filter(
            deleted_at__isnull=True, teams=team)
        serializer = UserWithProfileSerializer(
            instance=qs, many=True, read_only=True, context={
                "request": self.context['request']})
        return serializer.data

    class Meta:
        model = Team
        fields = ["id", "name", "description", "users"]


class TeamListSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)

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
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
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


class TeamTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by"
        ]
