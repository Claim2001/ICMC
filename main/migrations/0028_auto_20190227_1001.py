# Generated by Django 2.1.7 on 2019-02-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20190227_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='engine_model',
            field=models.CharField(max_length=300, verbose_name='Марка двигателя'),
        ),
        migrations.AlterField(
            model_name='boat',
            name='engine_power',
            field=models.PositiveIntegerField(verbose_name='Мощность двигателя/ей (кВт/л.с.)'),
        ),
        migrations.AlterField(
            model_name='boat',
            name='engine_type',
            field=models.CharField(max_length=300, verbose_name='Тип главного двигателя'),
        ),
        migrations.AlterField(
            model_name='boat',
            name='prev_numbers_or_name',
            field=models.CharField(max_length=300, verbose_name='Прежние регистр. No и название судна'),
        ),
        migrations.AlterField(
            model_name='boat',
            name='sail_area',
            field=models.PositiveIntegerField(verbose_name='Площадь парусов (м2)'),
        ),
    ]