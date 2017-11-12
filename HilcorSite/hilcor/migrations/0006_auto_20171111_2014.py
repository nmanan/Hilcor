# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-11 20:14
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hilcor', '0005_auto_20171029_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinquote',
            name='measure',
            field=models.CharField(choices=[(b'Kg', b'Kilogramos (Kg)')], default=b'Kg', max_length=3),
        ),
        migrations.AlterField(
            model_name='productinquote',
            name='price_p_u',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, b'Precio por unidad debe ser mayor a %(limit_value)s')]),
        ),
        migrations.AlterField(
            model_name='productinquote',
            name='total_price',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, b'Precio total debe ser mayor a %(limit_value)s')]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='iva',
            field=models.FloatField(default=12, validators=[django.core.validators.MinValueValidator(0.0, b'Precio por unidad debe ser mayor a %(limit_value)s')]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='number',
            field=models.CharField(blank=True, default=b'', max_length=12),
        ),
        migrations.AlterField(
            model_name='quote',
            name='subtotal',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, b'Precio por unidad debe ser mayor a %(limit_value)s')]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='total',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, b'Precio por unidad debe ser mayor a %(limit_value)s')]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='total_iva',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, b'Precio por unidad debe ser mayor a %(limit_value)s')]),
        ),
    ]