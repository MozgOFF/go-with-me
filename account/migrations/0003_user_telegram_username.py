# Generated by Django 3.0.4 on 2020-05-04 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200503_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=100, verbose_name='telegram_username'),
        ),
    ]
