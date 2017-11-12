# -*- coding: utf-8 -*-
from datetime           import datetime
from django.core.mail   import send_mail
from dateutil.parser    import parse
from hilcor.models      import *

################################################################################
#                                  FUNCTIONS                                   #
################################################################################

def get_quote_number():
	today = datetime.today()
	return str(today.day) + str(today.month) + str(today.year)[2:] + '-' +str(today.hour) + str(today.minute)

def get_invoice_number():
    today      = datetime.today()
    n_invoices = str(Invoice.objects.count() + 1)
    serial     = '0000'
    serial     = serial[len(n_invoices):] + n_invoices
    return str(today.year)[2:] + '-' + serial

################################################################################
#                                     EMAIL                                    #
################################################################################
def successfully_sent_quote(quote):
    quote  = Quote.objects.get(id = quote)
    send_mail(
        '[Hilcor] Su cotizacion ha sido enviada.',
        'Saludos, '+ quote.contact +'. Su cotizacion ha sido enviada satisfactoriamente.\n' +
        'Usted puede revisar el estado de su cotizacion en el area de consultas ingresando el numero: \n' + str(quote.number),
        'noeply@hilcor.com',
        [quote.email],
        fail_silently=False,
    )

def invoice_sent(invoice):
    invoice  = Invoice.objects.get(id = invoice)
    send_mail(
        '[Hilcor] Su factura esta lista.',
        'Saludos, '+ invoice.business_name +'. Su factura asociada a la cotizacion ' + str(invoice.quote.number) + ' ya se encuentra disponible.\n' +
        'Numero de Factura: \n' +str(invoice.number) + '.\n' +
        'Usted puede descargar la factura en el area de consultas usando el numero de su cotizacion.',
        'noeply@hilcor.com',
        [invoice.quote.email],
        fail_silently=False,
    )


def get_supervisers(activity):
    pass
