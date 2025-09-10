from django.contrib import admin

from dashboard.models import Alerts,Logistic,TallyIpAdress

# Register your models here.

admin.site.register(Alerts)
admin.site.register(Logistic)
admin.site.register(TallyIpAdress)