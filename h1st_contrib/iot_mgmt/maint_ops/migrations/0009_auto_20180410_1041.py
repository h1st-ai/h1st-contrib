# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-10 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_MaintOps', '0008_remove_blueprint_equipment_unique_types'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blueprint',
            options={'ordering': ('equipment_general_type', 'equipment_unique_type', 'trained_to_date', 'timestamp')},
        ),
        migrations.AddField(
            model_name='blueprint',
            name='trained_to_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
