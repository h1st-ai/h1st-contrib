# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-02 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_DataMgmt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentuniquetype',
            name='data_fields',
            field=models.ManyToManyField(blank=True, to='IoT_DataMgmt.EquipmentDataField'),
        ),
    ]
