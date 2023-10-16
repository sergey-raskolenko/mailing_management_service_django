from django.db import models

from users.models import NULLABLE, User


class Client(models.Model):
	"""
	Модель для описания клиента
	"""
	email = models.EmailField(max_length=50, verbose_name='email')
	name = models.CharField(max_length=50, verbose_name='имя', **NULLABLE)
	surname = models.CharField(max_length=50, verbose_name='фамилия', **NULLABLE)
	middle_name = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)
	comment = models.TextField(verbose_name='комментарий', **NULLABLE)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создан', related_name='clients')

	class Meta:
		verbose_name = 'Клиент'
		verbose_name_plural = 'Клиенты'
		db_table = 'clients'
		ordering = ['id']

	def __str__(self):
		return self.email
