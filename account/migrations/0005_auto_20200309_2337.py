# Generated by Django 3.0.3 on 2020-03-09 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200309_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Verified'),
        ),
    ]
