# Generated by Django 4.2.4 on 2023-09-28 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0008_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('size', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='ayurvedicjuice',
            name='image',
            field=models.ImageField(default='static/images/VitaminGummies/cart.png', upload_to='static/images/VitaminGummies/'),
        ),
        migrations.AddField(
            model_name='ayurvedicpower',
            name='image',
            field=models.ImageField(default='static/images/VitaminGummies/cart.png', upload_to='static/images/VitaminGummies/'),
        ),
        migrations.AddField(
            model_name='effervescenttablets',
            name='image',
            field=models.ImageField(default='static/images/VitaminGummies/cart.png', upload_to='static/images/VitaminGummies/'),
        ),
        migrations.AddField(
            model_name='tropicalskinhair',
            name='image',
            field=models.ImageField(default='static/images/VitaminGummies/cart.png', upload_to='static/images/VitaminGummies/'),
        ),
        migrations.AddField(
            model_name='vitamincapsules',
            name='image',
            field=models.ImageField(default='static/images/VitaminGummies/cart.png', upload_to='static/images/VitaminGummies/'),
        ),
        migrations.AddField(
            model_name='vitamingummies',
            name='image',
            field=models.ImageField(default='static/images/VitaminGummies/cart.png', upload_to='static/images/VitaminGummies/'),
        ),
        migrations.CreateModel(
            name='Men',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hydrations.size')),
            ],
        ),
    ]