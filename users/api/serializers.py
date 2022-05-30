import re
from rest_framework import serializers
from users.models import User, Team, Reminder, Holiday, Notification, TeamUser
from drf_extra_fields.fields import Base64ImageField


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


class UploadedBase64ImageSerializer(serializers.Serializer):
    profile = Base64ImageField(required=False)


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
        ]


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile",
        ]


class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamUser
        fields = "type"


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
