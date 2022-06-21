from django.urls import path, include, re_path
from projects.api.project.views import ProjectViewSet
from projects.api.views import (
    IncomeViewSet,
    PaymentViewSet,
    FocalPointViewSet,
    LocationCreateAPIView,
    CountryListAPIView,
    StateListAPIView,
    StageViewSet,
    ProjectCategoryViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"focal_points", FocalPointViewSet, basename="focal_points")
router.register(r"incomes", IncomeViewSet, basename="incomes")
router.register(r"stages", StageViewSet, basename="stages")
router.register(r"project_categories", ProjectCategoryViewSet,
                basename="project_categories")

urlpatterns = [
    path('locations/', LocationCreateAPIView.as_view(), name='locations'),
    path('countries/', CountryListAPIView.as_view(), name='countries'),
    path('states/', StateListAPIView.as_view(), name='states'),
    re_path(r'', include((router.urls))),
]
