# Generated by Django 4.1.13 on 2024-03-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productimages_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
