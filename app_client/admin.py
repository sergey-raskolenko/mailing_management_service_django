from django.contrib import admin

from app_client.models import Client


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	fields = ['pk', 'email', 'name', 'surname', 'middle_name', 'comment']
	ordering = ('pk',)
