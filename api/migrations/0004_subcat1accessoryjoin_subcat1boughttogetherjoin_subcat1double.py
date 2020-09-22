# Generated by Django 3.1 on 2020-09-21 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200914_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcat1Double',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcat_1_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.subcategory1')),
            ],
            options={
                'verbose_name_plural': 'subcategory_1_double',
                'db_table': 'subcategory_1_double',
            },
        ),
        migrations.CreateModel(
            name='Subcat1BoughtTogetherJoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_field', models.IntegerField(blank=True, unique=True)),
                ('accessory_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bought_join', to='api.subcat1double', to_field='subcat_1_id')),
                ('subcat_1_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bought_together_join', to='api.subcategory1')),
            ],
            options={
                'verbose_name_plural': 'subcategory_1_bought_together',
                'db_table': 'subcategory_1_bought_together',
            },
        ),
        migrations.CreateModel(
            name='Subcat1AccessoryJoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_field', models.IntegerField(blank=True, unique=True)),
                ('accessory_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_join', to='api.subcat1double', to_field='subcat_1_id')),
                ('subcat_1_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accessory_join', to='api.subcategory1')),
            ],
            options={
                'verbose_name_plural': 'subcategory_1_accessories',
                'db_table': 'subcategory_1_accessories',
            },
        ),
    ]
