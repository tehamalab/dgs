# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0013_create_model_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='goals.Target', verbose_name='Target'),
        ),
    ]
