from users.api.serializers import UserWithProfileSerializer
from rest_framework import serializers
from projects.models import (
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    Project,
    Attachment,
    State,
    Action,
    ProjectPermission,
    SubAction
)


class ProjectNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class StateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name"]


class StateSerializer(serializers.ModelSerializer):
    country = CountryListSerializer(read_only=True)

    class Meta:
        model = State
        fields = ["id", "name", "state_code",
                  "latitude", "longitude", "country"]


class LocationSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = Location
        fields = [
            "id",
            "address_line_one",
            "address_line_two",
            "city",
            "state",
        ]


class FocalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocalPoint
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()
    # amount = serializers.SerializerMethodField()
    project = ProjectNameListSerializer()

    def get_payments(self, income):
        qs = Payment.objects.filter(
            deleted_at__isnull=True, income=income).order_by('-date')
        serializer = PaymentSerializer(instance=qs, many=True, context={
                                       "request": self.context['request']})
        return serializer.data

    # def get_amount(self, income):
    #     qs = Payment.objects.filter(
    #         deleted_at__isnull=True, income=income).order_by('-date')
    #     amount = 0
    #     for payment in qs:
    #         amount += payment.amount
    #     return amount

    class Meta:
        model = Income
        fields = "__all__"


class IncomeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "amount",
            "date"
        ]


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserWithProfileSerializer()

    class Meta:
        model = Attachment
        fields = ["id", "name", "attachment",
                  "size", "description", "uploaded_by", "created_at"]


class FocalPointTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return '{} {}'.format(obj.contact_name, obj.contact_last_name)

    class Meta:
        model = FocalPoint
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by"
        ]


class IncomeTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.CharField(source="title")

    class Meta:
        model = FocalPoint
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by"
        ]


class PaymentTrashedSerializer(serializers.ModelSerializer):
    created_by = UserWithProfileSerializer(read_only=True)
    updated_by = UserWithProfileSerializer(read_only=True)
    deleted_by = UserWithProfileSerializer(read_only=True)
    name = serializers.CharField(source="source")

    class Meta:
        model = FocalPoint
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by"
        ]


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "name", "model"]


class SubActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAction
        fields = ["id", "code", 'name']


class ProjectPermissionActionSerializer(serializers.ModelSerializer):
    sub_action = SubActionSerializer()

    class Meta:
        model = ProjectPermission
        fields = ["sub_action"]


class ProjectPermissionUserSerializer(serializers.ModelSerializer):
    action = serializers.SerializerMethodField()

    def get_action(self, obj):
        return ProjectPermissionActionSerializer(obj).data

    class Meta:
        model = ProjectPermission
        fields = ["action"]
