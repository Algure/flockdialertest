# Generated by Django 3.0.3 on 2021-07-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialerapp', '0002_company_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name=False),
            preserve_default=False,
        ),
    ]
