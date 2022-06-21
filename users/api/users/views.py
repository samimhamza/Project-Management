from common.actions import (withTrashed, trashList, restore, delete,
                            allItems, filterRecords, dataWithPermissions, searchRecords, convertBase64ToImage)
from users.api.serializers import UserSerializer, UserWithProfileSerializer, UserPermissionListSerializer
from common.permissions import addPermissionsToUser, addRolesToUser
from common.permissions_scopes import UserPermissions
from common.custom import CustomPageNumberPagination
from users.models import User, UserPermissionList
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
import os


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (UserPermissions,)

    queryset_actions = {
        "check_uniqueness": User.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        columns = ['username', 'first_name',
                   'last_name', 'email', 'phone', 'whatsapp']
        queryset = searchRecords(queryset, request, columns)
        if request.GET.get("items_per_page") == "-1":
            return allItems(UserWithProfileSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        imageField = convertBase64ToImage(data["profile"])
        data["created_by"] = request.user
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
            updated_by=data["created_by"],
        )
        new_user.set_password(data["password"])
        addPermissionsToUser(data['permissions'], new_user)
        addRolesToUser(request.data.get("roles"), new_user)
        new_user.save()

        serializer = UserSerializer(new_user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = self.get_object()
        if request.data.get("profile"):
            imageField = convertBase64ToImage(request.data.get("profile"))
            if os.path.isfile('media/'+str(user.profile)):
                os.remove('media/'+str(user.profile))
            user.profile = imageField
        for key, value in request.data.items():
            if key != "profile" and key != "permissions_users" and key != "roles_users":
                setattr(user, key, value)
        user.updated_by = request.user
        addPermissionsToUser(request.data.get("permissions"), user)
        addRolesToUser(request.data.get("roles"), user)
        user.save()
        serializer = UserSerializer(user, context={"request": request})
        if user == request.user:
            try:
                permissions = UserPermissionList.objects.get(user=user)
                serializer.data['permissions'] = UserPermissionListSerializer(
                    permissions).data['permissions_list']

            except UserPermissionList.DoesNotExist:
                serializer.data['permissions'] = []
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, pk=None):
        return dataWithPermissions(self, 'users')

    def destroy(self, request, pk=None):
        return delete(self, request, User, 'profile')

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, User, order_by="-created_at")

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, User)

    @action(detail=True, methods=["post"])
    def change_password(self, request, pk=None):
        try:
            user = self.get_object()
            data = request.data
            user.set_password(data['password'])
            user.save()
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

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

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
