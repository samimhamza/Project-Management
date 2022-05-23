from rest_framework import serializers
from projects.models import Project
from users.api.serializers import LessFieldsUserSerializer
from users.api.teams.serializers import LessFieldsTeamSerializer
from projects.api.serializers import LessFieldsLocationSerializer
from tasks.api.serializers import TaskSerializer, LessFieldsTaskSerializer
from expenses.api.serializers import ExpenseSerializer


class ProjectExpensesSerializer(serializers.ModelSerializer):
    expenses = ExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["expenses"]


class ProjectListSerializer(serializers.ModelSerializer):
    company_location = LessFieldsLocationSerializer(many=True, read_only=True)
    users = LessFieldsUserSerializer(many=True, read_only=True)
    projects = LessFieldsTeamSerializer(many=True, read_only=True)
    created_by = LessFieldsUserSerializer()
    updated_by = LessFieldsUserSerializer()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "p_start_date",
            "p_end_date",
            "a_start_date",
            "a_end_date",
            "status",
            "progress",
            "priority",
            "company_name",
            "company_email",
            "company_location",
            "users",
            "projects",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "deleted_at",
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "p_start_date",
            "p_end_date",
            "users",
            "projects",
        ]


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "p_start_date",
            "p_end_date",
            "a_start_date",
            "a_end_date",
            "status",
            "priority",
            "progress",
            "company_name",
            "company_email",
            "users",
            "projects",
        ]
