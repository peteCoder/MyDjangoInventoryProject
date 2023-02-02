# Generated by Django 4.1.6 on 2023-02-01 23:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Supermarket', '0004_alter_customer_id_alter_procurement_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producttype',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]