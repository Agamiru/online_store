# Generated by Django 3.1 on 2020-12-10 08:46

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20201210_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alias',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=products.models.json_default),
        ),
        migrations.AlterField(
            model_name='category',
            name='main_features',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=products.models.json_default),
        ),
    ]