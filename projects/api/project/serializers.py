from rest_framework import serializers
from projects.models import Project
from users.api.serializers import UserWithProfileSerializer
from projects.api.serializers import LocationSerializer, AttachmentSerializer
from users.models import User


class ProjectSerializer(serializers.ModelSerializer):
    company_location = LocationSerializer(read_only=True)
    users = serializers.SerializerMethodField()
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()

    def get_users(self, project):
        qs = User.objects.filter(
            deleted_at__isnull=True, project_users=project)
        serializer = UserWithProfileSerializer(
            instance=qs, many=True, read_only=True)
        return serializer.data

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
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "deleted_at",
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]
