# Generated by Django 4.0b1 on 2022-01-30 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_alter_baseinvoice_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinvoice',
            name='paid_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
