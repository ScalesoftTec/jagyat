from django.contrib import admin
from crm.models import Inquiry,Lead,Event
# Register your models here.

admin.site.register(Inquiry)
admin.site.register(Lead)
admin.site.register(Event)