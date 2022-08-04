from projects.api.my_projects.serializers import ProjectPermissionSerializer
from users.api.serializers import PermissionSerializer
from projects.models import Project, ProjectPermission
from users.models import Permission, Role
from django.db.models import Q


def getProjectPermissions(user, project, project_id=None):
    if project is None:
        project = Project.objects.get(pk=project_id)
    permissions_list = ProjectPermission.objects.filter(
        users=user, project=project)
    serializer = ProjectPermissionSerializer(permissions_list, many=True)
    permissions = []
    for permission in serializer.data:
        per = permission['action']['name']
        action = permission['sub_action']['code']
        code = per + "_" + action
        if code not in permissions:
            permissions.append(code)
    user_role = Role.objects.only('name').filter(users=user)
    permissions_list2 = Permission.objects.filter(
        Q(users=user) | Q(roles__in=user_role)).filter(action__name__icontains="project")
    serializer2 = PermissionSerializer(permissions_list2, many=True)
    for permission in serializer2.data:
        per = permission['action']['name']
        action = permission['sub_action']['code']
        code = per + "_" + action
        if code not in permissions:
            permissions.append(code)
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
