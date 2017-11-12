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


################################################################################
#                                     EMAIL                                    #
################################################################################
def successfully_sent_quote(quote):
    quote  = Quote.objects.get(id = quote)
    print(str(quote.number))
    send_mail(
        '[Hilcor] Su cotizacion ha sido enviada.',
        'Saludos, '+ quote.contact +'. Su cotizacion ha sido enviada satisfactoriamente.\n' +
        'Usted puede revisar el estado de su cotizacion en el area de consultas ingresando el numero: \n' + str(quote.number),
        'noeply@hilcor.com',
        [quote.email],
        fail_silently=False,
    )

def new_user_email(user, password):
    user  = User.objects.get(username = user)
    user_name = str(user.first_name) + " " + str(user.last_name)
    send_mail(
        '[INEA TUGS] Bienvenido a INEA TUGS',
        'Hola, ' + user_name +'. Bienvenido a INEA TUGS. Un administrador te ha creado una cuenta para que puedas ingresar al sistema \n' +
        'Estos son tus datos de acceso: \n\n' +
        'Usuario: '+ user.username + '\n' +
        'Correo Electrónico: '+ user.email +' \n' +
        'Contraseña: '+ password +'\n\n' +
        'Ten en cuenta que la contraseña fue generada por el administrador. ' +
        'Recuerda cambiarla por una que recuerdes más fácilmente al ingresar al sistema.',
        'noreply@ineatugs.com',
        [user.email],
        fail_silently=False,
    )


def get_supervisers(activity):
    pass
