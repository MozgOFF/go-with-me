# Generated by Django 3.0.2 on 2020-03-14 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20200314_0102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='corresponds_to_event',
        ),
        migrations.RemoveField(
            model_name='image',
            name='uploaded_by',
        ),
    ]