# Generated by Django 4.2.1 on 2023-10-28 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addons', '0006_remove_addon_category_addon_ccc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addon',
            old_name='ccc',
            new_name='category',
        ),
    ]
