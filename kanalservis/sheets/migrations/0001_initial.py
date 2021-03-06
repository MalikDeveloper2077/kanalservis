# Generated by Django 4.0.4 on 2022-05-22 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(verbose_name='Номер заказа')),
                ('usd_price', models.IntegerField(verbose_name='Стоимость в $')),
                ('rub_price', models.FloatField(blank=True, null=True, verbose_name='Стоимость в ₽')),
                ('delivery_date', models.DateField()),
            ],
        ),
    ]
