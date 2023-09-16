# Generated by Django 4.2.4 on 2023-09-13 07:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Hydrations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AyurvedicJuice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('max_quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/AyurvedicJuice/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AyurvedicPower',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('max_quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/AyurvedicPower/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('max_quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/CartModules/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=4000)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EffervescentTablets',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('max_quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/EffervescentTablets/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='final_order_list',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(default='INDIA', max_length=1000)),
                ('products_detail', models.CharField(default='empty', max_length=1000)),
                ('order_total', models.IntegerField()),
                ('shiprocket_dashboard', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('address_1', models.CharField(default='INDIA', max_length=1000)),
                ('products_detail', models.CharField(default='empty', max_length=1000)),
                ('order_total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TropicalSkinHair',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('max_quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/TropicalSkinHair/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100)),
                ('building', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(default='GUJRAT', max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VitaminCapsules',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.BooleanField()),
                ('max_quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/VitaminCapsules/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VitaminGummies',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('max_quantity', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='static/images/VitaminGummies/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
