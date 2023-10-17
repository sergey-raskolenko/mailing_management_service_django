from django.db import models
from django.utils.timezone import now

from app_client.models import Client
from app_message.models import Message
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Newsletter(models.Model):
	"""
	Модель для описания рассылки
	"""
	PERIODICITY_CHOICES = [
		('D', 'Раз в день'),
		('W', 'Раз в неделю'),
		('M', 'Раз в месяц')
	]
	mail_time_from = models.DateTimeField(verbose_name='рассылка с ', default=now)
	mail_time_to = models.DateTimeField(verbose_name='рассылка по', default=now)
	periodicity = models.CharField(max_length=20, verbose_name='периодичность', choices=PERIODICITY_CHOICES)
	clients = models.ManyToManyField(Client, verbose_name='клиенты')
	messages = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
	status = models.CharField(max_length=50, verbose_name='статус отправки')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создана', **NULLABLE)

	is_active = models.BooleanField(default=True, verbose_name='активность')

	class Meta:
		db_table = 'newsletters'
		verbose_name = 'Рассылка'
		verbose_name_plural = 'Рассылки'

	def __str__(self):
		return f"Рассылка #{self.pk}"


class LogManager(models.Manager):
	"""
	Модель менеджера для создания объекта с определенными атрибутами
	"""
	def create_log(self, newsletter, status, last_try=now(), server_answer=None):
		log = self.create(newsletter=newsletter, status=status, last_try=last_try, server_answer=server_answer)
		return log


class NewsletterLog(models.Model):
	"""
	Модель для описания лога рассылки
	"""
	newsletter = models.ForeignKey(Newsletter, verbose_name='рассылка', on_delete=models.CASCADE)
	status = models.CharField(max_length=50, verbose_name='статус попытки')
	last_try = models.DateTimeField(verbose_name='последняя отправка')
	server_answer = models.CharField(max_length=50, verbose_name='ответ сервера', blank=True, null=True)

	objects = LogManager()

	class Meta:
		db_table = 'newsletter_logs'
		verbose_name = 'Лог отправки письма'
		verbose_name_plural = 'Логи отправок писем'

	def __str__(self):
		return f'Лог #{self.pk}'
