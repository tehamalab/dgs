# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0036_change_area_code_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areatype',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='group',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='Code'),
        ),
    ]
