# Generated by Django 4.1.13 on 2024-03-22 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0002_purchase_stripe_checkout_session_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='mpesa_price',
            new_name='stripe_price',
        ),
    ]