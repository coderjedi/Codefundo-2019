# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-08-20 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0007_auto_20190820_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voterinfo',
            name='constituency_id',
            field=models.CharField(max_length=256),
        ),
    ]
