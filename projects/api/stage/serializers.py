# from projects.api.department.serializers import DepartmentListSerializer
from users.api.serializers import UserWithProfileSerializer
from projects.models import Stage, SubStage, Department
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
    # departments = serializers.SerializerMethodField()
    # sub_stage = serializers.SerializerMethodField()

    # def get_departments(self, stage):
    #     qs = Department.objects.filter(
    #         deleted_at__isnull=True, department_stages=stage)
    #     serializer = DepartmentListSerializer(instance=qs, many=True)
    #     return serializer.data

    # def get_sub_stage(self, stage):
    #     qs = SubStage.objects.filter(
    #         deleted_at__isnull=True, department_stages=stage)
    #     serializer = SubStageListSerializer(instance=qs, many=True)
    #     return serializer.data

    class Meta:
        model = Stage
        fields = "__all__"


class StageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["id", "name", "category"]


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
