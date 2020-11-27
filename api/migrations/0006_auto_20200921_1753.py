# Generated by Django 3.1 on 2020-09-21 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200921_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryaccessoryjoin',
            name='accessory_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='category_join', to='api.categorydouble', to_field='cat_id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryaccessoryjoin',
            name='cat_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accessory_join', to='api.category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryboughttogetherjoin',
            name='bought_together_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bought_join', to='api.categorydouble', to_field='cat_id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryboughttogetherjoin',
            name='cat_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bought_together_join', to='api.category'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Subcat2Double',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcat_2_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.subcategory2')),
            ],
            options={
                'verbose_name_plural': 'subcategory_2_double',
                'db_table': 'subcategory_2_double',
            },
        ),
        migrations.CreateModel(
            name='Subcat2BoughtTogetherJoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_field', models.IntegerField(blank=True, unique=True)),
                ('accessory_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bought_join', to='api.subcat2double', to_field='subcat_2_id')),
                ('subcat_2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bought_together_join', to='api.subcategory2')),
            ],
            options={
                'verbose_name_plural': 'subcategory_2_bought_together',
                'db_table': 'subcategory_2_bought_together',
            },
        ),
        migrations.CreateModel(
            name='Subcat2AccessoryJoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_field', models.IntegerField(blank=True, unique=True)),
                ('accessory_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_join', to='api.subcat2double', to_field='subcat_2_id')),
                ('subcat_2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessory_join', to='api.subcategory2')),
            ],
            options={
                'verbose_name_plural': 'subcategory_2_accessories',
                'db_table': 'subcategory_2_accessories',
            },
        ),
    ]