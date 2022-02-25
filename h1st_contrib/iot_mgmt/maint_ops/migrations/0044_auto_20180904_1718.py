# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-05 00:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_MaintOps', '0043_auto_20180904_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentuniquetypegroupserviceconfig',
            name='monitored_equipment_data_field_configs',
        ),
        migrations.AddField(
            model_name='monitoredequipmentdatafieldconfig',
            name='equipment_unique_type_group_service_config',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='monitored_equipment_data_field_configs', related_query_name='monitored_equipment_data_field_config', to='IoT_MaintOps.EquipmentUniqueTypeGroupServiceConfig'),
        ),
    ]
