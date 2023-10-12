# отправка письма и логирование
from smtplib import SMTPException

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
