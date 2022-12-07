from tasks.api.serializers import LessFieldsTaskSerializer, ParentTaskSerializer, TaskSerializer
from common.actions import allItems, countStatuses, getAttachments, bussinessHours, taskTimingCalculator
from users.api.serializers import UserWithProfileSerializer
from tasks.api.serializers import ProgressSerializer
from common.notification import sendNotification
from rest_framework.response import Response
from common.pusher import pusher_client
from tasks.models import Task, UserTask
from projects.models import Project
from rest_framework import status
from users.models import User
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
    if task.progress == 100:
        task.status == "completed"
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
    serializer1 = self.get_serializer(
        pending, many=True, context={"request": request})
    serializer2 = self.get_serializer(
        in_progress, many=True, context={"request": request})
    serializer3 = self.get_serializer(
        completed, many=True, context={"request": request})
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
    queryset = queryset.filter(project=project_id).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        if request.GET.get("extract_stages"):
            queryset = queryset.exclude(
                type="stage", childs__type="sub_stage").order_by("type")
            return allItems(LessFieldsTaskSerializer, queryset)
        if request.GET.get("excluded_dependencies"):
            return excludedDependencies(LessFieldsTaskSerializer, queryset, request)
        return allItems(LessFieldsTaskSerializer, queryset)
    if request.GET.get("items_per_page") == "-2":
        return allItems(self.get_serializer, queryset)
    if request.GET.get('thumbnail'):
        return taskThumbnail(self, request, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(
        page, many=True, context={"request": request})
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
    queryset = queryset.exclude(pk=task.id).order_by("type")
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


def create(request):
    [name, parent, project, start_date, end_date, description,
     priority, task_status, progress, creator] = checkAttributes(request)
    new_Task = Task.objects.create(
        parent=parent,
        name=name,
        p_start_date=start_date,
        p_end_date=end_date,
        description=description,
        project=project,
        created_by=creator,
        updated_by=creator,
        priority=priority,
        progress=progress,
        status=task_status,
    )
    new_Task.save()
    taskProgressCalculator(new_Task)
    serializer = TaskSerializer(new_Task, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def update(self, request, task, project=None):

    if "dependencies" in request.data:
        if task.dependencies is not None:
            task.dependencies = task.dependencies + \
                list(set(request.data.get("dependencies")) -
                     set(task.dependencies))
        else:
            task.dependencies = request.data.get("dependencies")
    if "users" in request.data:
        users = User.objects.filter(pk__in=request.data.get('users'))
        assignToUsers(request, task, users)
    if "status" in request.data:
        if request.data["status"] == "completed":
            if task.progress == 100:
                task.status = "completed"
            else:
                return Response({"detail": "Cannot complete task when progress is not 100!"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            task.status = request.data["status"]

    if "a_end_date" in request.data:
        if task.progress == 100 or request.data["a_end_date"] is None:
            task.a_end_date = request.data["a_end_date"]
        else:
            return Response({"detail": "Cannot add actual end date when Task is not completed!"},
                            status=status.HTTP_400_BAD_REQUEST)
    for key, value in request.data.items():
        if key != "users" and key != "dependencies" and key != "id"\
                and key != "progress" and key != "status" and key != "a_end_date":
            setattr(task, key, value)
    task.updated_by = request.user
    task.save()
    serializer = self.get_serializer(task, context={"request": request})
    data = serializer.data
    data = getAttachments(request, data,
                          task.id, "task_attachments_v", project=project)

    # Check For if plan dates changes to update the progress
    if "p_start_date" in request.data:
        taskProgressCalculator(task)

    return Response(data, status=status.HTTP_202_ACCEPTED)


def excluded_users(self, task):
    users = User.objects.filter(
        project_users=task.project).exclude(users=task)
    serializer = UserWithProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def delete_dependencies(request, task):
    task.dependencies.remove(request.data.get('id'))
    task.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


def progress(request, task):
    data = request.data
    try:
        user = User.objects.get(pk=data['user_id'])
    except User.DoesNotExist:
        return Response({'error': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        userTask = UserTask.objects.get(user=user, task=task)
    except UserTask.DoesNotExist:
        return Response({'error': "Task has not assigned to this user"}, status=status.HTTP_400_BAD_REQUEST)
    if Task.objects.filter(parent=task, deleted_at__isnull=True).exists():
        return Response({'error': "Task has Sub tasks, please remove sub tasks first!"}, status=status.HTTP_400_BAD_REQUEST)
    userTask.progress = data['progress']
    userTask.save()
    # taskProgress(task)
    # projectProgress(task.project)
    taskProgressCalculator(task)
    serializer = ProgressSerializer(
        userTask)
    serializerData = prepareData(serializer, task)
    broadcastProgress(serializerData)
    return Response(serializerData)


def calculateUsersPerformance(users, project_id=None):
    result = []
    for user in users:
        user_obj = {"name": user.username, "overdue": 0, "normal": 0,
                    "earlier": 0, "notclear": 0}
        task_ids = UserTask.objects.filter(
            user=user.id).values_list('task').distinct()

        tasks = []
        if project_id is None:
            tasks = Task.objects.filter(pk__in=task_ids)
        else:
            tasks = Task.objects.filter(pk__in=task_ids, project=project_id)

        for task in tasks:
            if all([task.p_start_date, task.p_end_date, task.a_start_date, task.a_end_date]) is False:
                user_obj['notclear'] = user_obj['notclear'] + 1
            else:
                businesshrs = bussinessHours()
                planDiff = businesshrs.difference(
                    task.p_start_date, task.p_end_date)
                actualDiff = businesshrs.difference(
                    task.a_start_date, task.a_end_date)
                taskTimingCalculator(
                    user_obj, planDiff.hours, actualDiff.hours)

        result.append(user_obj)
    return result


def taskProgressCalculator(task, type=None):
    if type == "parent":
        id = task.pk
    else:
        selfProgressCalculator(task)
        id = task.parent_id
    while id:
        pTask = Task.objects.get(deleted_at__isnull=True, pk=id)
        if pTask:
            pTask.progress = parentProgressCalculator(pTask, "")
            if pTask.progress == 100:
                pTask.status = "completed"
            elif task.status == "in_progress":
                pTask.status = "in_progress"
            pTask.save()
        id = pTask.parent_id

    task.project.progress = parentProgressCalculator(
        task.project_id, "project")
    task.project.save()
    return True


def selfProgressCalculator(task):
    userTasks = UserTask.objects.filter(task=task.pk)
    totalProgress = 0
    for ut in userTasks:
        totalProgress += ut.progress

    if userTasks.count():
        calculatedProgress = int(totalProgress / userTasks.count())
    else:
        calculatedProgress = 0

    if calculatedProgress == 100:
        task.status = "completed"
    task.progress = calculatedProgress
    task.save()
    return True


def parentProgressCalculator(item, type):
    if type == "project":
        tasks = Task.objects.filter(
            deleted_at__isnull=True, project=item, type="stage")
    else:
        tasks = Task.objects.filter(deleted_at__isnull=True, parent=item.pk)

    total = 0
    hours = 0
    for t in tasks:
        if all([t.p_start_date, t.p_end_date]):
            businesshrs = bussinessHours()
            planDiff = businesshrs.difference(
                t.p_start_date, t.p_end_date)
            hours += planDiff.hours
            total += planDiff.hours * t.progress
    if hours:
        return int(total/hours)
    else:
        return 0


def emp_task_report(request):
    users = ''
    if request.query_params.get('project_id'):
        user_ids = Project.objects.filter(
            pk=request.GET['project_id']).values_list('users')
        users = User.objects.filter(
            deleted_at__isnull=True, pk__in=user_ids)
        return Response(calculateUsersPerformance(users, request.GET['project_id']))
    else:
        if request.query_params.get('user_id'):
            users = User.objects.filter(pk=request.GET['user_id'])
        else:
            user_ids = Project.objects.values_list('users')
            users = User.objects.filter(
                deleted_at__isnull=True, pk__in=user_ids)[:10]
        return Response(calculateUsersPerformance(users))
