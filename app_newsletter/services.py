# отправка письма и логирование
from smtplib import SMTPException
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.utils.timezone import now
from app_newsletter.models import NewsletterLog, Newsletter
from config import settings


def send_newsletter(newsletter: Newsletter):
	try:
		send_mail(
			newsletter.messages.subject,
			newsletter.messages.body,
			settings.EMAIL_HOST_USER,
			[i.email for i in newsletter.clients.all()],
		)
		newsletter.last_send = now()
		NewsletterLog.objects.create_log(newsletter, 'отправлена', now())
	except SMTPException as error:
		NewsletterLog.objects.create_log(newsletter, 'не отправлена', now(), error)


def manage_schedule(scheduler):
	newsletters = Newsletter.objects.all()
	if newsletters:
		for newsletter in newsletters:
			job_id = newsletter.id
			if check_task_for_send(newsletter):
				create_newsletters_schedules(scheduler, newsletter)
			else:
				# Рассылка все равно приходит, не получается ее удалить или поставить на паузу
				if scheduler.get_job(job_id):
					scheduler.pause_job(job_id)


def create_newsletters_schedules(scheduler, newsletter: Newsletter):
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
	if now() <= newsletter.mail_time_to and newsletter.is_active:
		return True
	else:
		return False

