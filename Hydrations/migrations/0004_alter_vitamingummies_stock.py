# Generated by Django 4.2.4 on 2023-09-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0003_vitamingummies_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitamingummies',
            name='stock',
            field=models.BooleanField(default=True),
        ),
    ]