# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-12 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hilcor', '0011_auto_20171112_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=100, verbose_name=b'Banco *')),
                ('acc_type', models.CharField(choices=[(b'C', b'Corriente')], default=b'C', max_length=3, verbose_name=b'Tipo de Cuenta *')),
                ('account', models.CharField(max_length=100, unique=True, verbose_name=b'N\xc3\xbamero de Cuenta *')),
                ('check', models.BooleanField(default=False, verbose_name=b'Cheque')),
                ('transfer', models.BooleanField(default=False, verbose_name=b'Transferencia')),
                ('deposit', models.BooleanField(default=False, verbose_name=b'Dep\xc3\xb3sito')),
                ('acc_name', models.CharField(max_length=100, verbose_name=b'A Nombre de *')),
                ('enabled', models.BooleanField(default=False, verbose_name=b'Habilitar Me\xc3\xa9todo de Pagos')),
            ],
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[(b'B', b'Borrador'), (b'P', b'Pendiente'), (b'Pa', b'Pagada'), (b'C', b'Cancelada')], default=b'B', max_length=3, verbose_name=b'Estado'),
        ),
    ]
