from django.urls import path
from projects.api.projects.views import ProjectViewSet

# from projects.api.views import (
#     ProjectListCreateAPIView,
#     ProjectRetrieveAPIView,
#     CountryListCreateAPIView,
#     CountryDetailAPIView,
#     LocationListCreateAPIView,
#     LocationDetailAPIView,
#     FocalPointListCreateAPIView,
#     FocalPointDetailAPIView,
#     IncomeListCreateAPIView,
#     IncomeDetailAPIView,
#     PaymentListCreateAPIView,
#     PaymentDetailAPIView,
#     ProjectTasksListAPIView,
#     AttachmentListCreateAPIView,
#     AttachmentDetailAPIView,
#     ProjectTaskLlistAPIView,
#     ProjectDescriptionUpdateAPIView,
# )


urlpatterns = [
    path("test/", ProjectViewSet.as_view(), name="projects"),
    # path("projects/", ProjectListCreateAPIView.as_view(), name="projects-list"),
    # path(
    #     "projects/<uuid:pk>", ProjectRetrieveAPIView.as_view(), name="projects-detail"
    # ),
    # path(
    #     "projects/<uuid:pk>/description",
    #     ProjectDescriptionUpdateAPIView.as_view(),
    #     name="projects-description",
    # ),
    # path(
    #     "projects/<uuid:pk>/tasks",
    #     ProjectTaskLlistAPIView.as_view(),
    #     name="projects-tasks",
    # ),
    # path("countries/", CountryListCreateAPIView.as_view(), name="countries-list"),
    # path(
    #     "countries/<uuid:pk>", CountryDetailAPIView.as_view(), name="countries-detail"
    # ),
    # path("locations/", LocationListCreateAPIView.as_view(), name="locations-list"),
    # path(
    #     "locations/<uuid:pk>", LocationDetailAPIView.as_view(), name="locations-detail"
    # ),
    # path(
    #     "focal-points/", FocalPointListCreateAPIView.as_view(), name="focal-point-list"
    # ),
    # path(
    #     "focal-points/<uuid:pk>",
    #     FocalPointDetailAPIView.as_view(),
    #     name="focal-point-detail",
    # ),
    # path("incomes/", IncomeListCreateAPIView.as_view(), name="income-list"),
    # path(
    #     "incomes/<uuid:pk>",
    #     IncomeDetailAPIView.as_view(),
    #     name="income-detail",
    # ),
    # path("payments/", PaymentListCreateAPIView.as_view(), name="payments-list"),
    # path(
    #     "payments/<uuid:pk>",
    #     PaymentDetailAPIView.as_view(),
    #     name="payments-detail",
    # ),
    # path(
    #     "attachments/", AttachmentListCreateAPIView.as_view(), name="attachments-list"
    # ),
    # path(
    #     "attachments/<uuid:pk>",
    #     AttachmentDetailAPIView.as_view(),
    #     name="attachments-detail",
    # ),
]
