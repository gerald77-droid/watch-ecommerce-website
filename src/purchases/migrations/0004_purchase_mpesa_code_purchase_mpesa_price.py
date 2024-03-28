# Generated by Django 4.1.13 on 2024-03-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0003_rename_mpesa_price_purchase_stripe_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='mpesa_code',
            field=models.CharField(blank=True, max_length=22, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='mpesa_price',
            field=models.IntegerField(default=0),
        ),
    ]