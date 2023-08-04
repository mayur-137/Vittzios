# Generated by Django 4.1 on 2023-08-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0002_alter_ayurvedicjuice_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayurvedicpower',
            name='picture',
            field=models.ImageField(upload_to='static/images/AyurvedicPower/'),
        ),
        migrations.AlterField(
            model_name='effervescenttablets',
            name='picture',
            field=models.ImageField(upload_to='static/images/EffervescentTablets/'),
        ),
        migrations.AlterField(
            model_name='tropicalskinhair',
            name='picture',
            field=models.ImageField(upload_to='static/images/TropicalSkinHair/'),
        ),
        migrations.AlterField(
            model_name='vitamincapsules',
            name='picture',
            field=models.ImageField(upload_to='static/images/VitaminCapsules/'),
        ),
        migrations.AlterField(
            model_name='vitamingummies',
            name='picture',
            field=models.ImageField(upload_to='static/images/VitaminGummies/'),
        ),
    ]
