# Generated by Django 4.0.2 on 2022-02-23 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs_restorals', '0013_alter_serviceticket_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='admin_created',
            field=models.BooleanField(default=False),
        ),
    ]
