from tasks.models import Comment
from tasks.api.serializers import CommentSerializer
from .actions import allItems


def commentsOfProject(self, request):
    project_id = request.GET.get("project_id")
    queryset = Comment.objects.filter(
        object_id=project_id).order_by("-created_at")
    if request.GET.get("items_per_page") == "-1":
        return allItems(CommentSerializer, queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)
