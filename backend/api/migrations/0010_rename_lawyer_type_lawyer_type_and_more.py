# Generated by Django 4.2.5 on 2023-10-01 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_judge_user_alter_lawyer_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lawyer',
            old_name='lawyer_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='useraccount',
            old_name='user_type',
            new_name='type',
        ),
    ]
