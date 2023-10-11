from datetime import datetime
from django import forms
from .models import Newsletter


class NewsletterCreateForm(forms.ModelForm):

	class Meta:
		model = Newsletter
		fields = ['periodicity', 'mail_time_from', 'mail_time_to', 'clients', 'messages']
		widgets = {
			'periodicity': forms.Select(attrs={'class': 'form-control'}),
			'mail_time_from': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class': 'datetimefield'}),
			'mail_time_to': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class': 'datetimefield'}),
			'clients': forms.SelectMultiple(attrs={'class': 'form-control multiselect'}),
			'messages': forms.Select(attrs={'class': 'form-control'})
		}
