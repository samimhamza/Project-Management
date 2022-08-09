from expenses.api.serializers import ExpenseItemReportSerializer
from projects.api.serializers import IncomeReportSerializer
   



def totalExpenseAndIncome(expenses,incomes,year):
    data = [
		{
			"name": "JAN",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "FAB",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "MAR",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "APR",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "MAY",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "JUN",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "JUL",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "AUG",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "SEP",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "OCT",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "NOV",
			"income": 0,
			"expense": 0,
            "value":0
		},
		{
			"name": "DEC",
			"income": 0,
			"expense": 0,
            "value":0
		}
	]

    count = 1
    for d in data:
        d['expense'] = totalExpenseByMonth(expenses,year,count)
        d['income'] = totalIncomeByMonth(incomes,year,count)
        d['value'] = d['income'] - d['expense']

        count += 1 

    return data


def totalExpenseByMonth(items,year,month):
    items = items.filter(updated_at__year=year,updated_at__month=month)
    serializer = ExpenseItemReportSerializer(items,many=True)
    datas = serializer.data
    total = 0
    for item in datas:
        total += float(item['quantity']) * float(item['cost'])
    return total

def totalIncomeByMonth(items,year,month):
    items = items.filter(updated_at__year=year,updated_at__month=month)
    serializer = IncomeReportSerializer(items,many=True)
    datas = serializer.data
    total = 0
    for item in datas:
        total += float(item['amount'])
    return total

