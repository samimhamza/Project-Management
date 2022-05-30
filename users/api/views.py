from rest_framework import viewsets, status
from users.api.serializers import (
    UserSerializer,
    NotificationSerializer,
    ReminderSerializer,
    HolidaySerializer,
    UserWithProfileSerializer,
    CreateUserSerializer
)
from users.models import User, Reminder, Holiday, Notification
from common.custom import CustomPageNumberPagination
from common.actions import withTrashed, trashList, restore, delete, allItems
from rest_framework.response import Response
from rest_framework.decorators import action
import base64
from django.core.files.base import ContentFile

import uuid
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    serializer_action_classes = {
        "create": CreateUserSerializer,
        "update": CreateUserSerializer
    }
    queryset_actions = {
        "check_uniqueness": User.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()

        if request.GET.get("items_per_page") == "-1":
            return allItems(UserWithProfileSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        profile = data["profile"]
        format, imgstr = profile.split(';base64,')
        ext = format.split('/')[-1]
        imageField = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        data["created_by"] = request.user
        data["updated_by"] = request.user
        new_user = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            whatsapp=data["whatsapp"],
            profile=imageField,
            is_active=True,
            created_by=data["created_by"],
            updated_by=data["updated_by"],
        )
        new_user.set_password(data["password"])
        new_user.save()
        serializer = UserSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = self.get_object()
        if request.data.get("username"):
            project.username = request.data.get("username")
        if request.data.get("first_name"):
            project.first_name = request.data.get("first_name")
        if request.data.get("last_name"):
            project.last_name = request.data.get("last_name")
        if request.data.get("phone"):
            project.phone = request.data.get("phone")
        if request.data.get("whatsapp"):
            project.whatsapp = request.data.get("whatsapp")
        if request.data.get("email"):
            project.email = request.data.get("email")
        if request.data.get("profile"):
            project.profile = request.data.get("profile")
        project.updated_by = request.user
        project.save()
        serializer = UserSerializer(project)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, User)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, User, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, User)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, User)

    @action(detail=False, methods=["get"])
    def auth_user(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def check_uniqueness(self, request):
        if request.data.get("email"):
            try:
                User.objects.get(email=request.data.get("email"))
                return Response({"error": "email already in use"}, status=400)
            except User.DoesNotExist:
                return Response({"success": "email is available"}, status=200)
        if request.data.get("username"):
            try:
                User.objects.get(username=request.data.get("username"))
                return Response({"error": "username already in use"}, status=400)
            except User.DoesNotExist:
                return Response({"success": "username is available"}, status=200)

    # return different Serializers for different actions
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()


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
        return delete(self, request, Reminder)
