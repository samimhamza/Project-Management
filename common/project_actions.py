from common.notification import sendNotification
from projects.models import Stage, SubStage
from common.pusher import pusher_client
from users.models import User, Team
from tasks.models import Task


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
            # created_by=request.user,
            # updated_by=request.user,
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
                # created_by=request.user,
                # updated_by=request.user,
                type="sub_stage"
            )
