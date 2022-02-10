# Generated by Django 4.0.1 on 2022-02-08 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repairs_restorals', '0013_alter_serviceticket_customer_and_more'),
        ('invoices', '0015_remove_workshopcustomerinvoice_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopcustomerinvoice',
            name='service_ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairs_restorals.serviceticket'),
        ),
    ]