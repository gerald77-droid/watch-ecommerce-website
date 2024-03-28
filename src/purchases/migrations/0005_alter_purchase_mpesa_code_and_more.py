# Generated by Django 4.1.13 on 2024-03-26 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0004_purchase_mpesa_code_purchase_mpesa_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='mpesa_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='stripe_checkout_session_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
