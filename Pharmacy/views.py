from django.shortcuts import render,  get_object_or_404
from django.contrib.auth.decorators import  login_required, user_passes_test
from Pharmacy.models import Pharmaceuticals as Drugs
from Pharmacy.models import PharmaceuticalCategory as DrugCategory
from Pharmacy.models import PharmaceuticalType as DrugType
from Pharmacy.models import Supplier, Sales, SalesList, Transactions
from Pharmacy.models import *
from Pharmacy.forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Count
import csv
from django.http import HttpResponse
import datetime
from notification.models import PharmacyNotification
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.conf import settings
import os
from .bootstrap import boots

# Create your views here.

def user_is_manager(user):
	return user.profile.position == 'manager'

def user_is_cashier(user):
	return user.profile.position == 'cashier'



@login_required
def dashboard(request):

	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	today = datetime.date.today()

	total_daily_purchase = 0
	total_daily_sales = 0
	yesterday_purchase_total = 0
	yesterday_sales_total = 0

	daily_procurement = Transactions.objects.filter(date=datetime.date.today()).all()
	yesterday_purchase = Transactions.objects.filter(date=yesterday).all()	

	for transaction in daily_procurement:
		if transaction.transaction_type == 'Purchase':
			total_daily_purchase += transaction.amount_received
		elif transaction.transaction_type == 'Sales':
			total_daily_sales += transaction.amount_received

	for transaction in yesterday_purchase:
		if transaction.transaction_type == 'Purchase':
			yesterday_purchase_total += transaction.amount_received
		elif transaction.transaction_type == 'Sales':
			yesterday_sales_total += transaction.amount_received


	user = request.user
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]


	today_transactions = Transactions.objects.all().filter(
		date__exact=today
	).count()

	yesterday_transactions = Transactions.objects.all().filter(
		date__exact=yesterday
	).count()

	# all_transactions = Transactions.objects.all().count()
	all_transactions_for_yesterday_and_today = Transactions.objects.filter(date__range=[yesterday, today]).all().count()

	all_drugs = Drugs.objects.all().order_by('-ordered_date')

	_past_5_days = datetime.date.today() - datetime.timedelta(days=5)
	_5_days_from_now = datetime.date.today() + datetime.timedelta(days=5)

	
	drugs = ProcurementList.objects.filter(expiry_date__range=[_past_5_days, _5_days_from_now]).all()


	# drugs = Drugs.objects.filter(expiry_date__range=[_past_5_days, _5_days_from_now]).all()
	drug_out_of_stock = Drugs.objects.filter(quantity_available__lte=10)[:10]


	if drugs.count() == 0:
		for notify_obj in PharmacyNotification.objects.filter(notification_type=1).all():
			notify_obj.delete()

			
	if drug_out_of_stock.count() == 0:
		for notify_obj in PharmacyNotification.objects.filter(notification_type=2).all():
			notify_obj.delete()


	if all_drugs:
		for i in range(0, len(all_drugs)):
			if all_drugs[i].quantity_available > 10:
				notify = PharmacyNotification.objects.filter(
					drug=all_drugs[i], 
					notification_type=2,
				).all()
				notify.delete()

			elif all_drugs[i].quantity_available <= 10:
				if i > len(all_drugs):
					break
				notify = PharmacyNotification(
					drug=all_drugs[i], 
					notification_type=2,
					text_preview=f"Out of Stock alert for: {all_drugs[i].product_name}"					
				)
				notify.save()
	if drugs:
		for i in range(0, len(drugs)):
			if drugs[i].expiry_date > _past_5_days and drugs[i].expiry_date < _5_days_from_now:
				if i > len(drugs):
					break
				notify = PharmacyNotification(
					drug=drugs[i].product, 
					notification_type=1, 
					text_preview=f"Expiration alert for: {drugs[i].product_name}",
					date_of_action=drugs[i].expiry_date,
				)
				notify.save()
			elif drugs[i].expiry_date < _past_5_days or drugs[i].expiry_date > _5_days_from_now:
				notify = PharmacyNotification.objects.filter(
					drug=all_drugs[i], 
					notification_type=1,
				).all()
				notify.delete()

	context = {
		'user':user,
		'drugs': drugs,
		'drug_out_of_stock':drug_out_of_stock,
		'today_transactions':today_transactions,
		'all_transactions': all_transactions_for_yesterday_and_today, 
		'yesterday_transactions': yesterday_transactions,
		'notification_count':notification_count,
		'nav_notify': nav_notify,
		'total_daily_purchase': total_daily_purchase,
		'total_daily_sales': total_daily_sales,
		'yesterday_purchase_total': yesterday_purchase_total,
		'yesterday_sales_total': yesterday_sales_total
	}


	return render(request, 'Pharmacy/index.html', context)



def delete_expired_stock(request, id):
	product = get_object_or_404(ProcurementList, id=id)
	drug = Drugs.objects.get(product_name=product.product_name)
	drug.quantity_available -= product.quantity_ordered
	drug.save()
	product.delete()
	return redirect('phar:procurement')

@login_required
def expired_list_view(request):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	_5_days_ago = datetime.date.today() - datetime.timedelta(days=5)
	_5_days_after = datetime.date.today() + datetime.timedelta(days=5)
	drugs = ProcurementList.objects.filter(expiry_date__range=[_5_days_ago, _5_days_after]).all().order_by('-ordered_date')

	if request.method == 'POST' and 'PDFInventoryListButton' in request.POST:
		title = 'Expired Drugs Datatable'
		dir_ = os.path.join(settings.BASE_DIR, 'media')
		html_string = render_to_string('pdf/Pharmacy/expired_list_pdf.html', {'queryset': drugs, 'title': title})
		html = HTML(string=html_string)
		html.write_pdf(target=f'{dir_}/tmp/expired_list.pdf', stylesheets=[CSS(string=boots)])

		fs = FileSystemStorage(location=f'{dir_}/tmp')
		with fs.open('expired_list.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="expired_list.pdf"'
			return response

	if request.method == 'POST' and 'csvDownload' in request.POST:
		response = HttpResponse(content_type="text/csv")

		response['Content-Disposition'] = 'attachment; filename="ExpiredMedicine.csv"'
		writer = csv.writer(response)
		writer.writerow(['EXPIRED DRUGS'])
		writer.writerow([
			'PRODUCT NAME', 
			'PRODUCT CATEGORY', 
			'QUANTITY', 
			'EXPIRY DATE',
			'HAS EXPIRED',
			'COST PRICE', 
			'SALES PRICE' 
		])

		for drug in drugs:
			writer.writerow([
				drug.product_name, 
				drug.product.product_category.name,  
				drug.quantity_ordered,
				drug.expiry_date,
				drug.product_has_expired_already,
				drug.product.cost_price,
				drug.product.sales_price
			])

		return response

	context = {
		'drugs':drugs,
		'notification_count':notification_count,
		'nav_notify': nav_notify
	}
	return render(request, 'Pharmacy/expired_list.html', context)




@login_required
def product_list(request):
	user = request.user
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()

	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]

	drugs = Drugs.objects.all().order_by('-ordered_date')
	category = DrugCategory.objects.all().order_by('-ordered_date')
	product_type = DrugType.objects.all().order_by('-ordered_date')

	form_type = AddProductTypeForm()
	if request.method == 'POST' and 'typeBtn' in request.POST:
		form_type = AddProductTypeForm(request.POST)
		if form_type.is_valid():
			form_type.save()
			messages.success(request, 'Type Successfully Added')
			return redirect('phar:product-list')
		else:
			messages.error(request, 'Form Failed to Add Type. Check if type already exists. ')

	

	if request.method == 'POST' and 'pdfDownload' in request.POST:
		products = Drugs.objects.all()
		dir_ = os.path.join(settings.BASE_DIR, 'media')
		products = Drugs.objects.all().order_by('-ordered_date')
		html_string = render_to_string('pdf/Pharmacy/product_list.html', {'queryset': products})
		html = HTML(string=html_string)
		html.write_pdf(target=f'{dir_}/tmp/product_list.pdf', stylesheets=[CSS(string=boots)])

		fs = FileSystemStorage(location=f'{dir_}/tmp')
		with fs.open('product_list.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="product_list.pdf"'
			return response
		


	if request.method == 'POST' and 'csvDownload' in request.POST:
		response = HttpResponse(content_type="text/csv")
		response['Content-Disposition'] = 'attachment; filename="ListofMedicine.csv"'
		writer = csv.writer(response)
		writer.writerow([
			'PRODUCT NAME', 
			'PRODUCT ID', 
			'PRODUCT CATEGORY',
			'PRODUCT TYPE', 
			'QUANTY ON HAND', 
			'COST PRICE', 
			'SALES PRICE' 
		])

		instance = drugs
		for drug in instance:
			writer.writerow([
				drug.product_name, 
				drug.custom_id,
				drug.product_category.name, 
				drug.product_type.name, 
				drug.quantity_available,
				drug.cost_price,
				drug.sales_price
			])

		
		return response

	form_cat = AddCategoryForm()
	if request.method == 'POST' and 'catBtn' in request.POST:
		form_type = AddCategoryForm(request.POST)
		if form_type.is_valid():
			form_type.save()
			messages.success(request, 'Category Added Successfully')
			return redirect('phar:product-list')
		else:
			messages.error(request, 'Failed to add Category. Check if Category already exists. ')
	
	
	
	product_form = AddProductForm()
	if request.method == 'POST' and 'productBtn' in request.POST:
		form_type = AddProductForm(request.POST)
		if form_type.is_valid():
			form_type.save()
			messages.success(request, 'Product Added Successfully')
			return redirect('phar:product-list')
		else:
			messages.error(request, 'Failed to add Product. Product must have a unique name and ID. Check if name or Id already exists. If it does, edit Product instead. ')
	
	context = {
		'user':user,
		'drugs':drugs, 
		'form_cat': form_cat,
		'form_type': form_type,
		'product_form': product_form,
		'category':category,
		'product_type': product_type,
		'notification_count':notification_count,
		'nav_notify': nav_notify
	}
	return render(request, 'Pharmacy/product_list.html', context)


@login_required
def category_list_view(request):
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]

	categories = DrugCategory.objects.all().annotate(
		drug_count=Count('drug_cat')
	).order_by('-pk')

	if request.method == 'POST' and 'csvDownload' in request.POST:
		response = HttpResponse(content_type="text/csv")
		response['Content-Disposition'] = 'attachment; filename="Listofcategories.csv"'
		writer = csv.writer(response)
		writer.writerow(['CATEGORY', 'NUMBER OF PRODUCTS IN CATEGORY'])
		instance = categories
		for cat in instance:
			writer.writerow([
				cat.name,
				cat.drug_count
			])
		return response

	form_cat = AddCategoryForm()
	if request.method == 'POST' and 'catBtn' in request.POST:
		form_type = AddCategoryForm(request.POST)
		if form_type.is_valid():
			form_type.save()
			messages.success(request, 'Category Added Successfully')
			return redirect('phar:category-list')
		else:
			messages.error(request, 'Failed to add Category. Check if Category already exists. ')
	
	context = {
		'categories': categories, 
		'form_cat':form_cat,
		'notification_count':notification_count,
		'nav_notify': nav_notify
	}
	return render(request, 'Pharmacy/categories_list.html', context)





@login_required
def type_list_view(request):
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	product_types = DrugType.objects.all().annotate(
		type_count=Count('drug_type')
	).order_by('-pk')

	if request.method == 'POST' and 'csvDownload' in request.POST:
		response = HttpResponse(content_type="text/csv")
		response['Content-Disposition'] = 'attachment; filename="ListofTypes.csv"'
		writer = csv.writer(response)
		writer.writerow(['TYPE', 'NUMBER OF PRODUCTS IN TYPE'])
		instance = product_types
		for type_ in instance:
			writer.writerow([
				type_.name,
				type_.type_count
			])
		return response


	form_type = AddProductTypeForm()
	if request.method == 'POST' and 'typeBtn' in request.POST:
		form_type = AddProductTypeForm(request.POST)
		name = request.POST.get('name')
		if form_type.is_valid():
			form_type.save()
			messages.success(request, f'"{name}" Successfully Added')
			return redirect('phar:type-list')
		else:
			messages.error(request, f"Form Failed to Add Type. Check if '{name}' of Type already exists. ")


	context = {
		'product_types': product_types, 
		'form_type': form_type,
		'notification_count':notification_count,
		'nav_notify': nav_notify,
	}

	return render(request, 'Pharmacy/type.html', context)



# Modify the delete message further   
def delete_type_list_view(request, pk):
	product = DrugType.objects.get(pk=pk)
	product_name = product.name
	product.delete()
	messages.success(request, f"{product_name} was deleted successfully. ")
	return redirect('phar:type-list')


def delete_category_list_view(request, pk):
	product = DrugCategory.objects.get(pk=pk)
	product_name = product.name
	product.delete()
	messages.success(request, f"{product_name} was deleted successfully. ")
	return redirect('phar:category-list')


def delete_drugs(request, product_id):
	product = Drugs.objects.get(product_id=product_id)
	product_name = product.product_name
	procurements = ProcurementList.objects.filter(product_name=product_name)
	for procurement in procurements:
		procurement.delete()
	product.delete()
	messages.success(request, f"{product_name} was deleted successfully. ")

	return redirect('phar:product-list')


@login_required
@user_passes_test(user_is_manager)
def add_supplier_view(request):
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]

	suppliers = Supplier.objects.all().order_by('-pk')

	form = addSupplierForm()
	if request.method == 'POST':
		form = addSupplierForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Supplier was successfully saved. ")
			return redirect('phar:add-supplier')
		else:
			messages.success(request, "Data was not entered successfully. ")



	context = {
		'form': form,
		'suppliers': suppliers,
		'notification_count':notification_count, 
		'nav_notify': nav_notify
	}
	return render(request, 'Pharmacy/supplier.html', context)

def delete_supplier(request, pk):
	supplier = get_object_or_404(Supplier, pk=pk)
	supplier_name = supplier.name
	supplier.delete()
	messages.success(request, f"{supplier_name} was deleted successfully")
	return redirect('phar:add-supplier')


@login_required
@user_passes_test(user_is_manager)
def add_customer_view(request):
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]

	customers = Customer.objects.all().order_by('-pk')
	form = addCustomerForm()
	if request.method == "POST":
		form = addCustomerForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			form.save()
			messages.success(request, f"Customer {name} was successfully saved. ")
			return redirect('phar:add-customer')
		else:
			messages.success(request, "Data was not entered successfully. Check the errors below.")

	context = {
		'form': form, 
		'customers': customers,
		'notification_count':notification_count,
		'nav_notify': nav_notify
	}
	return render(request, 'Pharmacy/customer.html', context)


def delete_customer(request, pk):
	customer = get_object_or_404(Customer, pk=pk)
	customer.delete()
	messages.success(request, "Customer was deleted successfully")
	return redirect('phar:add-customer')



@login_required
def inventory(request):

	drugs = Drugs.objects.all().order_by('-ordered_date')
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]


	if request.method == 'POST' and 'PDFInventoryListButton' in request.POST:
		title = 'Inventory 	Datatable'
		dir_ = os.path.join(settings.BASE_DIR, 'media')
		html_string = render_to_string('pdf/Pharmacy/product_list.html', {'queryset': drugs, 'title': title})
		html = HTML(string=html_string)
		html.write_pdf(target=f'{dir_}/tmp/inventory_list.pdf', stylesheets=[CSS(string=boots)])

		fs = FileSystemStorage(location=f'{dir_}/tmp')
		with fs.open('inventory_list.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="inventory_list.pdf"'
			return response

	if request.method == "POST" and "csvDownload" in request.POST:
		response = HttpResponse(content_type="text/csv")
		response['Content-Disposition'] = 'attachment; filename="InventoryData.csv"'
		writer = csv.writer(response)
		writer.writerow(["INVENTORY DATA TABLE"])
		writer.writerow([
			'PRODUCT NAME', 
			'ID', 
			'CATEGORY', 
			'QUANTITY',  
			'COST PRICE', 
			'SALES PRICE',
			'LOW STOCK'
			])
		for drug in drugs:
			writer.writerow([
				drug.product_name,
				drug.custom_id,
				drug.product_category.name,
				drug.quantity_available,	
				drug.cost_price,
				drug.sales_price,
				drug.is_low_in_stock
			])

		messages.success(request, "Data successfully exported to CSV ")

		return response

	context = {
		'drugs': drugs,
		'nav_notify':nav_notify, 
		'notification_count':notification_count
	}
	return render(request, 'Pharmacy/inventory.html', context)





@login_required
def make_sales_view_wholesale(request):
	sales = Sales.objects.all()
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]

	get_total_quantity = Sales.get_total_quantity()
	
	get_total = Sales.get_total()

	form = SalesForm()
	if request.method == "POST" and "addToList" in request.POST:
		form = SalesForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Form was submitted successfully")
			return redirect('phar:wholesale_pos')
		messages.error(request, "There was problem submitting the form")

	if request.method == "POST" and "finalSubmit" in request.POST:
		Transactions.objects.create(
			total_amount=int(request.POST['total_amount']), 
			amount_tendered=int(request.POST['amount_tendered']), 
			discount=int(request.POST['discount']),
			amount_received=int(request.POST['amount_received']),
			change=int(request.POST['change_given']), 
			transaction_type="Sales"
		)
		for sale in sales:
			SalesList.objects.create(
				product_name=sale.product.product_name,
				price=sale.product.product.sales_price,
				sales_ref=sale.sales_ref,  
				customer= sale.customer.name,
				quantity_sold=sale.quantity_sold,
				total=sale.individual_total,
				sales_type='Wholesale'
			)

			procurement = ProcurementList.objects.get(
				product_name=sale.product.product_name,
				purchase_ref=sale.sales_ref
			)
			if procurement.purchase_ref == sale.sales_ref:
				procurement.quantity_ordered -= sale.quantity_sold
				procurement.save()

			product = Pharmaceuticals.objects.get(product_name=sale.product.product_name)
			product.quantity_available -= sale.quantity_sold
			product.save()


			zero_q_procurement = ProcurementList.objects.filter(quantity_ordered=0)
			if zero_q_procurement:
				for zero_q in zero_q_procurement:
					zero_q.delete()
			sale.delete()

			transactions = Transactions.objects.filter(
				total_amount=0, 
				amount_tendered=0, 
				change=0, 
				discount=0, 
				amount_received=0
			)
			if transactions:
				messages.error(request, "Zero  Transaction Operation was automatically cleaned out. ")
				for transaction in transactions:
					if transaction:
						transaction.delete()


		return redirect('phar:sales')

	context = {
		'sales':sales, 
		'get_total_quantity':get_total_quantity,
		'get_total': get_total,
		'form': form,
		'nav_notify': nav_notify,
		'notification_count':notification_count
	}
	return render(request, 'Pharmacy/wholesale_pos.html', context)


@login_required
def make_sales_view(request):
	sales = Sales.objects.all()
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]

	get_total_quantity = Sales.get_total_quantity()
	
	get_total = Sales.get_total()

	form = SalesForm()
	if request.method == "POST" and "addToList" in request.POST:
		form = SalesForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Form was submitted successfully")
			return redirect('phar:pos')
		messages.error(request, "There was problem submitting the form")

	if request.method == "POST" and "finalSubmit" in request.POST:
		Transactions.objects.create(
			amount_received=int(request.POST['total_amount']),
			total_amount=int(request.POST['total_amount']), 
			amount_tendered=int(request.POST['amount_tendered']),
			change=int(request.POST['change_given']), 
			transaction_type="Sales"
		)
		for sale in sales:
			SalesList.objects.create(
				product_name=sale.product.product_name,
				price=sale.product.product.sales_price,
				sales_ref=sale.sales_ref,  
				customer= sale.customer.name,
				quantity_sold=sale.quantity_sold,
				total=sale.individual_total,
				sales_type='Retail'
			)

			procurement = ProcurementList.objects.get(
				product_name=sale.product.product_name,
				purchase_ref=sale.sales_ref
			)
			if procurement.purchase_ref == sale.sales_ref:
				procurement.quantity_ordered -= sale.quantity_sold
				procurement.save()

			

			drug = Pharmaceuticals.objects.get(product_name=sale.product.product.product_name)
			drug.quantity_available -= sale.quantity_sold
			drug.save()

			zero_q_procurement = ProcurementList.objects.filter(quantity_ordered=0)
			if zero_q_procurement:
				for zero_q in zero_q_procurement:
					zero_q.delete()
			sale.delete()


		transactions = Transactions.objects.filter(
			total_amount=0, 
			amount_tendered=0, 
			change=0, 
			discount=0, 
			amount_received=0
		)
		if transactions:
			messages.error(request, "Zero Transaction Operation was automatically cleaned out. ")
			for transaction in transactions:
				if transaction:
					transaction.delete()

			
			

		return redirect('phar:sales')

	


	context = {
		'sales':sales, 
		'get_total_quantity':get_total_quantity,
		'get_total': get_total,
		'form': form,
		'nav_notify': nav_notify,
		'notification_count':notification_count
	}
	return render(request, 'Pharmacy/pos.html', context)

@login_required
def sales_list(request):
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	sales = SalesList.objects.all().order_by('-ordered_date')

	all_sales_dates = []
	for sale in sales:
		all_sales_dates.append(sale.date.strftime("%Y-%m-%d"))


	if request.method == 'POST' and 'WholesalePrint' in request.POST:
		querried_date = request.POST.get('WholesaleDate')
		if querried_date in all_sales_dates:
			title = f"Wholesale for {querried_date}"
			queryset = SalesList.objects.filter(sales_type='Wholesale', date=querried_date).all()
			dir_ = os.path.join(settings.BASE_DIR, 'media')
			html_string = render_to_string('pdf/Pharmacy/sales_list.html', {'queryset': queryset, 'title':title})
			html = HTML(string=html_string)
			html.write_pdf(target=f'{dir_}/tmp/transaction_list.pdf', stylesheets=[CSS(string=boots)])
			fs = FileSystemStorage(location=f'{dir_}/tmp')
			with fs.open('transaction_list.pdf') as pdf:
				response = HttpResponse(pdf, content_type='application/pdf')
				response['Content-Disposition'] = f'attachment; filename="wholesale-for-{querried_date}-list.pdf"'
				return response
		else:
			messages.error(request, 'Sales Data not available for the selected Date')

	if request.method == 'POST' and 'RetailPrint' in request.POST:
		querried_date = request.POST.get('RetailDate')
		if querried_date in all_sales_dates:
			title = f"Retail Sales for {querried_date}"
			queryset = SalesList.objects.filter(sales_type='Retail', date=querried_date).all()
			dir_ = os.path.join(settings.BASE_DIR, 'media')
			html_string = render_to_string('pdf/Pharmacy/sales_list.html', {'queryset': queryset, 'title':title})
			html = HTML(string=html_string)
			html.write_pdf(target=f'{dir_}/tmp/transaction_list.pdf', stylesheets=[CSS(string=boots)])
			fs = FileSystemStorage(location=f'{dir_}/tmp')
			with fs.open('transaction_list.pdf') as pdf:
				response = HttpResponse(pdf, content_type='application/pdf')
				response['Content-Disposition'] = f'attachment; filename="retail-for-{querried_date}-list.pdf"'
				return response
		else:
			messages.error(request, 'Sales Data not available for the selected Date')
	
	context = {
		'sales': sales, 
		'notification_count':notification_count,
		'nav_notify': nav_notify
	}
	return render(request, 'Pharmacy/sales.html', context)


def delete_sales(request, pk):
	sale = Sales.objects.get(pk=pk)
	sale.delete()
	messages.success(request, "Sales entry successfully deleted ")
	return redirect('phar:pos')


def delete_procurement_list(request, pk):
	purchase = Procurement.objects.get(pk=pk)
	purchase.delete()
	messages.success(request, "Purchase entry successfully deleted ")
	return redirect('phar:receiving')

@login_required
def receiving_view(request):
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	purchases = Procurement.objects.all()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:4]

	get_total_quantity = Procurement.get_total_quantity()
	
	get_total = Procurement.get_total()


	form = ProcurementForm()
	if request.method == "POST" and 'addToList' in request.POST:
		form = ProcurementForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Form was submitted successfully")
			return redirect('phar:receiving')
		messages.error(request, "Form not successfully submitted")

	if request.method == "POST" and "finalSubmit" in request.POST:
		Transactions.objects.create(
			total_amount=int(request.POST['total_amount']), 
			amount_tendered=int(request.POST['amount_tendered']), 
			discount=int(request.POST['discount']),
			amount_received=int(request.POST['amount_received']),
			change=int(request.POST['change_given']), 
			transaction_type="Purchase"
		)

		for purchase in purchases:
			ProcurementList.objects.create(
				product=purchase.product,
				product_name=purchase.product.product_name,
				price=purchase.product.cost_price,
				purchase_ref=purchase.purchase_ref,  
				supplier= purchase.supplier.name,
				quantity_ordered=purchase.quantity_ordered,
				total=purchase.individual_total,
				expiry_date=purchase.expiry_date
			)

			drug = Pharmaceuticals.objects.get(product_name=purchase.product.product_name)
			drug.quantity_available += purchase.quantity_ordered
			
			drug.save()


			transactions = Transactions.objects.filter(
				total_amount=0, 
				amount_tendered=0, 
				change=0, 
				discount=0, 
				amount_received=0
			)
			if transactions:
				messages.error(request, "Zero  Transaction Operation was automatically cleaned out. ")
				for transaction in transactions:
					if transaction:
						transaction.delete()

			purchase.delete()

		return redirect('phar:procurement')




	context = {
		'get_total_quantity':get_total_quantity,
		'get_total': get_total,
		'purchases': purchases,
		'form': form,
		'notification_count':notification_count,
		'nav_notify': nav_notify
	}
	return render(request, 'Pharmacy/new_receiving.html', context)



@login_required
def procurement_list(request):
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	purchases = ProcurementList.objects.all().order_by('-ordered_date')

	product_dates_list = []
	for purchase in ProcurementList.objects.all():
		product_dates_list.append(purchase.date.strftime("%Y-%m-%d"))
	
	if request.method == 'POST' and 'supplierReportPrint' in request.POST:
		supply_date = request.POST.get('dateToPrintField')
		if supply_date in product_dates_list:
			queryset = ProcurementList.objects.filter(date=supply_date).all()
			dir_ = os.path.join(settings.BASE_DIR, 'media')
			html_string = render_to_string('pdf/Pharmacy/supply_by_date.html', {'queryset': queryset, 'supply_date':supply_date})
			html = HTML(string=html_string)
			html.write_pdf(target=f'{dir_}/tmp/supply_by_date.pdf', stylesheets=[CSS(string=boots)])

			fs = FileSystemStorage(location=f'{dir_}/tmp')
			with fs.open('supply_by_date.pdf') as pdf:
				response = HttpResponse(pdf, content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="supply_by_date.pdf"'
				return response
		else:
			messages.error(request, 'Selected date does not exist.')

	context = {
		'purchases': purchases, 
		'notification_count':notification_count,
		'nav_notify': nav_notify
	}

	return render(request, 'Pharmacy/Receiving.html', context)




@login_required
def product_detail(request, product_id):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	product = get_object_or_404(Drugs, product_id=product_id)

	context = {
		'product': product,
		'notification_count':notification_count,
		'nav_notify':nav_notify
	}
	return render(request, 'Pharmacy/product_detail.html', context)


@login_required
@user_passes_test(user_is_manager)
def product_edit(request, product_id):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	product = Drugs.objects.get(product_id=product_id)
	form = EditProductForm(instance=product)
	if request.method == 'POST':
		form = EditProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			messages.success(request, "Form was submitted successfully... ")
			return redirect('phar:product-list')
		messages.error(request, 'Something went wrong with form submission... ')

	context = {
		'form': form,
		'notification_count':notification_count,
		'nav_notify':nav_notify
	}
	return render(request, 'Pharmacy/edit_product.html', context)

@login_required
def customer_detail_view(request, pk):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	customer = Customer.objects.get(pk=pk)
	context = {
		'customer':customer,
		'nav_notify': nav_notify,
		'notification_count': notification_count
	}
	return render(request, 'Pharmacy/customer_detail.html', context)


@login_required
def supplier_detail_view(request, pk):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	supplier = get_object_or_404(Supplier, pk=pk)
	context = {
		'supplier':supplier,
		'nav_notify': nav_notify,
		'notification_count': notification_count
	}
	return render(request, 'Pharmacy/supplier_detail.html', context)


@login_required
@user_passes_test(user_is_manager)
def customer_edit(request, pk):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	customer = get_object_or_404(Customer, pk=pk)
	form = editCustomerForm(instance=customer)
	if request.method == 'POST':
		form = editCustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('phar:add-customer')
	context = {
		'form': form,
		'customer': customer,
		'nav_notify': nav_notify,
		'notification_count': notification_count
	}
	return render(request, 'Pharmacy/customer_edit.html', context)


@login_required
@user_passes_test(user_is_manager)
def supplier_edit(request, pk):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	supplier = get_object_or_404(Supplier, pk=pk)

	form = editSupplierForm(instance=supplier)
	if request.method == 'POST':
		form = editSupplierForm(request.POST, instance=supplier)
		if form.is_valid():
			form.save()
			return redirect('phar:add-supplier')

	context = {
		'form': form,
		'nav_notify': nav_notify,
		'notification_count': notification_count
	}
	return render(request, 'Pharmacy/supplier_edit.html', context)


@login_required
def transaction_list(request):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	transactions = Transactions.objects.all().order_by('-ordered_date')

	transaction_dates_group = [transact.date.strftime("%Y-%m-%d") for transact in transactions]

	if request.method == 'POST' and 'transactionPDF' in request.POST:
		title = "All Transactions"
		dir_ = os.path.join(settings.BASE_DIR, 'media')
		html_string = render_to_string('pdf/Pharmacy/transaction_pdf.html', {'queryset': transactions, 'title':title})
		html = HTML(string=html_string)
		html.write_pdf(target=f'{dir_}/tmp/transactions.pdf', stylesheets=[CSS(string=boots)])

		fs = FileSystemStorage(location=f'{dir_}/tmp')
		with fs.open('transactions.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
			return response




	if request.method == 'POST' and 'TransactionPrint' in request.POST:
		transaction_date = request.POST.get('TransactionDate')
		if transaction_date in transaction_dates_group:
			title = f"Transactions for {transaction_date}"
			queryset = Transactions.objects.filter(date=transaction_date).order_by('-ordered_date').all()
			dir_ = os.path.join(settings.BASE_DIR, 'media')
			html_string = render_to_string('pdf/Pharmacy/transaction_pdf.html', {'queryset': queryset, 'title':title})
			html = HTML(string=html_string)
			html.write_pdf(target=f'{dir_}/tmp/transactions.pdf', stylesheets=[CSS(string=boots)])

			fs = FileSystemStorage(location=f'{dir_}/tmp')
			with fs.open('transactions.pdf') as pdf:
				response = HttpResponse(pdf, content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'
				return response
		else:
			messages.error(request, 'Selected date does match existing Transactions. ')



	context = {
		'nav_notify': nav_notify,
		'notification_count': notification_count,
		'transactions': transactions,
	}
	return render(request, 'Pharmacy/transaction.html', context)

@login_required
@user_passes_test(user_is_manager)
def edit_category_view(request, pk):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	category = get_object_or_404(DrugCategory, pk=pk)
	form = editCategoryForm(instance=category)
	if request.method == 'POST':
		form = editCategoryForm(request.POST, instance=category)
		if form.is_valid():
			form.save()
			return redirect('phar:category-list')

	context = {
		'form': form, 
		'nav_notify': nav_notify,
		'notification_count': notification_count
	}
	return render(request, 'Pharmacy/edit_cat.html', context)


@login_required
@user_passes_test(user_is_manager)
def edit_type_view(request, pk):
	nav_notify = PharmacyNotification.objects.all().order_by('-ordered_date')[:2]
	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()
	type_ = get_object_or_404(DrugType, pk=pk)

	form = editCategoryForm(instance=type_)

	if request.method == 'POST':
		form = editTypeForm(request.POST, instance=type_)
		if form.is_valid():
			form.save()
			return redirect('phar:type-list')

	context = {
		'form': form, 
		'nav_notify': nav_notify,
		'notification_count': notification_count
	}

	return render(request, 'Pharmacy/edit_type.html', context)




















