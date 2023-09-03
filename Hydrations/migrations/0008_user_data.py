# Generated by Django 4.2.4 on 2023-08-15 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0007_delete_user_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('building', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
        ),
    ]
