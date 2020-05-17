# Generated by Django 3.0.4 on 2020-05-04 19:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0004_auto_20200504_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='favorite_of',
            field=models.ManyToManyField(blank=True, related_name='favorite_category', related_query_name='favorite_category', to=settings.AUTH_USER_MODEL),
        ),
    ]
