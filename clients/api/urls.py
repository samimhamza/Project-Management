from clients.api.views import (ClientServiceViewSet, ClientProductViewSet, ServiceViewSet,
                               ProductViewSet, PricePlanViewSet, FeatureViewSet, RequirementViewSet)
from clients.api.clients.views import ClientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"client_services", ClientServiceViewSet,
                basename="client_services")
router.register(r"client_products", ClientProductViewSet,
                basename="client_products")
router.register(r"services", ServiceViewSet, basename="services")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"price_plans", PricePlanViewSet, basename="price_plans")
router.register(r"features", FeatureViewSet, basename="features")
router.register(r"requirements", RequirementViewSet, basename="requirements")
urlpatterns = router.urls
