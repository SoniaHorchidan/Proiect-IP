# Generated by Django 2.0.4 on 2018-04-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurante', '0010_auto_20180412_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
