# Generated by Django 4.0b1 on 2022-01-30 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinvoice',
            name='order_number',
            field=models.CharField(editable=False, max_length=100),
        ),
    ]