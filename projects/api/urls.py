from projects.api.income.views import PaymentViewSet, IncomeViewSet
from projects.api.my_projects.views import MyProjectViewSet
from projects.api.project.views import ProjectViewSet
from .stage.views import StageViewSet, SubStageViewSet
from rest_framework.routers import DefaultRouter
from .department.views import DepartmentViewSet
from django.urls import path, include, re_path
from projects.api.views import (
    FocalPointViewSet,
    LocationCreateAPIView,
    CountryListAPIView,
    StateListAPIView,
    MyLocationCreateAPIView
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"my_projects", MyProjectViewSet, basename="my_projects")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"focal_points", FocalPointViewSet, basename="focal_points")
router.register(r"incomes", IncomeViewSet, basename="incomes")
router.register(r"stages", StageViewSet, basename="stages")
router.register(r"sub_stages", SubStageViewSet, basename="sub_stages")
router.register(r"departments", DepartmentViewSet,
                basename="departments")

urlpatterns = [
    path('locations/', LocationCreateAPIView.as_view(), name='locations'),
    path('my_locations/', MyLocationCreateAPIView.as_view(), name='my_locations'),
    path('countries/', CountryListAPIView.as_view(), name='countries'),
    path('states/', StateListAPIView.as_view(), name='states'),
    re_path(r'', include((router.urls))),
]
