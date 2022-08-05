from projects.models import Action, SubAction, ProjectPermission
from rest_framework import serializers


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "name", "model"]


class SubActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAction
        fields = ["id", "code", 'name']


class ProjectPermissionSerializer(serializers.ModelSerializer):
    action = ActionSerializer()
    sub_action = SubActionSerializer()

    class Meta:
        model = ProjectPermission
        fields = ["action", "sub_action"]
