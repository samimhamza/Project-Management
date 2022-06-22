from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from projects.models import ProjectCategory


class ProjectCategorySerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()

    class Meta:
        model = ProjectCategory
        fields = "__all__"
