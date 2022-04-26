from rest_framework import generics
from expenses.api.serializers import (
    ExpenseSerializer,
    ExpenseItemSerializer,
    CategorySerializer,
)
from expenses.models import Expense, ExpenseItem, Category
import datetime

# Category CRUD
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(deleted_at__isnull=True)
    serializer_class = CategorySerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(created_by=request.user.id)
                request.data.update(updated_by=request.user.id)
        except:
            request.data.update(created_by=request.user.id)
            request.data.update(updated_by=request.user.id)
        return self.create(request, *args, **kwargs)


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.filter(deleted_at__isnull=True)
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(updated_by=request.user.id)
                request.data.update(updated_at=datetime.datetime.now())
        except:
            request.data.update(updated_by=request.user.id)
            request.data.update(updated_at=datetime.datetime.now())
        return self.update(request, *args, **kwargs)


# end of Category CRUD

# Expense CRUD
class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expense.objects.filter(deleted_at__isnull=True)
    serializer_class = ExpenseSerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(created_by=request.user.id)
                request.data.update(updated_by=request.user.id)
        except:
            request.data.update(created_by=request.user.id)
            request.data.update(updated_by=request.user.id)
        return self.create(request, *args, **kwargs)


class ExpenseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.filter(deleted_at__isnull=True)
    serializer_class = ExpenseSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(updated_by=request.user.id)
                request.data.update(updated_at=datetime.datetime.now())
        except:
            request.data.update(updated_by=request.user.id)
            request.data.update(updated_at=datetime.datetime.now())
        return self.update(request, *args, **kwargs)


# end of Expense CRUD

# ExpenseItem CRUD
class ExpenseItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = ExpenseItem.objects.all()
    serializer_class = ExpenseItemSerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpenseItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseItem.objects.all()
    serializer_class = ExpenseItemSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(updated_at=datetime.datetime.now())
        except:
            request.data.update(updated_at=datetime.datetime.now())
        return self.update(request, *args, **kwargs)


# end of ExpenseItem CRUD
