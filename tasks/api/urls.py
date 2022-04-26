from django.urls import path
from tasks.api.views import (
    CommentListCreateAPIView,
    CommentDetailAPIView,
    TaskListCreateAPIView,
    TaskDetailAPIView,
    UserTaskDetailAPIView,
    UserTaskListCreateAPIView,
)

urlpatterns = [
    path("tasks/", TaskListCreateAPIView.as_view(), name="tasks-list"),
    path("tasks/<uuid:pk>", TaskDetailAPIView.as_view(), name="tasks-detail"),
    path("user-tasks/", UserTaskListCreateAPIView.as_view(), name="user-tasks-list"),
    path(
        "user-tasks/<uuid:pk>",
        UserTaskDetailAPIView.as_view(),
        name="user-tasks-detail",
    ),
    path("comments/", CommentListCreateAPIView.as_view(), name="comments-list"),
    path("comments/<uuid:pk>", CommentDetailAPIView.as_view(), name="tasks-detail"),
]
