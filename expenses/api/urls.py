from django.urls import path
from expenses.api.views import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    ExpenseDetailAPIView,
    ExpenseListCreateAPIView,
    ExpenseItemDetailAPIView,
    ExpenseItemListCreateAPIView,
)

urlpatterns = [
    path("categories/", CategoryListCreateAPIView.as_view(), name="categories-list"),
    path(
        "categories/<uuid:pk>",
        CategoryDetailAPIView.as_view(),
        name="categories-detail",
    ),
    path("expenses/", ExpenseListCreateAPIView.as_view(), name="expenses-list"),
    path(
        "expenses/<uuid:pk>",
        ExpenseDetailAPIView.as_view(),
        name="expenses-detail",
    ),
    path(
        "expense-items/",
        ExpenseItemListCreateAPIView.as_view(),
        name="expense-items-list",
    ),
    path(
        "expense-items/<uuid:pk>",
        ExpenseItemDetailAPIView.as_view(),
        name="expense-items-detail",
    ),
]
