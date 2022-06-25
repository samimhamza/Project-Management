from django.contrib import admin
from .models import Client, ClientProduct, ClientService, Service, Product, PricePlan, Feature, Requirement

admin.site.register(Client)
admin.site.register(ClientProduct)
admin.site.register(ClientService)
admin.site.register(Service)
admin.site.register(Product)
admin.site.register(PricePlan)
admin.site.register(Feature)
admin.site.register(Requirement)
