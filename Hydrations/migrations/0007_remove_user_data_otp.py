# Generated by Django 4.2.4 on 2023-09-24 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0006_user_data_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_data',
            name='otp',
        ),
    ]
