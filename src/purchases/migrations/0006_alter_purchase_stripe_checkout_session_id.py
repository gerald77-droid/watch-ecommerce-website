# Generated by Django 4.1.13 on 2024-03-26 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0005_alter_purchase_mpesa_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='stripe_checkout_session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
