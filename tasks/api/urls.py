from tasks.api.views import TaskViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
urlpatterns = router.urls
