# Generated by Django 3.1 on 2020-09-05 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200905_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessories',
            name='subcat_1_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory1'),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='subcat_2_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory2'),
        ),
        migrations.AlterField(
            model_name='boughttogether',
            name='subcat_1_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory1'),
        ),
        migrations.AlterField(
            model_name='boughttogether',
            name='subcat_2_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory2'),
        ),
        migrations.AlterField(
            model_name='mainfeatures',
            name='subcat_1_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory1'),
        ),
        migrations.AlterField(
            model_name='mainfeatures',
            name='subcat_2_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcat_1_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory1'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcat_2_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory2'),
        ),
    ]