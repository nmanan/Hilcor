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

    default_comment = '''
        1. Deja sin efecto cualquier Cotización u Orden de Compra anterior. \n
        2. Se requiere la recepción de la Orden de Compra para el procesamiento del pedido.\n
        3. El IVA se aplicará de acuerdo a lo establecido en la G.O. Nº 41.239.\n
        4. Estos precios están sujetos a cambios SIN PREVIO AVISO, de acuerdo a las variaciones en el mercado nacional de la materia prima fundamental (fibra de algodón y material de empaque)\n
        5. La entrega de la mercancía está sujeta a la verificación del pago correspondiente.\n
        6: Solo se aceptan los métodos de pago mencionados en esta Cotización.
    '''

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

    comment   = models.TextField(blank=True, default = default_comment, verbose_name="Comentarios")
    status    = models.CharField(max_length=3, choices=status_list, blank=False, default = 'P', verbose_name="Estado")

class ProductInQuote(models.Model):

    quote       = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
    product     = models.ForeignKey(Product, null=True, on_delete = models.SET_NULL, verbose_name=Product._meta.verbose_name_plural)
    quantity    = models.PositiveIntegerField(verbose_name="Cantidad (Kg) * ", null=False)
    price_p_u   = models.FloatField(blank=False, default=0.00, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Precio por Unidad (Kg) *")
    total_price = models.FloatField(blank=False, default=0.00, validators=[MinValueValidator(0.00, "Precio total debe ser mayor a %(limit_value)s")], verbose_name="Precio Total")


class PurchaseOrder(models.Model):

    quote   = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
    date    = models.DateField(auto_now=True)
    po_file = models.FileField(verbose_name="Seleccione Archivo de Orden de Compra * ", upload_to='purchaseorders/')

class Invoice(models.Model):

    status_list   = [('B','Borrador'), ('P','Pendiente'), ('Pa','Pagada'), ('C','Cancelada')]

    quote         = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
    number        = models.CharField(max_length=12, blank=True, default='', verbose_name="Número")
    date          = models.DateField(auto_now=True)
    business_name = models.CharField(max_length=100, blank=False, default="", verbose_name="Razón Social *")
    address       = models.TextField(blank=False, default="", verbose_name="Domicilio Fiscal *")
    phone         = models.CharField(max_length=20, blank=False, default="", verbose_name="Teléfono *")
    rif           = models.CharField(max_length=100, blank=False, default="", verbose_name="RIF *")
    subtotal      = models.FloatField(blank=False, default=0.0, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Subtotal")
    iva           = models.FloatField(blank=False, default=12 , validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="(%) IVA")
    total_iva     = models.FloatField(blank=False, default=0.0, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Total IVA")
    total         = models.FloatField(blank=False, default=0.0, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Total a Pagar")

    comment       = models.TextField(blank=True, default = '', verbose_name="Comentarios")
    status        = models.CharField(max_length=3, choices=status_list, blank=False, default = 'B', verbose_name="Estado")
    deliver_date  = models.DateField(null=True, blank=True, verbose_name="Fecha de Entrega/Retiro *")

    def __unicode__(self):
        return u'%s' % (self.number)

class ProductInInvoice(models.Model):

    invoice      = models.ForeignKey(Invoice, null=True, on_delete = models.CASCADE)
    product      = models.ForeignKey(Product, null=True, on_delete = models.SET_NULL, verbose_name="Producto *")
    quantity     = models.PositiveIntegerField(verbose_name="Cantidad (Kg) * ")
    price_p_u    = models.FloatField(blank=False, default=0.00, validators=[MinValueValidator(0.00, "Precio por unidad debe ser mayor a %(limit_value)s")], verbose_name="Precio por Unidad (Kg) *")
    total_price  = models.FloatField(blank=False, default=0.00, validators=[MinValueValidator(0.00, "Precio total debe ser mayor a %(limit_value)s")], verbose_name="Precio Total")
    code         = models.CharField(max_length=12, blank=True, default='', verbose_name="Código *")
    order_number = models.CharField(max_length=12, blank=True, default='', verbose_name="Número de Orden de Entrega *")

class PaymentType(models.Model):

    account_types     = [('C','Corriente')]

    bank     = models.CharField(max_length=100, blank=False, verbose_name="Banco *")
    acc_type = models.CharField(max_length=3, choices=account_types, blank=False, default='C', verbose_name="Tipo de Cuenta *")
    account  = models.CharField(max_length=100, blank=False, unique=True,verbose_name="Número de Cuenta *")
    check    = models.BooleanField(default=False, verbose_name="Cheque")
    transfer = models.BooleanField(default=False, verbose_name="Transferencia")
    deposit  = models.BooleanField(default=False, verbose_name="Depósito")
    acc_name = models.CharField(max_length=100, blank=False, verbose_name="A Nombre de *")
    enabled  = models.BooleanField(default=False, verbose_name="Habilitar Método de Pago")


    def __unicode__(self):
        return u'%s | Cta. Nº %s' % (self.bank, self.account)

class Payment(models.Model):

    methods     = [('C','Cheque'),('T','Transferencia'),('D','Depósito')]

    quote        = models.ForeignKey(Quote, null=True, on_delete = models.CASCADE)
    PaymentType  = models.ForeignKey(PaymentType, null=True, on_delete = models.CASCADE)
    method       = models.CharField(max_length=3, choices=methods, blank=False, default='C', verbose_name="Tipo de Operación *")
    voucher      = models.FileField(verbose_name="Seleccione voucher o comprobante *", upload_to='vouchers/')
