from rest_framework import serializers
from users.models import PasswordReset


class PasswordResetSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField(source='id')

    class Meta:
        model = PasswordReset
        fields = ["token"]
