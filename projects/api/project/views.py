from common.actions import restore, delete, withTrashed, trashList, allItems, filterRecords
from rest_framework import viewsets, status
from projects.models import Project, Attachment
from users.models import User, Team
from projects.api.project.serializers import ProjectListSerializer, ProjectUsersSerializer
from projects.api.serializers import ProjectNameListSerializer, AttachmentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from common.custom import CustomPageNumberPagination
from common.permissions_scopes import ProjectPermissions
from users.models import User, Team
from rest_framework import viewsets, status
from projects.models import Project


# Sharing to Teams and Users
def shareTo(request, project_data, new_project):
    if request.data.get("share"):
        if project_data["share"] != "justMe":
            users = User.objects.filter(pk__in=project_data["users"])
            new_project.users.set(users)
            teams = Team.objects.filter(pk__in=project_data["teams"])
            new_project.teams.set(teams)
        if project_data["share"] == "everyone":
            users = User.objects.all()
            new_project.users.set(users)
    else:
        users = User.objects.filter(pk__in=project_data["users"])
        new_project.users.set(users)
        teams = Team.objects.filter(pk__in=project_data["teams"])
        new_project.teams.set(teams)
    return new_project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(
        deleted_at__isnull=True).order_by("-created_at")
    serializer_class = ProjectListSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (ProjectPermissions,)
    queryset_actions = {
        "destroy": Project.objects.all(),
        "trashed": Project.objects.all(),
        "restore": Project.objects.all(),
    }

    def list(self, request):
        queryset = self.get_queryset()
        queryset = filterRecords(queryset, request)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ProjectNameListSerializer, queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        project = self.get_object()
        data = ProjectListSerializer(project).data
        attachments = Attachment.objects.filter(
            object_id=project.id)
        data["attachments"] = AttachmentSerializer(
            attachments, many=True).data
        return Response(data)

    def create(self, request):
        project_data = request.data
        project_data["created_by"] = request.user
        project_data["updated_by"] = request.user
        new_project = Project.objects.create(
            name=project_data["name"],
            p_start_date=project_data["p_start_date"],
            p_end_date=project_data["p_end_date"],
            created_by=project_data["created_by"],
            updated_by=project_data["updated_by"],
        )
        new_project = shareTo(request, project_data, new_project)
        new_project.save()
        serializer = ProjectListSerializer(new_project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = self.get_object()
        if request.data.get("name"):
            project.name = request.data.get("name")
        if request.data.get("description"):
            project.description = request.data.get("description")
        if request.data.get("p_start_date"):
            project.p_start_date = request.data.get("p_start_date")
        if request.data.get("p_end_date"):
            project.p_end_date = request.data.get("p_end_date")
        if request.data.get("a_start_date"):
            project.a_start_date = request.data.get("a_start_date")
        if request.data.get("a_end_date"):
            project.a_end_date = request.data.get("a_end_date")
        if request.data.get("status"):
            project.status = request.data.get("status")
        if request.data.get("progress"):
            project.progress = request.data.get("progress")
        if request.data.get("priority"):
            project.priority = request.data.get("priority")
        if request.data.get("company_name"):
            project.company_name = request.data.get("company_name")
        if request.data.get("company_email"):
            project.company_email = request.data.get("company_email")
        if request.data.get("users"):
            users = User.objects.only('id').filter(
                pk__in=request.data.get("users"))
            project.users.set(users)
        if request.data.get("teams"):
            teams = Team.objects.only('id').filter(
                pk__in=request.data.get("teams"))
            project.teams.set(teams)
        project.updated_by = request.user
        project.save()
        serializer = ProjectListSerializer(project)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        return delete(self, request, Project)

    @ action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, Project, order_by="-created_at")

    @ action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, Project)

    # for multi and single restore
    @ action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, Project)

    # Custom Actions
    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        project = self.get_object()
        users = Project.objects.only('users').filter(pk=project)
        if request.GET.get("items_per_page") == "-1":
            return allItems(ProjectUsersSerializer, project)
        page = self.paginate_queryset(project)
        serializer = ProjectUsersSerializer(page)
        return self.get_paginated_response(serializer.data)

    # @action(detail=True, methods=["post"])
    # def add_user(self, request, pk=None):
    #     try:
    #         data = request.data
    #         team = self.get_object()
    #         user = get_object_or_404(User, pk=data["id"])
    #         team_user, created = TeamUser.objects.get_or_create(
    #             team=team, user=user)
    #         team_user.position = data["position"]
    #         team_user.save()
    #         serializer = TeamUserSerializer(team_user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except:
    #         return Response(
    #             {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    # @action(detail=True, methods=["get"])
    # def excluded_users(self, request, pk=None):

    #     users = User.objects.filter(
    #         deleted_at__isnull=True).exclude(teams__id=pk).order_by("-created_at")
    #     serializer = LessFieldsUserSerializer(users, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=["get"])
    # def excluded_projects(self, request, pk=None):

    #     projects = Project.objects.filter(deleted_at__isnull=True).exclude(
    #         teams__id=pk).order_by("-created_at")

    #     serializer = ProjectNameListSerializer(projects, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=["post"])
    # def add_project(self, request, pk=None):
    #     try:
    #         data = request.data
    #         team = self.get_object()
    #         team.projects.set(data["ids"])
    #         serializer = self.get_serializer(team)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except:
    #         return Response(
    #             {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    # @action(detail=True, methods=["post"])
    # def delete_user(self, request, pk=None):
    #     try:
    #         with transaction.atomic():
    #             team = self.get_object()
    #             data = request.data
    #             if request.data.get("ids"):
    #                 team_users = TeamUser.objects.filter(
    #                     team=team, user__in=data["ids"]
    #                 )
    #                 for team_user in team_users:
    #                     team_user.delete()
    #             elif request.data.get("id"):
    #                 team_user = TeamUser.objects.get(
    #                     team=team, user=data["id"])
    #                 team_user.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #     except:
    #         return Response(
    #             {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
