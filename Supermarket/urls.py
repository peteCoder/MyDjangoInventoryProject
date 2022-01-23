from os import name
from django.urls import path
from Supermarket.views import  *

app_name = 'super'

urlpatterns = [
	path('dashboard/', dashboard, name='dashboard'),
	path('inventory/', inventory, name='inventory'),
	path('product-list/', product_list, name='product-list'),
	path('product-delete/<int:product_id>/', delete_product, name='product-delete'),
	path('product-detail/<int:product_id>/', product_detail, name='product-detail'),
	path('product-edit/<int:product_id>/', product_edit, name='product-edit'),


	path('add-supplier/', add_supplier_view, name='add-supplier'),
	path('delete-supplier/<int:pk>/', delete_supplier, name='delete-supplier'),
	path('add-customer/', add_customer_view, name='add-customer'),
	path('delete-customer/<int:pk>/', delete_customer, name='delete-customer'),

	# Supplier and Customer detail and edit views
	path('customer-detail/<int:pk>/', customer_detail_view, name='customer-detail'),
	path('customer-edit/<int:pk>/', customer_edit, name='customer-edit'),
	path('supplier-detail/<int:pk>/', supplier_detail_view, name='supplier-detail'),
	path('supplier-edit/<int:pk>/', supplier_edit, name='supplier-edit'),


	path('category-list/', category_list_view, name='category-list'),
	path('category-list/<int:pk>/delete/', delete_category_list_view, name='category-delete'),

	path('type-list/', type_list_view, name='type-list'),
	path('type-list/<int:pk>/delete/', delete_type_list_view, name='type-delete'),



	path('point-of-sales/', make_sales_view, name='pos'),
	path('point-of-sales-for-wholesale/', make_sales_view_wholesale, name='wholesale_pos'),
	path('delete-sale/<int:pk>/', delete_sales, name='delete-sale'),
	path('sales-list/', sales_list, name='sales'),
	path('expired-list/', expired_list_view, name='expired-list'),



	path('receiving/', receiving_view, name='receiving'),
	path('procurement-list/', procurement_list, name='procurement'),
	path('delete-purchase/<int:pk>/', delete_procurement_list, name='delete-purchase'),

	path('transaction-history/', transaction_list, name='transaction'),

	path('edit-category/<int:pk>/', edit_category_view, name='edit_category_view'),
	path('edit-type/<int:pk>/', edit_type_view, name='edit_type_view'),
	path('delete_expired_stock/<int:id>/', delete_expired_stock, name='delete_expired_stock'),



]
