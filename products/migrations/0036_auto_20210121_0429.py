# Generated by Django 3.1 on 2021-01-21 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_auto_20210115_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='model_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.modelname'),
        ),
    ]