import datetime
from rest_framework.response import Response
from rest_framework import status


def all(self, table, *args, **kwargs):
    if order_by is not None:
        queryset = table.objects.all().order_by(order_by)
    else:
        queryset = table.objects.all()
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return serializer


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
