from rest_framework import serializers
from projects.models import Project, Country, Location, FocalPoint, Income, Payment
from tasks.api.serializers import TaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # task = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = "__all__"
        # depth = 1


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class FocalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocalPoint
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"
