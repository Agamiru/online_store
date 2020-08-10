# Generated by Django 3.1 on 2020-08-10 18:08

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioInterfaceFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputs', models.JSONField(default=api.models.json_default)),
                ('outputs', models.JSONField(default=api.models.json_default)),
                ('connection_type', models.CharField(max_length=200)),
                ('sample_rate', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=200)),
                ('power_source', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'audio_interface_features',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=200)),
                ('short_desc', models.CharField(max_length=200, verbose_name='Short Description')),
                ('in_the_box', models.JSONField(default=api.models.json_default)),
                ('specs', models.JSONField(default=api.models.json_default)),
                ('package_dimensions', models.CharField(max_length=200)),
                ('weight', models.IntegerField(null=True)),
                ('brand', models.ForeignKey(default='Generic', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.brand')),
                ('cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.category')),
                ('features', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.audiointerfacefeatures')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.AddField(
            model_name='audiointerfacefeatures',
            name='cat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_interface_features', to='api.category'),
        ),
    ]
