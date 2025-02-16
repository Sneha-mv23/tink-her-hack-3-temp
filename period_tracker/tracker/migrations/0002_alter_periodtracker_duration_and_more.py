# Generated by Django 5.1.6 on 2025-02-08 14:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodtracker',
            name='duration',
            field=models.IntegerField(help_text='Cycle duration in days'),
        ),
        migrations.AlterField(
            model_name='periodtracker',
            name='next_period_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, help_text='Height in cm', null=True)),
                ('cycle_length', models.IntegerField(default=28, help_text='Average cycle length in days')),
                ('activity_level', models.CharField(choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High')], default='Moderate', max_length=20)),
                ('medical_conditions', models.TextField(blank=True, help_text='Any relevant medical conditions', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
