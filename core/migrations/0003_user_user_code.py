# Generated by Django 5.0.6 on 2024-07-24 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_managers_user_otp_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_code',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
