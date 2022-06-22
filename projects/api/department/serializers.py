from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from projects.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer()
    updated_by = UserWithProfileSerializer()

    class Meta:
        model = Department
        fields = "__all__"
