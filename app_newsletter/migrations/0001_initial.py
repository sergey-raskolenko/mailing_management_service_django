# Generated by Django 4.2.4 on 2023-10-12 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_client', '0002_alter_client_options_alter_client_table'),
        ('app_message', '0004_alter_message_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_time_from', models.DateTimeField(default=django.utils.timezone.now, verbose_name='рассылка с ')),
                ('mail_time_to', models.DateTimeField(default=django.utils.timezone.now, verbose_name='рассылка по')),
                ('periodicity', models.CharField(choices=[('D', 'Раз в день'), ('W', 'Раз в неделю'), ('M', 'Раз в месяц')], max_length=20, verbose_name='периодичность')),
                ('status', models.CharField(max_length=50, verbose_name='статус отправки')),
                ('clients', models.ManyToManyField(to='app_client.client', verbose_name='клиенты')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создана')),
                ('messages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_message.message', verbose_name='сообщение')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'db_table': 'newsletters',
            },
        ),
        migrations.CreateModel(
            name='NewsletterLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, verbose_name='статус попытки')),
                ('last_try', models.DateTimeField(verbose_name='последняя отправка')),
                ('server_answer', models.SmallIntegerField(blank=True, null=True, verbose_name='ответ сервера')),
                ('newsletter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_newsletter.newsletter', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Лог отправки письма',
                'verbose_name_plural': 'Логи отправок писем',
                'db_table': 'newsletter_logs',
            },
        ),
    ]
