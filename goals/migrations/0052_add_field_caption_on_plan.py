# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-26 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0051_allow_blank_value_for_sector_target_and_theme_fields_on_indicator'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='caption',
            field=models.TextField(blank=True, verbose_name='Caption'),
        ),
        migrations.AddField(
            model_name='plan',
            name='caption_en',
            field=models.TextField(blank=True, null=True, verbose_name='Caption'),
        ),
        migrations.AddField(
            model_name='plan',
            name='caption_sw',
            field=models.TextField(blank=True, null=True, verbose_name='Caption'),
        ),
    ]
