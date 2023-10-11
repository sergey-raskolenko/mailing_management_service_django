from django.urls import path

from app_blog.apps import AppBlogConfig
from app_blog.views import BlogListView, BlogDetailView

app_name = AppBlogConfig.name

urlpatterns = [
    path('all/', BlogListView.as_view(), name='list_blog'),
    path('<int:pk>/', BlogDetailView.as_view(), name='detail_blog'),
]