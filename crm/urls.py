from django.urls import path
from crm import views
app_name = "crm"

urlpatterns = [
    # Index Dashboard
    path('<module>/crm-dashboard/',views.index,name='crm_index'),
    
    # Inquiry

    #events
    path('<module>/event/create/',views.create_event,name='create_event'),
    path('<module>/event/detail/',views.event_details,name='event_details'),
    path('<module>/event/update/<id>/',views.event_update,name='event_update'),
    path('<module>/event/delete/<id>/',views.event_delete,name='event_delete'),

    # sales party
    path('<module>/party/create/',views.create_sales_party,name='create_sales_party'),
    path('<module>/party/update/<id>/',views.sales_party_update,name='sales_party_update'),
    path('<module>/sales/party/details/',views.sales_party_details,name='sales_party_details'),
    path('<module>/sales/partydelete/<id>/',views.sales_party_delete,name='sales_party_delete'),



    path('<module>/inquiry/create/<extra_module>/',views.create_inquiry,name='create_inquiry'),
    path('<module>/inquiry/detail/<extra_module>/',views.inquiry_details,name='inquiry_details'),
    path('<module>/inquiry/update/<id>/<extra_module>/',views.inquiry_update,name='inquiry_update'),
    path('<module>/inquiry/delete/<id>/<extra_module>/',views.inquiry_delete,name='inquiry_delete'),
    path('inquiry/pdf/<id>/',views.inquiry_pdf,name='inquiry_pdf'),
    
    # Lead
    path('<module>/lead/create/',views.create_lead,name='create_lead'),
    path('<module>/lead/detail/',views.lead_details,name='lead_details'),
    path('<module>/lead/update/<id>/',views.lead_update,name='lead_update'),
    path('<module>/lead/delete/<id>/',views.lead_delete,name='lead_delete'),
    
]