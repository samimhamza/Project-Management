from tasks.models import Comment, Task
from tasks.api.serializers import CommentSerializer
from .actions import allItems, filterRecords
from projects.models import Project, Attachment
from rest_framework import status
from rest_framework.response import Response


def commentsOfTable(self, request, id):
    queryset = Comment.objects.filter(
        object_id=id).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(CommentSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)

def latestcommentsOfTable(self, request, id):
    queryset = Comment.objects.filter(
        object_id=id).order_by("-created_at")
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)


def checkCommnetable(request):
    if request.data.get("task_id"):
        return Task.objects.get(pk=request.data.get("task_id"))
    elif request.data.get("project_id"):
        return Project.objects.get(pk=request.data.get("project_id"))
    return None


def listComments(self, request):
    queryset = self.get_queryset()
    queryset = filterRecords(queryset, request)
    if request.GET.get("id"):
        id = request.GET.get("id")
        if request.GET.get("latest"):
            return latestcommentsOfTable(self, request, id)
        return commentsOfTable(self, request, id)
    return Response([])


def createComments(self, request):
    data = request.data
    commentable = checkCommnetable(request)
    if commentable:
        comment = Comment.objects.create(
            body=data['body'],
            commented_by=request.user,
            content_object=commentable
        )
        if request.data.get("attachments"):
            for attachment in data['attachments']:
                Attachment.objects.create(
                    content_object=comment,
                    attachment=attachment['file'],
                    name=attachment['file'])
        serializer = CommentSerializer(
            comment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Object id is not correct'}, status=status.HTTP_400_BAD_REQUEST)


def updateComments(self, request, pk):
    comment = self.get_object()
    comment.body = request.data.get('body')
    comment.save()
    serializer = CommentSerializer(comment,  context={"request": request})
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
