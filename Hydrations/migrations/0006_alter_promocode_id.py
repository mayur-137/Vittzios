# Generated by Django 4.2.4 on 2023-11-16 08:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0005_rename_user_email_promocode_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]