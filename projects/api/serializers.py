from rest_framework import serializers
from projects.models import Project, Country, Location, FocalPoint, Income, Payment
from users.models import User, Team


class LessFieldsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class LessFieldsTeamSerializer(serializers.ModelSerializer):
    team_users = LessFieldsUserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "description", "team_users"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class LessFieldsLocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Location
        fields = [
            "id",
            "address_line_one",
            "address_line_two",
            "city",
            "state",
            "country",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    company_location = LessFieldsLocationSerializer(read_only=True)
    users = LessFieldsUserSerializer(many=True, read_only=True)
    teams = LessFieldsTeamSerializer(many=True, read_only=True)
    created_by = LessFieldsUserSerializer(read_only=True)
    updated_by = LessFieldsUserSerializer(read_only=True)

    class Meta:
        model = Project
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
