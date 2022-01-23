from django.db import models
from django.contrib.auth.models import User


# Create your models here.

NOTIFICATION_TYPE = [ 
    (1, 'Expired'), # Notification Type for Expired Products
    (2, 'Out Of Stock') # Notification Type for Products out of stock
]

class PharmacyNotification(models.Model):
    drug = models.ForeignKey('Pharmacy.Pharmaceuticals', on_delete=models.CASCADE, related_name='drug_notify')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    text_preview = models.CharField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    date_of_action = models.DateTimeField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Pharmacy Notifications"
        verbose_name = "Pharmacy Notification"

    def date_of_action_format(self):
        date = self.date_of_action.strftime("%d/%m/%Y")
        return date


    def __str__(self):
        return "Notification for "+ self.drug.product_name


class SupermarketNotification(models.Model):
    product = models.ForeignKey('Supermarket.Products', on_delete=models.CASCADE, related_name='product_notify')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    text_preview = models.CharField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    date_of_action = models.DateTimeField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Supermarket Notifications"
        verbose_name = "Supermarket Notification"


    def __str__(self):
        return "Notification for "+ self.product.product_name
































