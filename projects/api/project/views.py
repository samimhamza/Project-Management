from tasks.models import Task
from projects.actions import (excluded_teams, excluded_users, member_actions, shareTo, broadcastProject,
                              addStagesToProject, list, update, retrieve, add_users, add_teams, users, teams,
                              delete_users, delete_teams, member_actions, destroy, projectTiming)
from projects.api.project.serializers import ProjectSerializer, ProjectTrashedSerializer
from common.actions import (
    addAttachment, deleteAttachments, convertBase64ToImage, countStatuses)
from common.permissions_scopes import ProjectPermissions
from projects.models import Project, Department
from rest_framework.response import Response
from rest_framework.decorators import action
from common.Repository import Repository
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
        return list(self, request, queryset)

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
        return destroy(self, request)

    # Custom Actions
    @ action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        project = self.get_object()
        return users(self, request, project)

    @ action(detail=True, methods=["get"])
    def teams(self, request, pk=None):
        project = self.get_object()
        return teams(self, request, project)

    @ action(detail=True, methods=["post"])
    def add_users(self, request, pk=None):
        return member_actions(self, add_users, request)

    @ action(detail=True, methods=["post"])
    def add_teams(self, request, pk=None):
        return member_actions(self, add_teams, request)

    @ action(detail=True, methods=["delete"])
    def delete_users(self, request, pk=None):
        return member_actions(self, delete_users, request)

    @ action(detail=True, methods=["delete"])
    def delete_teams(self, request, pk=None):
        return member_actions(self, delete_teams, request)

    @action(detail=True, methods=["post"])
    def add_attachments(self, request, pk=None):
        try:
            project = self.get_object()
            return addAttachment(request, project)
        except:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=True, methods=["delete"])
    def delete_attachments(self, request, pk=None):
        return deleteAttachments(self, request)

    @ action(detail=True, methods=["get"])
    def excluded_users(self, request, pk=None):
        return excluded_users(request, pk)

    @ action(detail=True, methods=["get"])
    def excluded_teams(self, request, pk=None):
        return excluded_teams(request, pk)

    @ action(detail=False, methods=["get"])
    def projects_status(self, request, pk=None):
        countables = [
            'pending', 'status', 'pending',
            'in_progress', 'status', 'in_progress',
            'completed', 'status', 'completed',
            'issue_faced', 'status', 'issue_faced',
            'failed', 'status', 'failed',
            'cancelled', 'status', 'cancelled'
        ]
        if request.query_params.get('project_id'):
            return Response(countStatuses(Task, countables,request.GET['project_id']))
        else:
            return Response(countStatuses(Project, countables))

    @ action(detail=False, methods=["get"])
    def project_timing(self, request, pk=None):
        projects = ''
        if request.query_params.get('project_id'):
            projects = Project.objects.filter(id=request.GET['project_id'])
        else:
            projects = Project.objects.filter(deleted_at__isnull=True).order_by("-created_at")[:10]
        return Response(projectTiming(projects))
