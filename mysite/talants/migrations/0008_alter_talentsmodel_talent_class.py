# Generated by Django 4.2.1 on 2023-11-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talants', '0007_alter_talentsmodel_talent_spec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentsmodel',
            name='talent_class',
            field=models.CharField(default='', max_length=128, verbose_name='Класс'),
        ),
    ]
