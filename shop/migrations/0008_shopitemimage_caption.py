# Generated by Django 4.0b1 on 2022-01-17 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_shopitemimage_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopitemimage',
            name='caption',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
