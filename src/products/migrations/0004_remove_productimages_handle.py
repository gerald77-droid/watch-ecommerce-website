# Generated by Django 4.1.13 on 2024-03-08 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productimages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimages',
            name='handle',
        ),
    ]
