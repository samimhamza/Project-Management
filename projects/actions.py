from common.actions import (convertBase64ToImage, getAttachments,
                            countStatuses, filterRecords, allItems, projectsOfUser, unAuthorized, delete)
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
import businesstimedelta
import datetime
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


# ProjectViewSet and MyProjectViewSet list function
def list(self, request, queryset, showPermissions=False):
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
    if showPermissions:
        for project in serializer.data:
            project["permissions"] = getProjectPermissions(
                request.user, None, project["id"])
    return self.get_paginated_response(serializer.data)


# ProjectViewSet and MyProjectViewSet update function
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


# ProjectViewSet and MyProjectViewSet retrieve function
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


def destroy(self, request):
    response = delete(self, request, Project)
    ids = []
    for id in response.data['deleted_ids']:
        ids.append(str(id))
    broadcastDeleteProject({'deleted_ids': ids})
    return response


# ProjectViewSet and MyProjectViewSet users action
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


# ProjectViewSet and MyProjectViewSet teams action
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


def delete_users(request, project):
    data = request.data
    for user in data['ids']:
        project.users.remove(user)
    notification(getRevokeNotification, project,
                 request, 'pk__in', data['ids'])
    return Response(status=status.HTTP_204_NO_CONTENT)


def delete_teams(request, project):
    data = request.data
    for team in data['ids']:
        project.teams.remove(team)
    notification(getRevokeNotification,
                 project, request, 'teams__in', data['ids'])
    return Response(status=status.HTTP_204_NO_CONTENT)


def attachments(method, scope, request, pk):
    try:
        try:
            project = Project.objects.only(
                'id').get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkProjectScope(request.user, project, scope):
            return method(request, project)
        else:
            return unAuthorized()
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


def excluded_members(method, request, pk):
    try:
        project = Project.objects.only(
            'id').get(pk=pk, users=request.user)
    except Project.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    if checkProjectScope(request.user, project, "project_m"):
        return method(request, pk)
    else:
        return unAuthorized()


# ProjectViewSet and MyProjectViewSet excluded_users
def excluded_users(request, pk):
    users = User.objects.filter(
        deleted_at__isnull=True).exclude(project_users=pk).order_by("-created_at")
    serializer = UserWithProfileSerializer(
        users, many=True,  context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ProjectViewSet and MyProjectViewSet excluded_teams
def excluded_teams(request, pk):
    teams = Team.objects.filter(deleted_at__isnull=True).exclude(
        projects__id=pk).order_by("-created_at")
    serializer = LessFieldsTeamSerializer(
        teams, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ProjectViewSet Member Actions
def member_actions(self, method, request):
    try:
        project = self.get_object()
        return method(request, project)
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


# MyProjectViewSet Member Actions
def my_project_member_actions(method, request, pk):
    try:
        try:
            project = Project.objects.only('id').get(pk=pk, users=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkProjectScope(request.user, project, "projectd_m"):
            return method(request, project)
        else:
            return unAuthorized()
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


def projectTiming(projects):
    result = []
    for project in projects:
        pro_obj = {}
        pro_obj['name'] = project['name']
        pro_obj['overdue'] = 0
        pro_obj['normal'] = 0
        pro_obj['earlier'] = 0
        pro_obj['notclear'] = 0
        pro_obj['total_tasks'] = len(project['tasks']);

        for task in project['tasks']:
            if task['p_start_date'] is None or task['p_end_date'] is None or task['a_start_date'] is None or task['a_end_date'] is None :
                pro_obj['notclear'] = pro_obj['notclear'] + 1;
            else:
                workday = businesstimedelta.WorkDayRule(
                    start_time=datetime.time(8),
                    end_time=datetime.time(17),
                    working_days=[0, 1, 2, 3, 4,5])
                lunchbreak = businesstimedelta.LunchTimeRule(
                    start_time=datetime.time(12),
                    end_time=datetime.time(13),
                    working_days=[0, 1, 2, 3, 4, 5])

                businesshrs = businesstimedelta.Rules([workday, lunchbreak])
                taskModel = Task.objects.get(id=task['id'])
                planDiff = businesshrs.difference(taskModel.p_start_date , taskModel.p_end_date)
                actualDiff = businesshrs.difference(taskModel.a_start_date , taskModel.a_end_date)

                if planDiff.hours < actualDiff.hours:
                    pro_obj['overdue'] = pro_obj['overdue'] + 1;
                elif planDiff.hours > actualDiff.hours:
                    pro_obj['earlier'] = pro_obj['earlier'] + 1;
                elif planDiff.hours == actualDiff.hours:
                    pro_obj['normal'] = pro_obj['normal'] + 1;

        result.append(pro_obj)
    return result