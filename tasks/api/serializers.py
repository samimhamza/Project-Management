from os import read
from rest_framework import serializers
from tasks.models import Task, UserTask, Comment
from users.api.serializers import UserWithProfileSerializer
from users.models import User
from projects.api.serializers import AttachmentSerializer
from tasks.models import UserTask


def users(self, task):
    qs = UserTask.objects.filter(task=task)
    serializer = UserTaskSerializer(
        instance=qs, many=True, read_only=True, context={"request": self.context['request']})
    for data in serializer.data:
        user = data['user']
        del data['user']
        data.update(user)
    return serializer.data


class UserTaskSerializer(serializers.ModelSerializer):
    user = UserWithProfileSerializer()

    class Meta:
        model = UserTask
        fields = ["description", "progress", "type", "user"]


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

    def get_users(self, task):
        return users(self, task)

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
            "project",
            "pin"
        ]


class SubTaskSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, task):
        return users(self, task)

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
            "priority",
            "status",
            "type",
            "users",
            "deleted_at"
        ]


class TaskListSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    parent = LessFieldsTaskSerializer()
    sub_tasks = serializers.SerializerMethodField()
    dependencies = serializers.SerializerMethodField()

    def get_users(self, task):
        return users(self, task)

    def get_sub_tasks(self, task):
        qs = Task.objects.filter(
            deleted_at__isnull=True, parent=task)
        serializer = SubTaskSerializer(
            instance=qs, many=True, read_only=True, context={"request": self.context['request']})
        return serializer.data

    def get_dependencies(self, task):
        if task.dependencies:
            qs = Task.objects.filter(
                deleted_at__isnull=True, pk__in=task.dependencies)
            serializer = SubTaskSerializer(
                instance=qs, many=True, read_only=True, context={"request": self.context['request']})
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
            "sub_tasks",
            "users",
            "deleted_at",
            "project"
        ]


class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserWithProfileSerializer(read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "attachments",
                  "created_at", "updated_at", "commented_by"]
