# Generated by Django 2.1.7 on 2019-03-07 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_auto_20190305_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='activation_code',
            field=models.PositiveIntegerField(default=1000),
            preserve_default=False,
        ),
    ]