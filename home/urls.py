from django.urls import path
from home import views


app_name = 'home'


urlpatterns = [
    # Authentication Part
    path('',views.handle_login,name="handle_login"),
    path('logout/',views.handle_logout,name="handle_logout"),
    # Authentication End
    
    # Main Home Page
    path('welcome/',views.home_index,name="home_index"),
    path('choose/operations/',views.choose_operations,name="choose_operations"),
    path('ajax/job/details/',views.job_details,name="ajax_load_jobdetails"),
    path('ajax/job-container/details/',views.job_hbl_container_details,name="ajax_load_job_hbl_container_details"),
    path('ajax/hbl/details/',views.hbl_details,name="ajax_hbl_details"),
    path('ajax/inquiry/details/',views.inquiry_details,name="ajax_inquiry_details"),
    path('ajax/party/details/',views.party_details,name="ajax_party_details"),
    path('ajax/party-address/details/',views.party_address_details,name="ajax_party_address_details"),
    path('ajax/job-gr/details/',views.job_gr_details,name="ajax_job_gr_details"),
    path('ajax/job-hbl/details/',views.job_hbl_details,name="ajax_job_hbl_details"),
    path('ajax/job-container/details/',views.job_container_details,name="ajax_job_container_details"),
    path('ajax/job-booking/details/',views.job_booking_details,name="ajax_job_booking_details"),
    path('ajax/payment-bill-details/',views.payment_bill_details,name="ajax_payment_bill_details"),
    path('ajax/reciept-bill-details/',views.reciept_bill_details,name="ajax_reciept_bill_details"),
    path('ajax/get_vendor_emails/',views.get_vendor_emails,name="get_vendor_emails"),
    path('ajax/get_party_emails/',views.get_party_emails,name="get_party_emails"),
    
    
    
    
    

    
    
    
    

    # Document Approvers
    path('<module>/document-approvers/',views.handle_document_approvers,name='handle_document_approvers'),
    
   
    
]