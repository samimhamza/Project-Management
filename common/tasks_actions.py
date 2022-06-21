from tasks.api.serializers import LessFieldsTaskSerializer, LessTaskSerializer
from common.notification import sendNotification
from .actions import allItems, countStatuses
from rest_framework.response import Response
from common.pusher import pusher_client
from tasks.models import Task, UserTask
from projects.models import Project


def broadcastProgress(task_id, data, user_id):
    newData = []
    for obj in data:
        obj['project'] = str(obj['project'])
        newData.append(obj)
    newData[0]['user_id'] = user_id
    pusher_client.trigger(
        u'task.'+str(task_id), u'progress', newData)


def prepareData(serializer, task):
    data = [serializer.data]
    newData = data[0]
    del data[0]
    data.append(
        {
            "id": newData['task']['id'],
            "progress": newData['task']['progress'],
            "user_progress": newData['progress'],
            "project": newData['task']['project'],
        })
    parent = task.parent
    while True:
        if parent:
            data.append(LessTaskSerializer(parent).data)
            parent = parent.parent
        else:
            break
    return data


def updateProgress(task):
    totalProgress = 0
    sub_tasks = Task.objects.filter(deleted_at__isnull=True, parent=task)
    if len(sub_tasks) > 0:
        for sub_task in sub_tasks:
            totalProgress += sub_task.progress
        totalProgress = totalProgress / len(sub_tasks)
    else:
        users = UserTask.objects.filter(task=task)
        for user in users:
            totalProgress += user.progress
        totalProgress = totalProgress / len(users)
    task.progress = int(totalProgress)
    task.save()


def taskProgress(task):
    updateProgress(task)
    parent = task.parent
    while True:
        if parent:
            updateProgress(parent)
            parent = parent.parent
        else:
            break


def getAssignNotification(data, request):
    obj = {
        'title': 'Task Assignment',
        'description': ("Task " + str(data.name) + " has assigned to you by " +
                        str(request.user.first_name) + " " + str(request.user.last_name)),
        # 'instance_id': data.id,
        'model_name': "projects/"+str(data.project.id) + '/tasks/'
    }
    return obj


def getRevokeNotification(data, request):
    data = {
        'title': 'Task Revokement',
        'description': ("You have been revoked from task " + str(data.name) + " by " +
                        str(request.user.first_name) + " " + str(request.user.last_name)),
    }
    return data


def tasksResponse(self, serializer, project_id=None):
    countables = [
        'pendingTotal', 'status', 'pending',
        'inProgressTotal', 'status', 'in_progress',
        'completedTotal', 'status', 'completed',
        'issuFacedTotal', 'status', 'issue_faced',
        'failedTotal', 'status', 'failed',
        'cancelledTotal', 'status', 'cancelled'
    ]
    data = self.get_paginated_response(serializer.data).data
    data['statusTotals'] = countStatuses(Task, countables, project_id)
    return Response(data)


def tasksAccordingToStatus(self, request, project_id):
    queryset = Task.objects.filter(
        deleted_at__isnull=True, project=request.GET.get("project_id"), status=request.GET.get('status')).order_by("-created_at")
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return tasksResponse(self, serializer, project_id)


def tasksOfProject(self, request):
    project_id = request.GET.get("project_id")
    if request.GET.get('status'):
        return tasksAccordingToStatus(self, request, project_id)
    queryset = Task.objects.filter(
        deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(LessFieldsTaskSerializer, LessTaskSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return tasksResponse(self, serializer, project_id)


def checkAttributes(request):
    data = request.data
    creator = request.user
    if request.data.get("parent"):
        parent = Task.objects.only('id').get(pk=data['parent'])
    else:
        parent = None
    if request.data.get("project"):
        project = Project.objects.only('id').get(pk=data['project'])
    else:
        project = None
    if request.data.get("p_start_date"):
        start_date = data["p_start_date"]
    else:
        start_date = None
    if request.data.get("p_end_date"):
        end_date = data["p_end_date"]
    else:
        end_date = None
    if request.data.get("description"):
        description = data["description"]
    else:
        description = None
    if request.data.get('priority'):
        priority = data['priority']
    else:
        priority = "normal"
    if request.data.get('status'):
        task_status = data['status']
    else:
        task_status = "pending"
    return [data['name'], parent, project, start_date, end_date, description, priority, task_status, creator]


def excludedDependencies(serializerName, queryset, request):
    task = Task.objects.get(pk=request.GET.get("excluded_dependencies"))
    queryset = queryset.exclude(pk=task.id)
    if task.dependencies:
        queryset = queryset.exclude(pk__in=task.dependencies)
    serializer = serializerName(queryset, many=True)
    return Response(serializer.data, status=200)


def assignToUsers(request, task, users):
    revoke(request, task, users)
    notify_users = []
    data = getAssignNotification(
        task, request)
    for user in users:
        userTask, created = UserTask.objects.get_or_create(
            task=task, user=user)
        userTask.created_by = request.user
        userTask.updated_by = request.user
        userTask.save()
        if created:
            notify_users.append(user)
    sendNotification(request, notify_users, data)


def user(userTask):
    return userTask.user


def revoke(request, task, users):
    deleted_task_users = UserTask.objects.filter(
        task=task).exclude(user__in=users)
    data = getRevokeNotification(
        task, request)
    deleted_users = list(map(user, deleted_task_users))
    sendNotification(request, deleted_users, data)
    deleted_task_users.delete()
