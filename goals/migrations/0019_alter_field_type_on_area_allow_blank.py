# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0018_add_mptt_tree_to_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='type',
            field=models.CharField(blank=True, max_length=255, verbose_name='Area type'),
        ),
    ]