# Generated by Django 4.0b1 on 2022-01-17 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopItemPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='shopitems',
            name='description',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopitems',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopitems',
            name='title',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
