from django.urls import path
from .views import ClientCreateView, ClientUpdateView, ClientDeleteView, ClientListView, \
	ClientDetailView

from app_client.apps import AppClientConfig

app_name = AppClientConfig.name

urlpatterns = [
	path('create/', ClientCreateView.as_view(), name='create_client'),
	path('update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
	path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
	path('all/', ClientListView.as_view(), name='list_client'),
	path('<int:pk>/', ClientDetailView.as_view(), name='detail_client'),
]
