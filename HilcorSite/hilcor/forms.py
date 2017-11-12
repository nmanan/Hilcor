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
	product = forms.ModelChoiceField(queryset=Product.objects.filter(availability = True))

	class Meta:
		model  = ProductInQuote
		fields = ("product", "quantity", "measure")

class FormEditQuote(forms.ModelForm):
	class Meta:
		model = Quote
		fields = ("number", "company", "address", "contact", "phone", "email","subtotal" ,"iva" ,"total_iva" ,"total" ,"comment", "status")

class FormEditProductInQuote(forms.ModelForm):
	product = forms.ModelChoiceField(queryset=Product.objects.filter(availability = True))

	class Meta:
		model  = ProductInQuote
		fields = ("product", "quantity", "measure", "price_p_u","total_price")

class FormConsult(forms.Form):
	number = forms.CharField(label='Número', max_length=12)

class FormAddPurchaseOrder(forms.ModelForm):
	class Meta:
		model = PurchaseOrder
		fields = ("po_file",)
