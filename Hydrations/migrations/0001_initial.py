# Generated by Django 4.1 on 2023-08-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AyurvedicJuice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='images/AyurvedicJuice/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AyurvedicPower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='images/AyurvedicPower/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EffervescentTablets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='images/EffervescentTablets/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TropicalSkinHair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='images/TropicalSkinHair/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VitaminCapsules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='images/VitaminCapsules/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VitaminGummies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='images/VitaminGummies/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
