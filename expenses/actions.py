from common.actions import filterRecords, allItems, checkAndReturn, unAuthorized, getAttachments
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from projects.models import Project


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


def categoryActions(request, scope, method):
    if request.GET.get("project_id"):
        try:
            project = Project.objects.get(pk=request.GET.get("project_id"))
        except Project.DoesNotExist:
            return unAuthorized()
        return checkAndReturn(request.user, project, scope,
                              method)
    else:
        return unAuthorized()


def categoryList(self, request, serializer_class):
    queryset = self.get_queryset()
    queryset = filterRecords(queryset, request, table=Category)
    if request.GET.get("items_per_page") == "-1":
        return allItems(serializer_class, queryset)

    page = self.paginate_queryset(queryset)
    serializer = self.get_serializer(page, many=True)
    return self.get_paginated_response(serializer.data)


def categoryCreate(self, request):
    data = request.data
    creator = request.user
    category = Category.objects.create(
        name=data["name"],
        created_by=creator,
        updated_by=creator,
    )
    category.save()
    serializer = self.get_serializer(category)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def categoryUpdate(self, request):
    category = self.get_object()
    for key, value in request.data.items():
        setattr(category, key, value)
    category.updated_by = request.user
    category.save()
    serializer = self.get_serializer(category)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


def expenseRetrieve(self, request, expense):
    serializer = self.get_serializer(expense, context={"request": request})
    data = serializer.data
    data = getAttachments(request, data, expense.id,
                          "expense_attachments_v", expense.project)
    return Response(data)
