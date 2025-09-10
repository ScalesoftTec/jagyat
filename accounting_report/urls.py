from django.urls import path
from accounting_report import views
app_name = "acr"

urlpatterns = [
    path('<module>/mis_report/',views.mis_report,name='mis_report'),
    
    # Bank Ledger
    path('<module>/bank/ledger/',views.bank_report,name='bank_report'),
    path('<module>/addBankClearingDate/<index>/',views.addBankClearingDate,name='addBankClearingDate'),
    
    # Cash Ledger
    path('<module>/cash/master/',views.cash_report,name='master_cashbook'),
    path('<module>/cash/petty/',views.petty_cashbook,name='petty_cashbook'),
    path('<module>/transfer_to_petty_cash/<int:id>/<int:index>/',views.transfer_to_petty_cash,name='transfer_to_petty_cash'),
    
    # Purchase Ledger
    path('<module>/purchase/ledger/',views.purchase_account,name='purchase_account'),
    
    # Sales Ledger
    path('<module>/sales/ledger/',views.sales_account,name='sales_account'),
    

    # Journal Book
    path('<module>/sales_invoice_journal/',views.sales_invoice_journal,name='sales_invoice_journal'),
    path('<module>/purchase_invoice_journal/',views.purchase_invoice_journal,name='purchase_invoice_journal'),
    path('<module>/indirect_expense_journal/',views.indirect_expense_journal,name='indirect_expense_journal'),
    path('<module>/crn_journal/',views.crn_journal,name='crn_journal'),
    path('<module>/drn_journal/',views.drn_journal,name='drn_journal'),
    path('<module>/reciept_voucher_journal/',views.reciept_voucher_journal,name='reciept_voucher_journal'),
    path('<module>/payment_voucher_journal/',views.payment_voucher_journal,name='payment_voucher_journal'),
    path('<module>/contra_voucher_journal/',views.contra_voucher_journal,name='contra_voucher_journal'),
    path('<module>/loan_journal/',views.loan_journal,name='loan_journal'),
    path('<module>/loan_record_journal/',views.loan_record_journal,name='loan_record_journal'),

    
    # Job Cost Sheet
    path('<module>/sale-person-performance/detail/',views.sale_person_performance_sheet,name='sale_person_performance_sheet'),
    path('<module>/job/cost/sheet/detail/',views.job_cost_sheet_detail,name='job_cost_sheet_detail'),
    path('master/job/cost/sheet/pdf/<id>/',views.job_cost_sheet_pdf,name='job_cost_sheet_pdf'),
    
   
    
    # Sales Outstanding
    path('<module>/sales-outstanding/',views.sales_outstanding_2,name='sales_outstanding'),
    path('<module>/outstanding/',views.outstading_report,name='outstading_report'),
    
    # Creditors Direct Outstanding
    path('<module>/direct-creditors-outstanding/',views.direct_creditors_outstanding_2,name='direct_creditors_outstanding'),
    
    # Creditors InDirect Outstanding
    path('<module>/indirect-creditors-outstanding/',views.indirect_creditors_outstanding_2,name='indirect_creditors_outstanding'),
    
    # Sundry Creditors
    path('<module>/sundry-creditors/detail/',views.sundry_creditors,name='sundry_creditors'),
    
    
    
    # Sundry Debtors
    path('<module>/sundry-debtors/detail/',views.sundry_debtors,name='sundry_debtors'),
    
    # Party Ledger
    path('<module>/party/ledger/detail/',views.PartyLedger,name='PartyLedger'),
    path('<module>/party/ledger/detail/<int:generate_report_pdf>/',views.PartyLedger,name='PartyLedger'),
    
    # Party Wise Outstanding
    path('<module>/party-wise/outstanding/detail/',views.party_wise_outstanding,name='party_wise_outstanding'),
    
    # Party Wise Outstanding Summary
    path('<module>/party-summary/outstanding/detail/',views.party_outstanding_summary,name='party_outstanding_summary'),
    
    # Sales And Purchase Register
    path('<module>/sales-register/',views.sales_register,name='sales_register'),
    path('<module>/purchase-register/',views.purchase_register,name='purchase_register'),
    path('<module>/sale-purchase-profit-loss/',views.sale_purchase_profit_loss,name='sale_purchase_profit_loss'),
    
    
    # Reciept TDS
    path('<module>/reciept/tds/detail/',views.reciept_tds,name='reciept_tds'),
    path('<module>/reciept_tds_claim_action/',views.reciept_tds_claim_action,name='reciept_tds_claim_action'),
    
    
    # Payment TDS
    path('<module>/payment/tds/detail/',views.payment_tds,name='payment_tds'),
    
    # GSTR1
    path('<module>/gstr1/recievable/detail/',views.gstr1_recievable_server_side,name='gstr1_recievable'),
    path('<module>/gstr1/hsn/recievable/detail/',views.gstr1_hsn_recievable,name='gstr1_hsn_recievable'),
    path('gstr1/excel/detail/',views.exportGSTR1DetailsExcel,name='exportGSTR1DetailsExcel'),
    
    
    # GSTR2
    path('<module>/gstr2/payable/detail/',views.gstr2_payable,name='gstr2_payable'),
    
    # GSTR3B
    path('<module>/gstr3b/detail/',views.gstr3b,name='gstr3b'),
    
    # Ageing Analysis
    path('<module>/ageing-analysis/detail/',views.ageing_analysis,name='ageing_analysis'),
    path('<module>/ageing-analysis-details/detail/<type>/<company>/<int:party>/<range>/',views.ageing_analysis_details,name='ageing_analysis_details'),
    

    
    # Ledger Report
    path('<module>/ledger-report/', views.ledger_report, name='ledger_report'),

    # Trial Balance Report
    path('<module>/trial_balance_report/', views.trial_balance_report_category, name='trial_balance_report'),
    path('<module>/trial_balance_pdf/', views.trial_balance_pdf, name='trial_balance_pdf'),


    # Ledger Category Transactions
    path('<module>/lct/<company>/<from_date>/<to_date>/<int:id>/', views.ledger_category_transactions, name='ledger_category_transactions'),
    path('<module>/lct/<company>/<from_date>/<to_date>/<int:id>/<profit_loss>/', views.ledger_category_transactions, name='ledger_category_transactions'),

    path('<module>/lct/<company>/<from_date>/<to_date>/<int:id>/<int:detail_id>/<profit_loss>/<int:detail>', views.ledger_category_transactions, name='ledger_category_transactions'),
    path('<module>/lct/<company>/<from_date>/<to_date>/<int:id>/<int:detail_id>/<profit_loss>/<int:detail>/<type>', views.ledger_category_transactions, name='ledger_category_transactions'),
    
    path('<module>/lct/<company>/<from_date>/<to_date>/<int:id>/<int:detail_id>/<int:detail>/<int:expanded>', views.ledger_category_transactions, name='ledger_category_transactions'),
    path('<module>/lct/<company>/<from_date>/<to_date>/<int:id>/<int:detail_id>/<int:detail>/<type>', views.ledger_category_transactions, name='ledger_category_transactions'),
    path('<module>/lct/<company>/<from_date>/<to_date>/<int:id>/<int:detail_id>/<int:detail>/<type>/<int:expanded>', views.ledger_category_transactions, name='ledger_category_transactions'),
    
    # Profit & Loss Report
    path('<module>/profit_loss_report/', views.profit_loss_report, name='profit_loss_report'),


    # Balance Sheet Report
    path('<module>/balance_sheet_report/', views.balance_sheet_report_category, name='balance_sheet_report'),
    path('<module>/balance_sheet_pdf/', views.balance_sheet_pdf, name='balance_sheet_pdf'),


    
]