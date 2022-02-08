# Generated by Django 4.0.1 on 2022-02-08 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0014_workshopcustomerinvoice_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopcustomerinvoice',
            name='customer',
        ),
        migrations.AlterField(
            model_name='baseinvoice',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
