from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from projects.models import Project, Income
from tasks.models import Task
from users.models import User, Team
from clients.models import Client
from expenses.models import ExpenseItem
from common.actions import fetchYears



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

@api_view()
def counterTables(request):
    result = []
    if request.query_params.get('project_id'):  
        user_ids = Project.objects.filter(pk = request.GET['project_id']).values_list('users')
        team_ids = Project.objects.filter(pk = request.GET['project_id']).values_list('teams')
        incomes = Income.objects.filter(deleted_at__isnull=True, project = request.GET['project_id'])
        expense = ExpenseItem.objects.filter(deleted_at__isnull=True, expense__type="actual",expense__project=request.GET['project_id'])
        result.append(counter(Task.objects.filter(project = request.GET['project_id']),"Tasks","fi fi-rr-list-check"))
        expenseEstimate = ExpenseItem.objects.filter(deleted_at__isnull=True, expense__type="estimate",expense__project=request.GET['project_id'])
        result.append({"name":"Estimate","total": totalExpense(expenseEstimate), "icon": "fi fi-rr-money-bill-wave"})
        result.append(counter(Team.objects.filter(deleted_at__isnull=True,pk__in=team_ids),"Teams","fi fi-rr-users-alt"))
        result.append(counter(User.objects.filter(deleted_at__isnull=True,pk__in=user_ids),"Users","fi fi-rr-users"))
    else:
        result.append(counter(Project.objects.filter(deleted_at__isnull=True),"Projects","fi fi-rr-document"))
        result.append(counter(Team.objects.filter(deleted_at__isnull=True),"Teams","fi fi-rr-users-alt"))
        result.append(counter(User.objects.filter(deleted_at__isnull=True),"Users","fi fi-rr-users"))
        result.append(counter(Client.objects.filter(deleted_at__isnull=True),"Clients","fi fi-rr-portrait"))
        incomes = Income.objects.filter(deleted_at__isnull=True)
        expense = ExpenseItem.objects.filter(deleted_at__isnull=True,expense__type="actual")

    result.insert(1,{"name":"expenses","total": totalExpense(expense), "icon": "fi fi-rr-money-bill-wave"})
    result.insert(1,{"name":"incomes","total": totalIncome(incomes), "icon":"fi fi-rr-sack-dollar"})
    return Response(result)

@api_view()
def fetchYearsAPI(request):
    return fetchYears()

def counter(model, name, icon):
    result = {"name": name, "total":model.count(), "icon":icon}
    return result

def totalIncome(incomes):
    total = 0
    for income in incomes:
        total += income.amount
    return total

def totalExpense(expenses):
    total = 0
    for expense in expenses:
        total += expense.quantity * expense.cost
    return total
    