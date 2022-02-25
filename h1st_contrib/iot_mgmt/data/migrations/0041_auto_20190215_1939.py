# Generated by Django 2.1.5 on 2019-02-15 19:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IoT_DataMgmt', '0040_numericmeasurementunit_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentuniquetype',
            name='foreign_lang_description',
        ),
        migrations.AlterField(
            model_name='equipmentuniquetype',
            name='description',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipmentuniquetypegroup',
            name='description',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
