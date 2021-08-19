# Generated by Django 3.2.5 on 2021-08-18 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_usersource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersource',
            name='current_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sourceowner', to=settings.AUTH_USER_MODEL),
        ),
    ]
