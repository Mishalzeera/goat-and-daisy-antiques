# Generated by Django 4.0.1 on 2022-02-07 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repairs_restorals', '0011_serviceticket_has_invoice'),
        ('invoices', '0011_baseinvoice_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopcustomerinvoice',
            name='service_ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairs_restorals.serviceticket'),
        ),
    ]
