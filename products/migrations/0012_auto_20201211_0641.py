# Generated by Django 3.1 on 2020-12-11 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20201211_0641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='new_alias',
            new_name='alias',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='new_features',
            new_name='main_features',
        ),
    ]
