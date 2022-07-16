from common.actions import (filterRecords, allItems, withTrashed,
                            trashList, restore, delete, convertBase64ToImage)
from .serializers import ProductSerializer, ProductListSerializer
from common.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from clients.models import Product
import os


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
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
        serializer = self.get_serializer(
            new_product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        product = self.get_object()
        if "photo" in request.data:
            imageField = convertBase64ToImage(request.data["photo"])
            product.photo = imageField
            if os.path.isfile('media/'+str(product.photo)):
                os.remove('media/'+str(product.photo))
        for key, value in request.data.items():
            if key != "photo":
                setattr(product, key, value)
        product.updated_by = request.user
        product.save()
        serializer = self.get_serializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Product)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Product, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Product)

    @action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, Product)

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
