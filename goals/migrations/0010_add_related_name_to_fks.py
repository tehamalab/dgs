# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0009_alter_field_label_stats_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='goals.Indicator', verbose_name='Indicator'),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='goals.Goal', verbose_name='Goal'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='goals.Area', verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='goals.Component', verbose_name='Component'),
        ),
    ]
