from django.db import models
import uuid
import datetime
from django.utils import timezone
from Pharmacy.utils import random_string


# Create your models here


class ProductType(models.Model):
    name = models.CharField(max_length=500, blank=False, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Types"
        verbose_name = "Type"


class ProductCategory(models.Model):
    name = models.CharField(max_length=500, blank=False, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Products(models.Model):
    product_name = models.TextField(blank=False, null=False)
    product_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    custom_id = models.CharField(
        max_length=50, blank=True, null=True, default=random_string)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='product_cat')
    quantity_available = models.IntegerField(
        verbose_name='quantity available', default=0)
    product_measurement = models.CharField(
        max_length=10, blank=True, null=True)
    product_description = models.TextField(
        max_length=600, blank=True, null=True)
    cost_price = models.IntegerField(default=0)
    sales_price = models.IntegerField(default=0)
    date_added = models.DateField(auto_now_add=True)
    reorder_level = models.IntegerField(default=10, blank=True, null=True)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name='product_type')
    ordered_date = models.DateTimeField(auto_now_add=True)

    @property
    def date_added_format(self):
        date = self.date_added.strftime("%d/%m/%Y")
        return date

    @property
    def class_of_low_and_empty(self):
        if self.quantity_available == 0:
            return "badge-danger"
        elif self.quantity_available <= self.reorder_level and self.quantity_available > 0:
            return "badge-warning"
        else:
            return ""

    @property
    def is_low_in_stock(self):
        if self.quantity_available == 0 or self.quantity_available <= self.reorder_level:
            return True
        return False

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Supplier(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, default="Default")
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=500, blank=True,
                            null=True, default="Default")
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Procurement(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='my_product_ordered')
    purchase_ref = models.CharField(
        max_length=500, blank=True, null=True, default=random_string)
    expiry_date = models.DateField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    quantity_ordered = models.IntegerField(
        verbose_name='quantity ordered', blank=False, null=True)
    supplier = models.ForeignKey(Supplier,
                                 on_delete=models.CASCADE,
                                 related_name='purchase_supplier',
                                 default=1
                                 )
    ordered_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_total_quantity():
        total = 0
        for purchase in Procurement.objects.all():
            quantity = purchase.quantity_ordered
            total += quantity
        return total

    @property
    def individual_total(self):
        total = self.product.cost_price * self.quantity_ordered
        return total

    @staticmethod
    def get_total():
        acc = 0
        purchases = Procurement.objects.all()
        for purchase in purchases:
            total = purchase.product.cost_price * purchase.quantity_ordered
            acc += total
        return acc


class ProcurementList(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='procurement')
    # product_name = models.CharField(max_length=40, blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    purchase_ref = models.CharField(
        max_length=500, blank=True, null=True, default=random_string)
    supplier = models.CharField(max_length=500, blank=True, null=True)
    quantity_ordered = models.IntegerField(
        verbose_name='quantity ordered', blank=True, null=True)
    total = models.IntegerField(
        help_text='total = price * quantity_ordered', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Procurement List"

    @property
    def indicate_product_has_expired_already(self):
        if self.expiry_date <= datetime.date.today():
            return 'Expired'
        return ''

    @property
    def expiry_date_format(self):
        if self.expiry_date:
            date = self.expiry_date.strftime("%d/%m/%Y")
            return date
        else:
            return "No Date"

    @property
    def product_has_expired(self):
        add_5_days_notice = datetime.timedelta(days=5)
        if self.expiry_date <= datetime.date.today():
            return "badge-danger"
        elif self.expiry_date <= (datetime.date.today() + add_5_days_notice):
            return "badge-warning"
        else:
            return ""

    @property
    def dashboard_product_has_expired(self):
        add_5_days_notice = datetime.timedelta(days=5)
        if self.expiry_date <= datetime.date.today():
            return "border-left-danger"
        elif self.expiry_date <= (datetime.date.today() + add_5_days_notice):
            return "border-left-warning"
        else:
            return "border-left-success"

    @property
    def product_has_expired_already(self):
        if self.expiry_date <= datetime.date.today():
            return True
        return False

    class Meta:
        verbose_name_plural = "Procurement List"

    def __str__(self):
        return self.product_name + " " + str(self.quantity_ordered) + " " + self.indicate_product_has_expired_already

    @property
    def expiry_date_format(self):
        date = self.expiry_date.strftime("%d/%m/%Y")
        return date

    @property
    def date_format(self):
        date = self.date.strftime("%Y/%m/%d")
        return date


class SalesList(models.Model):
    SALES_TYPE = [('Retail', 'Retail'), ('Wholesale', 'Wholesale')]
    product_name = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    sales_ref = models.CharField(
        max_length=500, blank=True, null=True, default=random_string)
    customer = models.CharField(max_length=500, blank=True, null=True)
    sales_type = models.CharField(
        max_length=9, choices=SALES_TYPE, blank=True, null=True, default='Retail')
    quantity_sold = models.IntegerField(
        verbose_name='quantity sold', blank=True, null=True)
    total = models.IntegerField(
        help_text='total = price * quantity_sold', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sales List"

    def __str__(self):
        return self.product_name

    @property
    def date_format(self):
        date = self.date.strftime("%Y/%m/%d")
        return date


class Transactions(models.Model):
    total_amount = models.IntegerField(verbose_name='total amount', default=0)
    amount_received = models.IntegerField(
        verbose_name='amount received', default=0)
    amount_tendered = models.IntegerField(
        verbose_name='amount tendered', default=0)
    discount = models.IntegerField(verbose_name='discount allowed', default=0)
    change = models.IntegerField(verbose_name='change', default=0)
    transaction_type = models.CharField(max_length=500, default="Sales")
    date = models.DateField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_type + " " + str(self.amount_tendered)

    @property
    def date_format(self):
        date = self.date.strftime("%Y/%m/%d")
        return date

    class Meta:
        verbose_name_plural = "Transactions"


class Sales(models.Model):
    product = models.ForeignKey(
        ProcurementList, on_delete=models.CASCADE, related_name='product_sold')
    sales_ref = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    quantity_sold = models.IntegerField(verbose_name='quantity sold')
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 related_name='sale_customer',
                                 default=1
                                 )
    ordered_date = models.DateTimeField(auto_now_add=True)

    @property
    def date_format(self):
        date = self.date.strftime("%Y/%m/%d")
        return date

    def __str__(self):
        return str(self.quantity_sold) + " " + self.product.product_name

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = "Sales"

    @staticmethod
    def get_total_quantity():
        total = 0
        for sale in Sales.objects.all():
            quantity = sale.quantity_sold
            total += quantity
        return total

    @property
    def individual_total(self):
        total = self.product.product.sales_price * self.quantity_sold
        return total

    @staticmethod
    def get_total():
        acc = 0
        sales = Sales.objects.all()
        for sale in sales:
            total = sale.product.product.sales_price * sale.quantity_sold
            acc += total
        return acc
