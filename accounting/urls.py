from django.urls import path
from accounting import views

app_name="accounting"

urlpatterns = [
   # Trailor Expense
    path('<module>/expense/trailor/create/',views.create_trailor_expense,name='create_trailor_expense'),
    path('<module>/master/update/trailor/expense/<id>/',views.trailor_expense_update,name='trailor_expense_update'),
    path('<module>/expense/trailor/detail/',views.trailor_expense_details,name='trailor_expense_details'),
    path('<module>/master/delete/trailor-expense/<id>/',views.trailor_expense_delete,name='trailor_expense_delete'),

   
    # Invoice Recievables
    path('<module>/invoice/recievable/create/',views.create_recievable_invoice,name='create_recievable_invoice'),
    path('<module>/invoice/recievable/detail/',views.recievable_invoice_details,name='recievable_invoice_details'),
    path('<module>/master/update/recievable/invoice/<id>/',views.recievable_invoice_update,name='recievable_invoice_update'),
    path('<module>/master/delete/recievable-invoice/<id>/',views.recievable_invoice_delete,name='recievable_invoice_delete'),
    path('<module>/e-invoice/recievable/detail/',views.e_invoice_recievable_details,name='e_invoice_recievable_details'),
    path('<module>/final-invoice/recievable/detail/',views.final_invoice_recievable_details,name='final_invoice_recievable_details'),
    path('<module>/master/create-einvoice/recievable-invoice/<id>/',views.make_eninvoice_recievable,name='make_eninvoice_recievable'),


    path('recievable-invoice/pdf/<id>/',views.recievable_invoice_pdf,name='recievable_invoice_pdf'),
    path('recievable-invoice/print/pdf/<id>/',views.recievable_invoice_print_pdf,name='recievable_invoice_print_pdf'),
    path('<module>/send-invoice/pdf/<id>/<from_url>/',views.send_rec_invoice,name='send_rec_invoice'),

    # path('payment/invoice/pdf/<id>/',views.payment_invoice_pdf,name='payment_invoice_pdf'),

    
    # Credit Note
    path('<module>/credit-note/create/',views.create_credit_note,name='create_credit_note'),
    path('<module>/credit-note/detail/',views.credit_note_details,name='credit_note_details'),
    path('<module>/e-credit-note/detail/',views.e_credit_note_details,name='e_credit_note_details'),
    path('<module>/final-credit-note/detail/',views.final_credit_note_details,name='final_credit_note_details'),
    path('<module>/master/update/credit-note/<id>/',views.credit_note_update,name='credit_note_update'),
    path('<module>/master/delete/credit-note/<id>/',views.credit_note_delete,name='credit_note_delete'),
    path('master/credit-note/pdf/<id>/',views.crn_pdf,name='credit_note_pdf'),
    path('master/credit-note/print/pdf/<id>/',views.crn_print_pdf,name='crn_print_pdf'),
    path('<module>/master/einvoice/credit-note/<id>/',views.make_eninvoice_credit_note,name='make_eninvoice_credit_note'),

   
    # Reciept Voucher
    path('reciept-voucher/pdf/<id>/',views.receipt_voucher_pdf,name='receipt_voucher_pdf'), 
    path('billwise/reciept-voucher/pdf/<id>/',views.bill_wise_receipt_voucher_pdf,name='bill_wise_receipt_voucher_pdf'), 
    
  
    
    # New Payment Voucher
    path('<module>/payment-voucher/create/',views.create_payment_voucher,name='create_payment_voucher'),
    path('<module>/update/payment-voucher/<id>/',views.payment_voucher_update,name='payment_voucher_update'),
    path('<module>/details/payment-voucher',views.payment_voucher_details,name='payment_voucher_details'),
    path('<module>/delete/payment-voucher/<id>',views.payment_voucher_delete,name='payment_voucher_delete'),
    
    # New Reciept Voucher
    path('<module>/reciept-voucher/create/',views.create_reciept_voucher,name='create_reciept_voucher'),
    path('<module>/update/reciept-voucher/<id>/',views.reciept_voucher_update,name='reciept_voucher_update'),
    path('<module>/details/reciept-voucher',views.reciept_voucher_details,name='reciept_voucher_details'),
    path('<module>/delete/reciept-voucher/<id>',views.reciept_voucher_delete,name='reciept_voucher_delete'),
    
    # Contra Voucher
    path('<module>/contra-voucher/create/',views.create_contra_voucher,name='create_contra_voucher'),
    path('<module>/contra-voucher/detail/',views.contra_voucher_details,name='contra_voucher_details'),
    path('<module>/master/update/contra-voucher/<id>/',views.contra_voucher_update,name='contra_voucher_update'),
    path('<module>/master/delete/contra-voucher/<id>/',views.contra_voucher_delete,name='contra_voucher_delete'),
    
    
    # Debit Note
    path('<module>/debit-note/create/',views.create_debit_note,name='create_debit_note'),
    path('<module>/debit-note/detail/',views.debit_note_details,name='debit_note_details'),
    path('<module>/master/update/debit-note/<id>/',views.debit_note_update,name='debit_note_update'),
    path('<module>/master/delete/debit-note/<id>/',views.debit_note_delete,name='debit_note_delete'),
    path('master/debit-note/pdf/<id>/',views.drn_pdf,name='debit_note_pdf'),
    
    # Invoice Payable
    path('<module>/invoice/payable/create',views.create_invoice_payable,name='create_invoice_payable'),
    path('<module>/invoice/payable/detail/',views.invoice_payable_details,name='invoice_payable_details'),
    path('<module>/master/update/invoice/payable/<id>',views.invoice_payable_update,name='invoice_payable_update'),
    path('<module>/master/adjustment/invoice/payable/<id>/',views.invoice_payable_adjustment,name='invoice_payable_adjustment'),
    path('<module>/master/delete/invoice/payable/<id>/',views.invoice_payable_delete,name='invoice_payable_delete'),
    path('<module>/master/approve/invoice/payable/<id>/',views.approve_invoice_payable,name='approve_invoice_payable'),
    path('master/invoice-payable/pdf/<id>/',views.invoice_payable_pdf,name='invoice_payable_pdf'),
    

    # Journal
    path('<module>/create_journal/', views.create_journal, name='create_journal'),
    path('<module>/journal_details/', views.journal_details, name='journal_details'),
    path('<module>/journal_update/<int:id>/', views.journal_update, name='journal_update'),
    path('<module>/journal_delete/<int:id>/', views.journal_delete, name='journal_delete'),

    # Tally Master
    path('set-party-group/tally/',views.set_party_tally_group,name='set_party_tally_group'),

    path('<module>/party/tally/',views.party_details_tally,name='party_details_tally'),
    

    # Tally 6 January 2025
    path('<module>/bh/tally/',views.bh_details_tally,name='bh_details_tally'),
    
    # Sales Invoice Tally
    path('<module>/sales-invoice-details/tally/',views.sales_invoice_details_tally,name='sales_invoice_details_tally'),
    path('<module>/sales-invoice-export/tally/',views.sales_invoice_export_tally,name='sales_invoice_export_tally'),
    
    # Receipts Voucher Tally
    path('<module>/receipt-voucher-details/tally/',views.reciept_details_tally,name='reciept_details_tally'),
    path('<module>/receipt-voucher-export/tally/',views.reciept_export_tally,name='reciept_export_tally'),
    
    # Payment Voucher Tally
    path('<module>/payment-voucher-details/tally/',views.payment_details_tally,name='payment_details_tally'),
    path('<module>/payment-voucher-export/tally/',views.payment_export_tally,name='payment_export_tally'),
    
    # Purchase Invoice Tally
    path('<module>/purchase-invoice-details/tally/',views.purchase_invoice_details_tally,name='purchase_invoice_details_tally'),
    path('<module>/purchase-invoice-export/tally/',views.purchase_invoice_export_tally,name='purchase_invoice_export_tally'),
    path('<module>/master/details/bop/',views.bop_details,name='bop_details'),

    
 
 
]
