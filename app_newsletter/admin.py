from django.contrib import admin

from .models import Newsletter, NewsletterLog


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
	list_display = ['mail_time_from', 'mail_time_to', 'periodicity', 'status', 'created_by', 'is_active']
	ordering = ['pk']


@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
	list_display = ['last_try', 'status', 'server_answer']
