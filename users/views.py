import secrets

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, ListView

from config import settings
from users.forms import UserForm, UserRegisterForm, UserLoginForm
from users.models import User


class LoginView(BaseLoginView):
	form_class = UserLoginForm
	template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
	pass


class RegisterView(CreateView):
	model = User
	form_class = UserRegisterForm
	success_url = reverse_lazy('users:login')
	template_name = 'users/register.html'

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		token = secrets.token_urlsafe(nbytes=8)

		user.token = token
		activate_url = reverse_lazy('users:email_verified', kwargs={'token': user.token})
		send_mail(
			subject='Подтверждение почты',
			message=f'Для подтверждения регистрации перейдите по ссылке: '
					f'http://localhost:8000/{activate_url}',
			from_email=settings.EMAIL_HOST_USER,
			recipient_list=[user.email],
			fail_silently=False
		)
		user.save()

		return redirect('users:to_verify')


class EmailConfirmationSentView(TemplateView):
	template_name = 'users/user_verification.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class UserConfirmEmailView(View):
	def get(self, request, token):
		user = User.objects.get(token=token)

		user.is_active = True
		user.token = None
		user.save()
		return redirect('users:login')


class UserUpdateView(UpdateView):
	model = User
	form_class = UserForm
	success_url = reverse_lazy('users:profile')

	def get_object(self, queryset=None):
		return self.request.user


class UserListView(ListView):
	model = User

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Список пользователей'
		return context_data


class UserDeleteView(DeleteView):
	model = User
	success_url = reverse_lazy('users:list_user')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление пользователя'
		return context_data


def generate_password(request):

	new_password = secrets.token_hex(nbytes=8)
	request.user.set_password(new_password)
	request.user.save()

	send_mail(
		subject='New Password',
		message=f'You registered a new password on our website: {new_password}',
		from_email=settings.EMAIL_HOST_USER,
		recipient_list=[request.user.email]
	)

	return redirect(reverse('main:index'))


def toggle_staff(*args, **kwargs):
	print(kwargs.get('pk'))
	user = get_object_or_404(User, pk=kwargs.get('pk'))
	if user.is_staff:
		user.is_staff = False
	else:
		user.is_staff = True

	user.save()

	return redirect(reverse_lazy('users:list_user'))
