from http import client
from clients.models import ClientFeature,  PricePlan, Feature, Requirement, ClientService,Client
from clients.api.serializers import (
    ClientFeatureSerializer, ClientFeature, RequirementSerializer, PricePlanSerializer)
from clients.api.clients.serializers import ClientServiceSerializer
from clients.api.products.serializers import FeatureSerializer
from rest_framework.response import Response
from common.Repository import Repository


class ClientServiceViewSet(Repository):
    model = ClientService
    queryset = ClientService.objects.all()
    serializer_class = ClientServiceSerializer


class ClientFeatureViewSet(Repository):
    model = ClientFeature
    queryset = ClientFeature.objects.all()
    serializer_class = ClientFeatureSerializer


class PricePlanViewSet(Repository):
    model = PricePlan
    queryset = PricePlan.objects.all()
    serializer_class = PricePlanSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FeatureViewSet(Repository):
    model = Feature
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RequirementViewSet(Repository):
    model = Requirement
    queryset = Requirement.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = RequirementSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        requirement = self.get_object()
        try:
            client = Client.objects.only(
                'id').get(pk=request.data["client"])
        except Client.DoesNotExist:
            return Response({"error": "Department does not exist!"}, status=404)
        for key, value in request.data.items():
            if key != "client":
                setattr(requirement, key, value)
        requirement.updated_by = request.user
        requirement.client=client
        requirement.save()
        serializer = self.get_serializer(requirement)
        return Response(serializer.data, status=202)
