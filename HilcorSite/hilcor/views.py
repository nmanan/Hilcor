# -*- coding: utf-8 -*-
from django.contrib.auth            import authenticate, login, logout
from django.shortcuts               import render
from django.http                    import HttpResponse, HttpResponseRedirect
from django.template                import loader
from django.contrib.auth.decorators import login_required
from django.forms.formsets          import formset_factory
from hilcor.models                  import *
from hilcor.forms                   import *
from hilcor.utils                   import *
from datetime                       import datetime, date, timedelta
from django_xhtml2pdf.utils         import generate_pdf
from django.db.models               import Sum

import calendar
import json
import numpy as np


def index(request):
    product_list = Product.objects.all()[:3]
    template = loader.get_template('index.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))

def us(request):
    product_list = Product.objects.all()[:3]
    template = loader.get_template('us.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))

def contact(request):
    product_list = Product.objects.all()[:3]
    template = loader.get_template('contact.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))

def access(request):
    template = loader.get_template('access.html')
    context = {
        'Greetings': 'Bienvenido',
    }

    if request.user.is_authenticated():
        return HttpResponseRedirect('dashboard')

    return HttpResponse(template.render(context, request))

def log_in(request):

    username = ''
    password = ''

    try:
        username = request.POST['login']
        password = request.POST['password']
    except: 
        return HttpResponseRedirect('access')

    if username == '' or password == '':
        return render(request, 'access.html', {
            'error_message' : 'Ingrese el usuario y contraseña.',
        })
    else: 

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('dashboard')
        else:
            return render(request, 'access.html', {'error_message' : 'Usuario no registrado o contraseña incorrecto.',})

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})

@login_required
def products(request):
    product_list = Product.objects.all()
    template = loader.get_template('products.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_product(request):
      # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormAddProduct(request.POST)
        # check whether it's valid:
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return HttpResponseRedirect('/products')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormAddProduct()

    return render(request, 'add_product.html', {'form': form})

@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return HttpResponseRedirect('/products')

@login_required
def edit_product(request, id):

    product = Product.objects.get(id=id)

      # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormAddProduct(request.POST, instance = product)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/products')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormAddProduct(instance=product)

    return render(request, 'edit_product.html', {'form': form})

def our_products(request):
    product_list = Product.objects.all()
    template = loader.get_template('our_products.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))

def request_quote(request):

    number_products = len(Product.objects.filter(availability = True))

    FormsetRequestProductInQuote = formset_factory(FormRequestProductInQuote, extra=number_products)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormRequestQuote(request.POST)
        product_formset = FormsetRequestProductInQuote(request.POST)
        # check whether it's valid:
        if form.is_valid() and product_formset.is_valid():
            quote = form.save(commit=False)
            quote.request_date = datetime.today()
            quote.number       = get_quote_number()
            quote.save()
            for product_form in product_formset:
                if product_form.is_valid() and product_form.has_changed():
                    product = product_form.save(commit=False)
                    product.quote = quote
                    product.save()

            # Send email to user
            successfully_sent_quote(quote.id)

            return HttpResponseRedirect('/quotes/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormRequestQuote()
        product_formset = FormsetRequestProductInQuote()

    return render(request, 'request_quote.html', {'form': form, 'product_formset' : product_formset })


def quote_thanks(request):
    return render(request, 'request_thanks.html', {})


@login_required
def quotes(request):
    quote_list = Quote.objects.all()
    template = loader.get_template('quotes.html')
    context = {
        'quote_list': quote_list,
    }
    return HttpResponse(template.render(context, request))

@login_required
def edit_quote(request, id):

    quote    = Quote.objects.get(id = id)
    products = ProductInQuote.objects.filter(quote=quote)

    initial_products = []
    for product in products:
        initial_products.append(
            {"product" : product.product, "quantity" : product.quantity,
             "price_p_u" :product.price_p_u,"total_price" : product.total_price}
            )

    number_products = len(products)
    FormsetEditProductInQuote = formset_factory(FormEditProductInQuote, max_num = number_products)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        print('HIEE')
        # create a form instance and populate it with data from the request:
        form = FormEditQuote(request.POST, instance = quote)
        product_formset = FormsetEditProductInQuote(request.POST, initial=initial_products)
        # check whether it's valid:
        if form.is_valid() and product_formset.is_valid():

            print('HIEE2')
            quote = form.save(commit=False)
            quote.answer_date = datetime.today()
            quote.save()
            for product_form in product_formset:
                if product_form.is_valid() and product_form.has_changed():
                    product = product_form.cleaned_data.get('product', product_form.initial['product'])
                    quantity = product_form.cleaned_data.get('quantity', product_form.initial['quantity'])
                    price_p_u = product_form.cleaned_data.get('price_p_u', product_form.initial['price_p_u'])
                    total_price = product_form.cleaned_data.get('total_price', product_form.initial['total_price'])

                    prod_obj = ProductInQuote.objects.get(product = product, quote = quote)
                    prod_obj.quantity = quantity
                    prod_obj.price_p_u = price_p_u
                    prod_obj.total_price = total_price
                    prod_obj.save()

            return HttpResponseRedirect('/quotes/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormEditQuote(instance = quote)
        product_formset = FormsetEditProductInQuote(initial = initial_products)

    return render(request, 'edit_quote.html', {'form': form, 'product_formset' : product_formset, 'number_products' : number_products })

@login_required
def cancel_quote(request, id):
    quote    = Quote.objects.get(id = id)
    quote.status = 'C'
    quote.save()
    return HttpResponseRedirect('/quotes/')

@login_required
def send_quote(request, id):
    quote    = Quote.objects.get(id = id)
    quote.status = 'A'
    quote.save()
    return HttpResponseRedirect('/quotes/')

def consult(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
         # create a form instance and populate it with data from the request:
        form = FormConsult(request.POST)
        # check whether it's valid:
        if form.is_valid():
            number = form.cleaned_data.get('number','')
            quote = Quote.objects.filter(number = number)
            if quote.exists():
                quote = quote[0]
                return HttpResponseRedirect('/consult/%i/'%(quote.id))
            else:
                template = loader.get_template('consult.html')
                context = {
                    'Greetings': 'Bienvenido',
                    'form' : form,
                    'error_message' : 'No existe cotización/pedido con el número ingresado.'
                }
                return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('consult.html')
        form = FormConsult()
        context = {
            'Greetings': 'Bienvenido',
            'form' : form
        }
    return HttpResponse(template.render(context, request))

def download(request, file_name):
    file_path = settings.MEDIA_ROOT + '/' + file_name
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response

def view_consult(request, id):

    # Loading quote and products
    quote = Quote.objects.get(id = id)
    products = ProductInQuote.objects.filter(quote = quote)

    # Loading Purchase Order (if any)
    po_file = PurchaseOrder.objects.filter(quote = quote)
    if po_file.exists():
        po_file = po_file[0]
        has_po  = True
    else:
        po_file = FormAddPurchaseOrder(prefix='PO')
        has_po  = False

    payments   = PaymentType.objects.filter(enabled=True)

    # Loading Purchase invoice (if any)
    invoice = Invoice.objects.filter(quote = quote)
    if invoice.exists():
        invoice = invoice[0]
        has_in  = True

    else:
        invoice  = None
        has_in   = False

    vouchers   = Payment.objects.filter(quote=quote)
    if vouchers.exists():
        has_vouchers = True
    else:
        has_vouchers = False

    form_vo = FormPayment(prefix='VO')

    # Proccessing forms
    if request.method == 'POST':
        if 'PO' in request.POST:
            form = FormAddPurchaseOrder(request.POST, request.FILES, prefix='PO')
            if form.is_valid():
                file_ob = form.save()
                file_ob.quote = quote
                file_ob.save()
                quote.status ='E'
                quote.save()
        if 'VO' in request.POST:
            form = FormPayment(request.POST, request.FILES, prefix='VO')
            if form.is_valid():
                file_ob = form.save()
                file_ob.quote = quote
                file_ob.save()

        return HttpResponseRedirect('/consult/%i/'%(quote.id))

    # Returning Template

    template = loader.get_template('view_consult.html')
    context = {
        'Greetings': 'Bienvenido',
        'quote' : quote,
        'products' : products,
        'form_po'  : po_file,
        'has_po'   : has_po,
        'invoice'  : invoice,
        'has_in'   : has_in,
        'has_vouchers' : has_vouchers,
        'vouchers' : vouchers,
        'payments' : payments,
        'form_vo'  : form_vo
    }
    return HttpResponse(template.render(context, request))

@login_required
def payment_orders(request):
    paymentorders = PurchaseOrder.objects.filter(quote__status = 'E') 
    template = loader.get_template('paymentorders.html')
    context  = {
        'Greetings': 'Bienvenido',
        'po_list'  : paymentorders
    }
    return HttpResponse(template.render(context, request))

@login_required
def invoices(request):
    invoices = Invoice.objects.all().exclude(status='B') 
    template = loader.get_template('invoices.html')
    context = {
        'Greetings': 'Bienvenido',
        'in_list'  :  invoices
    }
    return HttpResponse(template.render(context, request))

@login_required
def create_invoice(request, id):

    invoice = Invoice.objects.filter(quote = id)

    if invoice.exists():
        invoice = invoice[0]
    else:
        quote   = Quote.objects.get(id=id)
        if quote.company != '':
            business_name = quote.company
        else:
            business_name = quote.contact

        invoice = Invoice.objects.create(quote = quote, 
                                         number = get_invoice_number(), 
                                         business_name = business_name,
                                         address = quote.address,
                                         phone = quote.phone)
    
    return HttpResponseRedirect('/invoices/edit/%i/'%(invoice.id))

@login_required
def edit_invoice(request, id):
    invoice    = Invoice.objects.get(id = id)
    products   = ProductInInvoice.objects.filter(invoice=invoice)
    productinq = ProductInQuote.objects.filter(quote=invoice.quote)

    initial_products = []
    for product in products:
        initial_products.append(
            {"product" : product.product,
             "quantity" : product.quantity, 
             "price_p_u" :product.price_p_u,
             "total_price" : product.total_price}
            )

    number_products = len(productinq) + 2
    FormsetEditProductInInvoice = formset_factory(FormEditProductInInvoice, extra = number_products, max_num = number_products)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormInvoice(request.POST, instance = invoice)
        product_formset = FormsetEditProductInInvoice(request.POST, initial=initial_products)
        # check whether it's valid:
        if form.is_valid() and product_formset.is_valid():
            pass

            invoice = form.save(commit=False)
            invoice.save()

            for product_form in product_formset:
                if product_form.is_valid() and product_form.has_changed():

                    product = product_form.cleaned_data.get('product', '')
                    quantity = product_form.cleaned_data.get('quantity', '')
                    price_p_u = product_form.cleaned_data.get('price_p_u', '')
                    total_price = product_form.cleaned_data.get('total_price', '')
                    code = product_form.cleaned_data.get('code', '')
                    order_number = product_form.cleaned_data.get('order_number', '')

                    prod_obj = ProductInInvoice.objects.filter(invoice=invoice, product=product, order_number=order_number)
                    if prod_obj.exists():
                        prod_obj = prod_obj[0]
                        prod_obj.quantity = quantity
                        prod_obj.price_p_u = price_p_u
                        prod_obj.total_price = total_price
                        prod_obj.code = code
                        prod_obj.order_number = order_number
                        prod_obj.save()
                    else:
                        ProductInInvoice.objects.create(
                            invoice=invoice, 
                            product=product, 
                            order_number=order_number,
                            quantity = quantity,
                            price_p_u = price_p_u,
                            total_price = total_price,
                            code = code
                            )

            return HttpResponseRedirect('/paymentorders/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormInvoice(instance = invoice)
        product_formset = FormsetEditProductInInvoice(initial = initial_products)

    return render(request, 'edit_invoice.html', {'form': form, 'invoice' : invoice, 'product_formset' : product_formset, 'number_products' : number_products})

@login_required
def cancel_invoice(request, id):
    invoice    = Invoice.objects.get(id = id)
    invoice.status = 'C'
    invoice.save()
    return HttpResponseRedirect('/invoices/')
    
@login_required
def send_invoice(request, id):
    quote        = Quote.objects.get(id = id)
    quote.status = 'T'
    quote.save()

    invoice        = Invoice.objects.get(quote = quote)
    invoice.status = 'Pa'
    invoice.save()
    invoice_sent(invoice.id)
    return HttpResponseRedirect('/invoices/')

def view_invoice(request, id):
    invoice    = Invoice.objects.get(id = id)
    template = loader.get_template('view_invoice.html')
    products = ProductInInvoice.objects.filter(invoice=invoice)
    context  = {
        'invoice'  :  invoice,
        'products' : products
    }
    return HttpResponse(template.render(context, request))

@login_required 
def view_payments(request, id):
    vouchers = Payment.objects.filter(quote=id)
    template = loader.get_template('view_vouchers.html')
    context  = {
        'vouchers'  :  vouchers
    }
    return HttpResponse(template.render(context, request))

@login_required
def payment_types(request):
    payment_types_list = PaymentType.objects.all() 
    template = loader.get_template('payment_types.html')
    context  = {
        'Greetings': 'Bienvenido',
        'payment_types_list'  : payment_types_list
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_payment_type(request):
      # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormPaymentType(request.POST)
        # check whether it's valid:
        if form.is_valid():
            payment_type = form.save(commit=False)
            payment_type.save()
            return HttpResponseRedirect('/paymenttypes')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormPaymentType()

    return render(request, 'add_payment_type.html', {'form': form})

@login_required
def edit_payment_type(request, id):

    payment_type = PaymentType.objects.get(id=id)

      # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormPaymentType(request.POST, instance = payment_type)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/paymenttypes')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormPaymentType(instance=payment_type)

    return render(request, 'edit_payment_type.html', {'form': form})

@login_required
def reports(request):
    template = loader.get_template('reports.html')

    # Cotizaciones Por Mes
    today = datetime.today()

    initial_date = date(today.year, today.month, 1)

    date_lists = [initial_date]

    for i in range(11):
        alter_date = date_lists[0] - timedelta(days=1)
        alter_date = date(alter_date.year, alter_date.month, 1)
        date_lists = [alter_date] + date_lists


    quote_data = []

    # Getting queries for quotes betweetn dates
    for i in range(len(date_lists)):
        if i != len(date_lists) - 1:
            count = Quote.objects.filter(request_date__range=[date_lists[i], date_lists[i+1]]).count()
            quote_data.append([str(calendar.month_abbr[date_lists[i].month]) + ' ' + str(date_lists[i].year), count])
        else:
            count = Quote.objects.filter(request_date__range=[date_lists[i], today]).count()
            quote_data.append([str(calendar.month_abbr[date_lists[i].month]) + ' ' + str(date_lists[i].year), count])

    invoice_data = []

    # Getting queries for quotes betweetn dates
    for i in range(len(date_lists)):
        if i != len(date_lists) - 1:
            count = Invoice.objects.filter(date__range=[date_lists[i], date_lists[i+1]], status='Pa').count()
            invoice_data.append([str(calendar.month_abbr[date_lists[i].month]) + ' ' + str(date_lists[i].year), count])
        else:
            count = Invoice.objects.filter(date__range=[date_lists[i], today], status='Pa').count()
            invoice_data.append([str(calendar.month_abbr[date_lists[i].month]) + ' ' + str(date_lists[i].year), count])

    incomes_data = []

    # Getting queries for quotes betweetn dates
    for i in range(len(date_lists)):
        if i != len(date_lists) - 1:
            count = Invoice.objects.filter(date__range=[date_lists[i], date_lists[i+1]], status='Pa').aggregate(Sum('total'))
            if count['total__sum']:
                count = count['total__sum']
            else:
                count = 0
            incomes_data.append([str(calendar.month_abbr[date_lists[i].month]) + ' ' + str(date_lists[i].year), count])
        else:
            count = Invoice.objects.filter(date__range=[date_lists[i], today], status='Pa').aggregate(Sum('total'))
            if count['total__sum']:
                count = count['total__sum']
            else:
                count = 0
            incomes_data.append([str(calendar.month_abbr[date_lists[i].month]) + ' ' + str(date_lists[i].year), count])

    products_data = []
    products = Product.objects.all()
    for product in products:
        product_data = []
        for i in range(len(date_lists)):
            if i != len(date_lists) - 1:
                count = ProductInInvoice.objects.filter(product = product, invoice__status='Pa', invoice__date__range=[date_lists[i], date_lists[i+1]]).aggregate(Sum('quantity'))
                if count['quantity__sum']:
                    count = count['quantity__sum']
                else:
                    count = 0
                product_data.append(count)
            else:
                count = ProductInInvoice.objects.filter(product = product, invoice__status='Pa', invoice__date__range=[date_lists[i], today]).aggregate(Sum('quantity'))
                if count['quantity__sum']:
                    count = count['quantity__sum']
                else:
                    count = 0
                product_data.append(count)

        products_data.append([product.name, product_data])

    sum_products_data = []
    for data in products_data:
        sum_products_data.append([data[0], np.sum(data[1])])

    context = {
        'Greetings'  : 'Bienvenido',
        'quote_data' : quote_data,
        'json_quote_data' : json.dumps(quote_data),
        'invoice_data' : invoice_data,
        'json_invoice_data' : json.dumps(invoice_data),
        'incomes_data' : incomes_data,
        'json_incomes_data' : json.dumps(incomes_data),
        'products_data' : products_data,
        'json_products_data' : json.dumps(sum_products_data)
    }
    return HttpResponse(template.render(context, request))