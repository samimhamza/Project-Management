from users.api.serializers import UserWithProfileSerializer
from projects.models import Stage, SubStage
from rest_framework import serializers


class StageSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()

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
