# Generated by Django 5.0.6 on 2024-11-24 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0012_rename_survior_clientsurvey2024_surveyor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsurvey2024',
            name='medical_treatment',
            field=models.JSONField(default=list, help_text='Please select the appropriate options', verbose_name='If you sought medical care, did you have to see a doctor or go to the ER?'),
        ),
    ]
