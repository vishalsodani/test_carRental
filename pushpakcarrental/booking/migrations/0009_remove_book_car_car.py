# Generated by Django 4.1.1 on 2022-12-06 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0008_book_car_car"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book_car",
            name="car",
        ),
    ]