# Generated by Django 4.2.1 on 2023-11-26 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talants', '0005_remove_talentsmodel_char'),
        ('CharPage', '0005_alter_charmodel_char_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='charmodel',
            name='talents',
            field=models.ManyToManyField(null=True, to='talants.talentsmodel', verbose_name='Привязанные таланты'),
        ),
    ]