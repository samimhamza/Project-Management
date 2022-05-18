from rest_framework import serializers
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    Project,
    Attachment,
)
from users.models import User, Team
from tasks.api.serializers import TaskSerializer


class AttachmentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `Attachment_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Project):
            serializer = ProjectSerializer(value)
        else:
            raise Exception("Unexpected type of Attachment object")

        return serializer.data


class AttachmentSerializer(serializers.RelatedField):
    class Meta:
        model = Attachment
        fields = ["name", "path"]


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


class ProjectTasksSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["tasks"]


class ProjectSerializer(serializers.ModelSerializer):
    company_location = LessFieldsLocationSerializer(read_only=True)
    users = LessFieldsUserSerializer(many=True, read_only=True)
    teams = LessFieldsTeamSerializer(many=True, read_only=True)
    created_by = LessFieldsUserSerializer(read_only=True)
    updated_by = LessFieldsUserSerializer(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "tasks",
            "company_location",
            "users",
            "teams",
            "created_by",
            "updated_by",
        ]


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
