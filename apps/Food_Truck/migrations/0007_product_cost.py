# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-25 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food_Truck', '0006_report_upgrade'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]