# Generated by Django 4.0.1 on 2022-01-26 21:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='expiry_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
