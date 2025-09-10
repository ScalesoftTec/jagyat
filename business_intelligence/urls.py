from django.urls import path
from business_intelligence import views
app_name = "bi"

urlpatterns = [
    path('<module>/incompleted-jobs/',views.incompleted_jobs,name='incompleted_jobs'),
    path('<module>/jobs-profit-and-loss-status/',views.jobs_p_and_l_status,name='jobs_p_and_l_status'),
    path('<module>/jobs-psr/',views.jobs_psr,name='jobs_psr'),
    path('<module>/csr_report/',views.csr_report,name='csr_report'),
    path('<module>/day_book/',views.day_book,name='day_book'),
    
    path('<module>/data_changes_logs/',views.CrudLogs,name='crud_logs'),
    
    path('<module>/party-details/',views.customer_details,name='customer_details'),
    path('<module>/customer-report/',views.customer_report,name='customer_report'),

    
    path('<module>/get_sales_and_purchase_data/<year>/', views.get_sales_and_purchase_data, name='get_sales_and_purchase_data'),
    path('<module>/job_wise_data/<year>/', views.job_wise_data, name='job_wise_data'),
    path('<module>/profit_margin_date_wise/<year>/', views.profit_margin_date_wise, name='profit_margin_date_wise'),
    path('<module>/invoice_pay_margin_date_wise/<year>/', views.invoice_pay_margin_date_wise, name='invoice_pay_margin_date_wise'),
    
]