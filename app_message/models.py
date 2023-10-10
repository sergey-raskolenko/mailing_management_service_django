from django.db import models

from django.db import models


class Message(models.Model):
	subject = models.CharField(max_length=150, verbose_name='тема сообщения')
	body = models.CharField(max_length=150, verbose_name='тело сообщения')

	class Meta:
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'
		db_table = 'messages'

	def __str__(self):
		return self.subject

