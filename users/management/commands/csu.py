from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Консольная команда для создания суперпользователя
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.admin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('admin')
        user.save()
