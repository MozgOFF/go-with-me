# Generated by Django 3.0.4 on 2020-05-18 17:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0002_auto_20200503_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='favorite_of',
            field=models.ManyToManyField(blank=True, related_name='favorite_category', related_query_name='favorite_category', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.IntegerField(choices=[(1, 'In review'), (2, 'Accepted'), (3, 'Rejected')], default=1, verbose_name='Moderate status'),
        ),
        migrations.AddField(
            model_name='event',
            name='telegram_chat',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='event',
            name='latitude',
            field=models.DecimalField(decimal_places=16, max_digits=20, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='event',
            name='longitude',
            field=models.DecimalField(decimal_places=16, max_digits=20, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.IntegerField(verbose_name='Price'),
        ),
    ]