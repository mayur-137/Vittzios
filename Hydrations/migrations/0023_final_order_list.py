# Generated by Django 4.2.4 on 2023-09-12 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hydrations', '0022_alter_orders_order_id'),
    ]

    operations = [
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
    ]
