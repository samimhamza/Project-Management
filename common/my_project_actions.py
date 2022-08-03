from projects.api.my_projects.serializers import ProjectPermissionSerializer
from projects.models import Project, ProjectPermission


def getPermission(user, project, project_id=None):
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
    return permissions
