from django.contrib import admin

from app_blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ['title', 'content', 'image', 'views', 'published_date']
	ordering = ['pk']
