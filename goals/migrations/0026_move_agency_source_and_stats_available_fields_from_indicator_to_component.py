# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-28 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0025_make_plan_required_on_goal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='agency_en',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='agency_sw',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='data_source',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='data_source_en',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='data_source_sw',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='stats_available',
        ),
        migrations.AddField(
            model_name='component',
            name='agency',
            field=models.CharField(blank=True, max_length=255, verbose_name='Agency'),
        ),
        migrations.AddField(
            model_name='component',
            name='agency_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Agency'),
        ),
        migrations.AddField(
            model_name='component',
            name='agency_sw',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Agency'),
        ),
        migrations.AddField(
            model_name='component',
            name='data_source',
            field=models.CharField(blank=True, max_length=255, verbose_name='Data source'),
        ),
        migrations.AddField(
            model_name='component',
            name='data_source_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Data source'),
        ),
        migrations.AddField(
            model_name='component',
            name='data_source_sw',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Data source'),
        ),
        migrations.AddField(
            model_name='component',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Component description'),
        ),
        migrations.AddField(
            model_name='component',
            name='description_sw',
            field=models.TextField(blank=True, null=True, verbose_name='Component description'),
        ),
        migrations.AddField(
            model_name='component',
            name='image_en',
            field=models.ImageField(blank=True, null=True, upload_to='goals/components/images', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='component',
            name='image_sw',
            field=models.ImageField(blank=True, null=True, upload_to='goals/components/images', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='component',
            name='stats_available',
            field=models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No'), ('PARTIALLY', 'Partially'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=50, verbose_name='Statistics availble'),
        ),
    ]
