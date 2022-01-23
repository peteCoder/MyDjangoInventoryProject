from django.contrib import admin
from Supermarket.models import *
from Supermarket.forms import *

# Register your models here.


class ProductsAdmin(admin.ModelAdmin):
	list_display = ['product_name', 'product_category', 'quantity_available']
	# form = AddProductForm

class SalesAdmin(admin.ModelAdmin):
	list_display = ['product', 'date', 'quantity_sold', 'customer']
	form = SalesForm

admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductType)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Sales, SalesAdmin)
admin.site.register(SalesList)
admin.site.register(Transactions)

admin.site.register(ProcurementList)
admin.site.register(Procurement)