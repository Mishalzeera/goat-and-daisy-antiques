# Generated by Django 4.0.1 on 2022-01-27 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_rename_user_auth_account_staffmember_username'),
        ('repairs_restorals', '0008_remove_serviceticket_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('staff_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.staffmember')),
            ],
        ),
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('is_completed', models.BooleanField(default=False)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairs_restorals.todolist')),
            ],
        ),
    ]
