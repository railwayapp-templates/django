# Generated by Django 5.0.6 on 2024-10-21 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_expectations', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('volunteer_helpful', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('service_impact', models.TextField()),
                ('refer_friends', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
