# Generated by Django 3.1 on 2020-12-11 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20201211_0655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory1',
            old_name='new_alias',
            new_name='alias',
        ),
        migrations.RenameField(
            model_name='subcategory1',
            old_name='new_main_features',
            new_name='main_features',
        ),
        migrations.RenameField(
            model_name='subcategory2',
            old_name='new_alias',
            new_name='alias',
        ),
        migrations.RenameField(
            model_name='subcategory2',
            old_name='new_main_features',
            new_name='main_features',
        ),
    ]