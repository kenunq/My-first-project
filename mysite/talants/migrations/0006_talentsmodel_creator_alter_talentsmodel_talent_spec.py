# Generated by Django 4.2.1 on 2023-11-26 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('talants', '0005_remove_talentsmodel_char'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentsmodel',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель талантов'),
        ),
        migrations.AlterField(
            model_name='talentsmodel',
            name='talent_spec',
            field=models.CharField(default='', max_length=32, verbose_name='Путь до изображения спецификации'),
        ),
    ]
