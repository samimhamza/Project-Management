from rest_framework.routers import DefaultRouter
from users.api.teams.views import TeamViewSet
from users.api.views import (
    UserViewSet,
    HolidayViewSet,
    NotificationViewSet,
    ReminderViewSet,
)


router = DefaultRouter()
router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"users", UserViewSet, basename="users")
router.register(r"holidays", HolidayViewSet, basename="holidays")
router.register(r"reminders", ReminderViewSet, basename="reminders")
router.register(r"notifications", NotificationViewSet,
                basename="notifications")
urlpatterns = router.urls
