# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-08 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0031_alter_field_type_on_area_from_charfield_to_foreign_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='remarks',
            field=models.TextField(blank=True, verbose_name='Remarks'),
        ),
    ]
