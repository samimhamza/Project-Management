
from expenses.api.views import ExpenseViewSet, CategoryViewSet, ExpenseItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"expenses", ExpenseViewSet, basename="expenses")
router.register(r"expense_items", ExpenseItemViewSet, basename="expense_items")
urlpatterns = router.urls
