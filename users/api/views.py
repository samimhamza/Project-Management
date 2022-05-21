from rest_framework import viewsets, status
from users.api.serializers import (
    UserSerializer,
    NotificationSerializer,
    ReminderSerializer,
    HolidaySerializer,
)
from users.models import User, Reminder, Holiday, Notification
from common.custom_classes.custom import CustomPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
import datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted_at__isnull=True).order_by("-created_at")
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {}

    def destroy(self, request, pk=None):
        data = request.data
        if data:
            users = User.objects.filter(pk__in=data["ids"])
            for user in users:
                if user.deleted_at:
                    user.delete()
                else:
                    user.deleted_at = datetime.datetime.now()
                    user.save()
        else:
            user = self.get_object()
            if user.deleted_at:
                user.delete()
            else:
                user.deleted_at = datetime.datetime.now()
                user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def all(self, request):
        queryset = User.objects.all().order_by("-created_at")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        queryset = self.filter_queryset(
            User.objects.filter(deleted_at__isnull=False).order_by("-deleted_at")
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        try:
            with transaction.atomic():
                data = request.data
                users = User.objects.filter(pk__in=data["ids"])
                for user in users:
                    user.deleted_at = None
                    user.save()
                page = self.paginate_queryset(users)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    pagination_class = CustomPageNumberPagination


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = CustomPageNumberPagination


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all().order_by("-created_at")
    serializer_class = ReminderSerializer
    pagination_class = CustomPageNumberPagination

    def destroy(self, request, pk=None):
        data = request.data
        if data:
            users = User.objects.filter(pk__in=data["ids"])
            for user in users:
                user.delete()
        else:
            user = self.get_object()
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class RegisterView(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         try:
#             data = request.data
#             first_name = data["first_name"]
#             last_name = data["last_name"]
#             username = data["username"]
#             email = data["email"]
#             password = data["password"]
#             re_password = data["re_password"]
#             if password == re_password:
#                 if len(password) >= 8:
#                     if not User.objects.filter(username=username, email=email).exists():
#                         user = User.objects.create_user(
#                             first_name=first_name,
#                             last_name=last_name,
#                             username=username,
#                             email=email,
#                             password=password,
#                             created_by=request.user.id,
#                             updated_by=request.user.id,
#                         )
#                         user.save()
#                         if User.objects.filter(username=username).exists():
#                             return Response(
#                                 {"success": "Account Successfully Created"},
#                                 status=status.HTTP_201_CREATED,
#                             )
#                         else:
#                             return Response(
#                                 {
#                                     "error": "Something went wrong when registering account"
#                                 },
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             )
#                     else:
#                         return Response(
#                             {"error": "User Already Exists"},
#                             status=status.HTTP_400_BAD_REQUEST,
#                         )
#                 else:
#                     return Response(
#                         {"error": "Password must be at least 8 characters in length"},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             else:
#                 return Response(
#                     {"error": "Passwords do not match"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except:
#             return Response(
#                 {"error": "Something went wrong while trying to register account"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
