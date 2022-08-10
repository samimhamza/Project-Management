from users.api.serializers import UserWithProfileSerializer
from projects.api.serializers import AttachmentSerializer
from tasks.models import Task, UserTask, Comment
from rest_framework import serializers
from tasks.models import UserTask


class TaskTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Task
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


class LessFieldsTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "progress", "type"]


class LessTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["id", "progress", "project"]


class TaskReportSerializer(serializers.ModelSerializer):
    p_start_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
    p_end_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
    a_start_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
    a_end_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "p_start_date",
            "p_end_date",
            "a_start_date",
            "a_end_date",
        ]


class ParentTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["id", "progress"]


class UserTaskSerializer(serializers.ModelSerializer):
    user = UserWithProfileSerializer()

    class Meta:
        model = UserTask
        fields = ["description", "progress", "type", "user"]


class ProgressSerializer(serializers.ModelSerializer):
    task = LessTaskSerializer()

    class Meta:
        model = UserTask
        fields = ["progress", "task"]


def users(self, task):
    qs = UserTask.objects.filter(task=task)
    serializer = UserTaskSerializer(
        instance=qs, many=True, read_only=True, context={"request": self.context['request']})
    for data in serializer.data:
        user = data['user']
        del data['user']
        data.update(user)
    return serializer.data


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    parent = LessFieldsTaskSerializer()
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
            "parent",
            "priority",
            "progress",
            "status",
            "type",
            "dependencies",
            "users",
            "deleted_at",
            "project",
            "pin",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
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
            "progress",
            "status",
            "type",
            "pin",
            "users",
            "deleted_at"
        ]


class TaskListSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    parent = LessFieldsTaskSerializer()
    sub_tasks = serializers.SerializerMethodField()
    dependencies = serializers.SerializerMethodField()
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)

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
            "progress",
            "status",
            "type",
            "dependencies",
            "sub_tasks",
            "users",
            "pin",
            "deleted_at",
            "project",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserWithProfileSerializer(read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "attachments",
                  "created_at", "updated_at", "commented_by"]
