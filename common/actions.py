from users.api.serializers import PermissionActionSerializer, ActionSerializer, RoleListSerializer
from expenses.api.serializers import LessFieldExpenseSerializer
from projects.api.serializers import AttachmentSerializer
from .team_actions import get_leader_by_id, get_total_users
from users.models import Team, Permission, Action, Role
from common.permissions import checkCustomPermissions
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from projects.models import Project, Attachment
from expenses.models import Expense
from django.db.models import Q
from django.utils import timezone
import datetime
import os


def getAttachments(request, data, id, permission):
    # custom permission checking for attachments scopes
    attachments_permission = checkCustomPermissions(
        request, permission)
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


def filterRecords(queryset, request, columns=[]):
    data = request.query_params
    for key, value in data.lists():
        if len(value) == 1:
            value = value[0]
            if value.startswith('like@@'):
                likeValue = value[6:]
                queryset = queryset.filter(
                    **{'%s__icontains' % key: likeValue})
            elif value.startswith('exact@@'):
                exactValue = value[7:]
                queryset = queryset.filter(**{key: exactValue})
            elif "__" in key:
                queryset = queryset.filter(**{key: value})
        else:
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
    if table == Team:
        for team in serializer.data:
            team["total_users"] = get_total_users(team["id"])
            team["leader"] = get_leader_by_id(team["id"])
    return self.get_paginated_response(serializer.data)


def delete(self, request, table, imageField=None):
    data = request.data
    ids = []
    if data:
        items = table.objects.filter(pk__in=data["ids"])
        for item in items:
            ids.append(item.id)
            if getattr(item, 'deleted_at', False):
                if item.deleted_at:
                    item.delete()
                else:
                    item.deleted_at = datetime.datetime.now(tz=timezone.utc)
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
                item.save()
        else:
            if imageField:
                if os.path.isfile('media/'+str(getattr(table, imageField))):
                    os.remove('media/'+str(getattr(table, imageField)))
            item.delete()
    return Response({'deleted_ids': ids}, status=status.HTTP_204_NO_CONTENT)


def restore(self, request, table):
    try:
        with transaction.atomic():
            data = request.data
            items = table.objects.filter(pk__in=data["ids"])
            for item in items:
                item.deleted_at = None
                item.save()
            page = self.paginate_queryset(items)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


def allItems(serializerName, queryset):
    serializer = serializerName(queryset, many=True)
    return Response(serializer.data, status=200)


def expensesOfProject(self, request):
    queryset = Expense.objects.filter(
        deleted_at__isnull=True, project=request.GET.get("project_id")).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(LessFieldExpenseSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    for data in serializer.data:
        data = getAttachments(
            request, data, data['id'], "expense_attachments_v")
    return self.get_paginated_response(serializer.data)


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


def searchRecords(queryset, request, columns=[]):
    # search for different columns in one function
    if request.query_params.get('content'):
        queries = Q()
        for column in columns:
            queries = queries | Q(
                **{'%s__icontains' % column: request.query_params.get('content')})
        queryset = queryset.filter(queries)
    return queryset


def addAttachment(self, request):
    try:
        item = self.get_object()
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
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


def deleteAttachments(self, request):
    try:
        return delete(self, request, Attachment, 'attachment')
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )
