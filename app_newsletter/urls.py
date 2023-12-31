from django.urls import path

from app_newsletter.apps import AppNewsletterConfig
from app_newsletter.views import NewsletterListView, NewsletterCreateView, NewsletterUpdateView, NewsletterDeleteView, \
    NewsletterDetailView, NewsletterLogListView, toggle_is_active

app_name = AppNewsletterConfig.name

urlpatterns = [
    path('all/', NewsletterListView.as_view(), name='list_newsletter'),
    path('create/', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('update/<int:pk>/', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('delete/<int:pk>/', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('<int:pk>/', NewsletterDetailView.as_view(), name='detail_newsletter'),
    path('<int:pk>/newsletterlogs/', NewsletterLogListView.as_view(), name='list_newsletterlogs'),
    path('is_active/<int:pk>/', toggle_is_active, name='toggle_is_active'),
]
