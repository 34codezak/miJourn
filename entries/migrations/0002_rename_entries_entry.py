# Generated by Django 5.2.3 on 2025-06-26 19:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entries',
            new_name='Entry',
        ),
    ]
