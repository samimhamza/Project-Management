from projects.api.department.serializers import DepartmentListSerializer
from users.api.serializers import UserWithProfileSerializer
from projects.models import Stage, SubStage, Department
from rest_framework import serializers


class StageSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()
    departments = serializers.SerializerMethodField()

    def get_departments(self, stage):
        qs = Department.objects.filter(
            deleted_at__isnull=True, department_stages=stage)
        serializer = DepartmentListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Stage
        fields = "__all__"


class StageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["id", "name", "category"]


class SubStageSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()

    class Meta:
        model = SubStage
        fields = "__all__"


class SubStageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStage
        fields = ["id", "name"]
