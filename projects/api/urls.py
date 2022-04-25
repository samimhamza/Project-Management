from django.urls import path
from projects.api.views import (
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
    CountryListCreateAPIView,
    CountryDetailAPIView,
)


urlpatterns = [
    path("projects/", ProjectListCreateAPIView.as_view(), name="projects-list"),
    path("projects/<uuid:pk>", ProjectDetailAPIView.as_view(), name="projects-detail"),
    path("countries/", CountryListCreateAPIView.as_view(), name="countries-list"),
    path(
        "countries/<uuid:pk>", CountryDetailAPIView.as_view(), name="countries-detail"
    ),
]
