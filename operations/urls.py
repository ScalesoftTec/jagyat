from django.urls import path
from operations import views,pdf
from masters.pdf import AWB_pdf

app_name = "operations"

urlpatterns = [
    

    
    # Booking
    path('<module>/master/booking/create/',views.create_booking_master,name='create_booking_master'),
    path('<module>/master/booking/details/',views.booking_master_details,name='booking_master_details'),
    path('<module>/master/all_booking/details/',views.all_booking_master_details,name='all_booking_master_details'),
    path('<module>/master/update/booking/<id>/',views.booking_master_update,name='booking_master_update'),
    path('<module>/master/delete/booking/<id>/',views.booking_master_delete,name='booking_master_delete'),
    
    
    # Jobs
    path('<module>/master/job/create/',views.create_job,name='create_job'),
    path('<module>/master/job/details/',views.job_details,name='job_details'),

    path('<module>/master/job/all_details/',views.all_job_details,name='all_job_details'),

    path('<module>/master/job-pending/details/',views.job_pending_approve_details,name='job_pending_approve_details'),
    path('<module>/master/job-approve/details/<int:id>/',views.approve_job,name='approve_job'),
    path('<module>/master/update/job/<id>/',views.job_update,name='job_update'),
    path('<module>/master/delete/job/<id>/',views.job_delete,name='job_delete'),
    path('<module>/master/closed/job/',views.closed_jobs,name='closed_jobs'),
    path('<module>/master/closed/job/update/<int:id>/',views.close_job_update,name='close_job_update'),
    path('<module>/master/cancelled/job/',views.cancelled_jobs,name='cancelled_jobs'),
    path('<module>/master/reterive/job/<id>',views.reterive_cancelled_jobs,name='reterive_cancelled_jobs'),
    
   
    # Booking
    path('<module>/master/transport/booking/create/',views.create_booking,name='create_booking'),
    path('<module>/master/transport/booking/details/',views.booking_details,name='booking_details'),
    path('<module>/master/update/transport/booking/<id>/',views.booking_update,name='booking_update'),
    path('<module>/master/delete/transport/booking/<id>/',views.booking_delete,name='booking_delete'),
    
    # GR
    path('<module>/master/gr/create/',views.create_gr,name='create_gr'),
    path('<module>/master/gr/details/',views.gr_details,name='gr_details'),
    path('<module>/master/update/gr/<id>/',views.gr_update,name='gr_update'),
    path('<module>/master/delete/gr/<id>/',views.gr_delete,name='gr_delete'),
    path('master/pdf/gr/<id>/',pdf.gr_pdf,name='gr_pdf'),
    
 
    # Cargo Arrival
    path('<module>/master/cargo/arrival/notice/create/',views.create_can,name='create_can'),
    path('<module>/master/cargo/arrival/notice/details/',views.can_details,name='can_details'),
    path('<module>/master/update/cargo/arrival/notice/<id>/',views.can_update,name='can_update'),
    path('<module>/master/delete/cargo/arrival/notice/<id>/',views.can_delete,name='can_delete'),
    path('master/cargo/arrival/notice/pdf/<id>/',pdf.can_pdf,name='cargo_arrival_pdf'),
 
    # VGM
    path('<module>/master/vgm/create/',views.create_vgm,name='create_vgm'),
    path('<module>/master/vgm/details/',views.vgm_details,name='vgm_details'),
    path('<module>/master/update/vgm/<id>/',views.vgm_update,name='vgm_update'),
    path('<module>/master/delete/vgm/<id>/',views.vgm_delete,name='vgm_delete'),
    path('master/vgm/pdf/<id>/',pdf.vgm_pdf,name='vgm_pdf'),
 
    # Delivery Order
    path('<module>/master/delivery/order/create/',views.create_do,name='create_do'),
    path('<module>/master/delivery/order/details/',views.do_details,name='do_details'),
    path('<module>/master/update/delivery/order/<id>/',views.do_update,name='do_update'),
    path('<module>/master/delete/delivery/order/<id>/',views.do_delete,name='do_delete'),
    path('master/delivery/order/pdf/<id>/',views.do_pdf,name='do_pdf'),
 
    # Freight Certificate
    path('<module>/master/freight/certificate/create/',views.create_fc,name='create_fc'),
    path('<module>/master/freight/certificate/details/',views.fc_details,name='fc_details'),
    path('<module>/master/update/freight/certificate/<id>/',views.fc_update,name='fc_update'),
    path('<module>/master/delete/freight/certificate/<id>/',views.fc_delete,name='fc_delete'),
    path('master/freight/certificate/pdf/<id>/',views.fc_pdf,name='freight_certificate_pdf'),
 
 
    # Master Bill Of Lading
    path('<module>/master/mbl/create/',views.create_mbl,name='create_mbl'),
    path('<module>/master/mbl/details/',views.mbl_details,name='mbl_details'),
    path('<module>/master/update/mbl/<id>/',views.mbl_update,name='mbl_update'),
    path('<module>/master/mbl/duplicate/<id>/',views.mbl_duplicate,name='mbl_duplicate'),
    path('<module>/master/delete/mbl/<id>/',views.mbl_delete,name='mbl_delete'),
    path('master/mbl/pdf/<id>/',pdf.mbl_pdf,name='mbl_pdf'),
    path('master/print/mbl/pdf/<id>/',pdf.print_mbl_pdf,name='print_mbl_pdf'),
    
 
    # AWB
    path('<module>/master/awb/create/',views.create_awb,name='create_awb'),
    path('<module>/master/awb/details/',views.awb_details,name='awb_details'),
    path('<module>/master/update/awb/<id>/',views.awb_update,name='awb_update'),
    path('<module>/master/delete/awb/<id>/',views.awb_delete,name='awb_delete'),
    path('master/awb/pdf/<id>/',AWB_pdf,name='awb_pdf'),
    # DSR

    path('<module>/master/dsr/create/',views.create_dsr,name='create_dsr'),
    path('<module>/master/dsr/details/',views.dsr_details,name='dsr_details'),
    path('<module>/master/dsr-hbl/details/',views.dsr_hbl_details,name='dsr_hbl_details'),
    path('<module>/master/dsr-actions/details/',views.dsr_actions,name='dsr_actions'),
    path('<module>/master/update/dsr/<id>/',views.dsr_update,name='dsr_update'),
    path('<module>/master/delete/dsr/<id>/',views.dsr_delete,name='dsr_delete'),
    path('master/dsr/pdf/<id>/',pdf.dsr_pdf,name='dsr_pdf'),

    # Rate
    path('<module>/master/create_rate/',views.create_rate,name='create_rate'),
    path('<module>/master/rate_details/',views.rate_details,name='rate_details'),
    path('<module>/master/rate_old_details/',views.rate_old_details,name='rate_old_details'),
    path('<module>/master/rate_update/<id>/',views.rate_update,name='rate_update'),
    path('<module>/master/rate_delete/<id>/',views.rate_delete,name='rate_delete'),
    path('<module>/master/rate_duplicate/<id>/',views.rate_duplicate,name='rate_duplicate'),
 
    # Manifest
    path('<module>/manifest/create/',views.create_manifest,name='create_manifest'),
    path('<module>/manifest/details/',views.manifest_details,name='manifest_details'),
    path('<module>/update/manifest/<id>/',views.manifest_update,name='manifest_update'),
    path('<module>/delete/manifest/<id>/',views.manifest_delete,name='manifest_delete'),
    path('pdf/manifest/<id>/',views.manifest_pdf,name='manifest_pdf'),
    
   
 
    
]