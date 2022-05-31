from tasks.api.views import TaskViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"comments", CommentViewSet, basename="comments")
urlpatterns = router.urls
