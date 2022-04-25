from django.urls import path
from projects.api.views import ProjectListCreateAPIView


urlpatterns = [
    path("projects/", ProjectListCreateAPIView.as_view(), name="projects-list")
]
