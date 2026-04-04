from django.contrib import admin

from dashboard.models import Alerts,Logistic,TallyIpAdress,SequenceSettings

# Register your models here.



class SequenceSettingsList(admin.ModelAdmin):
    list_display = ['voucher_type','from_date','prefix','suffix', 'zero_length','skip_count','is_active']
    list_filter = ('voucher_type',)
    list_per_page = 100


    class Meta:
        fields = "__all__"
admin.site.register(SequenceSettings,SequenceSettingsList)

admin.site.register(Alerts)
admin.site.register(Logistic)
admin.site.register(TallyIpAdress)