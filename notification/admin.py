from django.contrib import admin
from .models import SupermarketNotification, PharmacyNotification
# Register your models here.

admin.site.register(SupermarketNotification)
admin.site.register(PharmacyNotification)