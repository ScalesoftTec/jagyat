from django.urls import path
from api import views
app_name = 'api' 


urlpatterns = [
    path('event-api/details',views.EventListView.as_view()),
    path('billing-head/details',views.BillingHeadListView.as_view()),
    path('billing-head/details/<int:pk>/',views.BillingHeadDetailView.as_view()),
    path('currency/details',views.CurrencyListView.as_view()),
    path('city/details',views.CityListView.as_view()),
    path('receipt/vouchers/details',views.RecieptVoucherListView.as_view()),
    path('payment/vouchers/details',views.PaymentVoucherListView.as_view()),
    path('jobs/details',views.JobListView.as_view()),
    path('jobs/hbl/details',views.HBLListView.as_view()),
    path('company-jobs/details',views.CompanyJobListView.as_view()),
    path('invoice/details',views.InvoiceReceivableView.as_view()),
    path('all-invoice/details',views.AllInvoiceReceivableView.as_view()),
    path('all-invoice/details/<pk>/',views.InvoiceReceivableDetailView.as_view()),
    path('rv-invoice/details',views.RecieptVoucherDetailListView.as_view()),
    path('invoice/gstr/details',views.InvoiceReceivableGSTRView.as_view()),
    path('invoice/report/details',views.InvoiceReceivableReportView.as_view()),
    path('invoice-payable/report/details',views.InvoicePayableReportView.as_view()),
    path('indirect-expense/report/details',views.IndirectExpenseReportView.as_view()),
    path('ledger/details',views.LedgerMasterListView.as_view()),
    path('party/details',views.PartyAddressListView.as_view()),
    path('party/limited/details',views.PartyAddressLimitedListView.as_view()),
    path('dsr/details',views.DSRListView.as_view()),
    path('inquiry/details',views.InquiryView.as_view()),
    path('mbl/details',views.MBLView.as_view()),
    path('job-cost-sheet/details',views.JobCostSheetView.as_view()),
    path('vendor/details',views.VendorListView.as_view()),
    path('payable/invoice-purchase-no/details',views.InvoicePayablePurchaseList.as_view()),
    path('rv/party/advance-details',views.RecieptVoucherPartyWiseListView.as_view()),
    path('pv/party/advance-details',views.PaymentVoucherPartyWiseListView.as_view()),
    path('rv/update/<pk>',views.RecieptVoucherUpdateView.as_view()),
    path('pv/update/<pk>',views.PaymentVoucherUpdateView.as_view()),
    path('cv/update/<pk>',views.ContraVoucherUpdateView.as_view()),
]