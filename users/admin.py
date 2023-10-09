from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ['email', 'first_name', 'last_name', 'avatar', 'is_active', 'is_staff']
	ordering = ('email',)
