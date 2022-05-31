from os import read
from rest_framework import serializers
from tasks.models import Task, UserTask, Comment
from users.api.serializers import UserWithProfileSerializer
from users.models import User


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = "__all__"


class LessFieldsTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
        ]


class TaskSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    parent = LessFieldsTaskSerializer()

    def get_users(self, user):
        qs = User.objects.filter(
            deleted_at__isnull=True, users=user)
        serializer = UserWithProfileSerializer(
            instance=qs, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "p_start_date",
            "p_end_date",
            "a_start_date",
            "a_end_date",
            "parent",
            "priority",
            "status",
            "type",
            "dependencies",
            "users",
            "deleted_at",
            "project"
        ]


class TaskNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name"]


class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at", "updated_at", "commented_by"]
