# Generated by Django 5.0.6 on 2024-11-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0005_dmeorder_dmeorderitem_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmeorder',
            name='rental_date',
            field=models.DateField(help_text='Please provide date the equipment was rented', verbose_name='Rental Date'),
        ),
    ]
