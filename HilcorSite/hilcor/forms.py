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
        self.fields['product'].label = "Producto *"    
        self.fields['product'].empty_label = "Seleccione..."    


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
        self.fields['total'].widget.attrs['readonly'] = True


    class Meta:
        model = Quote
        fields = ("number", "company", "address", "contact", "phone", "email", "total" ,"comment", "status")

class FormEditProductInQuote(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(availability = True))

    def __init__(self, *args, **kwargs):
        super(FormEditProductInQuote, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True 
        self.fields['product'].label = "Producto *"    
        self.fields['product'].empty_label = "Seleccione..." 
        self.fields['product'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['quantity'].widget.attrs['onkeyup']  = "update_prize_q(this);"  
        self.fields['price_p_u'].widget.attrs['onkeyup']  = "update_prize_ppu(this);"    

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
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['total_iva'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['iva'].widget.attrs['onkeyup']  = "update_iva(this);"
        
    class Meta:
        model = Invoice
        fields = ("number", "business_name", "address", "rif", "phone", "subtotal" ,"iva" ,"total_iva" ,"total", "status", 'comment','deliver_date')
        widgets = {
            'deliver_date': forms.DateInput(attrs={'class':'datepicker'}),
        }

class FormEditProductInInvoice(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(availability = True))

    def __init__(self, *args, **kwargs):
        super(FormEditProductInInvoice, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True 
        self.fields['product'].label = "Producto *"   
        self.fields['product'].empty_label = "Seleccione..."         
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['quantity'].widget.attrs['onkeyup']  = "update_prize_q(this);"  
        self.fields['price_p_u'].widget.attrs['onkeyup'] = "update_prize_ppu(this);"   

    class Meta:
        model  = ProductInInvoice 
        fields = ("product", "quantity", "code", "order_number","price_p_u", "total_price")

class FormPaymentType(forms.ModelForm):
    class Meta:
        model  = PaymentType
        fields = ("bank", "acc_type", "account", "check", "transfer","deposit", "acc_name", "enabled")

class FormPayment(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormPayment, self).__init__(*args, **kwargs)
        self.fields['PaymentType'].label = "Método de Pago *"
        self.fields['PaymentType'].empty_label = "Seleccione..."    

    class Meta:
        model  = Payment
        fields = ("PaymentType", "method", "voucher")