# Generated by Django 4.0.2 on 2022-02-22 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_shopitemimage_is_primary_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopitems',
            name='shipping',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=12),
        ),
    ]
