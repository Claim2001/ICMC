# Generated by Django 2.1.7 on 2019-03-14 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_auto_20190313_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoveRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('change', 'Изменение владельца или места жительства'), ('broke', 'Износ или поломка судна'), ('ticket', 'Утеря или порча судового билета')], max_length=300)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Boat')),
            ],
        ),
    ]