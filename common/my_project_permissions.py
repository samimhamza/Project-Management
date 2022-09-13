from projects.api.my_projects.serializers import ProjectPermissionSerializer, ProjectPermissionUserSerializer
from projects.models import Project, ProjectPermission, ProjectPermissionUser
from users.api.serializers import PermissionSerializer
from users.models import Permission, Role
from django.db.models import Q


def projectPermissions(user, project, permissions):
    try:
        project_permissions_user = ProjectPermissionUser.objects.only('project_permission').filter(
            project=project, user=user).distinct()
    except:
        return []
    serializer = ProjectPermissionUserSerializer(
        project_permissions_user, many=True)
    for permission in serializer.data:
        per = permission['project_permission']['action']['name']
        action = permission['project_permission']['sub_action']['code']
        code = per + "_" + action
        if code not in permissions:
            permissions.append(code)


def userPromissions(user, permissions):
    user_role = Role.objects.only('name').filter(users=user)
    permissions_list2 = Permission.objects.filter(
        Q(users=user) | Q(roles__in=user_role)).filter(
            Q(action__name__icontains="project") | Q(action__name__icontains="task") |
            Q(action__name__icontains="expense") | Q(action__name__icontains="income") |
            Q(action__name__icontains="focal_point"))
    serializer2 = PermissionSerializer(permissions_list2, many=True)
    for permission in serializer2.data:
        per = permission['action']['name']
        action = permission['sub_action']['code']
        code = per + "_" + action
        if code not in permissions:
            permissions.append(code)


def getProjectPermissions(user, project, project_id=None):
    if project is None:
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return []
    permissions = []
    projectPermissions(user, project, permissions)
    userPromissions(user, permissions)
    return permissions


def getTaskPermissions(user, project, project_id=None):
    if project is None:
        project = Project.objects.get(pk=project_id)
    permissions_list = ProjectPermission.objects.filter(
        users=user, project=project, action__name__icontains="task")
    serializer = ProjectPermissionSerializer(permissions_list, many=True)
    permissions = []
    for permission in serializer.data:
        per = permission['action']['name']
        action = permission['sub_action']['code']
        code = per + "_" + action
        if code not in permissions:
            permissions.append(code)
    return permissions
