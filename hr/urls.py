from django.urls import path
from hr import views
app_name = "hr"

urlpatterns = [
    
    # Event
    path('<module>/event/create/',views.create_event,name='create_event'),
    path('<module>/event/detail/',views.event_details,name='event_details'),
    path('<module>/event/update/<id>/',views.event_update,name='event_update'),
    path('<module>/event/delete/<id>/',views.event_delete,name='event_delete'),
    
    
    # Leave
    path('<module>/leave/create/',views.create_leave,name='create_leave'),
    path('<module>/leave/detail/',views.leave_details,name='leave_details'),
    path('<module>/leave/update/<id>/',views.leave_update,name='leave_update'),
    path('<module>/leave/delete/<id>/',views.leave_delete,name='leave_delete'),
    
    # Leave Status
    path('<module>/leave-status/create/',views.create_leave_status,name='create_leave_status'),
    path('<module>/leave-status/detail/',views.leave_status_details,name='leave_status_details'),
    path('<module>/leave-status/update/<id>/',views.leave_status_update,name='leave_status_update'),
    path('<module>/leave-status/delete/<id>/',views.leave_status_delete,name='leave_status_delete'),
    
    # Leave Type
    path('<module>/leave-type/create/',views.create_leave_type,name='create_leave_type'),
    path('<module>/leave-type/detail/',views.leave_type_details,name='leave_type_details'),
    path('<module>/leave-type/update/<id>/',views.leave_type_update,name='leave_type_update'),
    path('<module>/leave-type/delete/<id>/',views.leave_type_delete,name='leave_type_delete'),
    
    # HR
    path('<module>/my-profile/',views.my_profile,name='my_profile'),
    
    
]