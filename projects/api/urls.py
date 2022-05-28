from projects.api.project.views import ProjectViewSet
from projects.api.views import (
    CountryViewSet,
    IncomeViewSet,
    PaymentViewSet,
    FocalPointViewSet,
    AttachmentViewSet,
    LocationViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"focal_points", FocalPointViewSet, basename="focal_points")
router.register(r"incomes", IncomeViewSet, basename="incomes")
router.register(r"locations", LocationViewSet, basename="locations")
router.register(r"attachments", AttachmentViewSet, basename="attachments")
urlpatterns = router.urls
