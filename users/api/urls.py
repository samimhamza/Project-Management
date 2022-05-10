from django.urls import path
from users.api.views import (
    TeamListCreateAPIView,
    TeamDetailAPIView,
    UserListCreateAPIView,
    UserDetailAPIView,
    TeamUserListCreateAPIView,
    TeamUserDetailAPIView,
    UserNoteListCreateAPIView,
    UserNoteDetailAPIView,
    ReminderListCreateAPIView,
    ReminderDetailAPIView,
    HolidayListCreateAPIView,
    HolidayDetailAPIView,
    NotificationListCreateAPIView,
    NotificationDetailAPIView,
)

urlpatterns = [
    path("teams/", TeamListCreateAPIView.as_view(), name="teams-list"),
    path("teams/<uuid:pk>", TeamDetailAPIView.as_view(), name="teams-detail"),
    path("users/", UserListCreateAPIView.as_view(), name="users-list"),
    path("users/<uuid:pk>", UserDetailAPIView.as_view(), name="users-detail"),
    path("team-users/", TeamUserListCreateAPIView.as_view(), name="team-users-list"),
    path(
        "team-users/<int:pk>", TeamUserDetailAPIView.as_view(), name="team-users-detail"
    ),
    path("user-notes/", UserNoteListCreateAPIView.as_view(), name="user-notes-list"),
    path(
        "user-notes/<int:pk>", UserNoteDetailAPIView.as_view(), name="user-notes-detail"
    ),
    path("reminders/", ReminderListCreateAPIView.as_view(), name="reminders-list"),
    path(
        "reminders/<int:pk>", ReminderDetailAPIView.as_view(), name="reminders-detail"
    ),
    path("holidays/", HolidayListCreateAPIView.as_view(), name="holidays-list"),
    path("holidays/<int:pk>", HolidayDetailAPIView.as_view(), name="holidays-detail"),
    path(
        "notifications/",
        NotificationListCreateAPIView.as_view(),
        name="notifications-list",
    ),
    path(
        "notifications/<int:pk>",
        NotificationDetailAPIView.as_view(),
        name="notifications-detail",
    ),
]
