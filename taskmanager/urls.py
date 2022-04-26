from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/token/verify/", TokenVerifyView.as_view()),
    path("admin/", admin.site.urls),
    path("api/", include("projects.api.urls")),
    path("api/", include("tasks.api.urls")),
    path("api/", include("users.api.urls")),
    path("api/", include("expenses.api.urls")),
]
