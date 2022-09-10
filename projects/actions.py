from itertools import permutations
from common.actions import (convertBase64ToImage, getAttachments, countStatuses, filterRecords,
                            allItems, projectsOfUser, unAuthorized, delete, bussinessHours, taskTimingCalculator)
from projects.models import Project, FocalPoint, ProjectPermission, ProjectPermissionUser, Action, SubAction
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
    # broadcastProject(project, serializer.data)
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
    response = delete(self, request, Project, imageField="banner")
    ids = []
    for id in response.data['deleted_ids']:
        ids.append(str(id))
    # broadcastDeleteProject({'deleted_ids': ids})
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
    for user in users:
        for key, value in data["permissions"].items():
            permissions = ProjectPermission.objects.filter(
                action=key, sub_action__in=value)
            for permission in permissions:
                p, created = ProjectPermissionUser.objects.get_or_create(
                    project_permission=permission, project=project, user=user)
    # notification(getAssignNotification, project,
    #              request, 'pk__in', data['ids'])
    serializer = UserWithProfileSerializer(
        users, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def add_teams(request, project):
    data = request.data
    teams = Team.objects.filter(pk__in=data['ids'])
    for team in data['ids']:
        project.teams.add(team)
    users = User.objects.filter(teams__in=teams)
    for user in users:
        for key, value in data["permissions"].items():
            permissions = ProjectPermission.objects.filter(
                action=key, sub_action__in=value)
            for permission in permissions:
                p, created = ProjectPermissionUser.objects.get_or_create(
                    project_permission=permission, project=project, user=user)
    # notification(getAssignNotification,
    #              project, request, 'teams__in', data['ids'])
    serializer = LessFieldsTeamSerializer(
        teams, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_users(request, project):
    data = request.data
    for user in data['ids']:
        project.users.remove(user)
    users = User.objects.filter(pk__in=data['ids'])
    for user in users:
        permissions = ProjectPermissionUser.objects.filter(
            project=project, user=user)
        permissions.delete()
    # notification(getRevokeNotification, project,
    #              request, 'pk__in', data['ids'])
    return Response(status=status.HTTP_204_NO_CONTENT)


def delete_teams(request, project):
    data = request.data
    for team in data['ids']:
        project.teams.remove(team)
    users = User.objects.filter(teams__in=data['ids'])
    for user in users:
        permissions = ProjectPermissionUser.objects.filter(
            project=project, user=user)
        permissions.delete()
    # notification(getRevokeNotification,
    #              project, request, 'teams__in', data['ids'])
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
    if checkProjectScope(request.user, project, "projects_m"):
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
        if checkProjectScope(request.user, project, "projects_m"):
            return method(request, project)
        else:
            return unAuthorized()
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


def get_user(request, project):
    try:
        user = User.objects.only('id').get(pk=request.GET.get("user_id"))
    except User.DoesNotExist:
        return Response({"detail": "User does not exists!"}, status=status.HTTP_404_NOT_FOUND)
    try:
        projectPermissionsUser = ProjectPermissionUser.objects.get(
            user=user, project=project)
        for permission in projectPermissionsUser:
            permission_action = Action.objects.get(
                pk=permission.action).values_list("id", "name", "model")
            actions = SubAction.objects.filter(permission_action)

    except ProjectPermissionUser.DoesNotExist:
        return Response({"detail": "UserPermission does not exists!"}, status=status.HTTP_404_NOT_FOUND)


def abbr(text=None):
    if(text is not None):
        abbr = ''
        x = text.split()
        if len(x) >= 2:
            for i in x:
                abbr += i[0]
        elif len(x) == 1:
            count = 0
            for j in x[0]:
                abbr += j
                count = count+1
                if count == 3:
                    break
        return abbr.upper()
    return ''


def projectTiming(projects):
    result = []
    for project in projects:
        pro_obj = {"name": project.name, "abbr": abbr(
            project.name), "overdue": 0, "normal": 0, "earlier": 0, "notclear": 0, "total_tasks": project.tasks.count()}
        for task in project.tasks.filter(deleted_at__isnull=True):
            if all([task.p_start_date, task.p_end_date, task.a_start_date, task.a_end_date]) is False:
                pro_obj['notclear'] = pro_obj['notclear'] + 1
            else:
                businesshrs = bussinessHours()
                planDiff = businesshrs.difference(
                    task.p_start_date, task.p_end_date)
                actualDiff = businesshrs.difference(
                    task.a_start_date, task.a_end_date)
                taskTimingCalculator(pro_obj, planDiff.hours, actualDiff.hours)

        result.append(pro_obj)
    return result


def focalPointList(self, request, queryset):
    queryset = FocalPoint.objects.filter(
        deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)


def focalPointCreate(self, request, data, project):
    data["created_by"] = request.user
    profile = convertBase64ToImage(data["profile"])
    new_focalPoint = FocalPoint.objects.create(
        project=project,
        profile=profile,
        contact_name=data["contact_name"],
        contact_last_name=data["contact_last_name"],
        phone=data["phone"],
        email=data["email"],
        whatsapp=data["whatsapp"] if request.data.get(
            'whatsapp') else None,
        position=data["position"] if request.data.get(
            'position') else None,
        prefer_communication_way=data["prefer_communication_way"] if request.data.get(
            'prefer_communication_way') else "email",
        created_by=data["created_by"],
        updated_by=data["created_by"],
    )
    new_focalPoint.save()
    serializer = self.get_serializer(
        new_focalPoint, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def focalPointUpdate(self, request, focal_point):
    data = request.data
    if request.data.get("profile"):
        imageField = convertBase64ToImage(data["profile"])
        if imageField:
            if os.path.isfile('media/'+str(focal_point.profile)):
                os.remove('media/'+str(focal_point.profile))
            focal_point.profile = imageField
    for key, value in data.items():
        if key != "id" and key != "project" and key != "profile":
            setattr(focal_point, key, value)
    focal_point.updated_by = request.user
    focal_point.save()
    serializer = self.get_serializer(
        focal_point, context={"request": request})
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
