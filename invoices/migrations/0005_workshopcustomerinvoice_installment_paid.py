# Generated by Django 4.0b1 on 2022-01-30 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_alter_baseinvoice_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopcustomerinvoice',
            name='installment_paid',
            field=models.BooleanField(default=False),
        ),
    ]
