from rest_framework import serializers
from tasks.models import Task, UserTask
from users.models import User


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = "__all__"


class LessFieldsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class TaskSerializer(serializers.ModelSerializer):
    task_users = LessFieldsUserSerializer(many=True, read_only=True)

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
        depth = 1


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = "__all__"
