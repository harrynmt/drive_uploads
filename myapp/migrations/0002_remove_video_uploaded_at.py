# Generated by Django 4.2.15 on 2024-08-21 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='uploaded_at',
        ),
    ]