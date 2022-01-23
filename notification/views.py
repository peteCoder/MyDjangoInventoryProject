from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import PharmacyNotification, SupermarketNotification




# Create your views here.
def showNotificationsPharmacy(request):
    notification = PharmacyNotification.objects.filter(is_seen=False).all()
    notifications = PharmacyNotification.objects.all().order_by('-ordered_date')[:5]
    notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()

    for notify in notification:
        if notify.is_seen == False:
            notify.is_seen = True
        notify.save()


    template = loader.get_template('Pharmacy/alert.html')
    context = {
        'notification_count':notification_count,
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))




def showNotificationsSupermarket(request):
    notifications = SupermarketNotification.objects.all().order_by('-ordered_date')[:5]
    notification_count = SupermarketNotification.objects.filter(is_seen=False).all().count()
    notification = SupermarketNotification.objects.filter(is_seen=False).all()

    for notify in notification:
        if notify.is_seen == False:
            notify.is_seen = True
        notify.save()


    template = loader.get_template('Supermarket/alert.html')
    context = {
        'notification_count':notification_count,
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))


















