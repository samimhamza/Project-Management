from tasks.models import Comment, Task
from tasks.api.serializers import CommentSerializer
from .actions import allItems
from projects.models import Project


def commentsOfProject(self, request):
    id = request.GET.get("id")
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
