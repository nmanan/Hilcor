# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import *
from django.conf import settings
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
import mimetypes

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=100, blank=False, unique=True, verbose_name=" Nombre del Producto *")
	description = models.TextField(blank=False, default ='' ,verbose_name="Descripción")
	availability = models.BooleanField(default=False, verbose_name="Producto Disponible")

	def __unicode__(self):
		return u'%s' % (self.name)

class Quote(models.Model):

	status_list = [('P','Pendiente'), ('A','Activo'), ('E','Procesando'), ('T','Terminado'), ('C','Cancelado')]

	number  = models.CharField(max_length=12, blank=True, default='', verbose_name="Número")
	company = models.CharField(max_length=100, blank=True, verbose_name="Empresa")
	address = models.TextField(blank=False, verbose_name="Dirección *")
	contact = models.CharField(max_length=100, blank=False, verbose_name="Persona de Contacto *")
	phone   = models.CharField(max_length=20, blank=False, verbose_name="Teléfono *")
	email   = models.CharField(max_length=100, blank=False, verbose_name="Correo Electrónico *")

	request_date = models.DateField(verbose_name="Fecha de Solicitud")
	answer_date  = models.DateField(null=True, verbose_name="Fecha de Respuesta")

	subtotal  = models.FloatField(blank=False, default=0.0, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Subtotal")
	iva       = models.FloatField(blank=False, default=12 , validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="(%) IVA")
	total_iva = models.FloatField(blank=False, default=0.0, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Total IVA")
	total     = models.FloatField(blank=False, default=0.0, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Total a Pagar")

	comment   = models.TextField(blank=True, default = '', verbose_name="Comentarios")
	status    = models.CharField(max_length=3, choices=status_list, blank=False, default = 'P', verbose_name="Estado")

class ProductInQuote(models.Model):

	measures    = [('Kg','Kilogramos (Kg)')]

	quote       = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
	product     = models.ForeignKey(Product, null=True, on_delete = models.SET_NULL, verbose_name=Product._meta.verbose_name_plural)
	quantity    = models.PositiveIntegerField(verbose_name="Cantidad * ")
	measure     = models.CharField(max_length=3, choices=measures, blank=False, default='Kg', verbose_name="Medida")
	price_p_u   = models.FloatField(blank=False, default=0.00, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Precio por Unidad de Medida *")
	total_price = models.FloatField(blank=False, default=0.00, validators=[MinValueValidator(0.00, "Precio total debe ser mayor a %(limit_value)s")], verbose_name="Precio Total")


class PurchaseOrder(models.Model):
	quote   = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
	date    = models.DateField(auto_now=True)
	po_file = models.FileField(verbose_name="Seleccione Archivo de Orden de Compra (PDF) * ", upload_to='purchaseorders/')