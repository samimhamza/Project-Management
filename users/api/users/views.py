from common.actions import withTrashed, trashList, restore, delete, allItems, filterRecords
from users.api.serializers import UserSerializer, UserWithProfileSerializer
from common.permissions import addPermissionsToUser, addRolesToUser
from common.permissions_scopes import UserPermissions
from common.custom import CustomPageNumberPagination
from common.base64_image import convertBase64ToImage
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import User


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
        if request.GET.get("items_per_page") == "-1":
            return allItems(UserWithProfileSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        data = request.data
        imageField = convertBase64ToImage(data["profile"])
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
        addPermissionsToUser(data['permissions'], new_user)
        addRolesToUser(request.data.get("roles"), new_user)
        new_user.save()

        serializer = UserSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = self.get_object()
        if request.data.get("username"):
            user.username = request.data.get("username")
        if request.data.get("first_name"):
            user.first_name = request.data.get("first_name")
        if request.data.get("last_name"):
            user.last_name = request.data.get("last_name")
        if request.data.get("phone"):
            user.phone = request.data.get("phone")
        if request.data.get("whatsapp"):
            user.whatsapp = request.data.get("whatsapp")
        if request.data.get("email"):
            user.email = request.data.get("email")
        if request.data.get("profile"):
            imageField = convertBase64ToImage(request.data.get("profile"))
            user.profile = imageField
        user.updated_by = request.user
        addPermissionsToUser(request.data.get("permissions"), user)
        addRolesToUser(request.data.get("roles"), user)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, User)

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
