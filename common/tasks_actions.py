from tasks.api.serializers import LessFieldsTaskSerializer
from .actions import allItems, countStatuses
from tasks.models import Task
from rest_framework.response import Response
from projects.models import Project


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
        return allItems(LessFieldsTaskSerializer, queryset)
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
