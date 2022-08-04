from common.actions import (convertBase64ToImage, getAttachments,
                            countStatuses, filterRecords, allItems, projectsOfUser)
from users.api.teams.serializers import LessFieldsTeamSerializer
from common.my_project_permissions import getProjectPermissions
from projects.api.serializers import ProjectNameListSerializer
from users.api.serializers import UserWithProfileSerializer
from common.notification import sendNotification
from common.permissions import checkProjectScope
from rest_framework.response import Response
from projects.models import Stage, SubStage
from common.pusher import pusher_client
from users.models import User, Team
from projects.models import Project
from rest_framework import status
from tasks.models import Task
import os


def broadcastProject(item, data, update=False):
    pusher_client.trigger(
        u'project', u'new_project', {
            "id": data['id'],
        })


def broadcastDeleteProject(deleted_ids):
    pusher_client.trigger(
        u'project', u'delete_project', deleted_ids)


def broadcastMember(item, data, update=False):
    try:
        instance = item.id
    except:
        instance = item
    pusher_client.trigger(
        u'project.'+str(instance), u'new_project', {
            "id": data['id'],
            "body": data['body'],
            "created_at": data['created_at'],
            "updated_at": data['updated_at'],
            "commented_by": data['commented_by'],
            "update": update,
        })


def getAssignNotification(data, request):
    obj = {
        'title': 'Project Assignment',
        'description': (str(data.name) + " Project has assigned to you by " +
                        str(request.user.first_name) + " " + str(request.user.last_name)),
        'instance_id': data.id,
        'model_name': 'projects'
    }
    return obj


def getNotificationData(project_data, new_project, request):
    team_users = User.objects.only('id').filter(
        teams__in=project_data["teams"])
    obj = getAssignNotification(new_project, request)
    return [team_users, obj]


def getRevokeNotification(data, request):
    data = {
        'title': 'Project Revokement',
        'description': ("You have been revoked from Project " + str(data.name) + " by " +
                        str(request.user.first_name) + " " + str(request.user.last_name)),
    }
    return data


def notification(funcName, table, request, column, ids):
    data = funcName(
        table, request)
    users = User.objects.filter(**{column: ids})
    sendNotification(request, users, data)


def shareTo(request, project_data, new_project):
    if project_data["share"] != "justMe":
        users = User.objects.only('id').filter(pk__in=project_data["users"])
        new_project.users.set(users)
        teams = Team.objects.only('id').filter(pk__in=project_data["teams"])
        new_project.teams.set(teams)
    if project_data["share"] == "everyone":
        users = User.objects.filter(deleted_at__isnull=True)
        new_project.users.set(users)
    if project_data["share"] != "justMe":
        [team_users, data] = getNotificationData(
            project_data, new_project, request)
        sendNotification(request, users, data, team_users)
    return new_project


def addStagesToProject(project, department, request):
    stages = Stage.objects.filter(
        department=department, deleted_at__isnull=True)
    for stage in stages:
        task = Task.objects.create(
            name=stage.name,
            description=stage.description,
            project=project,
            type="stage"
        )
        sub_stages = SubStage.objects.filter(
            stage=stage, deleted_at__isnull=True)
        for sub_stage in sub_stages:
            Task.objects.create(
                name=sub_stage.name,
                description=sub_stage.description,
                parent=task,
                project=project,
                type="sub_stage"
            )


def list(self, request, queryset):
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


def update(self, request, project):
    data = request.data
    if request.data.get("users") is not None:
        project.users.set(request.data.get("users"))
    if request.data.get("teams") is not None:
        project.teams.set(request.data.get("teams"))
    if request.data.get("banner"):
        imageField = convertBase64ToImage(data["banner"])
        if imageField:
            if os.path.isfile('media/'+str(project.banner)):
                os.remove('media/'+str(project.banner))
            project.banner = imageField
    for key, value in data.items():
        if key != "users" and key != "teams" and key != "id" and key != "department" and key != "banner":
            setattr(project, key, value)
    project.updated_by = request.user
    project.save()
    serializer = self.get_serializer(
        project, context={"request": request})
    broadcastProject(project, serializer.data)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


def retrieve(self, request, project, showPermission=False):
    serializer = self.get_serializer(project)
    data = serializer.data
    countables = [
        'pendingTasksTotal', 'status', 'pending',
        'inProgressTasksTotal', 'status', 'in_progress',
        'completedTasksTotal', 'status', 'completed',
        'issuFacedTasksTotal', 'status', 'issue_faced',
        'failedTasksTotal', 'status', 'failed',
        'cancelledTasksTotal', 'status', 'cancelled'
    ]
    data = getAttachments(request, data, project.id,
                          "project_attachments_v")
    data['statusTotals'] = countStatuses(Task, countables, project.id)
    if showPermission:
        data["permissions"] = getProjectPermissions(request.user, project)
    return Response(data)


def users(self, request, project):
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


def teams(self, request, project):
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


def add_users(request, project):
    data = request.data
    users = User.objects.filter(pk__in=data['ids'])
    for user in data['ids']:
        project.users.add(user)
    notification(getAssignNotification, project,
                 request, 'pk__in', data['ids'])
    serializer = UserWithProfileSerializer(
        users, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def add_teams(request, project):
    data = request.data
    teams = Team.objects.filter(pk__in=data['ids'])
    for user in data['ids']:
        project.teams.add(user)
    notification(getAssignNotification,
                 project, request, 'teams__in', data['ids'])
    serializer = LessFieldsTeamSerializer(
        teams, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def members(method, request, pk):
    try:
        try:
            project = Project.objects.get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkProjectScope(request.user, project, "projectd_m"):
            return method(request, project)
        else:
            return Response({
                "detail": "You do not have permission to perform this action."
            }, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )
