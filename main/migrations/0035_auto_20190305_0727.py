# Generated by Django 2.1.7 on 2019-03-05 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20190305_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='address',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='owner',
            name='city',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='owner',
            name='country',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='owner',
            name='date_of_passport',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='owner',
            name='first_name',
            field=models.CharField(max_length=250, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='gender',
            field=models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=20, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='inn',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='owner',
            name='last_name',
            field=models.CharField(max_length=250, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='mail_index',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='owner',
            name='name_of_organization',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='owner',
            name='phone_number',
            field=models.CharField(default='', max_length=100),
        ),
    ]