# Generated by Django 3.2.8 on 2021-10-29 06:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message='Length of number must be between 5 and 15 digits.', regex='^\\+?\\d{5,15}$')])),
                ('email', models.EmailField(max_length=254)),
                ('date_born', models.DateField(blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
