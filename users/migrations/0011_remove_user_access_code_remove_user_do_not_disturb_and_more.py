# Generated by Django 4.0.1 on 2022-02-05 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_do_not_disturb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='access_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='do_not_disturb',
        ),
        migrations.AlterField(
            model_name='survey',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DND',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dnd_user_id', models.IntegerField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dnd_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccessCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_code', models.CharField(default=None, max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
