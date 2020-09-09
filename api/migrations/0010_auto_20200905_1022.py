# Generated by Django 3.1 on 2020-09-05 09:22

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200905_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='accessories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='api.accessories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='bought_together',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='api.boughttogether'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default='Generic', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='api.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.storage_dir),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_features',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='api.mainfeatures'),
        ),
        migrations.AlterField(
            model_name='product',
            name='package_dimensions',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
