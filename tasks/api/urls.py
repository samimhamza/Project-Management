from tasks.api.views import TaskViewSet, ProjectCommentViewSet, TaskCommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"project_comments",
                ProjectCommentViewSet, basename="project_comments")
router.register(r"task_comments", TaskCommentViewSet, basename="task_comments")
urlpatterns = router.urls
