# Generated by Django 4.0.1 on 2022-01-11 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0006_alter_customer_user_auth_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usernames', to=settings.AUTH_USER_MODEL),
        ),
    ]
