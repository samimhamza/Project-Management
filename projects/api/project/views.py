from common.project_actions import (shareTo, notification, getRevokeNotification, broadcastProject,
                                    broadcastDeleteProject, addStagesToProject, update, retrieve, add_users, add_teams)
from projects.api.project.serializers import ProjectSerializer, ProjectTrashedSerializer
from common.actions import (delete, allItems, filterRecords, addAttachment,
                            deleteAttachments, projectsOfUser, convertBase64ToImage)
from users.api.teams.serializers import LessFieldsTeamSerializer
from projects.api.serializers import ProjectNameListSerializer
from users.api.serializers import UserWithProfileSerializer
from common.permissions_scopes import ProjectPermissions
from projects.models import Project, Department
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
from users.models import User, Team
from rest_framework import status


class ProjectViewSet(Repository):
    model = Project
    queryset = Project.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProjectSerializer
    permission_classes = (ProjectPermissions,)
    serializer_action_classes = {
        "trashed": ProjectTrashedSerializer,
    }
    queryset_actions = {
        "destroy": Project.objects.all(),
        "trashed": Project.objects.all(),
        "restore": Project.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request, table=Project)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ProjectNameListSerializer, queryset)
        if request.GET.get("items_per_page") == "-2":
            return allItems(self.get_serializer, queryset)

        if request.GET.get("user_id"):
            return projectsOfUser(self, request, queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        project = self.get_object()
        return retrieve(self, request, project)

    def create(self, request):
        data = request.data
        data["created_by"] = request.user
        try:
            department = Department.objects.only(
                'id').get(pk=data["department"])
        except Department.DoesNotExist:
            return Response({"error": "Department does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        imageField = convertBase64ToImage(data["banner"])
        new_project = Project.objects.create(
            name=data["name"],
            department=department,
            priority=data["priority"],
            company_name=data["company_name"],
            company_email=data["company_email"],
            description=data["description"],
            p_start_date=data["p_start_date"],
            p_end_date=data["p_end_date"],
            banner=imageField,
            created_by=data["created_by"],
            updated_by=data["created_by"],
        )
        new_project = shareTo(request, data, new_project)
        new_project.save()
        serializer = ProjectSerializer(
            new_project, context={"request": request})
        broadcastProject(new_project, serializer.data)
        addStagesToProject(new_project, department, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = self.get_object()
        return update(self, request, project)

    def destroy(self, request, pk=None):
        response = delete(self, request, Project)
        ids = []
        for id in response.data['deleted_ids']:
            ids.append(str(id))
        broadcastDeleteProject({'deleted_ids': ids})
        return response

    # Custom Actions
    @ action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        project = Project.objects.only('id').get(pk=pk)
        users = User.objects.filter(project_users=project)
        if request.query_params.get('content'):
            columns = ['first_name', 'last_name', 'email']
            users = filterRecords(users, request, columns, table=User)
            serializer = UserWithProfileSerializer(
                users, many=True,  context={"request": request})
            return Response(serializer.data)

        page = self.paginate_queryset(users)
        serializer = UserWithProfileSerializer(
            page, many=True,  context={"request": request})
        return self.get_paginated_response(serializer.data)

    @ action(detail=True, methods=["get"])
    def teams(self, request, pk=None):
        project = Project.objects.only('id').get(pk=pk)
        teams = Team.objects.filter(projects=project)
        if request.query_params.get('content'):
            columns = ['name']
            teams = filterRecords(teams, request, columns, table=Team)
            serializer = LessFieldsTeamSerializer(
                teams, many=True, context={"request": request})
            return Response(serializer.data)
        page = self.paginate_queryset(teams)
        serializer = LessFieldsTeamSerializer(
            page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    @ action(detail=True, methods=["post"])
    def add_users(self, request, pk=None):
        try:
            project = self.get_object()
            return add_users(request, project)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["post"])
    def add_teams(self, request, pk=None):
        try:
            project = self.get_object()
            return add_teams(request, project)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["delete"])
    def delete_users(self, request, pk=None):
        try:
            project = self.get_object()
            data = request.data
            for user in data['ids']:
                project.users.remove(user)
            notification(getRevokeNotification, project,
                         request, 'pk__in', data['ids'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["delete"])
    def delete_teams(self, request, pk=None):
        try:
            project = self.get_object()
            data = request.data
            for team in data['ids']:
                project.teams.remove(team)
            notification(getRevokeNotification,
                         project, request, 'teams__in', data['ids'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        return addAttachment(self, request)

    @ action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @ action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        users = User.objects.filter(
            deleted_at__isnull=True).exclude(project_users=pk).order_by("-created_at")
        serializer = UserWithProfileSerializer(
            users, many=True,  context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @ action(detail=True, methods=["get"])
    def excluded_teams(self, request, pk=None):
        teams = Team.objects.filter(deleted_at__isnull=True).exclude(
            projects__id=pk).order_by("-created_at")
        serializer = LessFieldsTeamSerializer(
            teams, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
