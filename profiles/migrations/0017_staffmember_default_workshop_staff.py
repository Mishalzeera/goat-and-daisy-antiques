# Generated by Django 4.0.2 on 2022-02-22 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_rename_user_auth_account_staffmember_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='default_workshop_staff',
            field=models.BooleanField(default=False),
        ),
    ]
