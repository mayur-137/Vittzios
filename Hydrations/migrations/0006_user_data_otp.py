# Generated by Django 4.2.4 on 2023-09-24 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0005_alter_ayurvedicjuice_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]