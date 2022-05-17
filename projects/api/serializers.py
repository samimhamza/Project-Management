from rest_framework import serializers
from projects.models import Project, Country, Location, FocalPoint, Income, Payment
from users.api.serializers import UserSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    company_location = LocationSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    teams = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
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
