# Generated by Django 3.0.4 on 2020-05-13 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_event_telegram_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='telegram_chat',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
