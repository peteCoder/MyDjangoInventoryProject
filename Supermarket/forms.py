from django import forms
from Supermarket.models import *


class AddCategoryForm(forms.ModelForm):
	class Meta:
		model =   ProductCategory
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'ProductCategory',
				'aria-describedby': 'productCategory',
				'placeholder': 'Enter product Category',
			}),
		}

	def clean_name(self):
		name = self.cleaned_data.get('name')
		
		for instance in ProductCategory.objects.all():
			if instance.name == name:
				raise forms.ValidationError(name + " already exists.")
		return name




class AddProductTypeForm(forms.ModelForm):
	class Meta:
		model = ProductType
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'ProductType',
				'aria-describedby': 'productType',
				'placeholder': 'Enter product Type',
			}),
		}

	def clean_name(self):
		name = self.cleaned_data.get('name')
		
		for instance in ProductType.objects.all():
			if instance.name == name:
				raise forms.ValidationError(name + " already exists.")
		return name


class EditProductForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = '__all__'
		widgets = {
			'product_name': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'Productname',
				'aria-describedby': 'productNameHelp',
				'placeholder': 'Enter product name',
				"readonly": "readonly",
			}),
			'custom_id': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'ProductID',
				'aria-describedby': 'productIDHelp',
				'placeholder': 'Product ID',
			}),

			'product_category': forms.Select(attrs={
				'id':'selector',
				'class': 'js-example-basic-single form-control w-100',
				'style': "width: 100%;"
			}),


			'product_type': forms.Select(attrs={
				'id':'select2 selector',
				'class': 'js-example-basic-single form-control w-100',
				'style': "width: 100%;"
			}),

			'product_measurement': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'ProductMeasurement',
				'aria-describedby': 'productMeasurementHelp',
				'placeholder': 'Enter Product Measurement',
			}),

			'quantity_available': forms.TextInput(attrs={
				'type': 'number',
				'class': 'form-control',
				"readonly": "readonly",
			}),

			

			'cost_price': forms.TextInput(attrs={
				'type': 'number',
				'class': 'form-control',
			}),

			'sales_price': forms.TextInput(attrs={
				'type': 'number',
				'class': 'form-control',
			}),

			'product_description': forms.Textarea(attrs={
				'type': 'text',
				'class': 'form-control', 
				'cols': '20',
				'id':'ProductDescription',
				'aria-describedby': 'productDescriptionHelp',
				'placeholder': 'Enter further details about product',
			}),

		}



class AddProductForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = '__all__'
		widgets = {
			'product_name': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'Productname',
				'aria-describedby': 'productNameHelp',
				'placeholder': 'Enter product name',
			}),
			'custom_id': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'ProductID',
				'aria-describedby': 'productIDHelp',
				'placeholder': 'Product ID',
			}),

			'product_category': forms.Select(attrs={
				'id':'selector',
				'class': 'js-example-basic-single form-control w-100',
				'style': "width: 100%;"
			}),


			'product_type': forms.Select(attrs={
				'id':'select2 selector',
				'class': 'js-example-basic-single form-control w-100',
				'style': "width: 100%;"
			}),

			'product_measurement': forms.TextInput(attrs={
				'type': 'text',
				'class': 'form-control', 
				'id':'ProductMeasurement',
				'aria-describedby': 'productMeasurementHelp',
				'placeholder': 'Enter Product Measurement',
			}),

			'quantity_available': forms.TextInput(attrs={
				'type': 'number',
				'class': 'form-control',
				"readonly": "readonly",
			}),

			
			'cost_price': forms.TextInput(attrs={
				'type': 'number',
				'class': 'form-control',
			}),

			'sales_price': forms.TextInput(attrs={
				'type': 'number',
				'class': 'form-control',
			}),

			'product_description': forms.Textarea(attrs={
				'type': 'text',
				'class': 'form-control', 
				'cols': '20',
				'id':'ProductDescription',
				'aria-describedby': 'productDescriptionHelp',
				'placeholder': 'Enter further details about product',
			}),

		}


	def clean_product_name(self):
		product_name = self.cleaned_data['product_name']
		if not product_name or product_name == "":
			raise forms.ValidationError("Product Name input must not empty.")
		else:
			for instance in Products.objects.all():
				if instance.product_name == product_name:
					raise forms.ValidationError(product_name + " already exists, edit product instead.. ")
		return product_name

	def clean_custom_id(self):
		custom_id = self.cleaned_data['custom_id']
		if custom_id:
			for instance in Products.objects.all():
				if instance.custom_id == custom_id:
					raise forms.ValidationError(custom_id + " id already exists. Each product must have a unique id")
		return custom_id



class addSupplierForm(forms.ModelForm):
	class Meta:
		model = Supplier
		fields = "__all__"
		widgets = {
			'name': forms.TextInput(attrs={
				'name':'name',
				'class': 'form-control form-control-user',
				'placeholder': 'Supplier Name',
				'type': 'text'
			}),
			'email': forms.TextInput(attrs={
				'name':'contact',
				'class': 'form-control',
				'placeholder':'Enter Email Address',
				'type': 'text' 
			}),
			'phone': forms.TextInput(attrs={
				'type': 'tel',
				'class': 'form-control',
				'placeholder': 'contact',
				'name': 'contact'
			}),
			'address': forms.Textarea(attrs={
				'class': 'form-control',
				'cols': '30',
				'rows': '3',
				'name': 'address'
			}),

		}

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if not name or name == "":
			raise forms.ValidationError("The name field is required")
		else:
			for instance in Supplier.objects.all():
				if instance.name == name:
					raise forms.ValidationError(name + " already exists.")
		return name

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not email or email == "":
			raise forms.ValidationError("The email field is required")
		else:
			if "@" not in email:
				raise forms.ValidationError("Email must be valid. Try adding an '@' symbol to the email. ")
			for instance in Supplier.objects.all():
				if instance.email == email:
					raise forms.ValidationError(email + " already exists.")
		return email

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if not phone or phone == "":
			raise forms.ValidationError("The phone field is required")
		else:
			for instance in Supplier.objects.all():
				if instance.phone == phone:
					raise forms.ValidationError(phone + " already exists.")
		return phone







class addCustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = "__all__"
		widgets = {
			'name': forms.TextInput(attrs={
				'name':'name',
				'class': 'form-control form-control-user',
				'placeholder': 'Customer Name',
				'type': 'text'
			}),
			'email': forms.TextInput(attrs={
				'name':'contact',
				'class': 'form-control',
				'placeholder':'Enter Email Address',
				'type': 'text' 
			}),
			'phone': forms.TextInput(attrs={
				'type': 'tel',
				'class': 'form-control',
				'placeholder': 'contact',
				'name': 'contact'
			}),
			'address': forms.Textarea(attrs={
				'class': 'form-control',
				'cols': '30',
				'rows': '3',
				'name': 'address'
			}),

		}

class editSupplierForm(forms.ModelForm):
	class Meta:
		model = Supplier
		fields = "__all__"
		widgets = {
			'name': forms.TextInput(attrs={
				'name':'name',
				'class': 'form-control form-control-user',
				'placeholder': 'Customer Name',
				'type': 'text'
			}),
			'email': forms.TextInput(attrs={
				'name':'contact',
				'class': 'form-control',
				'placeholder':'Enter Email Address',
				'type': 'text' 
			}),
			'phone': forms.TextInput(attrs={
				'type': 'tel',
				'class': 'form-control',
				'placeholder': 'contact',
				'name': 'contact'
			}),
			'address': forms.Textarea(attrs={
				'class': 'form-control',
				'cols': '30',
				'rows': '3',
				'name': 'address'
			}),

		}


class editTypeForm(forms.ModelForm):
	class Meta:
		model = ProductType
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={
				'name':'name',
				'class': 'form-control form-control-user',
				'placeholder': '',
				'type': 'text'
			}),
		}


class editCategoryForm(forms.ModelForm):
	class Meta:
		model = ProductCategory
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={
				'name':'name',
				'class': 'form-control form-control-user',
				'placeholder': '',
				'type': 'text'
			}),
		}




class editCustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = "__all__"
		widgets = {
			'name': forms.TextInput(attrs={
				'name':'name',
				'class': 'form-control form-control-user',
				'placeholder': 'Customer Name',
				'type': 'text'
			}),
			'email': forms.TextInput(attrs={
				'name':'contact',
				'class': 'form-control',
				'placeholder':'Enter Email Address',
				'type': 'text' 
			}),
			'phone': forms.TextInput(attrs={
				'type': 'tel',
				'class': 'form-control',
				'placeholder': 'contact',
				'name': 'contact'
			}),
			'address': forms.Textarea(attrs={
				'class': 'form-control',
				'cols': '30',
				'rows': '3',
				'name': 'address'
			}),

		}




class SalesForm(forms.ModelForm):
	class Meta:
		model = Sales
		fields = '__all__'
		widgets = {
			'customer': forms.Select(attrs={
				'id':'selector',
				'class': 'js-example-basic form-control w-100',
				'name': 'select',
				'style': "width:50%;"
			}),

			'sales_ref': forms.TextInput(attrs={
				'name':'sales_ref',
				'class': 'form-control form-control-user',
				'placeholder': 'Sales Ref',
				'type': 'text',
				'style': "width: 50%;"
			}),

			'product': forms.Select(attrs={
				'id':'select2 selector',
				'class': 'js-example-basic-single form-control w-100',
				'style': "width: 100%;"
			}),

			'quantity_sold': forms.TextInput(attrs={
				'placeholder': "Enter Quantity",
				'class': "form-control w-50 ",
				'type': "number",
				"style": "height: 30px !important;"
			})


		}

	def clean(self):
		cleaned_data = super().clean()
		entered_product_name = self.cleaned_data.get('product')
		quantity_sold = self.cleaned_data.get('quantity_sold')

		
		purchase_ref = entered_product_name.purchase_ref
		
		product = ProcurementList.objects.get(purchase_ref=purchase_ref)

		product_available = product.quantity_ordered


		self.cleaned_data['sales_ref'] = purchase_ref

		sales_ref = self.cleaned_data.get('sales_ref')

		p_name = product.product_name

		sales = Sales.objects.filter(
			product__product_name=p_name, 
			sales_ref=purchase_ref
		)

		total_q_sold = 0

		for sale in sales:
			if sale.sales_ref == purchase_ref:
				total_q_sold += sale.quantity_sold

		left_in_stock = product_available - total_q_sold

		if product.product_has_expired_already:
			raise forms.ValidationError({'product': 'Already Expired.'})

		if int(quantity_sold) < 1:
			raise forms.ValidationError({'quantity_sold': 'You cannot enter quantity less than 1'})


		if int(total_q_sold + quantity_sold) > int(product_available):
			raise forms.ValidationError({'quantity_sold':f"You have already entered {total_q_sold} '{entered_product_name}' to sell. {quantity_sold} is a bit too much. {left_in_stock} left in stock."})

		if int(product_available) < int(quantity_sold):
			raise forms.ValidationError({'quantity_sold':f"{product.quantity_ordered} {p_name} \
			 available in stock. \
			 The quantity input is greater than \
			 the quantity available. "})

		return cleaned_data
	

class ProcurementForm(forms.ModelForm):
	class Meta:
		model = Procurement
		fields = '__all__'
		widgets = {
			'supplier': forms.Select(attrs={
				'id':'selector',
				'class': 'js-example-basic form-control w-100',
				'name': 'select',
				'style': "width:50%;"
			}),

			'purchase_ref': forms.TextInput(attrs={
				'name':'sales_ref',
				'class': 'form-control form-control-user',
				'placeholder': 'Sales Ref',
				'type': 'text',
				'style': "width: 50%;"
			}),

			'product': forms.Select(attrs={
				'id':'select2 selector',
				'class': 'js-example-basic-single form-control w-100',
				'style': "width: 100%;"
			}),

			'quantity_ordered': forms.TextInput(attrs={
				'placeholder': "Enter Quantity",
				'class': "form-control w-50 ",
				'type': "number"
			}), 

			'expiry_date': forms.DateInput(attrs={
				'type': 'date',
				'class': 'form-control',
				'style': 'width: 250px !important;'
			})


		}

	def clean(self):
		cleaned_data = super().clean()
		quantity_ordered = self.cleaned_data.get('quantity_ordered')

		if int(quantity_ordered) < 1:
			raise forms.ValidationError({'quantity_ordered': 'You cannot enter quantity less than 1'})

		return cleaned_data

