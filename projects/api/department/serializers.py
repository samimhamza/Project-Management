from users.api.serializers import UserWithProfileSerializer
from projects.api.stage.serializers import StageSerializer
from rest_framework import serializers
from projects.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class DepartmentTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Department
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
