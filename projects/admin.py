from django.contrib import admin
from .models import (
    Project,
    Income,
    Payment,
    FocalPoint,
    Reason,
    Attachment,
    Country,
    Location
)

admin.site.register(Project)
admin.site.register(Income)
admin.site.register(Payment)
admin.site.register(Location)
admin.site.register(Country)
admin.site.register(Attachment)
admin.site.register(Reason)
admin.site.register(FocalPoint)
