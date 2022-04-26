from pyexpat import model
from rest_framework import serializers
from projects.models import Project, Country, Location, FocalPoint, Income, Payment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


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
        exclude = ["deleted_at"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ["deleted_at"]


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        exclude = ["deleted_at"]
