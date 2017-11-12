from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^us$', views.us, name='us'),
	url(r'^contact$', views.contact, name='contact'),
	# url(r'^contact/thanks/$', views.contact, name='contact'),	
	url(r'^our_products$', views.our_products, name='our_products'),
	url(r'^access$', views.access, name='access'),
	url(r'^login$', views.log_in, name='login'),
	url(r'^logout$', views.log_out, name='logout'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^products$', views.products, name='products'),
	url(r'^products/add/$', views.add_product, name='add_product'),
	url(r'^products/edit/(?P<id>[0-9]+)/$', views.edit_product, name='edit_product'),
	url(r'^products/delete/(?P<id>[0-9]+)/$', views.delete_product, name='delete_product'),
	url(r'^quotes/$', views.quotes, name='quotes'),
	url(r'^quotes/request/$', views.request_quote, name='request_quote'),
	url(r'^quotes/edit/(?P<id>[0-9]+)/$', views.edit_quote, name='edit_quote'),
	url(r'^quotes/cancel/(?P<id>[0-9]+)/$', views.cancel_quote, name='cancel_quote'),
	url(r'^quotes/send/(?P<id>[0-9]+)/$', views.send_quote, name='send_quote'),
	url(r'^quotes/thanks/$', views.quote_thanks, name='quote_thanks'),
	url(r'^consult$', views.consult, name='consult'),
	url(r'^consult/(?P<id>[0-9]+)/$', views.view_consult, name='view_consult'),
	url(r'^paymentorders/$', views.payment_orders, name='payment_orders'),
	url(r'^invoices/$', views.invoices, name='invoices'),
	url(r'^reports/$', views.reports, name='reports'),
	url(r'^download/(?P<file_name>.+)$', views.download, name='download'),
]