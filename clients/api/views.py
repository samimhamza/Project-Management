from clients.models import ClientFeature,  PricePlan, Feature, Requirement, ClientService
from clients.api.serializers import (
    ClientFeatureSerializer, ClientFeature, RequirementSerializer, PricePlanSerializer)
from clients.api.clients.serializers import ClientServiceSerializer
from clients.api.products.serializers import FeatureSerializer
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets


class ClientServiceViewSet(viewsets.ModelViewSet):
    queryset = ClientService.objects.all()
    serializer_class = ClientServiceSerializer


class ClientFeatureViewSet(viewsets.ModelViewSet):
    queryset = ClientFeature.objects.all()
    serializer_class = ClientFeatureSerializer


class PricePlanViewSet(viewsets.ModelViewSet):
    queryset = PricePlan.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = PricePlanSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = FeatureSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = RequirementSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
