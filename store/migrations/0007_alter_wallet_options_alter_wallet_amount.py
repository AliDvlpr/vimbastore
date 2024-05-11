# Generated by Django 5.0.4 on 2024-04-30 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_customer_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'verbose_name_plural': 'کیف پول ها'},
        ),
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
    ]
