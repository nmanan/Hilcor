# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hilcor', '0015_auto_20171202_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='invoice',
        ),
        migrations.AddField(
            model_name='payment',
            name='quote',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hilcor.Quote'),
        ),
    ]
