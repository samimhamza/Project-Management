from django.urls import path
from projects.api.views import (
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
    CountryListCreateAPIView,
    CountryDetailAPIView,
    LocationListCreateAPIView,
    LocationDetailAPIView,
    FocalPointListCreateAPIView,
    FocalPointDetailAPIView,
)


urlpatterns = [
    path("projects/", ProjectListCreateAPIView.as_view(), name="projects-list"),
    path("projects/<uuid:pk>", ProjectDetailAPIView.as_view(), name="projects-detail"),
    path("countries/", CountryListCreateAPIView.as_view(), name="countries-list"),
    path(
        "countries/<uuid:pk>", CountryDetailAPIView.as_view(), name="countries-detail"
    ),
    path("locations/", LocationListCreateAPIView.as_view(), name="locations-list"),
    path(
        "locations/<uuid:pk>", LocationDetailAPIView.as_view(), name="locations-detail"
    ),
    path(
        "focal-point/", FocalPointListCreateAPIView.as_view(), name="focal-point-list"
    ),
    path(
        "focal-point/<uuid:pk>",
        FocalPointDetailAPIView.as_view(),
        name="focal-point-detail",
    ),
]
