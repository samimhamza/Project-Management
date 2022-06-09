from users.models import (User,  Reminder, Holiday, Notification,
                          TeamUser, Action, SubAction, Permission, UserPermissionList, Role)

from rest_framework import serializers


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


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "name", "model"]


class SubActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAction
        fields = ["id", "code", 'name']


class PermissionSerializer(serializers.ModelSerializer):
    action = ActionSerializer()
    sub_action = SubActionSerializer()

    class Meta:
        model = Permission
        fields = ["action", "sub_action"]


class PermissionActionSerializer(serializers.ModelSerializer):
    sub_action = SubActionSerializer()

    class Meta:
        model = Permission
        fields = ["sub_action"]


class UserPermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionList
        fields = ["permissions_list"]


class RoleSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, role):
        qs = User.objects.filter(
            deleted_at__isnull=True, roles_users=role)
        serializer = UserWithProfileSerializer(
            instance=qs, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Role
        fields = "__all__"


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]
