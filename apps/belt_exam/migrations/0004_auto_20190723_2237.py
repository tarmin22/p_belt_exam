# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-24 05:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam', '0003_auto_20190723_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='joined_by',
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
    ]
