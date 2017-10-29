# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=100, blank=False, unique=True)
	description = models.TextField(blank=False, default ='')
	availability = models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s' % (self.name)

class Quote(models.Model):

	status_list = [('P','Pendiente'), ('A','Activa'), ('T','Terminada'), ('C','Cancelada')]

	number  = models.CharField(max_length=10, blank=True)
	company = models.CharField(max_length=100, blank=True)
	address = models.TextField(blank=False)
	contact = models.CharField(max_length=100, blank=False)
	phone   = models.CharField(max_length=20, blank=False)
	email   = models.CharField(max_length=100, blank=False)

	request_date = models.DateField()
	answer_date  = models.DateField(null=True)

	subtotal  = models.FloatField(blank=False, default=0.0)
	iva       = models.FloatField(blank=False, default=0.0)
	total_iva = models.FloatField(blank=False, default=0.0)
	total     = models.FloatField(blank=False, default=0.0)

	comment   = models.TextField(blank=True, default = '')
	status    = models.CharField(max_length=3, choices=status_list, blank=False, default = 'P')

class ProductInQuote(models.Model):

	measures    = [('Kg','Kilogramos (Kg)')]

	quote       = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
	product     = models.ForeignKey(Product, null=True, on_delete = models.SET_NULL)
	quantity    = models.PositiveIntegerField()
	measure     = models.CharField(max_length=3, choices=measures, blank=False)
	price_p_u   = models.FloatField(blank=False, default=0.0)
	total_price = models.FloatField(blank=False, default=0.0)


class PurchaceOrder(models.Model):
	quote = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
	date  = models.DateField()
	order_file = models.FileField()