from users.models import (User,  Reminder, Holiday, Notification,
                          TeamUser, Action, SubAction, Permission, UserPermissionList, Role, UserNotification)
from rest_framework.validators import UniqueValidator
from rest_framework import serializers


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
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

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
            "position",
            "created_by",
            "updated_by",
            "deleted_by",
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
            "position",
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
        fields = ["id", "title", "description", "icon", "type"]


class UserNotificationSerializer(serializers.ModelSerializer):
    # sender = UserWithProfileSerializer()
    # receiver = UserWithProfileSerializer()
    notification = NotificationSerializer()

    class Meta:
        model = UserNotification
        fields = ["id", "notification", "seen", "description",
                  "created_at", "model_name", "instance_id"]


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
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Role
        fields = "__all__"


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class RoleTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Role
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


class UserTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
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
