from django.contrib import admin
from .models import Expense, ExpenseItem, Category

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(ExpenseItem)
