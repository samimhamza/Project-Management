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
    payments = serializers.SerializerMethodField()

    def get_payments(self, income):
        qs = Payment.objects.filter(
        deleted_at__isnull=True, income=income)
        serializer = PaymentSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Income
        fields = "__all__"


class ProjectLessListSerializer(serializers.ModelSerializer):
    company_location = LessFieldsLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "p_start_date",
            "p_end_date",
            "a_start_date",
            "a_end_date",
            "status",
            "progress",
            "priority",
            "company_name",
            "company_email",
            "company_location",
        ]


class ProjectNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
        ]


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
            serializer = ProjectNameListSerializer(value)
        else:
            raise Exception("Unexpected type of Attachment object")

        return serializer.data


class AttachmentSerializer(serializers.ModelSerializer):
    # project = AttachmentObjectRelatedField(read_only=True)

    class Meta:
        model = Attachment
        fields = "__all__"
        depth = 1
