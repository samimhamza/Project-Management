import re
from rest_framework import serializers
from users.models import User, Team, Reminder, Holiday, Notification, TeamUser


class LessFieldsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class UserWithProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "profile"]


class CustoUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile",
            "phone",
            "whatsapp",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "profile",
            "phone",
            "whatsapp",
            "password",
        ]


class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamUser
        fields = "type"


class TeamSerializer(serializers.ModelSerializer):
    users = TeamUserSerializer(many=True, read_only=True)
    created_by = LessFieldsUserSerializer(read_only=True)
    updated_by = LessFieldsUserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = "__all__"


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
