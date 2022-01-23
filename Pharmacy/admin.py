from django.contrib import admin
from Pharmacy.models import *
from Pharmacy.forms import *

# Register your models here.


class PharmaceuticalsAdmin(admin.ModelAdmin):
	list_display = ['product_name', 'product_category', 'quantity_available']
	# form = AddProductForm

class SalesAdmin(admin.ModelAdmin):
	list_display = ['product', 'date', 'quantity_sold', 'customer']
	form = SalesForm

admin.site.register(Pharmaceuticals, PharmaceuticalsAdmin)
admin.site.register(PharmaceuticalCategory)
admin.site.register(PharmaceuticalType)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Sales, SalesAdmin)
admin.site.register(SalesList)
admin.site.register(Transactions)

admin.site.register(ProcurementList)
admin.site.register(Procurement)






