from common.permissions_scopes import HolidayPermissions, ReminderPermissions, RolePermissions
from users.models import Reminder, Holiday, Action, Permission, Role, UserNotification
from common.actions import allItems, dataWithPermissions, filterRecords
from rest_framework.permissions import IsAuthenticated
from common.permissions import addPermissionsToRole
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from rest_framework import status
from users.api.serializers import (
    ReminderSerializer,
    HolidaySerializer,
    ActionSerializer,
    PermissionActionSerializer,
    RoleSerializer,
    RoleListSerializer,
    UserNotificationSerializer,
    RoleTrashedSerializer
)
from rest_framework import generics


class HolidayViewSet(Repository):
    model = Holiday
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = (HolidayPermissions,)


class PermmissionListAPIView(generics.ListAPIView):
    queryset = Action.objects.all().order_by('order')
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


class NotificationViewSet(Repository):
    model = UserNotification
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(
            receiver=request.user).order_by('-created_at')
        unseenTotal = queryset.filter(seen=False).count()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data).data
        data['unseenTotal'] = unseenTotal
        return Response(data)

    @action(detail=True, methods=["get"])
    def seen(self, request, pk=None):
        userNotification = self.get_object()
        userNotification.seen = True
        userNotification.save()
        return Response()


class ReminderViewSet(Repository):
    model = Reminder
    queryset = Reminder.objects.all().order_by("-updated_at")
    serializer_class = ReminderSerializer
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


class RoleViewSet(Repository):
    model = Role
    queryset = Role.objects.filter(
        deleted_at__isnull=True).order_by("-updated_at")
    serializer_class = RoleSerializer
    permission_classes = (RolePermissions,)
    serializer_action_classes = {
        "trashed": RoleTrashedSerializer
    }
    queryset_actions = {
        "destroy": Role.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request,  table=Role)
        if request.GET.get("items_per_page") == "-1":
            return allItems(RoleListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        new_role = Role.objects.create(
            name=data["name"],
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        addPermissionsToRole(data['permissions'], new_role)
        serializer = RoleSerializer(new_role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        return dataWithPermissions(self, 'roles')

    def update(self, request, pk=None):
        role = self.get_object()
        if "name" in request.data:
            role.name = request.data.get("name")
        role.updated_by = request.user
        addPermissionsToRole(request.data.get('permissions'), role)
        role.save()
        serializer = RoleSerializer(role, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["get"])
    def auth_user(self, request, pk=None):
        user = request.user
        serializer = RoleSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
