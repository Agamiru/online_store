# Generated by Django 3.1 on 2021-01-10 19:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_auto_20201216_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alias',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='category',
            name='main_features',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None),
        ),
        migrations.AlterField(
            model_name='subcategory1',
            name='alias',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='subcategory1',
            name='main_features',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='subcategory2',
            name='alias',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='subcategory2',
            name='main_features',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), default=list, size=None),
        ),
    ]
