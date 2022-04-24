from django.contrib import admin
from .models import Project, Income, Payment

admin.site.register(Project)
admin.site.register(Income)
admin.site.register(Payment)
