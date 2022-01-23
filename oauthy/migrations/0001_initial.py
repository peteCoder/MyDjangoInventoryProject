# Generated by Django 3.0.6 on 2022-01-13 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6)),
                ('position', models.CharField(blank=True, choices=[('manager', 'manager'), ('cashier', 'cashier')], default='cashier', max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to='profile')),
                ('bio', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
