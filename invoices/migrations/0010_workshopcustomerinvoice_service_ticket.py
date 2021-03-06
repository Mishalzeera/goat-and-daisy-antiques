# Generated by Django 4.0b1 on 2022-01-30 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repairs_restorals', '0011_serviceticket_has_invoice'),
        ('invoices', '0009_remove_workshopcustomerinvoice_service_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopcustomerinvoice',
            name='service_ticket',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='repairs_restorals.serviceticket'),
            preserve_default=False,
        ),
    ]
