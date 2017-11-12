# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.shortcuts    import render
from django.http         import HttpResponse, HttpResponseRedirect
from django.template     import loader
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from hilcor.models import *
from hilcor.forms  import *
from hilcor.utils  import *
from datetime      import datetime

# Create your views here.
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

    FormsetRequestProductInQuote = formset_factory(FormRequestProductInQuote, extra= number_products)

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
            {"product" : product.product, "quantity" : product.quantity, "measure" :product.measure, 
             "price_p_u" :product.price_p_u,"total_price" : product.total_price}
            )

    number_products = len(products)
    print(number_products)
    FormsetEditProductInQuote = formset_factory(FormEditProductInQuote, max_num = number_products)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormEditQuote(request.POST, instance = quote)
        product_formset = FormsetEditProductInQuote(request.POST, initial=initial_products)
        # check whether it's valid:
        if form.is_valid() and product_formset.is_valid():

            quote = form.save(commit=False)
            quote.answer_date = datetime.today()
            quote.save()
            for product_form in product_formset:

                product = product_form.cleaned_data.get('product', product_form.initial['product'])
                quantity = product_form.cleaned_data.get('quantity', product_form.initial['quantity'])
                measure = product_form.cleaned_data.get('measure', product_form.initial['measure'])
                price_p_u = product_form.cleaned_data.get('price_p_u', product_form.initial['price_p_u'])
                total_price = product_form.cleaned_data.get('total_price', product_form.initial['total_price'])

                prod_obj = ProductInQuote.objects.get(product = product, quote = quote)
                prod_obj.quantity = quantity
                prod_obj.measure = measure
                prod_obj.price_p_u = price_p_u
                prod_obj.total_price = total_price
                prod_obj.save()

            return HttpResponseRedirect('/quotes/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormEditQuote(instance = quote)
        product_formset = FormsetEditProductInQuote(initial = initial_products)

    return render(request, 'edit_quote.html', {'form': form, 'product_formset' : product_formset })

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
    quote = Quote.objects.get(id = id)
    products = ProductInQuote.objects.filter(quote = quote)

    if request.method == 'POST':
        form = FormAddPurchaseOrder(request.POST, request.FILES)
        if form.is_valid():
            file_ob = form.save()
            file_ob.quote = quote
            file_ob.save()

    po_file = PurchaseOrder.objects.filter(quote = quote)
    if po_file.exists():
        po_file = po_file[0]
        has_po  = True
    else:
        po_file = FormAddPurchaseOrder()
        has_po  = False


    template = loader.get_template('view_consult.html')
    context = {
        'Greetings': 'Bienvenido',
        'quote' : quote,
        'products' : products,
        'form_po'  : po_file,
        'has_po'   : has_po,
    }
    return HttpResponse(template.render(context, request))

@login_required
def payment_orders(request):
    paymentorders = PurchaseOrder.objects.filter(quote__status = 'A') 
    template = loader.get_template('paymentorders.html')
    context  = {
        'Greetings': 'Bienvenido',
        'po_list'  : paymentorders
    }
    return HttpResponse(template.render(context, request))

@login_required
def invoices(request):

    template = loader.get_template('invoices.html')
    context = {
        'Greetings': 'Bienvenido',
    }
    return HttpResponse(template.render(context, request))
    
@login_required
def reports(request):
    template = loader.get_template('reports.html')
    context = {
        'Greetings': 'Bienvenido',
    }
    return HttpResponse(template.render(context, request))
