from django.urls import path
from .views import *

app_name = 'notify'


urlpatterns = [
    path('pharmacy/alert/', showNotificationsPharmacy, name='phar_notification'),
    path('supermarket/alert/', showNotificationsSupermarket, name='super_notification'),
]


