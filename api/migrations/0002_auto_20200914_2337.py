# Generated by Django 3.1 on 2020-09-14 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryaccessories',
            options={'verbose_name_plural': 'category_double'},
        ),
        migrations.AlterModelOptions(
            name='categoryaccessoryjoin',
            options={'verbose_name_plural': 'category_accessories'},
        ),
        migrations.AlterModelTable(
            name='categoryaccessories',
            table='category_double',
        ),
        migrations.AlterModelTable(
            name='categoryaccessoryjoin',
            table='category_accessories',
        ),
    ]