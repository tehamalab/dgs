# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-28 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0052_add_field_caption_on_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='themes',
            field=models.ManyToManyField(related_name='sectors', to='goals.Theme', verbose_name='Themes'),
        ),
    ]
