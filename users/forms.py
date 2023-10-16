from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from users.models import User


class StyleFormMixin:
	"""
	Миксин-класс для применения к полям формы CSS стилей
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'


class UserLoginForm(StyleFormMixin, AuthenticationForm):
	"""
	Форма аутентификации пользователя
	"""
	pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
	"""
	Форма регистрации пользователя
	"""

	class Meta:
		model = User
		fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
	"""
	Форма для изменения пользователя
	"""

	class Meta:
		model = User
		fields = ('email', 'password', 'first_name', 'last_name', 'avatar',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].widget = forms.HiddenInput()
