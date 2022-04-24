from django.contrib import admin
from .models import Task
from .models import UserTask

admin.site.register(Task)
admin.site.register(UserTask)
