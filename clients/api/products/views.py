from multiprocessing import context
from .serializers import ProductSerializer, ProductListSerializer
from common.custom import CustomPageNumberPagination
from common.actions import filterRecords, allItems
from rest_framework import viewsets
from clients.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Product)
        if request.GET.get("items_per_page") == "-1":
            return allItems(self.get_serializer, queryset, request)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
