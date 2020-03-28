# Generated by Django 3.0.2 on 2020-03-13 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '__first__'),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='file',
        ),
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
        migrations.AddField(
            model_name='image',
            name='corresponds_to_event',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='event.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='image_file',
            field=models.FileField(default=django.utils.timezone.now, upload_to='images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='uploaded_by',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
