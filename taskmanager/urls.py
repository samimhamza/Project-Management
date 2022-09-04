from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,

)
from taskmanager.api.views import MyObtainTokenPairView, counterTables, fetchYearsAPI
from projects.api import views

urlpatterns = [
    # path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/", MyObtainTokenPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/token/verify/", TokenVerifyView.as_view()),
    path("api/counter/", counterTables),
    path("api/fetch-years/", fetchYearsAPI),
    path("admin/", admin.site.urls),
    path("api/", include("projects.api.urls")),
    path("api/", include("tasks.api.urls")),
    path("api/", include("users.api.urls")),
    path("api/", include("expenses.api.urls")),
    path("api/", include("clients.api.urls")),
    path("", views.indexPage),

] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
