from users.api.forgot_password.views import ForgotPasswordCreateAPIView, ForgotPasswordRetrieveAPIView, ChangePasswordAPIView
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from users.api.teams.views import TeamViewSet
from users.api.views import (
    HolidayViewSet,
    NotificationViewSet,
    ReminderViewSet,
    PermmissionListAPIView,
    RoleViewSet
)
from users.api.users.views import UserViewSet
from users import views
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
    path('forgot_password/', ForgotPasswordCreateAPIView.as_view(),
         name='forgot_password'),
    path('forgot_password/<uuid:pk>/', ForgotPasswordRetrieveAPIView.as_view(),
         name='forgot_password'),
    path('change_password/', ChangePasswordAPIView.as_view(),
         name='change_password'),
    # path('html/', views.index, name='html'),
    re_path(r'', include((router.urls))),
]
