# Generated by Django 4.0.2 on 2022-02-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_shopitems_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopitems',
            name='shipping',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
