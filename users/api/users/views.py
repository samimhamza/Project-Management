from users.api.serializers import (
    UserSerializer, UserWithProfileSerializer, UserPermissionListSerializer, UserTrashedSerializer)
from common.actions import (allItems, filterRecords,
                            dataWithPermissions, convertBase64ToImage)
from common.permissions import addPermissionsToUser, addRolesToUser
from common.permissions_scopes import UserPermissions
from users.models import User, UserPermissionList
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from tasks.models import Task, UserTask
from projects.models import Project
from rest_framework import status
import os


class UserViewSet(Repository):
    model = User
    queryset = User.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)
    serializer_action_classes = {
        "trashed": UserTrashedSerializer
    }
    queryset_actions = {
        "check_uniqueness": User.objects.all(),
        "destroy": User.objects.all()
    }

    def list(self, request):
        queryset = self.get_queryset()
        columns = ['username', 'first_name',
                   'last_name', 'email', 'phone', 'whatsapp']
        queryset = filterRecords(queryset, request, columns, table=User)

        if request.GET.get("items_per_page") == "-1":
            return allItems(UserWithProfileSerializer, queryset, request)
        if request.GET.get("items_per_page") == "-2":
            return allItems(self.get_serializer, queryset)

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
            position=data["position"],
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
            if imageField:
                if os.path.isfile('media/'+str(user.profile)):
                    os.remove('media/'+str(user.profile))
                user.profile = imageField
        for key, value in request.data.items():
            if key != "profile" and key != "permissions_users" and key != "roles_users" and key != "password":
                setattr(user, key, value)
        if "password" in request.data:
            user.set_password(request.data.get("password"))
        user.updated_by = request.user
        if "permissions" in request.data:
            addPermissionsToUser(request.data.get("permissions"), user)
        if "roles" in request.data:
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

    @action(detail=True, methods=["post"])
    def change_password(self, request, pk=None):
        try:
            user = self.get_object()
            data = request.data
            user.set_password(data['password'])
            user.save()
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=True, methods=["get"])
    def tasks_projects(self, request, pk=None):
        user = self.get_object()
        projects = Project.objects.filter(
            users=user, status__in=['in_progress', 'completed'])
        in_progress = projects.filter(status="in_progress").count()
        completed = projects.filter(status="completed").count()
        projects = projects.count()
        userTasks = UserTask.objects.filter(user=user).values('task')
        tasks = Task.objects.filter(
            pk__in=userTasks, status__in=['in_progress', 'completed'])
        in_progress_tasks = tasks.filter(status="in_progress").count()
        completed_tasks = tasks.filter(status="completed").count()
        tasks = tasks.count()
        return Response({"projects": {
            "all": projects,
            "in_progress": in_progress,
            "completed": completed
        },
            "tasks": {
            "all": tasks,
            "in_progress": in_progress_tasks,
            "completed": completed_tasks
        }}, status=status.HTTP_200_OK)
