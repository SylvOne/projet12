from django.contrib import admin
from .models import Client, Contract, Event


class ContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'commercial_contact', 'total_amount', 'amount_due', 'creation_date', 'status']


# Register your models here.
admin.site.register(Client)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event)
