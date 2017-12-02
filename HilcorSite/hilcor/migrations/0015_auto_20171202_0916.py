# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 13:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hilcor', '0014_auto_20171112_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productininvoice',
            name='measure',
        ),
        migrations.RemoveField(
            model_name='productinquote',
            name='measure',
        ),
        migrations.AlterField(
            model_name='productininvoice',
            name='price_p_u',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, b'Precio por unidad debe ser mayor a %(limit_value)s')], verbose_name=b'Precio por Unidad (Kg) *'),
        ),
        migrations.AlterField(
            model_name='productininvoice',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name=b'Cantidad (Kg) * '),
        ),
        migrations.AlterField(
            model_name='productinquote',
            name='price_p_u',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, b'Precio por unidad debe ser mayor a %(limit_value)s')], verbose_name=b'Precio por Unidad (Kg) *'),
        ),
        migrations.AlterField(
            model_name='productinquote',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name=b'Cantidad (Kg) * '),
        ),
    ]
