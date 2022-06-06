from common.permissions_scopes import HolidayPermissions, ReminderPermissions, RolePermissions
from users.models import Reminder, Holiday, Notification, Action, Permission, Role
from common.actions import withTrashed, trashList, restore, delete, allItems
from common.custom import CustomPageNumberPagination
from rest_framework.permissions import IsAuthenticated
from common.permissions import addPermissionsToRole
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from users.api.serializers import (
    NotificationSerializer,
    ReminderSerializer,
    HolidaySerializer,
    ActionSerializer,
    PermissionActionSerializer,
    RoleSerializer,
    RoleListSerializer
)
from rest_framework import generics


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (HolidayPermissions,)


class PermmissionListAPIView(generics.ListAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ActionSerializer(queryset, many=True)
        for permission in serializer.data:
            sub_action_ids = Permission.objects.filter(action=permission['id'])
            actionSerializer = PermissionActionSerializer(
                sub_action_ids, many=True)
            permission['actions'] = []
            for action in actionSerializer.data:
                permission['actions'].append(action['sub_action'])
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = CustomPageNumberPagination


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all().order_by("-updated_at")
    serializer_class = ReminderSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ReminderPermissions,)

    def list(self, request):
        queryset = self.get_queryset()

        if request.GET.get("items_per_page") == "-1":
            return allItems(ReminderSerializer, queryset)

        if request.GET.get("user_id"):
            queryset = Reminder.objects.filter(
                user=request.GET.get("user_id")).order_by("-updated_at")

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, pk=None):
        return delete(self, request, Reminder)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.filter(
        deleted_at__isnull=True).order_by("-updated_at")
    serializer_class = RoleSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (RolePermissions,)

    def list(self, request):
        queryset = self.get_queryset()
        if request.GET.get("items_per_page") == "-1":
            return allItems(RoleListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        data["updated_by"] = request.user
        new_role = Role.objects.create(
            name=data["name"],
            created_by=data["created_by"],
            updated_by=data["updated_by"],
        )
        addPermissionsToRole(data['permissions'], new_role)
        serializer = RoleSerializer(new_role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        role = self.get_object()
        serializer = self.get_serializer(role)
        data = serializer.data
        permissions = Permission.objects.only('id').filter(roles=role)
        actions = Action.objects.filter(
            permission_action__in=permissions).distinct()
        actionSerializer = ActionSerializer(actions, many=True)
        for action in actionSerializer.data:
            sub_action_ids = permissions.filter(
                action=action['id'])
            subActionSerializer = PermissionActionSerializer(
                sub_action_ids, many=True)
            action['actions'] = []
            for subAction in subActionSerializer.data:
                action['actions'].append(subAction['sub_action'])
        data['permissions'] = actionSerializer.data
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        role = self.get_object()
        if request.data.get("name"):
            role.name = request.data.get("name")
        role.updated_by = request.user
        addPermissionsToRole(request.data.get('permissions'), role)
        role.save()
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Role)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Role, order_by="-updated_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Role)

    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Role)

    @action(detail=False, methods=["get"])
    def auth_user(self, request, pk=None):
        user = request.user
        serializer = RoleSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
