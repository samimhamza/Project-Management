from rest_framework import serializers
from users.models import PasswordReset
from users.api.serializers import UserWithProfileSerializer


class PasswordResetSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField(source='id')

    class Meta:
        model = PasswordReset
        fields = ["token"]


class PasswordResetUserSerializer(serializers.ModelSerializer):
    user = UserWithProfileSerializer()

    class Meta:
        model = PasswordReset
        fields = ["user"]
