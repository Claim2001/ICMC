# Generated by Django 2.1.7 on 2019-04-03 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_paymentrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='status',
            field=models.CharField(choices=[('wait', 'wait'), ('look', 'look'), ('rejected', 'rejected'), ('payment', 'waiting for payment'), ('payment_check', 'waiting for payment check'), ('inspector_check', 'waiting for data check'), ('accepted', 'accepted')], default='wait', max_length=100),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('wait', 'wait'), ('look', 'look'), ('rejected', 'rejected'), ('payment', 'waiting for payment'), ('payment_check', 'waiting for payment check'), ('inspector_check', 'waiting for data check'), ('accepted', 'accepted')], max_length=250),
        ),
    ]
