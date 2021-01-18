# Generated by Django 3.1 on 2021-01-10 21:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20210110_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='features_alias',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), default=list, size=None),
        ),
    ]
