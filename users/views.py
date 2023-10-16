import secrets
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
	"""
	Представление для формы входа и обработки действия входа
	"""
	form_class = UserLoginForm
	template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
	"""
	Представление для выхода пользователем из системы
	"""
	pass


class RegisterView(UserPassesTestMixin, CreateView):
	"""
	Представление для создания нового пользователя (кроме стаффа)
	При создании отправляется верификационное письмо на почту, для подтверждения регистрации
	"""
	model = User
	form_class = UserRegisterForm
	success_url = reverse_lazy('users:login')
	template_name = 'users/register.html'

	def test_func(self):
		if self.request.user.is_staff and not self.request.user.is_superuser:
			return False
		return True

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
	"""
	Представление для отображения страницы с информацией о верификации
	"""
	template_name = 'users/user_verification.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class UserConfirmEmailView(View):
	"""
	Представление для верификации пользователя по токену, полученному при переходе по ссылке из верификационного письма
	"""
	def get(self, request, token):
		user = User.objects.get(token=token)

		user.is_active = True
		user.token = None
		user.save()
		return redirect('users:login')


class UserUpdateView(LoginRequiredMixin, UpdateView):
	"""
	Представление для обновления пользователя
	"""
	model = User
	form_class = UserForm
	success_url = reverse_lazy('users:profile')

	def get_object(self, queryset=None):
		return self.request.user


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
	"""
	Представление для отображения списка пользователей авторизованному пользователю с правами стаффа
	"""
	model = User

	def test_func(self):
		return self.request.user.is_staff

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Список пользователей'
		context_data['object_list'] = User.objects.all()
		return context_data


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	"""
	Представление для удаления клиента авторизованному пользователю с правами стаффа
	"""
	model = User
	success_url = reverse_lazy('users:list_user')

	def test_func(self):
		return self.request.user.is_staff

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление пользователя'
		return context_data


def generate_password(request):
	"""
	Контроллер для генерации нового пароля пользователю, с отправкой пароля на почту
	"""

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


@user_passes_test(lambda u: u.is_superuser)
def toggle_staff(*args, **kwargs):
	"""
	Контроллер для редактирования прав стаффа пользователем, являющимся суперпользователем
	"""
	user = get_object_or_404(User, pk=kwargs.get('pk'))
	if user.is_staff:
		user.is_staff = False
	else:
		user.is_active = True
		user.is_staff = True

	user.save()

	return redirect(reverse_lazy('users:list_user'))


def toggle_activity(*args, **kwargs):
	"""
	Контроллер для редактирования активности пользователя
	"""
	user = get_object_or_404(User, pk=kwargs.get('pk'))
	if user.is_active:
		user.is_active = False
	else:
		user.is_active = True

	user.save()

	return redirect(reverse_lazy('users:list_user'))
