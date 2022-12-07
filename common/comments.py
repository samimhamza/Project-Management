from .actions import allItems, filterRecords, convertBase64ToImage
from tasks.api.serializers import CommentSerializer
from common.permissions import checkProjectScope
from common.actions import unAuthorized, delete
from projects.models import Project, Attachment
from rest_framework.response import Response
from common.pusher import pusher_client
from tasks.models import Comment, Task
from rest_framework import status


def broadcastComment(item, data, update=False):
    try:
        instance = item.id
    except:
        instance = item
    pusher_client.trigger(
        u'projectComment.'+str(instance), u'comments', {
            "id": data['id'],
            "body": data['body'],
            "created_at": data['created_at'],
            "updated_at": data['updated_at'],
            "commented_by": data['commented_by'],
            "update": update,
        })


def broadcastDeleteComment(deleted_ids):
    pusher_client.trigger(
        u'deleteComments', u'comments', deleted_ids)


def commentsOfTable(self, request, id):
    queryset = Comment.objects.filter(
        object_id=id).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(CommentSerializer, queryset)
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
        if "attachment" in request.data:
            imageField = convertBase64ToImage(data["attachment"])
            Attachment.objects.create(
                content_object=comment,
                attachment=imageField
            )
        serializer = CommentSerializer(
            comment, context={"request": request})
        # broadcastComment(commentable, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Object id is not correct'}, status=status.HTTP_400_BAD_REQUEST)


def updateComments(self, request, pk):
    comment = self.get_object()
    comment.body = request.data.get('body')
    comment.save()
    serializer = CommentSerializer(comment,  context={"request": request})
    # broadcastComment(comment.object_id, serializer.data, update=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


def comments(self, method, request, permission, type="project"):
    id = request.GET.get("id")
    if type == "project":
        if checkProjectScope(request.user, None, permission, id):
            return method(self, request)
        return unAuthorized()
    elif type == "task":
        task = Task.objects.get(pk=id)
        if checkProjectScope(request.user, task.project, permission):
            return method(self, request)
        return unAuthorized()
    return unAuthorized()


def destroy(self, request):
    response = delete(self, request, Comment)
    # broadcastDeleteComment(response.data)
    return response
