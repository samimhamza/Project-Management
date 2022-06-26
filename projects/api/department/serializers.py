from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from projects.models import Department, Stage, SubStage


class SubStageListSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()
    key = serializers.CharField(source="id")

    class Meta:
        model = SubStage
        fields = ["id", "key", "name", "description", "created_by",
                  "updated_by", "created_at", "updated_at"]


class StageListSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()
    sub_stages = serializers.SerializerMethodField()
    key = serializers.CharField(source="id")

    def get_sub_stages(self, stage):
        qs = SubStage.objects.filter(
            deleted_at__isnull=True, stage=stage).order_by('-updated_at')
        serializer = SubStageListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Stage
        fields = ["id", "key", "name", "description", "created_by",
                  "updated_by", "created_at", "updated_at", "sub_stages"]


class DepartmentSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()
    stages = serializers.SerializerMethodField()

    def get_stages(self, department):
        qs = Stage.objects.filter(
            deleted_at__isnull=True, department=department).order_by('-updated_at')
        serializer = StageListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Department
        fields = ["id", "name", "description", "created_by",
                  "updated_by", "created_at", "updated_at", "stages"]


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description", "created_by",
                  "updated_by", "created_at", "updated_at", ]


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
