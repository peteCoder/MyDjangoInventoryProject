# Generated by Django 3.0.6 on 2022-01-13 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Supermarket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procurementlist',
            name='product_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='saleslist',
            name='product_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
