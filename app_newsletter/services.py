# отправка письма и логирование
from smtplib import SMTPException
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.utils.timezone import now
from app_newsletter.models import NewsletterLog, Newsletter
from config import settings


def send_newsletter(newsletter: Newsletter):
	"""
	Функция для отправки сообщения из рассылки всем клиентам из рассылки с созданием логов действий
	"""
	try:
		send_mail(
			newsletter.messages.subject,
			newsletter.messages.body,
			settings.EMAIL_HOST_USER,
			[i.email for i in newsletter.clients.all()],
		)
		newsletter.last_send = now()
		newsletter.status = 'запущена'
		newsletter.save()
		NewsletterLog.objects.create_log(newsletter, newsletter.status, now(), '200')
	except SMTPException as error:
		NewsletterLog.objects.create_log(newsletter, 'ошибка', now(), error.args[0])


def manage_schedule(scheduler):
	"""
	Функция для добавления рассылки в очередь задач, если она не завершена.
	Постановка рассылки на паузу в очереди задач, если она не активна
	"""
	newsletters = Newsletter.objects.all()
	if newsletters:
		for newsletter in newsletters:
			if not newsletter.status == 'завершена':
				job_id = newsletter.id
				if check_task_for_send(newsletter):
					create_newsletter_task(scheduler, newsletter)
				else:
					# Рассылка все равно приходит, не получается ее удалить или поставить на паузу
					if scheduler.get_job(job_id):
						scheduler.pause_job(job_id)
						newsletter.status = 'приостановлена'
						newsletter.save()
						NewsletterLog.objects.create_log(newsletter, newsletter.status, now(), '')


def create_newsletter_task(scheduler, newsletter: Newsletter):
	"""
	Создание задачи для рассылки исходя из ее периодичности
	"""
	if newsletter.periodicity == 'D':
		scheduler.add_job(
			send_newsletter,
			trigger=CronTrigger(second="*/10"),
			# trigger=CronTrigger(day="*/1"),
			id=str(newsletter.id),
			max_instances=1,
			replace_existing=True,
			args=(newsletter,)
		)
	elif newsletter.periodicity == 'W':
		scheduler.add_job(
			send_newsletter,
			trigger=CronTrigger(second="*/12"),
			# trigger=CronTrigger(week="*/1"),
			id=str(newsletter.id),
			max_instances=1,
			replace_existing=True,
			args=(newsletter,)
		)
	elif newsletter.periodicity == 'M':
		scheduler.add_job(
			send_newsletter,
			trigger=CronTrigger(second="*/15"),
			# trigger=CronTrigger(mont="*/1"),
			id=str(newsletter.id),
			max_instances=1,
			replace_existing=True,
			args=(newsletter,)
		)


def check_task_for_send(newsletter: Newsletter) -> bool:
	"""
	Проверка активности рассылки, и верности времени ее начала
	"""
	if newsletter.is_active:
		if newsletter.mail_time_from <= now():
			if now() <= newsletter.mail_time_to:
				return True
			else:
				newsletter.status = 'завершена'
				newsletter.save()
				NewsletterLog.objects.create_log(newsletter, newsletter.status, now(), '')
				return False
		else:
			return False
	else:
		return False
