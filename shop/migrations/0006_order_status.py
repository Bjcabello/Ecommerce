# Generated by Django 5.0.4 on 2024-07-25 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10, verbose_name='Estado'),
        ),
    ]
