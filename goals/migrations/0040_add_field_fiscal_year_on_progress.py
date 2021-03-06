# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0039_alter_field_code_on_component_allow_blank'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='fiscal_year',
            field=models.CharField(blank=True, max_length=8, verbose_name='Fiscal year'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year'),
        ),
    ]
