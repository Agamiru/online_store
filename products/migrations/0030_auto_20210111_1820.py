# Generated by Django 3.1 on 2021-01-11 17:20

from django.db import migrations
from django.contrib.postgres.operations import (
    HStoreExtension, TrigramExtension
)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_auto_20210111_0120'),
    ]

    operations = [
        HStoreExtension(),
        TrigramExtension()
    ]
