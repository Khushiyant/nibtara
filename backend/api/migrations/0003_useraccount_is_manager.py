# Generated by Django 4.2.5 on 2023-09-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_useraccount_is_active_useraccount_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_manager',
            field=models.BooleanField(default=False),
        ),
    ]