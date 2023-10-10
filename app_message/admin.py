from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	fields = ['pk', 'subject', 'body']
	ordering = ('pk',)
