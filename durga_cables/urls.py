from django.conf.urls import *
# from django.contrib import admin

urlpatterns = patterns('durga_cables.views',
    # Examples:
    # url(r'^$', 'listCustomers'),
    url(r'^$', 'home'),
    url('^addNewCustomer/$', 'addNewCustomer'),
    url('^customer/(?P<c_id>.+?)/', 'viewCustomer'),
    url('^customers/', 'listCustomers'),
    url('^updateCustomer/(?P<c_id>.+?)/', 'updateCustomer'),
    url('^deleteCustomer/(?P<c_id>.+?)/', 'deleteCustomer'),
    url('^addPayment/(?P<c_id>.+?)/', 'addPayment'),
    url('^addBulkPayment/(?P<c_id>.+?)/', 'addBulkPayment'),
    # url('^autoMapProducts/$', 'autoMapProducts'),
)
