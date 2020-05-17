# Generated by Django 3.0.4 on 2020-05-04 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200504_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='latitude',
            field=models.DecimalField(decimal_places=14, max_digits=17, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='user',
            name='longitude',
            field=models.DecimalField(decimal_places=14, max_digits=17, null=True, verbose_name='Longitude'),
        ),
    ]
