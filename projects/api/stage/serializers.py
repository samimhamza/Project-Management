from projects.api.department.serializers import DepartmentListSerializer
from users.api.serializers import UserWithProfileSerializer
from projects.models import Stage, SubStage
from rest_framework import serializers


class SubStageSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()

    class Meta:
        model = SubStage
        fields = "__all__"


class StageSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()
    department = DepartmentListSerializer()

    class Meta:
        model = Stage
        fields = "__all__"


class StageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["id", "name", "department"]


class SubStageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStage
        fields = ["id", "name"]


class StageTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Stage
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


class SubStageTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = SubStage
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
