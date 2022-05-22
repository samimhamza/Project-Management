from rest_framework import serializers
from tasks.models import Task, UserTask
from users.api.serializers import UserWithProfileSerializer


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
    task_users = UserWithProfileSerializer(many=True, read_only=True)
    parent = LessFieldsTaskSerializer()

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
            "task_users",
        ]


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = "__all__"
