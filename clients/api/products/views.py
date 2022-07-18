from hashlib import new
from clients.api.serializers import PricePlanSerializer
from .serializers import ProductSerializer, ProductListSerializer, ProductTrashedSerializer
from common.actions import (filterRecords, allItems, convertBase64ToImage)
from rest_framework.response import Response
from common.Repository import Repository
from clients.models import Product, Feature, PricePlan
from rest_framework import status
import os


class ProductViewSet(Repository):
    model = Product
    queryset = Product.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProductSerializer
    serializer_action_classes = {
        "trashed": ProductTrashedSerializer
    }
    queryset_actions = {
        "destroy": Product.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Product)
        if request.GET.get("items_per_page") == "-1":
            if request.GET.get("lessData"):
                serializer = ProductListSerializer(
                    queryset, many=True, context={"request": request})
                return Response(serializer.data, status=200)
            return allItems(self.get_serializer, queryset, request)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        imageField = convertBase64ToImage(data["photo"])
        creator = request.user
        new_product = Product.objects.create(
            photo=imageField,
            name=data['name'],
            details=data["details"],
            developed_by=data["developed_by"],
            created_by=creator,
            updated_by=creator,
        )
        new_product.save()
        feature = Feature.objects.create(
            name=data['name'], description=data['details'], product=new_product)
        for price_plan in request.data['price_plans']:
            price_plan = feature.price_plans.create(
                plan_name=price_plan['plan_name'], plan_price=price_plan['plan_price'])
        if "features" in request.data:
            for feature in request.data['features']:
                new_feature = Feature.objects.create(
                    name=feature['name'], description=feature['description'], product=new_product, type='additional')
                for price_plan in feature['price_plans']:
                    new_feature.price_plans.create(
                        plan_name=price_plan['plan_name'], plan_price=price_plan['plan_price'])
                new_feature.save()

        serializer = self.get_serializer(
            new_product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        product = self.get_object()
        if "photo" in request.data:
            imageField = convertBase64ToImage(request.data["photo"])
            if imageField:
                if os.path.isfile('media/'+str(product.photo)):
                    os.remove('media/'+str(product.photo))
                product.photo = imageField

        for key, value in request.data.items():
            if key != "photo":
                setattr(product, key, value)
        product.updated_by = request.user
        product.save()
        serializer = self.get_serializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
