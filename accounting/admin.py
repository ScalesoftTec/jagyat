from django.contrib import admin
from accounting.models import PettyCash, ContraVoucher, InvoicePayable, InvoicePayableDetail, InvoiceReceivable,InvoiceReceivableDetail,CreditNote,CreditNoteDetail, PaymentVoucher, RecieptVoucher,Journal,JournalEntry,RecieptVoucherDetails,DebitNote,DebitNoteDetail,IndirectExpense,IndirectExpenseDetail,PaymentVoucherDetails,Manifest,IrisInvoiceSetting,TrailorExpense,TrailorExpenseDetail,Loan,LoanPaymentRecord,Salary,Voucher
from masters.models import Party,PartyAddress,currency,BillingHead
from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget,DateWidget,DateTimeWidget
from import_export.fields import Field


# Register your models here.
class InvoiceRecievableList(admin.ModelAdmin):
    search_fields = ['final_invoice_no']
    list_display = ['final_invoice_no','invoice_no','dr_ledger_category','cr_ledger_category','bill_to','company_type','is_einvoiced','is_single','is_child','old_invoice','type_of_invoice','created_at','created_by', 'is_deleted']
    list_filter = ('company_type', 'type_of_invoice','is_einvoiced','is_deleted','old_invoice','job_no__module')
    list_per_page = 100
class JournalList(admin.ModelAdmin):
    list_display = ['date','total_dr_amount','total_cr_amount','company_type','created_at','created_by', 'is_deleted']
    list_filter = ('company_type', 'date','is_deleted')
    list_per_page = 100

class JournalEntryList(admin.ModelAdmin):
    list_display = ['particular','party','amount','dr_cr']
    list_filter = ('dr_cr',)
    list_per_page = 100
class InvoiceRecDetailsList(admin.ModelAdmin):
    list_display = ['billing_head','invoice_receivable','gst','gst_amount','total']
    list_filter = ('billing_head',)
    list_per_page = 100

class InvoicePayableList(admin.ModelAdmin):
    search_fields = ['purchase_invoice_no','invoice_no']
    list_display = ['company_type','invoice_no','purchase_invoice_no','bill_from','net_amount','pending_amount','bill_from','is_rcm']
    list_filter = ('bill_from','compnay_type',)
    list_per_page = 100

class RecieptVoucherList(admin.ModelAdmin):
    search_fields = ['instrument_no']
    list_display = ['voucher_no','dr_ledger_category','cr_ledger_category','tds_ledger_category','adjustment_ledger_category','bank_charges_ledger_category','party_name','party_address','advance_amount','old_voucher']
    list_filter = ('party_name','old_voucher','is_reversed')
    list_per_page = 100

class RecieptVoucherDetailList(admin.ModelAdmin):
    list_display = ['voucher','received_amount','tds_amount','adjustment_amount']
    list_filter = ('voucher',)
    list_per_page = 100



class PaymentVoucherList(admin.ModelAdmin):
    search_fields = ['instrument_no']
    list_display = ['voucher_no','party_name','party_address','vendor','instrument_no','old_voucher','payment_type','is_deleted']
    list_filter = ('old_voucher','is_reversed','payment_type','is_deleted')
    list_per_page = 100

class InvoicePayableResource(resources.ModelResource):
    bill_from = fields.Field(
        column_name='bill_from',
        attribute='bill_from',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    bill_from_address = fields.Field(
        column_name='bill_from_address',
        attribute='bill_from_address',
        widget=ForeignKeyWidget(PartyAddress, field='party__party_name'))
    
    invoice_currency = fields.Field(
        column_name='invoice_currency',
        attribute='invoice_currency',
        widget=ForeignKeyWidget(currency, field='short_name'))
    
    date_of_invoice = Field(attribute='date_of_invoice', column_name='date_of_invoice', widget=DateWidget('%d-%b-%Y'))
    due_date = Field(attribute='due_date', column_name='due_date', widget=DateWidget('%d-%b-%Y'))
    created_at = Field(attribute='created_at', column_name='created_at', widget=DateTimeWidget('%d-%b-%Y'))
    
    

    class Meta:
        model = InvoicePayable
        import_id_fields = ['id']
       
        fields = ("id","invoice_no","purchase_invoice_no","date_of_invoice","job_no","bill_from","bill_from_address","invoice_currency","currency_ex_rate","due_date","invoice_status","gross_amount","pending_amount","gst_amount","net_amount","tds_payable","remark_on_invoice","company_type","created_at",'round_off','is_uploaded','is_rcm','tds_section','tds_percentage')

class InvoicePayableAdmin(ImportExportModelAdmin):
    resource_class = InvoicePayableResource
    search_fields = ['purchase_invoice_no','invoice_no']
    list_display = ['date_of_invoice','invoice_no','purchase_invoice_no','dr_ledger_category','cr_ledger_category','tds_ledger_category','bill_from','net_amount','pending_amount','bill_from','is_rcm']
    list_filter = ('company_type','is_deleted','date_of_invoice','old_invoice')
    list_per_page = 100
    class Meta:
        fields = '__all__'


class InvoicePayableDetailResource(resources.ModelResource):
    billing_head = fields.Field(
        column_name='billing_head',
        attribute='billing_head',
        widget=ForeignKeyWidget(BillingHead, field='billing_head'))
    
    invoice_payable = fields.Field(
        column_name='invoice_payable',
        attribute='invoice_payable',
        widget=ForeignKeyWidget(InvoicePayable, field='purchase_invoice_no'))
    
    currency = fields.Field(
        column_name='currency',
        attribute='currency',
        widget=ForeignKeyWidget(currency, field='short_name'))
    
   
    class Meta:
        model = InvoicePayableDetail
        import_id_fields = []
        fields = ('invoice_payable','billing_head','rate','qty_unit','gst','gst_amount','amount','ex_rate','currency','total')


class InvoicePayDetailsList(ImportExportModelAdmin):
    resource_class = InvoicePayableDetailResource
    search_fields = ['invoice_payable__invoice_no','invoice_payable__purchase_invoice_no']
    list_display = ['billing_head','invoice_payable','gst','gst_amount','total']
    list_filter = ('is_checked','billing_head')
    list_per_page = 100
    class Meta:
        fields = '__all__'


class DebitNoteResource(resources.ModelResource):
    bill_from = fields.Field(
        column_name='bill_from',
        attribute='bill_from',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    bill_from_address = fields.Field(
        column_name='bill_from_address',
        attribute='bill_from_address',
        widget=ForeignKeyWidget(PartyAddress, field='party__party_name'))
    
    invoice_currency = fields.Field(
        column_name='invoice_currency',
        attribute='invoice_currency',
        widget=ForeignKeyWidget(currency, field='short_name'))
    
    date_of_note = Field(attribute='date_of_note', column_name='date_of_note', widget=DateWidget('%d-%b-%Y'))
    
    created_at = Field(attribute='created_at', column_name='created_at', widget=DateTimeWidget('%d-%b-%Y'))
    
    

    class Meta:
        model = DebitNote
        import_id_fields = ['id']
       
        fields = ("id","debit_note_no","invoice_no","date_of_note","job_no","bill_from","bill_from_address","invoice_currency","currency_ex_rate","invoice_status","gross_amount","pending_amount","gst_amount","net_amount","remark_on_note","company_type","created_at",'round_off','is_uploaded','is_rcm')


class DebitNoteAdmin(ImportExportModelAdmin):
    resource_class = DebitNoteResource
    list_display = ['company_type','party_type','debit_note_no','dr_ledger_category','cr_ledger_category','date_of_note','company_type','created_at','updated_at','created_by','updated_by', 'is_deleted']
    list_filter = ('company_type','job_no','is_deleted')
    list_per_page = 100
    class Meta:
        fields = '__all__'


class DebitNoteDetailResource(resources.ModelResource):
    billing_head = fields.Field(
        column_name='billing_head',
        attribute='billing_head',
        widget=ForeignKeyWidget(BillingHead, field='billing_head'))
    
    debit_note = fields.Field(
        column_name='debit_note',
        attribute='debit_note',
        widget=ForeignKeyWidget(DebitNote, field='debit_note_no'))
    
    currency = fields.Field(
        column_name='currency',
        attribute='currency',
        widget=ForeignKeyWidget(currency, field='short_name'))
    
   
    class Meta:
        model = DebitNoteDetail
        import_id_fields = []
        fields = ('debit_note','billing_head','rate','qty_unit','gst','gst_amount','amount','ex_rate','currency','total')


class DebitNoteDetailsList(ImportExportModelAdmin):
    resource_class = DebitNoteDetailResource
    list_display = ['billing_head','debit_note','gst','gst_amount','total']
    list_filter = ('debit_note',)
    list_per_page = 100
    class Meta:
        fields = '__all__'
    
    
class ContraVoucherList(admin.ModelAdmin):
    search_fields = ['instrument_no']
    list_display = ["company_type","voucher_no","dr_ledger_category","cr_ledger_category","contra_choice","voucher_date","account_from","account_to","cash","amount","instrument_no","bank_clearing_date","bank_charges"]
    list_per_page = 100
    
class CreditNoteList(admin.ModelAdmin):
    search_fields = ['final_invoice_no','credit_note_no']
    list_display = ["credit_note_no","final_invoice_no","dr_ledger_category","cr_ledger_category","date_of_note",'einvoice_date',"gross_amount","gst_amount","net_amount",'created_at','updated_at','created_by','updated_by']
    list_per_page = 100
    

    
    
class SalaryList(admin.ModelAdmin):
    search_fields = ['bill_no']
    list_display = ["company_type","employee","bank","basic","tds_amount","esi_amount","pf_amount","net_amount","dr_ledger_category","cr_ledger_category","tds_ledger_category","esi_ledger_category","pf_ledger_category"]
    list_per_page = 100

class VoucherList(admin.ModelAdmin):
    search_fields = ['bill_no']
    list_display = ["company_type","voucher_type","bank","indirect_expense","sales_invoice","purchase_invoice","crn","drn","receipt","payment","contra","loan","loan_record","journal"]
    list_per_page = 100
    

admin.site.register(InvoiceReceivable,InvoiceRecievableList)
admin.site.register(InvoiceReceivableDetail,InvoiceRecDetailsList)
admin.site.register(InvoicePayable,InvoicePayableAdmin)
admin.site.register(InvoicePayableDetail,InvoicePayDetailsList)
admin.site.register(TrailorExpense)
admin.site.register(TrailorExpenseDetail)

admin.site.register(CreditNote,CreditNoteList)
admin.site.register(CreditNoteDetail)
admin.site.register(RecieptVoucher,RecieptVoucherList)
admin.site.register(PaymentVoucher,PaymentVoucherList)
admin.site.register(ContraVoucher,ContraVoucherList)
admin.site.register(PettyCash)

admin.site.register(Journal,JournalList)
admin.site.register(JournalEntry,JournalEntryList)
admin.site.register(RecieptVoucherDetails,RecieptVoucherDetailList)
admin.site.register(DebitNote,DebitNoteAdmin)
admin.site.register(DebitNoteDetail,DebitNoteDetailsList)
admin.site.register(IndirectExpense)
admin.site.register(IndirectExpenseDetail)
admin.site.register(PaymentVoucherDetails)
admin.site.register(Manifest)
admin.site.register(IrisInvoiceSetting)
admin.site.register(Loan)
admin.site.register(Salary,SalaryList)
admin.site.register(LoanPaymentRecord)
admin.site.register(Voucher,VoucherList)