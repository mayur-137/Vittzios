# Generated by Django 4.1 on 2023-08-11 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0003_alter_ayurvedicpower_picture_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/CartModules/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
