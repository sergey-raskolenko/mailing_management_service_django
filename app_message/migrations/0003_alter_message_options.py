# Generated by Django 4.2.4 on 2023-10-10 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_message', '0002_message_created_by_alter_message_body_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['id'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
    ]