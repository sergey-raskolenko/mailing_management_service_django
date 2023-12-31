from django.db import models

from users.models import User


class Message(models.Model):
	"""
	Модель для описания сообщения
	"""
	subject = models.CharField(max_length=50, verbose_name='тема сообщения')
	body = models.CharField(max_length=250, verbose_name='тело сообщения')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создан', related_name='messages')

	class Meta:
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'
		db_table = 'messages'
		ordering = ['id']

	def __str__(self):
		return self.subject
