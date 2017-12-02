# -*- coding: utf-8 -*-
from django  import forms
from .models import *


class FormAddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description','availability',)

class FormRequestQuote(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ("company", "address", "contact", "phone", "email")

class FormRequestProductInQuote(forms.ModelForm):
    product = forms.ModelChoiceField(queryset = Product.objects.filter(availability = True))


    def __init__(self, *args, **kwargs):
        super(FormRequestProductInQuote, self).__init__(*args, **kwargs)
        self.fields['product'].required = True
        self.fields['quantity'].required = True 


    class Meta:
        model  = ProductInQuote
        fields = ("product", "quantity",)

class FormEditQuote(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormEditQuote, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['readonly'] = True
        self.fields['company'].widget.attrs['readonly'] = True
        self.fields['address'].widget.attrs['readonly'] = True
        self.fields['contact'].widget.attrs['readonly'] = True
        self.fields['phone'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = Quote
        fields = ("number", "company", "address", "contact", "phone", "email", "total" ,"comment", "status")

class FormEditProductInQuote(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(availability = True))

    def __init__(self, *args, **kwargs):
        super(FormEditProductInQuote, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True 

    class Meta:
        model  = ProductInQuote
        fields = ("product", "quantity", "price_p_u", "total_price")

class FormConsult(forms.Form):
    number = forms.CharField(label='Número', max_length=12)

class FormAddPurchaseOrder(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ("po_file",)

class FormInvoice(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormInvoice, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['readonly'] = True
        
    class Meta:
        model = Invoice
        fields = ("number", "business_name", "address", "rif", "phone", "subtotal" ,"iva" ,"total_iva" ,"total", "status", 'comment')

class FormEditProductInInvoice(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(availability = True))

    def __init__(self, *args, **kwargs):
        super(FormEditProductInInvoice, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True 

    class Meta:
        model  = ProductInInvoice 
        fields = ("product", "quantity", "code", "order_number","price_p_u", "total_price")

class FormPaymentType(forms.ModelForm):
    class Meta:
        model  = PaymentType
        fields = ("bank", "acc_type", "account", "check", "transfer","deposit", "acc_name", "enabled")

class FormPayment(forms.ModelForm):

    class Meta:
        model  = Payment
        fields = ("PaymentType", "method", "voucher")