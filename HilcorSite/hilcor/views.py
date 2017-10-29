# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.shortcuts    import render
from django.http         import HttpResponse, HttpResponseRedirect
from django.template     import loader
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from .models import *
from .forms import *
from datetime import datetime

# Create your views here.
def index(request):
    product_list = Product.objects.all()[:3]
    template = loader.get_template('index.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))


def access(request):
    template = loader.get_template('access.html')
    context = {
        'Greetings': 'Holaddewwfefw',
    }
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
            quote.save()
            for product_form in product_formset:
                product = product_form.save(commit=False)
                product.quote = quote
                product.save()

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
                product.save()

            return HttpResponseRedirect('/quotes/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormEditQuote(instance = quote)
        product_formset = FormsetEditProductInQuote(initial = initial_products)

    return render(request, 'edit_quote.html', {'form': form, 'product_formset' : product_formset })

