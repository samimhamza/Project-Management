from django.urls import path
from projects.api.views import ProjectListCreateAPIView, ProjectDetailAPIView


urlpatterns = [
    path("projects/", ProjectListCreateAPIView.as_view(), name="projects-list"),
    path("projects/<uuid:pk>", ProjectDetailAPIView.as_view(), name="projects-detail"),
]
