from .models import Category
from common.actions import filterRecords, allItems


def totalExpenseAndIncome(expenses, incomes, year):
    data = [
        {
            "name": "JAN",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "FEB",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "MAR",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "APR",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "MAY",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "JUN",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "JUL",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "AUG",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "SEP",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "OCT",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "NOV",
            "income": 0,
            "expense": 0,
            "value": 0
        },
        {
            "name": "DEC",
            "income": 0,
            "expense": 0,
            "value": 0
        }
    ]
    count = 1
    for d in data:
        d['expense'] = totalExpenseByMonth(expenses, year, count)
        d['income'] = totalIncomeByMonth(incomes, year, count)
        d['value'] = d['income'] - d['expense']

        count += 1

    return data


def totalExpenseByMonth(items, year, month):
    items = items.filter(updated_at__year=year, updated_at__month=month)
    total = 0
    for item in items:
        total += float(item.quantity) * float(item.cost)
    return total


def totalIncomeByMonth(items, year, month):
    items = items.filter(updated_at__year=year, updated_at__month=month)
    total = 0
    for item in items:
        total += float(item.amount)
    return total


def categoryList(self, request, serializer_class):
    queryset = self.get_queryset()
    queryset = filterRecords(queryset, request, table=Category)
    if request.GET.get("items_per_page") == "-1":
        return allItems(serializer_class, queryset)

    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)
