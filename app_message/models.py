from django.db import models

from django.db import models

from users.models import User, NULLABLE


class Message(models.Model):
	subject = models.CharField(max_length=50, verbose_name='тема сообщения')
	body = models.CharField(max_length=250, verbose_name='тело сообщения')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создан', related_name='messages',
								   **NULLABLE)

	class Meta:
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'
		db_table = 'messages'

	def __str__(self):
		return self.subject

