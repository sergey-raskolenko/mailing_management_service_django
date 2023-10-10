from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, EmailConfirmationSentView, \
	generate_password, UserConfirmEmailView

app_name = UsersConfig.name

urlpatterns = [
	path('', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('register/', RegisterView.as_view(), name='register'),
	path('profile/', UserUpdateView.as_view(), name='profile'),
	path('to_verify/', EmailConfirmationSentView.as_view(), name='to_verify'),
	path('confirm-email/<str:token>/', UserConfirmEmailView.as_view(), name='email_verified'),
	path('profile/generate_password', generate_password, name='generate_password'),
]
