import datetime
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


def withTrashed(self, table, *args, **kwargs):
    if kwargs.get("order_by") is not None:
        queryset = table.objects.all().order_by(kwargs.get("order_by"))
    else:
        queryset = table.objects.all()
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return serializer


def trashList(self, table, *args, **kwargs):
    queryset = self.filter_queryset(
        table.objects.filter(deleted_at__isnull=False).order_by("-deleted_at")
    )
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)


def delete(self, request, table):
    data = request.data
    if data:
        teams = table.objects.filter(pk__in=data["ids"])
        for team in teams:
            if team.deleted_at:
                team.delete()
            else:
                team.deleted_at = datetime.datetime.now()
                team.save()
    else:
        team = self.get_object()
        if team.deleted_at:
            team.delete()
        else:
            team.deleted_at = datetime.datetime.now()
            team.save()
    return Response(
        {"message": "successfully deleted"}, status=status.HTTP_204_NO_CONTENT
    )


def restore(self, request, table):
    try:
        with transaction.atomic():
            data = request.data
            teams = table.objects.filter(pk__in=data["ids"])
            for team in teams:
                team.deleted_at = None
                team.save()
            page = self.paginate_queryset(teams)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    except:
        return Response(
            {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )
