from rest_framework import serializers
from projects.models import Project, Country, Location, FocalPoint, Income, Payment
from users.models import User, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "description"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class CustomLocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Location
        fields = ["address_line_one", "address_line_two", "city", "state", "country"]


class ProjectSerializer(serializers.ModelSerializer):
    company_location = CustomLocationSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectTasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["tasks"]
        depth = 1


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
