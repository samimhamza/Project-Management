from os import stat
from tasks.api.serializers import LessFieldsTaskSerializer, ParentTaskSerializer
from common.notification import sendNotification
from .actions import allItems, countStatuses
from rest_framework.response import Response
from common.pusher import pusher_client
from tasks.models import Task, UserTask
from projects.models import Project
import math


def broadcastProgress(data):
    project_id = {"project_id": str(data['project_id'])}
    data.update(project_id)
    pusher_client.trigger(
        u'tasks', u'progress', data)


def prepareData(serializer, task):
    data = {"serializer_data": serializer.data}
    newData = data["serializer_data"]
    del data["serializer_data"]
    project_id = {"project_id": newData['task']['project']}
    project = Project.objects.get(pk=newData['task']['project'])
    project_progress = {"project_progress": project.progress}
    data.update(project_id)
    data.update(project_progress)
    user_progress = {"user_progress": newData['progress']}
    data.update(user_progress)
    data['tasks'] = []
    data['tasks'].append(
        {
            "id": newData['task']['id'],
            "progress": newData['task']['progress']
        })
    parent = task.parent
    while True:
        if parent:
            data['tasks'].append(ParentTaskSerializer(parent).data)
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


def projectProgress(project):
    project = Project.objects.get(pk=project.id)
    tasks_progress = Task.objects.only('progress').filter(
        project=project, parent__isnull=True).values('progress')
    totalProgress = 0
    for task in tasks_progress:
        totalProgress += task['progress']
    totalProgress = totalProgress / len(tasks_progress)
    project.progress = int(totalProgress)
    project.save()


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


def taskThumbnail(self, request, queryset):
    items_per_page = request.GET.get(
        "items_per_page") if request.GET.get("items_per_page") else 10
    page = request.GET.get(
        "page") if request.GET.get("page") else 1
    page = int(page)
    items_per_page = int(items_per_page)
    pendingTotal = queryset.filter(status='pending').count()
    inProgressTotal = queryset.filter(status='in_progress').count()
    completedTotal = queryset.filter(status='completed').count()
    pending = queryset.filter(status='pending')[
        0 if page == 1 else ((page-1) * items_per_page): page * items_per_page]
    in_progress = queryset.filter(status='in_progress')[
        0 if page == 1 else ((page-1) * items_per_page): page * items_per_page]
    completed = queryset.filter(status='completed')[
        0 if page == 1 else ((page-1) * items_per_page): page * items_per_page]
    if pending.count() == 0 and in_progress.count() == 0 and completed.count() == 0:
        return Response(
            {
                "detail": "Invalid page"
            }
        )
    serializer1 = self.get_serializer(pending, many=True)
    serializer2 = self.get_serializer(in_progress, many=True)
    serializer3 = self.get_serializer(completed, many=True)
    return Response(
        {
            "count": queryset.filter(status__in=["in_progress", "pending", "completed"]).count(),
            "total_pages": math.ceil(queryset.count() / (items_per_page * 3)),
            "total": int(request.GET.get("items_per_page")) if request.GET.get("items_per_page") else 10,
            "current_page": int(request.GET.get("page")) if request.GET.get("page") else 1,
            "pendingTotal": pendingTotal,
            "inProgressTotal": inProgressTotal,
            "completedTotal": completedTotal,
            "results": {'pending': serializer1.data, 'in_progress': serializer2.data, 'completed': serializer3.data},
        }
    )


def tasksOfProject(self, request, queryset):
    project_id = request.GET.get("project_id")
    queryset = queryset.filter(project=request.GET.get(
        "project_id")).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        if request.GET.get("extract_stages"):
            queryset = queryset.exclude(
                type="stage", childs__type="sub_stage")
            return allItems(LessFieldsTaskSerializer, queryset)
        return allItems(LessFieldsTaskSerializer, queryset)
    if request.GET.get("items_per_page") == "-2":
        return allItems(self.get_serializer, queryset)
    if request.GET.get('thumbnail'):
        return taskThumbnail(self, request, queryset)
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
    if request.data.get('progress'):
        progress = data['progress']
    else:
        progress = 0
    return [data['name'], parent, project, start_date, end_date, description, priority, task_status, progress, creator]


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
