# -*- coding: utf-8 -*-
from datetime               import datetime
from django.core.mail       import send_mail, EmailMultiAlternatives
from dateutil.parser        import parse
from hilcor.models          import *
from io                     import BytesIO
from django.http            import HttpResponse
from django.template.loader import get_template, render_to_string
from django.utils.html      import strip_tags


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
    html_content = render_to_string('emails/successfully_sent_quote.html', {'quote': quote})
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives('[Hilcor] Su cotizacion ha sido enviada.', text_content, 'noeply@hilcor.com', [quote.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def invoice_sent(invoice):
    invoice  = Invoice.objects.get(id = invoice)
    html_content = render_to_string('emails/invoice_sent.html', {'invoice': invoice})
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives('[Hilcor] Su factura esta lista.', text_content, 'noeply@hilcor.com', [invoice. quote.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
