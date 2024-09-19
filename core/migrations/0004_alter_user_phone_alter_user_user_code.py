# Generated by Django 5.1 on 2024-09-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, unique=True, verbose_name='موبایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_code',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='کد کاربری'),
        ),
    ]
