# Generated by Django 3.0.5 on 2020-09-21 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20200921_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='user',
        ),
        migrations.AddField(
            model_name='city',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
