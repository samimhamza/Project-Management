from django.contrib import admin
from .models import User, Team, Reminder, TeamUser, Holiday, Role, Permission


admin.site.register(User)
admin.site.register(Team)
admin.site.register(Reminder)
admin.site.register(TeamUser)
admin.site.register(Holiday)
admin.site.register(Role)
