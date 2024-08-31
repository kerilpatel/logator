# Generated by Django 5.1 on 2024-08-31 07:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service_registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('log_level', models.CharField(choices=[('DEBUG', 'Debug'), ('INFO', 'Info'), ('WARNING', 'Warning'), ('ERROR', 'Error'), ('CRITICAL', 'Critical')], max_length=10)),
                ('log_tag', models.CharField(blank=True, max_length=50)),
                ('message', models.TextField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_registration.service')),
            ],
        ),
    ]
