from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from users.api.teams.views import TeamViewSet
from users.api.views import (
    UserViewSet,
    HolidayViewSet,
    NotificationViewSet,
    ReminderViewSet,
    PermmissionListAPIView,
    RoleViewSet
)


router = DefaultRouter()
router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"users", UserViewSet, basename="users")
router.register(r"holidays", HolidayViewSet, basename="holidays")
router.register(r"reminders", ReminderViewSet, basename="reminders")
router.register(r"roles", RoleViewSet, basename="roles")
router.register(r"notifications", NotificationViewSet,
                basename="notifications")

# urlpatterns = router.urls
urlpatterns = [
    path('permissions/', PermmissionListAPIView.as_view(), name='permissions'),
    re_path(r'', include((router.urls))),
]
