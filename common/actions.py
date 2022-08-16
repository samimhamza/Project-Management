from projects.models import Income
from users.api.serializers import PermissionActionSerializer, ActionSerializer, RoleListSerializer
from projects.api.serializers import AttachmentSerializer, ProjectNameListSerializer
from common.permissions import checkCustomPermissions, checkProjectScope
from expenses.api.serializers import LessFieldExpenseSerializer
from users.api.teams.actions import get_leader_by_id, get_total_users
from users.api.teams.serializers import TeamListSerializer
from users.models import Team, Permission, Action, Role
from projects.models import Project, Attachment
from django.core.files.base import ContentFile
from rest_framework.response import Response
from expenses.models import Expense
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
import businesstimedelta
import datetime
import base64
import uuid
import os


def convertBase64ToImage(base64file):
    if base64file and base64file != "" and ';base64,' in base64file:
        format, imgstr = base64file.split(';base64,')
        ext = format.split('/')[-1]
        name = str(uuid.uuid4())+'.' + ext
        imageField = ContentFile(base64.b64decode(
            imgstr), name)
        return imageField
    return ''


def getAttachments(request, data, id, permission, project=None):
    # custom permission checking for attachments scopes
    if project is None:
        attachments_permission = checkCustomPermissions(
            request, permission)
    else:
        attachments_permission = checkProjectScope(
            request.user, project, permission)
    if attachments_permission:
        attachments = Attachment.objects.filter(object_id=id)
        data['attachments'] = AttachmentSerializer(
            attachments, many=True, context={"request": request}).data
    return data


def countStatuses(table, countables, project_id=None):
    totals = {}
    for x in range(0, len(countables), 3):
        if project_id is not None:
            project = Project.objects.only('id').get(pk=project_id)
            itemTotal = table.objects.filter(
                **{countables[x+1]: countables[x+2]}, project=project, deleted_at__isnull=True).count()
        else:
            itemTotal = table.objects.filter(
                **{countables[x+1]: countables[x+2]}, deleted_at__isnull=True).count()
        totals[countables[x]] = itemTotal
    return totals


def countTime(table, countables, project_id=None):
    totals = {}
    return totals


def filterRecords(queryset, request, columns=[], **kwargs):
    data = request.query_params
    if request.query_params.get('content'):
        queries = Q()
        for column in columns:
            queries = queries | Q(
                **{'%s__icontains' % column: request.query_params.get('content')})
        queryset = queryset.filter(queries)
    for key, value in data.lists():
        if len(value) == 1:
            value = value[0]
            if value.startswith('like@@'):
                likeValue = value[6:]
                queryset = queryset.filter(
                    **{'%s__icontains' % key: likeValue})
                continue

            elif value.startswith('exact@@'):
                exactValue = value[7:]
                queryset = queryset.filter(**{key: exactValue})
                continue

            elif "__" in key:
                queryset = queryset.filter(**{key: value})
                continue

        if kwargs.get("table") is not None:
            if isinstance(value, str):
                value = [value]
            if value[0].startswith('range@@'):
                startValue = value[0][7:]
                endValue = value[1][7:]
                startDate = datetime.datetime.strptime(startValue, '%Y-%m-%d')
                endDate = datetime.datetime.strptime(endValue, '%Y-%m-%d')
                queryset = queryset.filter(**{"%s__range" % key: [datetime.datetime.combine(
                    startDate, datetime.time.min), datetime.datetime.combine(endDate, datetime.time.max)]})
                continue

            elif getattr(kwargs.get("table"), key, False):
                queryset = queryset.filter(**{"%s__in" % key: value})

    return queryset


def withTrashed(self, table, *args, **kwargs):
    if kwargs.get("order_by") is not None:
        queryset = table.objects.all().order_by(kwargs.get("order_by"))
    else:
        queryset = table.objects.all()

    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    if table == Team:
        for team in serializer.data:
            team["total_users"] = get_total_users(team["id"])
            team["leader"] = get_leader_by_id(team["id"])
    return self.get_paginated_response(serializer.data)


def trashList(self, table, *args, **kwargs):
    queryset = self.filter_queryset(
        table.objects.filter(deleted_at__isnull=False).order_by("-deleted_at")
    )
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)


def delete(self, request, table, imageField=None):
    data = request.data
    ids = []
    if data:
        items = table.objects.filter(pk__in=data["ids"])
        for item in items:
            ids.append(item.id)
            if getattr(table, 'deleted_at', False):
                if item.deleted_at:
                    item.delete()
                else:
                    item.deleted_at = datetime.datetime.now(tz=timezone.utc)
                    item.deleted_by = request.user
                    item.save()
            else:
                if imageField:
                    if os.path.isfile('media/'+str(getattr(item, imageField))):
                        os.remove('media/'+str(getattr(item, imageField)))
                item.delete()
    else:
        item = self.get_object()
        ids.append(item.id)
        if getattr(table, 'deleted_at', False):
            if item.deleted_at:
                item.delete()
            else:
                item.deleted_at = datetime.datetime.now(tz=timezone.utc)
                item.deleted_by = request.user
                item.save()
        else:
            if imageField:
                if os.path.isfile('media/'+str(getattr(table, imageField))):
                    os.remove('media/'+str(getattr(table, imageField)))
            item.delete()
    if len(ids) == 0:
        return Response({'detail': "Invalid Id"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'deleted_ids': ids}, status=status.HTTP_204_NO_CONTENT)


def restore(self, request, table):
    try:
        with transaction.atomic():
            data = request.data
            items = table.objects.filter(pk__in=data["ids"])
            for item in items:
                item.deleted_at = None
                item.deleted_by = None
                item.save()
            page = self.paginate_queryset(items)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


def allItems(serializerName, queryset, request=None):
    serializer = serializerName(
        queryset, many=True, context={"request": request})
    return Response(serializer.data, status=200)


def expensesOfProject(self, request, queryset):
    actualCount = None
    estimateCount = None
    queryset = queryset.filter(project=request.GET.get(
        "project_id")).order_by("-created_at")
    if request.GET.get("type"):
        queryset = queryset.filter(type=request.GET.get("type"))
        if request.GET.get("type") == "actual":
            actualCount = queryset.count()
        else:
            estimateCount = queryset.count()

    if actualCount is None:
        actualCount = Expense.objects.filter(
            project=request.GET.get("project_id"), type="actual").count()

    if estimateCount is None:
        estimateCount = Expense.objects.filter(
            project=request.GET.get("project_id"), type="estimate").count()

    if request.GET.get("items_per_page") == "-1":
        return allItems(LessFieldExpenseSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(
        page, many=True, context={"request": request})
    for data in serializer.data:
        data = getAttachments(
            request, data, data['id'], "expense_attachments_v")
    data = self.get_paginated_response(serializer.data).data
    data['actualCount'] = actualCount
    data['estimateCount'] = estimateCount
    return Response(data)


def dataWithPermissions(self, field):
    object = self.get_object()
    serializer = self.get_serializer(object)
    data = serializer.data
    if field == 'users':
        role = Role.objects.filter(users=object)
        data['roles'] = RoleListSerializer(role, many=True).data
    permissions = Permission.objects.only('id').filter(**{field: object})
    actions = Action.objects.filter(
        permission_action__in=permissions).distinct()
    actionSerializer = ActionSerializer(actions, many=True)
    for action in actionSerializer.data:
        sub_action_ids = permissions.filter(
            action=action['id'])
        subActionSerializer = PermissionActionSerializer(
            sub_action_ids, many=True)
        action['actions'] = []
        for subAction in subActionSerializer.data:
            action['actions'].append(subAction['sub_action'])
    data['permissions'] = actionSerializer.data
    return Response(data, status=status.HTTP_200_OK)


def addAttachment(request, item):
    data = request.data
    attachment_obj = Attachment.objects.create(
        content_object=item,
        attachment=data['file'],
        name=data['file'],
        uploaded_by=request.user
    )
    attachment_obj.size = attachment_obj.fileSize()
    attachment_obj.save()
    serializer = AttachmentSerializer(
        attachment_obj, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def deleteAttachments(self, request):
    try:
        return delete(self, request, Attachment, 'attachment')
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


def teamsOfUser(self, request, queryset):
    user_id = request.GET.get("user_id")
    queryset = queryset.filter(users=user_id).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(TeamListSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)


def projectsOfUser(self, request, queryset):
    user_id = request.GET.get("user_id")
    queryset = queryset.filter(users=user_id).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(ProjectNameListSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)


def unAuthorized():
    return Response({
        "detail": "You do not have permission to perform this action."
    }, status=status.HTTP_403_FORBIDDEN)


def bussinessHours():
    workday = businesstimedelta.WorkDayRule(
        start_time=datetime.time(8),
        end_time=datetime.time(17),
        working_days=[0, 1, 2, 3, 4, 5])
    lunchbreak = businesstimedelta.LunchTimeRule(
        start_time=datetime.time(12),
        end_time=datetime.time(13),
        working_days=[0, 1, 2, 3, 4, 5])
    return businesstimedelta.Rules([workday, lunchbreak])


def taskTimingCalculator(obj, planHour, actualHour):
    if planHour < actualHour:
        obj['overdue'] = obj['overdue'] + 1
    elif planHour > actualHour:
        obj['earlier'] = obj['earlier'] + 1
    elif planHour == actualHour:
        obj['normal'] = obj['normal'] + 1
    return obj


def expenseItemsOfExpense(self, request, queryset):
    total = 0
    queryset = queryset.filter(expense=request.GET.get(
        "expense_id")).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(self.get_serializer, queryset)
    page = self.paginate_queryset(queryset)
    data = self.get_serializer(page, many=True, context={
                               "request": request}).data
    for item in data:
        item["total"] = int(item["quantity"]) * float(item["cost"])
        total += item["total"]

    data = self.get_paginated_response(data).data
    data['total_expense'] = total
    return Response(data)


def fetchYears():
    x1 = Income.objects.filter(
        deleted_at__isnull=True).order_by("created_at")[:1]
    y1 = Income.objects.filter(
        deleted_at__isnull=True).order_by("-updated_at")[:1]
    x2 = Expense.objects.filter(deleted_at__isnull=True).order_by("date")[:1]
    y2 = Expense.objects.filter(deleted_at__isnull=True).order_by("-date")[:1]

    x1 = x1[0].date.year
    x2 = x2[0].created_at.year
    x = x1 if x1 < x2 else x2

    y1 = y1[0].updated_at.year
    y2 = y2[0].date.year
    y = y1 if y1 > y2 else y2

    years = []
    while x <= y:
        years.append(x)
        x += 1

    if len(years) == 0:
        years.append(datetime.datetime.now().year)

    return Response(years)


def checkAndReturn(user, project, scope, method):
    if checkProjectScope(user, project, scope):
        return method
    else:
        return unAuthorized()
