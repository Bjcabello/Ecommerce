# Generated by Django 5.0.4 on 2024-07-25 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_order_status_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
