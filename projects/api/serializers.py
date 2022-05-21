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
from projects.api.projects import serializers as api_serializers


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
            serializer = api_serializers.ProjectListSerializer(value)
        else:
            raise Exception("Unexpected type of Attachment object")

        return serializer.data


class AttachmentSerializer(serializers.ModelSerializer):
    project = AttachmentObjectRelatedField(read_only=True)

    class Meta:
        model = Attachment
        fields = ["name", "path", "object_id", "project"]


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
    country = CountrySerializer()

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
