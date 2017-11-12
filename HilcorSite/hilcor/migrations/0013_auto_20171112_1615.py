# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-12 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hilcor', '0012_auto_20171112_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[(b'C', b'Cheque'), (b'T', b'Cheque'), (b'D', b'Cheque')], default=b'C', max_length=3, verbose_name=b'Tipo de Operaci\xc3\xb3n *')),
                ('voucher', models.FileField(upload_to=b'vouchers/', verbose_name=b'Seleccione voucher o comprobante *')),
            ],
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='enabled',
            field=models.BooleanField(default=False, verbose_name=b'Habilitar M\xc3\xa9todo de Pago'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_file',
            field=models.FileField(upload_to=b'purchaseorders/', verbose_name=b'Seleccione Archivo de Orden de Compra * '),
        ),
        migrations.AddField(
            model_name='payment',
            name='PaymentType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hilcor.PaymentType'),
        ),
        migrations.AddField(
            model_name='payment',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hilcor.Invoice'),
        ),
    ]