# Generated by Django 3.1 on 2021-01-10 22:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_auto_20210110_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alias',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), default=list, size=None),
        ),
    ]
