# Generated by Django 4.2.1 on 2023-12-14 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addons', '0009_compatible_versions_addon_author_addon_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='author',
            field=models.CharField(default='Jojin', max_length=32, verbose_name='Автор'),
        ),
    ]