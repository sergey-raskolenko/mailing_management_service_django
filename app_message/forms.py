from django import forms
from .models import Message


class MessageForm(forms.ModelForm):

	class Meta:
		model = Message
		fields = ['subject', 'body',]

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

		self.fields['subject'].widget.attrs['placeholder'] = 'Введите тему сообщения'
		self.fields['body'].widget.attrs['placeholder'] = 'Введите сообщение'
