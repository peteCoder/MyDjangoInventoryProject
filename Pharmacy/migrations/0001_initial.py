# Generated by Django 3.0.6 on 2022-01-13 13:55

import Pharmacy.utils
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Default', max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, max_length=100, null=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='PharmaceuticalCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('ordered_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Pharmaceuticals',
            fields=[
                ('product_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.TextField()),
                ('custom_id', models.CharField(blank=True, default=Pharmacy.utils.random_string, max_length=50, null=True)),
                ('quantity_available', models.IntegerField(default=0, verbose_name='quantity available')),
                ('product_measurement', models.CharField(blank=True, max_length=10, null=True)),
                ('product_description', models.TextField(blank=True, max_length=600, null=True)),
                ('cost_price', models.IntegerField(default=0)),
                ('sales_price', models.IntegerField(default=0)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('reorder_level', models.IntegerField(blank=True, default=10, null=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drug_cat', to='Pharmacy.PharmaceuticalCategory')),
            ],
            options={
                'verbose_name': 'Drug',
                'verbose_name_plural': 'Drugs',
            },
        ),
        migrations.CreateModel(
            name='PharmaceuticalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default', max_length=100, null=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.CreateModel(
            name='ProcurementList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=40, null=True)),
                ('price', models.IntegerField(default=0)),
                ('purchase_ref', models.CharField(blank=True, default=Pharmacy.utils.random_string, max_length=20, null=True)),
                ('supplier', models.CharField(blank=True, max_length=60, null=True)),
                ('quantity_ordered', models.IntegerField(blank=True, null=True, verbose_name='quantity ordered')),
                ('total', models.IntegerField(blank=True, help_text='total = price * quantity_ordered', null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procurement', to='Pharmacy.Pharmaceuticals')),
            ],
            options={
                'verbose_name_plural': 'Procurement List',
            },
        ),
        migrations.CreateModel(
            name='SalesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=40, null=True)),
                ('price', models.IntegerField(default=0)),
                ('sales_ref', models.CharField(blank=True, default=Pharmacy.utils.random_string, max_length=20, null=True)),
                ('customer', models.CharField(blank=True, max_length=60, null=True)),
                ('sales_type', models.CharField(blank=True, choices=[('Retail', 'Retail'), ('Wholesale', 'Wholesale')], default='Retail', max_length=9, null=True)),
                ('quantity_sold', models.IntegerField(blank=True, null=True, verbose_name='quantity sold')),
                ('total', models.IntegerField(blank=True, help_text='total = price * quantity_ordered', null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Sales List',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Default', max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, max_length=100, null=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.IntegerField(default=0, verbose_name='total amount')),
                ('amount_received', models.IntegerField(default=0, verbose_name='amount received')),
                ('amount_tendered', models.IntegerField(default=0, verbose_name='amount tendered')),
                ('discount', models.IntegerField(default=0, verbose_name='discount allowed')),
                ('change', models.IntegerField(default=0, verbose_name='change')),
                ('transaction_type', models.CharField(default='Sales', max_length=20)),
                ('date', models.DateField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_ref', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('quantity_sold', models.IntegerField(verbose_name='quantity sold')),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sale_customer', to='Pharmacy.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sold', to='Pharmacy.ProcurementList')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='Procurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_ref', models.CharField(blank=True, default=Pharmacy.utils.random_string, max_length=20, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('quantity_ordered', models.IntegerField(null=True, verbose_name='quantity ordered')),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ordered', to='Pharmacy.Pharmaceuticals')),
                ('supplier', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_supplier', to='Pharmacy.Supplier')),
            ],
            options={
                'verbose_name': 'Procurement',
                'verbose_name_plural': 'Procurements',
            },
        ),
        migrations.AddField(
            model_name='pharmaceuticals',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drug_type', to='Pharmacy.PharmaceuticalType'),
        ),
    ]
