# Generated by Django 3.1 on 2020-09-01 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200825_1317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory2',
            old_name='sub_cat_id',
            new_name='subcat_id',
        ),
        migrations.RemoveField(
            model_name='accessories',
            name='cat_name',
        ),
        migrations.RemoveField(
            model_name='accessories',
            name='sub_cat_1_name',
        ),
        migrations.RemoveField(
            model_name='accessories',
            name='sub_cat_2_name',
        ),
        migrations.RemoveField(
            model_name='boughttogether',
            name='cat_name',
        ),
        migrations.RemoveField(
            model_name='boughttogether',
            name='sub_cat_1_name',
        ),
        migrations.RemoveField(
            model_name='boughttogether',
            name='sub_cat_2_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='cat_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sub_cat_1_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sub_cat_2_name',
        ),
        migrations.AddField(
            model_name='accessories',
            name='cat_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.category'),
        ),
        migrations.AddField(
            model_name='accessories',
            name='subcat_1_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory1'),
        ),
        migrations.AddField(
            model_name='accessories',
            name='subcat_2_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory2'),
        ),
        migrations.AddField(
            model_name='boughttogether',
            name='cat_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.category'),
        ),
        migrations.AddField(
            model_name='boughttogether',
            name='subcat_1_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory1'),
        ),
        migrations.AddField(
            model_name='boughttogether',
            name='subcat_2_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory2'),
        ),
        migrations.AddField(
            model_name='product',
            name='cat_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcat_1_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory1'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcat_2_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.subcategory2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='api.brand'),
        ),
    ]
