from django.contrib import admin
from hr import models
# Register your models here.

admin.site.register(models.Department)
admin.site.register(models.Designation)
admin.site.register(models.Event)
admin.site.register(models.LeaveStatus)
admin.site.register(models.LeaveType)
admin.site.register(models.Leave)
admin.site.register(models.Employee)