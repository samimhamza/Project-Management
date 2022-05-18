from rest_framework import generics, status
from rest_framework.views import APIView
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
    ProjectSerializer,
    CountrySerializer,
    LocationSerializer,
    FocalPointSerializer,
    IncomeSerializer,
    PaymentSerializer,
    AttachmentSerializer,
    ProjectTasksSerializer,
)
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
import datetime

# Project CRUD
# class ProjectListCreateAPIView(APIView):
#     def get(self, request):
#         projects = Project.objects.filter(deleted_at__isnull=True)
#         serializers = ProjectSerializer(projects, many=True)
#         return Response(serializers.data)

#     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data["created_by"] = request.user
#             serializer.validated_data["updated_by"] = request.user
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectTaskLlistAPIView(APIView):
    def get_object(self, pk):
        project = get_object_or_404(Project, pk=pk)
        return project

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectTasksSerializer(project)
        return Response(serializer.data)


class AttachmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class AttachmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


# class ProjectDetailAPIView(APIView):
#     def get_object(self, pk):
#         project = get_object_or_404(Project, pk=pk)
#         return project

#     def get(self, request, pk):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project, data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data["updated_by"] = request.user
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         project = self.get_object(pk)
#         project.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# end of Project CRUD

class ProjectTasksListAPIView(APIView):
    def get(self, request,pk):
        return Response('everything we want we can response')

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
