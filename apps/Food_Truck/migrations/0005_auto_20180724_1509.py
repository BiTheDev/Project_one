# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-24 22:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Food_Truck', '0004_auto_20180724_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trucks_in_location', to='Food_Truck.Location'),
        ),
    ]