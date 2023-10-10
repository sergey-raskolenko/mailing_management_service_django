from django.urls import path
from app_message.apps import AppMessageConfig
from app_message.views import MessageCreateView, MessageUpdateView, MessageDeleteView, MessageListView, \
	MessageDetailView

app_name = AppMessageConfig.name

urlpatterns = [
	path('create/', MessageCreateView.as_view(), name='create_message'),
	path('update/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
	path('delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
	path('all/', MessageListView.as_view(), name='list_message'),
	path('<int:pk>/', MessageDetailView.as_view(), name='detail_message'),
]