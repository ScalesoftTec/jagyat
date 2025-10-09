from django.urls import path
from dashboard import views
from masters import views as master_views
from accounting import views as fa_views
from business_intelligence import views as bi_views

app_name = 'dashboard'

urlpatterns = [
    path('<module>/',views.index,name='dashboard'),
    path('reporting-dashboard/<module>/',bi_views.index,name='bi_dashboard'),
    path('accounting-dashboard/<module>/',fa_views.index,name='accounting_dashboard'),
    path('sea_export-dashboard/<module>/',views.sea_export_dashboard,name='sea_export_dashboard'),
    path('sea_import-dashboard/<module>/',views.sea_import_dashboard,name='sea_import_dashboard'),
    path('air_import-dashboard/<module>/',views.air_import_dashboard,name='air_import_dashboard'),
    path('air_export-dashboard/<module>/',views.air_export_dashboard,name='air_export_dashboard'),
    path('alert_mark_as_read/<int:id>/',views.alert_mark_as_read,name='alert_mark_as_read'),


]
