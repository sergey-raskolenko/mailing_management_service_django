from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from app_newsletter.services import manage_schedule


class Command(BaseCommand):
	help = "Runs APScheduler."

	def handle(self, *args, **options):
		scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
		scheduler.add_jobstore(DjangoJobStore(), "default")

		manage_schedule(scheduler)

		try:
			scheduler.start()
		except KeyboardInterrupt:
			scheduler.shutdown()
