from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
import datetime
from projects.models import (
    Project,
    Country,
    Location,
    FocalPoint,
    Income,
    Payment,
    Attachment,
)
from projects.api.serializers import (
    CountrySerializer,
    LocationSerializer,
    FocalPointSerializer,
    IncomeSerializer,
    PaymentSerializer,
    AttachmentSerializer,
)


class AttachmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class AttachmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


# Country CRUD
class CountryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# end of Location CRUD

# Location CRUD
class LocationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# end of Location CRUD

# Payment CRUD
class PaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer
    paginate_by = 10

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


class PaymentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer

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


# end of Payment CRUD

# Income CRUD
class IncomeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

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


class IncomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

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


# end of Income CRUD

# FocalPoint CRUD
class FocalPointListCreateAPIView(generics.ListCreateAPIView):
    queryset = FocalPoint.objects.all()
    serializer_class = FocalPointSerializer

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


class FocalPointDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FocalPoint.objects.all()
    serializer_class = FocalPointSerializer

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


# end of FocalPoint CRUD
