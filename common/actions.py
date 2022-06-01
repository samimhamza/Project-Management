import datetime
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from users.models import Team
from .team_actions import get_leader_by_id, get_total_users
from projects.models import Project
from expenses.models import Expense
from expenses.api.serializers import LessFieldExpenseSerializer


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


def delete(self, request, table):
    data = request.data
    if data:
        items = table.objects.filter(pk__in=data["ids"])
        for item in items:
            if getattr(table, 'deleted_at', False):
                if item.deleted_at:
                    item.delete()
                else:
                    item.deleted_at = datetime.datetime.now()
                    item.save()
            else:
                item.delete()

    else:
        item = self.get_object()
        if getattr(table, 'deleted_at', False):
            if item.deleted_at:
                item.delete()
            else:
                item.deleted_at = datetime.datetime.now()
                item.save()
        else:
            item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


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
    return self.get_paginated_response(serializer.data)
