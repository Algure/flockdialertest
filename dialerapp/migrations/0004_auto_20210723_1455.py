# Generated by Django 3.0.3 on 2021-07-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialerapp', '0003_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
