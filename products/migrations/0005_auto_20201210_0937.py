# Generated by Django 3.1 on 2020-12-10 08:37

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20201210_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alias',
            field=models.JSONField(default=products.models.json_default),
        ),
        migrations.AlterField(
            model_name='category',
            name='main_features',
            field=models.JSONField(default=products.models.json_default),
        ),
        migrations.AlterField(
            model_name='subcategory1',
            name='alias',
            field=models.JSONField(default=products.models.json_default),
        ),
        migrations.AlterField(
            model_name='subcategory1',
            name='main_features',
            field=models.JSONField(default=products.models.json_default),
        ),
        migrations.AlterField(
            model_name='subcategory2',
            name='alias',
            field=models.JSONField(default=products.models.json_default),
        ),
        migrations.AlterField(
            model_name='subcategory2',
            name='main_features',
            field=models.JSONField(default=products.models.json_default),
        ),
    ]