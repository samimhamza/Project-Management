
from expenses.api.views import ExpenseViewSet, CategoryViewSet, ExpenseItemViewSet
from .my_project_expenses.views import MyCategoryViewSet, MyExpenseViewSet, MyExpenseItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"my_categories", MyCategoryViewSet, basename="my_categories")
router.register(r"expenses", ExpenseViewSet, basename="expenses")
router.register(r"my_expenses", MyExpenseViewSet, basename="my_expenses")
router.register(r"expense_items", ExpenseItemViewSet, basename="expense_items")
router.register(r"my_expense_items", MyExpenseItemViewSet,
                basename="my_expense_items")
urlpatterns = router.urls
