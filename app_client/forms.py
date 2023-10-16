from django import forms

from .models import Client


class ClientCreateForm(forms.ModelForm):
	"""
	Форма создания нового клиента для рассылки сообщений
	"""

	class Meta:
		model = Client
		fields = ['email', 'name', 'surname', 'middle_name', 'comment']

	def __init__(self, *args, **kwargs):
		"""
		Инициализатор формы, применяет к полям CSS стили и добавляет плейсхолдеры
		"""
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

		self.fields['email'].widget.attrs['placeholder'] = 'Введите электронную почту клиента'
		self.fields['name'].widget.attrs['placeholder'] = 'Введите имя клиента'
		self.fields['surname'].widget.attrs['placeholder'] = 'Введите фамилию клиента'
		self.fields['middle_name'].widget.attrs['placeholder'] = 'Введите отчество клиента'
		self.fields['comment'].widget.attrs['placeholder'] = 'Комментарий'
