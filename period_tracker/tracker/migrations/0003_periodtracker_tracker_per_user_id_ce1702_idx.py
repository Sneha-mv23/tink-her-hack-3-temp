# Generated by Django 5.1.6 on 2025-02-08 18:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_alter_periodtracker_duration_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='periodtracker',
            index=models.Index(fields=['user', 'next_period_date'], name='tracker_per_user_id_ce1702_idx'),
        ),
    ]
