from django.db import models
from masters.models import Bank, BillingHead, CategoryMaster,TrailorBillingHead, JobMaster,Party,Location,ShippingLines,currency,Airlines,LogFolder,LedgerMaster,Ports,Vendor,PartyAddress,TrailorMaster,DriverMaster,OWNERHIRE,GRMaster,JobHBL,LedgerCategory
from django.contrib.auth.models import User
from dashboard.models import Logistic
from home.models import DocumentHandler
from crm.models import Inquiry
import qrcode
from django.core.files import File
from io import BytesIO
from datetime import date,datetime,timedelta
import calendar
from PIL import Image
from django.db.models import Sum
from hr.models import Employee
import pyqrcode
from pyqrcode import QRCode
import png



DR_CR = (
    ('Debit','Debit'),
    ('Credit','Credit'),
)

PARTY_TYPE = (
    ('Direct','Direct'),
    ('Indirect','Indirect'),
)

DR_CR = (
    ('Debit','Debit'),
    ('Credit','Credit'),
)

PARTY_TYPE = (
    ('Direct','Direct'),
    ('Indirect','Indirect'),
)

GST_TYPE = (
    ('CGST 2.5% IN','CGST 2.5% IN'),
    ('CGST 2.5% OUT','CGST 2.5% OUT'),
    ('SGST 2.5% IN','SGST 2.5% IN'),
    ('SGST 2.5% OUT','SGST 2.5% OUT'),
    ('IGST 5% IN','IGST 5% IN'),
    ('IGST 5% OUT','IGST 5% OUT'),
    
    ('CGST 6% IN','CGST 6% IN'),
    ('CGST 6% OUT','CGST 6% OUT'),
    ('SGST 6% IN','SGST 6% IN'),
    ('SGST 6% OUT','SGST 6% OUT'),
    ('IGST 12% IN','IGST 12% IN'),
    ('IGST 12% OUT','IGST 12% OUT'),
    
    ('CGST 9% IN','CGST 9% IN'),
    ('CGST 9% OUT','CGST 9% OUT'),
    ('SGST 9% IN','SGST 9% IN'),
    ('SGST 9% OUT','SGST 9% OUT'),
    ('IGST 18% IN','IGST 18% IN'),
    ('IGST 18% OUT','IGST 18% OUT'),
    
    ('CGST 14% IN','CGST 14% IN'),
    ('CGST 14% OUT','CGST 14% OUT'),
    ('SGST 14% IN','SGST 14% IN'),
    ('SGST 14% OUT','SGST 14% OUT'),
    ('IGST 28% IN','IGST 28% IN'),
    ('IGST 28% OUT','IGST 28% OUT'),
)


Choose_tds_section=(
    ('TDS RECEIVABLE','TDS RECEIVABLE'),
    ('TDS PAYABLE','TDS PAYABLE'),
    ('192','192'),
    ('192A','192A'),
    ('194C','194C'),
    ('194H','194H'),
    ('194I','194I'),
    ('194J','194J'),
    ('PPH23','PPH23'),
    ('PP','PP'),
    ('WHT','WHT'),
)


class Voucher(models.Model):
    company_type = models.ForeignKey(Logistic,related_name='voucher_company',null=True,blank=True,on_delete=models.SET_NULL)
    voucher_type = models.CharField(max_length=120,null=True,blank=True)
    amount = models.FloatField(default=0,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    category = models.ForeignKey(LedgerCategory,related_name='voucher_category',null=True,blank=True,on_delete=models.SET_NULL)
    salary = models.ForeignKey('accounting.Salary',on_delete=models.CASCADE,null=True,blank=True,related_name="salary_voucher")
    indirect_expense = models.ForeignKey('accounting.IndirectExpense',on_delete=models.CASCADE,null=True,blank=True,related_name="expense_voucher")
    sales_invoice = models.ForeignKey('accounting.InvoiceReceivable',on_delete=models.CASCADE,null=True,blank=True,related_name="sales_voucher")
    sales_invoice_details = models.ForeignKey('accounting.InvoiceReceivableDetail',on_delete=models.CASCADE,null=True,blank=True,related_name="sales_details_voucher")
    purchase_invoice = models.ForeignKey('accounting.InvoicePayable',on_delete=models.CASCADE,null=True,blank=True,related_name="purchase_voucher")
    purchase_invoice_details = models.ForeignKey('accounting.InvoicePayableDetail',on_delete=models.CASCADE,null=True,blank=True,related_name="purchase_details_voucher")
    crn = models.ForeignKey('accounting.CreditNote',on_delete=models.CASCADE,null=True,blank=True,related_name="crn_voucher")
    crn_details = models.ForeignKey('accounting.CreditNoteDetail',on_delete=models.CASCADE,null=True,blank=True,related_name="crn_details_voucher")
    drn = models.ForeignKey('accounting.DebitNote',on_delete=models.CASCADE,null=True,blank=True,related_name="drn_voucher")
    drn_details = models.ForeignKey('accounting.DebitNoteDetail',on_delete=models.CASCADE,null=True,blank=True,related_name="drn_details_voucher")
    receipt = models.ForeignKey('accounting.RecieptVoucher',on_delete=models.CASCADE,null=True,blank=True,related_name="receipt_voucher")
    payment = models.ForeignKey('accounting.PaymentVoucher',on_delete=models.CASCADE,null=True,blank=True,related_name="payment_voucher")
    contra = models.ForeignKey('accounting.ContraVoucher',on_delete=models.CASCADE,null=True,blank=True,related_name="contra_voucher")
    loan = models.ForeignKey('accounting.Loan',on_delete=models.CASCADE,null=True,blank=True,related_name="loan_voucher")
    loan_record = models.ForeignKey('accounting.LoanPaymentRecord',on_delete=models.CASCADE,null=True,blank=True,related_name="loan_record_voucher")
    journal = models.ForeignKey('accounting.Journal',on_delete=models.CASCADE,null=True,blank=True,related_name="jv_voucher")
    journal_entry = models.ForeignKey('accounting.JournalEntry',on_delete=models.CASCADE,null=True,blank=True,related_name="jv_entry_voucher")
    
    party_opening = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_party_opening')
    vendor_opening = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_vendor_opening')
    bank_opening = models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_bank_opening')
    ledger_opening = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_ledger_opening')

    ledger = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_ledger')
    party = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_party')
    party_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_party_address')
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_vendor')
    bank = models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_bank')
    cash = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_cash')
    employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True,related_name='voucher_employee')

    gst_type = models.CharField(max_length=50,null=True,blank=True,choices=GST_TYPE)
    tds_section = models.CharField(max_length=50,null=True,blank=True,choices=Choose_tds_section)
    dr_cr = models.CharField(max_length=10,null=True,blank=True,choices=DR_CR)


def createVoucher(voucher_type,amount,category,dr_cr,salary=None,indirect_expense=None,sales_invoice=None,purchase_invoice=None,crn=None,drn=None,receipt=None,payment=None,contra=None,loan=None,loan_record=None,journal=None,party=None,party_address=None,vendor=None,bank=None,employee=None,cash=None,gst_type=None,sales_invoice_details=None,date=None,company_type=None,purchase_invoice_details=None,tds_section=None,crn_details=None,drn_details=None,ledger=None,party_opening=None,ledger_opening=None,vendor_opening=None,bank_opening=None,journal_entry=None):
    if amount == 0:
        return
    voucher = Voucher.objects.create(voucher_type=voucher_type,amount=amount,category=category,dr_cr=dr_cr)

    if gst_type:
        voucher.gst_type = gst_type
    if ledger:
        voucher.ledger = ledger
    if party:
        voucher.party = party
    if party_address:
        voucher.party_address = party_address
    if vendor:
        voucher.vendor = vendor
    if bank:
        voucher.bank = bank
    if employee:
        voucher.employee = employee
    if cash:
        voucher.cash = cash

    if salary:
        voucher.salary = salary
        voucher.company_type = salary.company_type
        voucher.date = salary.date

    if indirect_expense:
        voucher.indirect_expense = indirect_expense
        voucher.company_type = indirect_expense.company_type
        voucher.date = indirect_expense.bill_date
    
    if party_opening:
        voucher.party_opening = party_opening
        voucher.company_type = party_opening.company_type
        voucher.date = party_opening.opening_date
    
    if ledger_opening:
        voucher.ledger_opening = ledger_opening
        voucher.company_type = ledger_opening.company_type
        voucher.date = ledger_opening.opening_date
    
    if bank_opening:
        voucher.bank_opening = bank_opening
        voucher.company_type = bank_opening.company_type
        voucher.date = bank_opening.opening_date
    
    if vendor_opening:
        voucher.vendor_opening = vendor_opening
        voucher.company_type = vendor_opening.company_type
        voucher.date = vendor_opening.opening_date

    if sales_invoice_details:
        voucher.sales_invoice_details = sales_invoice_details
        voucher.date = date
        voucher.company_type = company_type
        
    if sales_invoice:
        voucher.sales_invoice = sales_invoice
        voucher.company_type = sales_invoice.company_type
        if sales_invoice.is_einvoiced:
            
            voucher.date = sales_invoice.einvoice_date.date()
        else:
            voucher.date = sales_invoice.date_of_invoice


    if purchase_invoice_details:
        voucher.purchase_invoice_details = purchase_invoice_details
        voucher.company_type = company_type
        voucher.date = date
        
    if tds_section:
        voucher.tds_section = tds_section

        
    if purchase_invoice:
        voucher.purchase_invoice = purchase_invoice
        voucher.company_type = purchase_invoice.company_type
        voucher.date = purchase_invoice.date_of_invoice
    
    if crn:
        voucher.crn = crn
        voucher.company_type = crn.company_type
       

        if crn.is_einvoiced:
            voucher.date = crn.einvoice_date.date()
        else:
            voucher.date = crn.date_of_note
    
    if crn_details:
        voucher.crn_details = crn_details
        voucher.company_type = company_type
        voucher.date = date
    
    if drn_details:
        voucher.drn_details = drn_details
        voucher.company_type = company_type
        voucher.date = date

    
    if drn:
        voucher.drn = drn
        voucher.company_type = drn.company_type
        voucher.date = drn.date_of_note

    if receipt:
        voucher.receipt = receipt
        voucher.company_type = receipt.company_type
        voucher.date = receipt.voucher_date

    if payment:
        voucher.payment = payment
        voucher.company_type = payment.company_type
        voucher.date = payment.voucher_date

    if contra:
        voucher.contra = contra
        voucher.company_type = contra.company_type
        voucher.date = contra.voucher_date

    if loan:
        voucher.loan = loan
        voucher.company_type = loan.company_type
        voucher.date = loan.loan_date
        
    if loan_record:
        voucher.loan_record = loan_record
        voucher.company_type = loan_record.loan.company_type
        voucher.date = loan_record.payment_date
    
    if journal:
        voucher.journal = journal
        voucher.journal_entry = journal_entry
        voucher.company_type = journal.company_type
        voucher.date = journal.date

    voucher.save()




class Journal(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=False,blank=False,related_name="journal_company")
    date = models.DateField(null=True,blank=True)
    total_dr_amount = models.FloatField(default=0)
    total_cr_amount = models.FloatField(default=0)
    description = models.TextField(null=True,blank=True)
    auto_generated = models.BooleanField(default=True)
    class Meta:
        ordering = ('date',)

DR_CR = (
    ('Debit','Debit'),
    ('Credit','Credit'),
)

class JournalEntry(LogFolder):
    voucher = models.ForeignKey(Journal,on_delete=models.CASCADE,null=True,blank=True,related_name="journal_entry")
    
    particular = models.TextField(null=True,blank=True)
    
    ledger = models.ForeignKey(LedgerMaster,on_delete=models.CASCADE,null=True,blank=True,related_name="account_ledger")
    
    party = models.ForeignKey(Party,on_delete=models.CASCADE,null=True,blank=True,related_name="account_party")
    
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True,blank=True,related_name="account_vendor")
    
    amount = models.FloatField(default=0)
    dr_cr = models.CharField(max_length=10,choices=DR_CR)

INV = (
    ("Open", "Open"),
    ("Close", "Close"),
    ("Cancel", "Cancel"),
)

MOD = (
    ("Sea Export", "Sea Export"),
    ("Sea Import", "Sea Import"),
    ("Air Export", "Air Export"),
    ("Air Import", "Air Import"),
    )

INVOICE_MODE = (
    ("Overseas Invoice", "Overseas Invoice"),
    ("Local Invoice", "Local Invoice"),
    )

INVOICE_TYPE = (
    ('TAX INVOICE','TAX INVOICE'),
    ('BILL OF SUPPLY','BILL OF SUPPLY'),
    ('RCM','RCM')
)

Choose_tds_section=(
    ('192','192'),
    ('192A','192A'),
    ('194C','194C'),
    ('194H','194H'),
    ('194I','194I'),
    ('194J','194J'),
    ('PPH23','PPH23'),
    ('PP','PP'),
    ('WHT','WHT'),
)

class Salary(LogFolder):
    company_type = models.ForeignKey(Logistic,related_name='salary_company',null=True,blank=True,on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,null=True,blank=True,related_name="employee_salary",on_delete=models.SET_NULL)
    bank = models.ForeignKey(Bank,null=True,blank=True,related_name="bank_salary",on_delete=models.SET_NULL)
    salary_currency = models.ForeignKey(currency,null=True,blank=True,related_name="bank_currency",on_delete=models.SET_NULL)
    date = models.DateField(null=True,blank=True)
    basic = models.FloatField(default=0)
    tds_amount = models.FloatField(default=0)
    esi_amount = models.FloatField(default=0)
    pf_amount = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    # Ledger Category
    
    dr_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,related_name='salary_dr_category',default=16,blank=True, null=True)
    
    cr_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,related_name='salary_cr_category',default=13,blank=True, null=True)
    
    tds_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,related_name='salary_tds_category',default=11,blank=True, null=True)
    
    esi_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,related_name='salary_esi_category',default=11,blank=True, null=True)
    
    pf_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,related_name='salary_pf_category',default=11,blank=True, null=True)

    def __str__(self) -> str:
        return self.employee

    def save(self,*args,**kwargs):
        
        self.net_amount = self.basic - (self.tds_amount + self.esi_amount + self.pf_amount)
        
        
        return super(Salary,self).save(*args,**kwargs)
    
# Create your models here.

# Create your models here.
class TrailorExpense(LogFolder):
    journal = models.ForeignKey(Journal,on_delete=models.SET_NULL,null=True,blank=True,related_name='trailor_exp_journal')
    company_type = models.ForeignKey(Logistic,related_name='trailor_expense_company',null=True,blank=True,on_delete=models.SET_NULL)
    job_no = models.ForeignKey(JobMaster,related_name='trailor_exp_job',null=True,blank=True,on_delete=models.SET_NULL)
    trailor_no = models.ForeignKey(TrailorMaster,on_delete=models.SET_NULL,related_name='trailor_exp_tn',null=True,blank=True)
    driver = models.ForeignKey(DriverMaster,on_delete=models.SET_NULL,related_name='trailor_exp_driver',null=True,blank=True)
    container_no = models.CharField(max_length=120,blank=True, null=True)
    cash_expense = models.FloatField(default=0)
    card_expense = models.FloatField(default=0)
    fast_card_expense = models.FloatField(default=0)
    pump_expense = models.FloatField(default=0)
    customer_expense = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    own_hire = models.CharField(max_length=30,choices=OWNERHIRE,default='Owned')
    file1 = models.FileField(null=True,blank=True,upload_to="trailor_expense/")
    file2 = models.FileField(null=True,blank=True,upload_to="trailor_expense/")
    file3 = models.FileField(null=True,blank=True,upload_to="trailor_expense/")
    

    
    remarks = models.TextField(null=True,blank=True)
   
    def __str__(self):
        return str(self.job_no)
    


PAYMENT_TYPE = (
    ('CASH','CASH'),
    ('DIESEL CARD','DIESEL CARD'),
    ('FASTTAG CARD','FASTTAG CARD'),
    ('PUMP','PUMP'),
    ('DIRECT CUSTOMER','DIRECT CUSTOMER'),
)

class TrailorExpenseDetail(LogFolder):
    expense = models.ForeignKey(TrailorExpense,related_name="trailor_expense_reference",null=True,on_delete=models.CASCADE)
    billing_head = models.ForeignKey(TrailorBillingHead,related_name='trailor_expense_billing_head',null=True, blank=True, on_delete=models.SET_NULL)
    vendor = models.ForeignKey(Vendor,related_name='trailor_expense_vendor',null=True, blank=True, on_delete=models.SET_NULL)
    party = models.ForeignKey(Party,related_name='trailor_expense_party',null=True, blank=True, on_delete=models.SET_NULL)
    party_address = models.ForeignKey(PartyAddress,related_name='trailor_expense_party_address',null=True, blank=True, on_delete=models.SET_NULL)
    invoice = models.ForeignKey('accounting.InvoiceReceivable',related_name='trailor_expense_party_invoice',null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(null=True,blank=True)
    charges = models.FloatField(default=0)
    paid_amount = models.FloatField(default=0,null=True,blank=True)
    remarks = models.CharField(max_length=120,null=True,blank=True)
    payment_type = models.CharField(max_length=30,choices=PAYMENT_TYPE,default='CASH')
  
class IndirectExpense(LogFolder):
    # journal = models.ForeignKey(Journal,on_delete=models.SET_NULL,null=True,blank=True,related_name='indirect_exp_journal')
    company_type = models.ForeignKey(Logistic,related_name='indirect_expense_company',null=True,blank=True,on_delete=models.CASCADE)
    job_no = models.ForeignKey(JobMaster,related_name='indirect_exp_job',null=True,blank=True,on_delete=models.SET_NULL)
    bill_no = models.CharField(max_length=200,null=True,blank=True)
    bill_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,related_name='billing_vendor',blank=True, null=True)
    remarks = models.TextField(null=True,blank=True)
    gross_amount = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    advance_amount = models.FloatField(default=0,null=True,blank=True)
    net_amount = models.FloatField(default=0)
    pending_amount = models.FloatField(default=0,null=True,blank=True)
    is_final = models.BooleanField(default=False)
    old_invoice = models.BooleanField(default=False)
    tds_amount = models.FloatField(default=0,blank=True,null=True)
    file1 = models.FileField(null=True,blank=True,upload_to="indirect_expense/")
    file2 = models.FileField(null=True,blank=True,upload_to="indirect_expense/")
    file3 = models.FileField(null=True,blank=True,upload_to="indirect_expense/")
    claim_date = models.DateField(null=True,blank=True)
    currency_ex_rate = models.FloatField(default=1)
    invoice_currency = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True,related_name="indirect_expense_currency")
    tds_section=models.CharField(max_length=200,choices=Choose_tds_section,null=True,blank=True)
    tds_percentage = models.IntegerField(default=0,blank=True)
    
   
    is_transfered = models.BooleanField(default=False,null=True,blank=True)
    
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,default=16,related_name='billing_ledger_dr_category',blank=True, null=True)
    cr_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,default=13,related_name='billing_ledger_cr_category',blank=True, null=True)
    tds_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,default=11,related_name='tds_ledger_dr_category',blank=True, null=True)
    cgst_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,default=11,related_name='cgst_ledger_expense_category',blank=True, null=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,default=11,related_name='sgst_ledger_expense_category',blank=True, null=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,default=11,related_name='igst_ledger_expense_category',blank=True, null=True)

    def __str__(self):
        return str(self.bill_no)
    
    def save(self,*args,**kwargs):
        
        if self.old_invoice:
            self.dr_ledger_category = LedgerCategory.objects.filter(id=1).first()
            
        
        return super(IndirectExpense,self).save(*args,**kwargs)
    
class IndirectExpenseDetail(LogFolder):
    expense = models.ForeignKey(IndirectExpense,related_name="indirect_expense_reference",null=True,on_delete=models.CASCADE)
    billing_head = models.ForeignKey(BillingHead,related_name='indirect_expense_billing_head',null=True, blank=True, on_delete=models.CASCADE)
    ex_rate = models.FloatField(default=1)
    rate = models.FloatField(default=0)
    qty_unit = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    gst = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    currency = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True,related_name="indirect_expense_detail_currency")


INVOICE_TYPE_2 = (
    ('ORIGINAL','ORIGINAL'),
    ('DUPLICATE','DUPLICATE'),
    ('TRIPLICATE','TRIPLICATE'),
)
GST_APPLICABLE = (
    ('Yes','Yes'),
    ('No','No'),
)

INVOICE_CATEGORY = (
    ('B2B','B2B'),
    ('B2CL','B2CL'),
    ('B2CS','B2CS'),
    ('DE','DE'),
    ('SEWOP','SEWOP'),
    ('SEWP','SEWP'),
    ('EXWP','EXWP'),
    ('EXWOP','EXWOP'),
)

SUPPLY_TYPE = (
    ('O','Outward'),
    ('I','Inward'), 
)



def create_qr_code(self):
    data = self.signed_qr_code
    qrcode = pyqrcode.create(data)

    # Create a temporary PNG file in memory
    buffer = BytesIO()
    qrcode.png(buffer, scale=6)  # Adjust scale for resolution
    buffer.seek(0)

    # Convert PNG (from pyqrcode) to JPEG using PIL
    image = Image.open(buffer).convert('RGB')

    # Save final image in JPEG format to a new buffer
    jpeg_buffer = BytesIO()
    image.save(jpeg_buffer, format='png')
    jpeg_buffer.seek(0)

    # Save to Django ImageField
    fname = f'qr_code{self.signed_qr_code[:5]}{self.id}.png'
    self.qr_code_image.save(fname, File(jpeg_buffer), save=False)

    # Close buffers
    buffer.close()
    jpeg_buffer.close()
    image.close()        


class InvoiceReceivable(LogFolder):
    invoice_no = models.CharField(max_length=200,null=True,blank=True)
    final_invoice_no = models.CharField(max_length=200,null=True,blank=True)
    qr_code = models.TextField(null=True,blank=True)
    einvoice_date = models.DateTimeField(null=True,blank=True)
    signed_qr_code = models.TextField(null=True,blank=True)
    irn_no = models.TextField(null=True,blank=True)
    ack_no = models.CharField(max_length=200,null=True,blank=True)
    einvoice_id = models.CharField(max_length=200,null=True,blank=True)
    category = models.CharField(max_length=200,default="B2B",choices=INVOICE_CATEGORY)
    date_of_invoice = models.DateField(blank=True, null=True)
    # journal = models.ForeignKey(Journal,on_delete=models.SET_NULL,null=True,blank=True,related_name='rec_inv_journal')
    due_date = models.DateField(blank=True, null=True)
    job_no = models.ForeignKey(JobMaster, on_delete=models.CASCADE, null=True,related_name='recievable_invoice_job',blank=True)
    mode_of_invoice = models.CharField(max_length=200,choices=INVOICE_MODE, null=True, blank=True,default="Local Invoice")
    bill_to = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True,blank=True,related_name='recievable_invoice_bill_to')
    bill_to_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='bill_address')
    shipper = models.ForeignKey(Party, on_delete=models.SET_NULL,blank=True, null=True,related_name='recievable_invoice_shipper')
    shipper_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='shipper_address')
    gst_applicable = models.CharField(max_length=10,default="Yes",choices=GST_APPLICABLE)
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="inv_rec_company_type")
    is_proforma = models.BooleanField(default=True)
    invoice_currency = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True,related_name="invoice_rec_currency")
    quotation = models.ForeignKey(Inquiry,on_delete=models.SET_NULL,null=True,blank=True,related_name="quotation")
    currency_ex_rate = models.FloatField(default=1)
    inv_type_2 = models.CharField(max_length=50,null=True,blank=True,choices=INVOICE_TYPE_2)
    gross = models.CharField(max_length=50,null=True,blank=True)
    volume = models.CharField(max_length=50,null=True,blank=True)
    nett = models.CharField(max_length=50,null=True,blank=True)
    invoice_status = models.CharField(max_length=50,null=True,blank=True,choices=INV,default="Open")
    type_of_invoice = models.CharField(max_length=200, default="TAX INVOICE",choices=INVOICE_TYPE)   
    account_number = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True,related_name='recievable_invoice_account_no',blank=True)
    gross_amount = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    advance_amount = models.FloatField(default=0,null=True,blank=True)
    net_amount = models.FloatField(default=0)
    remark_on_invoice = models.CharField(max_length=300, null=True, blank=True)
    tax_status = models.CharField(max_length=200,null=True,blank=True,default='Unpaid')
    sales_person = models.CharField(max_length=100, null=True, blank=True)
    pending_amount = models.FloatField(default=0,blank=True)
    application_handler = models.ForeignKey(DocumentHandler,null=True,blank=True,on_delete=models.SET_NULL,related_name="rec_inv_approver")
    is_einvoiced = models.BooleanField(default=False)
    qr_code_image = models.ImageField(upload_to='rec_inv/qr_codes/',null=True,blank=True)
    gr_options = models.ManyToManyField(GRMaster,blank=True,related_name='invoice_gr')
    hbl_options = models.ManyToManyField(JobHBL,blank=True,related_name='invoice_job_hbl')
    old_invoice = models.BooleanField(default=False,blank=True)
    is_cancel = models.BooleanField(default=False)
    tds_section=models.CharField(max_length=200,choices=Choose_tds_section,null=True,blank=True)
    tds_percentage = models.IntegerField(default=0,blank=True)
    tds_payable = models.FloatField(default=0,blank=True)
    detention_from = models.DateField(null=True,blank=True)
    detention_to = models.DateField(null=True,blank=True)
    deductible_amount=models.FloatField(default=0,blank=True)
    tds_claimed = models.BooleanField(default=False)
    is_single = models.BooleanField(default=True)
    is_child = models.BooleanField(default=False)
    tds_claim_date = models.DateField(null=True,blank=True)
    json_data = models.TextField(null=True,blank=True)
    dr_ledger = models.ForeignKey(LedgerMaster, on_delete=models.SET_NULL, null=True,blank=True,related_name='sales_ledger_dr')
    cr_ledger = models.ForeignKey(LedgerMaster, on_delete=models.SET_NULL, null=True,blank=True,related_name='sales_ledger_cr')
    cgst_ledger = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,related_name='cgst_sales',blank=True, null=True)
    sgst_ledger = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,related_name='sgst_sales',blank=True, null=True)
    igst_ledger = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,related_name='igst_sales',blank=True, null=True)
    
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory,default=9, on_delete=models.SET_NULL, null=True,blank=True,related_name='sales_ledger_dr_category')
    cr_ledger_category = models.ForeignKey(LedgerCategory,default=24, on_delete=models.SET_NULL, null=True,blank=True,related_name='sales_ledger_cr_category')
    cgst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='cgst_sales_category',blank=True, null=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='sgst_sales_category',blank=True, null=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='igst_sales_category',blank=True, null=True)
    
    def __str__(self):
        return str(self.invoice_no)
    
    class Meta:
        ordering = ('-created_at','-id',)
        
    def save(self,*args,**kwargs):
        
        if self.signed_qr_code:
            try:
                create_qr_code(self)
            except:
                pass

        
            
        if not self.invoice_no:
            current_year = datetime.now().year
            current_month = datetime.now().month
           
            INVOICE_PREFIX = self.company_type.pre_recievable_invoice

          

            current_year = datetime.now().year
            _,end_day = calendar.monthrange(current_year, current_month)
            from_date = date(current_year,current_month,1)
        
            to_date = date(current_year,current_month,end_day)

            current_length  = InvoiceReceivable.objects.filter(created_at__range=[from_date,to_date]).filter(company_type=self.company_type).filter(created_at__gte = self.company_type.financial_from).filter(is_deleted=False).count() + 1

            duplicate = True
            while duplicate:
                company_invoice_no = INVOICE_PREFIX + str(current_length).zfill(4)

                already_invoice_no = InvoiceReceivable.objects.filter(invoice_no = company_invoice_no).count()
               
                if already_invoice_no  == 0:
                    duplicate = False
                    self.invoice_no = company_invoice_no
                else:
                    current_length += 1
        
        
        if self.old_invoice:
            self.cr_ledger_category = LedgerCategory.objects.filter(id=1).first()
            
        
        return super(InvoiceReceivable,self).save(*args,**kwargs)
    

    def count_invoice_days(self):
        return  abs((date.today() - self.einvoice_date.date()).days)
    
    def get_received_amount(self):
        amount = 0
        query = self.reciept_rec_inv.aggregate(sum=Sum('received_amount'))
        if query['sum']:
            amount = query['sum']

        return  amount
    
    def get_tds_amount(self):
        amount = 0
        query = self.reciept_rec_inv.aggregate(sum=Sum('tds_amount'))
        if query['sum']:
            amount = query['sum']

        return  amount
    
    def get_adjustment_amount(self):
        amount = 0
        query = self.reciept_rec_inv.aggregate(sum=Sum('adjustment_amount'))
        if query['sum']:
            amount = query['sum']

        return  amount


TAX_APPLICABLE_OPTIONS = (
    ('T','Taxable'),
    ('L','Nil'),
    ('E','Exempt'),
    ('N','Non GST'),
    ('F','Free Supplies'),   
)

class InvoiceReceivableDetail(LogFolder):
    invoice_receivable = models.ForeignKey(InvoiceReceivable,related_name="recievable_invoice_reference",null=True,on_delete=models.CASCADE)
    billing_head = models.ForeignKey(BillingHead,related_name='recievable_invoice_billing_head',null=True, blank=True, on_delete=models.CASCADE)
    tax_applicable = models.CharField(max_length=20,default="T",choices=TAX_APPLICABLE_OPTIONS)
    currency = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True, blank=True,related_name='recievable_invoice_estimate_currency')
    ex_rate = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    qty_unit = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    gst = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    cr_ledger_category = models.ForeignKey(LedgerCategory,default=24, on_delete=models.SET_NULL, null=True,blank=True,related_name='sales_ledger_cr_category_detail')
    gst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='gst_sales_category',blank=True, null=True)
    
PARTY_TYPE = (
    ('Direct','Direct'),
    ('Indirect','Indirect'),
)

# Create your models here.
class InvoicePayable(LogFolder):
    expense = models.ForeignKey(IndirectExpense,on_delete=models.SET_NULL,null=True,blank=True,related_name='payable_expense')
    invoice_no = models.CharField(max_length=200, null=True,blank=True)
    purchase_invoice_no = models.CharField(max_length=120,null=True,blank=False)
    party_type = models.CharField(max_length=120,null=True,blank=True,choices=PARTY_TYPE,default="Direct")
    date_of_invoice = models.DateField(blank=True, null=True)
    tds_booking_date = models.DateField(null=True,blank=True)
    job_no = models.ForeignKey(JobMaster, on_delete=models.CASCADE, null=True,related_name='payable_invoice_job',blank=True)
    bill_from = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True,related_name='payable_invoice_bill_to',blank=True)
    bill_from_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='bill_from_address')
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,blank=True,related_name='bill_from_vendor')
    invoice_currency = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,related_name="invoice_pay_currency")
    currency_ex_rate = models.FloatField(default=1)
    old_invoice = models.BooleanField(default=False)
    due_date = models.DateField(null=True,blank=True)
    invoice_status = models.CharField(max_length=200, default="Open", choices=INV,null=True, blank=True )
    account_number = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True,related_name='payable_account_no',blank=True)
    gross_amount = models.FloatField(default=0)
    pending_amount = models.FloatField(default=0,null=True,blank=True)
    gst_amount = models.FloatField(default=0)
    advance_amount = models.FloatField(default=0,null=True,blank=True)
    net_amount = models.FloatField(default=0)
    tds_payable = models.FloatField(default=0)
    round_off = models.FloatField(default=0)
    remark_on_invoice = models.CharField(max_length=300, null=True, blank=True)
    sales_person = models.CharField(max_length=100, null=True, blank=True)
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="inv_pay_company_type")
    is_final = models.BooleanField(default=False,blank=True)
    is_uploaded = models.BooleanField(default=False,blank=True)
    is_rcm = models.BooleanField(default=False,blank=True)
    claim_date = models.DateField(null=True,blank=True)
    tds_section=models.CharField(max_length=200,choices=Choose_tds_section,null=True,blank=True)
    tds_percentage = models.IntegerField(default=0,blank=True)
    tds_payable = models.FloatField(default=0,blank=True)
    is_single = models.BooleanField(default=True,null=True,blank=True)
    invoice_file_2 = models.FileField(upload_to='payable_invoice/', null=True,blank=True)
    invoice_file_1 = models.FileField(upload_to='payable_invoice/', null=True,blank=True)
    invoice_file_3 = models.FileField(upload_to='payable_invoice/', null=True,blank=True)
    invoice_file_4 = models.FileField(upload_to='payable_invoice/', null=True,blank=True)

    invoice_file_5 = models.FileField(upload_to='payable_invoice/', null=True,blank=True)
    
    
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory, default = 23, on_delete=models.SET_NULL, null=True,related_name='purchase_ledger_dr_category',blank=True)
    cr_ledger_category = models.ForeignKey(LedgerCategory, default = 13, on_delete=models.SET_NULL, null=True,related_name='purchase_ledger_cr_category',blank=True)
    tds_ledger_category = models.ForeignKey(LedgerCategory, default = 11, on_delete=models.SET_NULL, null=True,related_name='purchase_ledger_tds_category',blank=True)
    cgst_ledger_category = models.ForeignKey(LedgerCategory, default = 11,on_delete=models.SET_NULL,related_name='cgst_payable_category',blank=True, null=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory, default = 11,on_delete=models.SET_NULL,related_name='sgst_payable_category',blank=True, null=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory, default = 11,on_delete=models.SET_NULL,related_name='igst_payable_category',blank=True, null=True)
    
    
    def __str__(self):
        return str(self.invoice_no)
    
    class Meta:
        ordering = ('-id',)
        
    
        
    def save(self,*args,**kwargs):
        
        if self.old_invoice:
            self.dr_ledger_category = LedgerCategory.objects.filter(id=1).first()
        
        if self.party_type == "Indirect":
            self.dr_ledger_category = LedgerCategory.objects.filter(id=16).first()
      
        
        return super(InvoicePayable,self).save(*args,**kwargs)


class InvoicePayableDetail(LogFolder):
    invoice_payable = models.ForeignKey(InvoicePayable,related_name="payable_invoice_reference",null=True,on_delete=models.CASCADE)

    billing_head = models.ForeignKey(BillingHead,related_name='payable_invoice_billing_head',null=True, blank=True, on_delete=models.CASCADE)
    
    currency = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True, blank=True,related_name='payable_invoice_estimate_currency')
    
    ex_rate = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    qty_unit = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    gst = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    dr_ledger_category = models.ForeignKey(LedgerCategory,default=23, on_delete=models.SET_NULL, null=True,blank=True,related_name='purchase_ledger_dr_category_detail')
    gst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='gst_purchase_category',blank=True, null=True)
    tds_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='tds_purchase_category',blank=True, null=True)
     

# Create your models here.
class CreditNote(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="credit_note_company_type")
    credit_note_no = models.CharField(max_length=120,null=True,blank=True)
    final_invoice_no = models.CharField(max_length=200,null=True,blank=True)
    qr_code = models.TextField(null=True,blank=True)
    einvoice_date = models.DateTimeField(null=True,blank=True)
    signed_qr_code = models.TextField(null=True,blank=True)
    against_debit_note = models.BooleanField(default=False)
    irn_no = models.TextField(null=True,blank=True)
    category = models.CharField(max_length=200,default="B2B",choices=INVOICE_CATEGORY)
    is_einvoiced = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    is_rcm = models.BooleanField(default=False)
    ack_no = models.CharField(max_length=200,null=True,blank=True)
    einvoice_id = models.CharField(max_length=200,null=True,blank=True)
    date_of_note = models.DateField(blank=True, null=True)
    job_no = models.ForeignKey(JobMaster, on_delete=models.CASCADE,blank=True, null=True,related_name='credit_note_job')
    reference_invoice = models.ForeignKey(InvoiceReceivable,on_delete=models.SET_NULL,related_name='crn_ref_invoice',null=True,blank=True)
    invoice_no = models.CharField(max_length=100,null=True,blank=True)
    invoice_date = models.CharField(max_length=100,null=True,blank=True)
    invoice_currency = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,related_name="invoice_cr_currency")
    currency_ex_rate = models.FloatField(default=1)
    bill_to = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True,related_name='credit_note_bill_to')
    bill_to_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='bill_to_cn_address')
    shipper = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True,related_name='shipper_cn')
    shipper_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='shipper_address_cn_address')
    invoice_status = models.CharField(max_length=50,null=True,blank=True,choices=INV,default="Open")
    account_number = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True,related_name='credit_note_account_no',blank=True)
    gross_amount = models.FloatField(default=0,blank=True)
    # journal = models.ForeignKey(Journal,null=True,blank=True,on_delete=models.SET_NULL,related_name="crn_journal")
    gst_amount = models.FloatField(default=0)
    advance_amount = models.FloatField(default=0,null=True,blank=True)
    net_amount = models.FloatField(default=0,blank=True)
    remark_on_note = models.CharField(max_length=300, null=True, blank=True)
    qr_code_image = models.ImageField(upload_to='crn_inv/qr_codes/',null=True,blank=True)
    hbl_options = models.ManyToManyField(JobHBL,blank=True,related_name='credit_note_job_hbl')
    
    dr_ledger = models.ForeignKey(LedgerMaster, on_delete=models.SET_NULL, null=True, blank=True,related_name='crn_ledger_dr')
    cr_ledger = models.ForeignKey(LedgerMaster, on_delete=models.SET_NULL, null=True, blank=True,related_name='crn_ledger_cr')
    cgst_ledger = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,related_name='cgst_crn',blank=True, null=True)
    sgst_ledger = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,related_name='sgst_crn',blank=True, null=True)
    igst_ledger = models.ForeignKey(LedgerMaster,on_delete=models.SET_NULL,related_name='igst_crn',blank=True, null=True)
    
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory, default=24 , on_delete=models.SET_NULL, null=True, blank=True,related_name='crn_ledger_dr_category')
    cr_ledger_category = models.ForeignKey(LedgerCategory, default=9, on_delete=models.SET_NULL, null=True, blank=True,related_name='crn_ledger_cr_category')
    cgst_ledger_category = models.ForeignKey(LedgerCategory, default=11 ,on_delete=models.SET_NULL,related_name='cgst_crn_category',blank=True, null=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory, default=11 ,on_delete=models.SET_NULL,related_name='sgst_crn_category',blank=True, null=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory, default=11 ,on_delete=models.SET_NULL,related_name='igst_crn_category',blank=True, null=True)
   
    class Meta:
        ordering = ('-id',)
   
    def __str__(self):
        return str(self.credit_note_no)
    
    def save(self,*args,**kwargs):
        if self.signed_qr_code:
            try:
                create_qr_code(self)
            except:
                pass
            
        
       

        if not self.credit_note_no:
            current_year = datetime.now().year
            current_month = datetime.now().month
            # prefix = str(current_year).zfill(2)[2:4] + str(current_month).zfill(2)
            
            if self.is_rcm:
                INVOICE_PREFIX = self.company_type.rcm_cn_prefix
            else:
                INVOICE_PREFIX = self.company_type.pre_credit_note

            pre_prefix = "CRN-"

            # INVOICE_PREFIX= pre_prefix + prefix + INVOICE_PREFIX
            INVOICE_PREFIX= INVOICE_PREFIX

            current_year = datetime.now().year
            _,end_day = calendar.monthrange(current_year, current_month)
            from_date = date(current_year,current_month,1)
        
            to_date = date(current_year,current_month,end_day)
            current_length  = CreditNote.objects.filter(created_at__range=[from_date,to_date]).filter(company_type=self.company_type).filter(created_at__gte = self.company_type.financial_from).filter(is_deleted=False).count() + 1
            
            duplicate = True
            while duplicate:
                company_invoice_no = INVOICE_PREFIX + str(current_length).zfill(4)
                already_invoice_no = CreditNote.objects.filter(credit_note_no = company_invoice_no).count()
               
                if already_invoice_no  == 0:
                    duplicate = False
                    self.credit_note_no = company_invoice_no
                else:
                    current_length += 1

        
        return super(CreditNote,self).save(*args,**kwargs)


class CreditNoteDetail(LogFolder):
    credit_note = models.ForeignKey(CreditNote,related_name="credit_note_reference",null=True,on_delete=models.CASCADE)
    billing_head = models.ForeignKey(BillingHead,related_name='credit_note_billing_head',null=True, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True, blank=True,related_name='credit_note_estimate_currency')
    ex_rate = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    qty_unit = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    gst = models.FloatField(default=0)
    tax_applicable = models.CharField(max_length=20,default="T",choices=TAX_APPLICABLE_OPTIONS)
    gst_amount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    dr_ledger_category = models.ForeignKey(LedgerCategory,default=24, on_delete=models.SET_NULL, null=True,blank=True,related_name='crn_ledger_dr_category_detail')
    gst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='gst_crn_category',blank=True, null=True)


PARTY_TYPE = (
    ('Direct','Direct'),
    ('Indirect','Indirect'),
)

AMM_TYPE = (
    ("I","I"),
    ("C","C"),
)

class Ammendment(LogFolder):
    invoice_no = models.CharField(max_length=120,null=True,blank=True)
    amm_date = models.DateField(auto_now_add=True)
    invoice_date = models.DateField(null=True,blank=True)
    party = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name="ammendment_party")
    party_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name="ammendment_party_address")
    invoice = models.ForeignKey(InvoiceReceivable,on_delete=models.SET_NULL,null=True,blank=True,related_name="ammendment_sales_invoice")
    credit_note = models.ForeignKey(CreditNote,on_delete=models.SET_NULL,null=True,blank=True,related_name="ammendment_crn")
    category = models.CharField(max_length=20,choices=INVOICE_CATEGORY,blank=True)
    amm_type = models.CharField(max_length=5,choices=AMM_TYPE,default="I",blank=True)

    def save(self,*args,**kwargs):
        if not self.party and not self.party_address:
            if self.invoice:
                self.amm_type = "I"
               
                self.party = self.invoice.bill_to
                self.party_address = self.invoice.bill_to_address
                self.category = self.invoice.category
            
            if self.credit_note:
                self.amm_type = "C"
                self.invoice_no = self.credit_note.final_invoice_no
                self.invoice_date = self.credit_note.einvoice_date
                self.party = self.credit_note.bill_to
                self.party_address = self.credit_note.bill_to_address
                self.category = self.credit_note.category
       
        return super(Ammendment,self).save(*args,**kwargs)


class DebitNote(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="debit_note_company_type")
    debit_note_no = models.CharField(max_length=200)
    date_of_note = models.DateField(blank=True, null=True)
    party_type = models.CharField(max_length=40,null=True,blank=True,default="Direct",choices=PARTY_TYPE)
    job_no = models.ForeignKey(JobMaster, on_delete=models.CASCADE,blank=True, null=True,related_name='debit_note_job')
    invoice_no = models.CharField(max_length=100,null=True,blank=True)
    bill_from_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='bill_from_dn_address')
    invoice_currency = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,related_name="invoice_dr_currency")
    currency_ex_rate = models.FloatField(default=1)
    bill_from = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True,related_name='debit_note_bill_to')
    bill_from_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True,related_name='debit_note_bill_from_vendor')
    invoice_status = models.CharField(max_length=50,null=True,blank=True,choices=INV,default="Open")
    round_off = models.FloatField(default=0,blank=True)
    is_final = models.BooleanField(default=False,blank=True)
    is_uploaded = models.BooleanField(default=False,blank=True)
    claim_date = models.DateField(null=True,blank=True)
    is_rcm = models.BooleanField(default=False,blank=True)
    
    account_number = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True,related_name='debit_note_account_no',blank=True)
    gross_amount = models.FloatField(default=0,blank=True)
    gst_amount = models.FloatField(default=0,blank=True)
    advance_amount = models.FloatField(default=0,blank=True)
    net_amount = models.FloatField(default=0,blank=True)
    remark_on_note = models.CharField(max_length=300, null=True, blank=True)
    
   
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory,default=13, on_delete=models.SET_NULL, null=True, blank=True,related_name='drn_ledger_dr_category')
    cr_ledger_category = models.ForeignKey(LedgerCategory,default=23, on_delete=models.SET_NULL, null=True, blank=True,related_name='drn_ledger_cr_category')
    cgst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='cgst_drn_category',blank=True, null=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='sgst_drn_category',blank=True, null=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='igst_drn_category',blank=True, null=True)
    
    def __str__(self):
        return str(self.debit_note_no)
    
    class Meta:
        ordering = ('-id',)
        
    def save(self,*args,**kwargs):
        
        return super(DebitNote,self).save(*args,**kwargs)


class DebitNoteDetail(LogFolder):
    
    debit_note = models.ForeignKey(DebitNote,related_name="debit_note_reference",null=True,on_delete=models.CASCADE)
    billing_head = models.ForeignKey(BillingHead,related_name='debit_note_billing_head',null=True, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True, blank=True,related_name='debit_note_estimate_currency')
    ex_rate = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    qty_unit = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    gst = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    cr_ledger_category = models.ForeignKey(LedgerCategory,default=23, on_delete=models.SET_NULL, null=True,blank=True,related_name='drn_ledger_cr_category_detail')
    gst_ledger_category = models.ForeignKey(LedgerCategory,default=11,on_delete=models.SET_NULL,related_name='gst_drn_category',blank=True, null=True)
    
    
Models = (
    ("Sea Export", "Sea Export"),
    ("Sea Import", "Sea Import"),
    ("Air Export", "Air Export"),
    ("Air Import", "Air Import")
)
TDS = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('5', '5'),
    ('10', '10')
   
)

PURPOSE = (
    ('GST','GST'),
    ('Others','Others'),
    ('Cash','Cash')
)
CHOOSE_RV_FROM = (
    ('BANK','BANK'),
    ('ADVANCE','ADVANCE'),
    
)

CHOOSE_RECIEVE_IN = (
    ('BANK','BANK'),
    ('CASH','CASH'),
    
)

VOUCHER_TYPE = (
    ('Direct','Direct'),
    ('Indirect','Indirect'),
    ('Other','Other'),
)

CASH_BANK = (
    ('Bank','Bank'),
    ('Cash','Cash'),
)

PAY_TYPE = (
    ('OAC','On A/C'),
    ('BW','Agst. Ref')
)

class RecieptVoucher(LogFolder):
    voucher_no = models.CharField(max_length=200, null=True, blank=True)
    voucher_date = models.DateField(null=True, blank=True)
    instrument_no = models.CharField(max_length=200, null=True, blank=True)
    
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="rec_voucher_company_type")
    
    voucher = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name="advance_voucher")
    
    party_name = models.ForeignKey(Party, on_delete=models.CASCADE,null=True,blank=True, related_name='received_party_name')
    party_address = models.ForeignKey(PartyAddress, on_delete=models.CASCADE,null=True,blank=True, related_name='received_party_address')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True, related_name='reciept_vendor')

    recieve_in = models.CharField(max_length=30,null=True, blank=True,choices=CHOOSE_RECIEVE_IN,default="BANK")
    cash = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name="cash_in")
    bank = models.ForeignKey(Bank,on_delete=models.SET_NULL, null=True, related_name='receive_in_bank',blank=True)

    bank_clearing_date = models.DateField(null=True, blank=True)
    payment_type = models.CharField(max_length=30,default='Direct',choices=VOUCHER_TYPE,blank=True)
    to_bank = models.ForeignKey(Bank,on_delete=models.SET_NULL, null=True, related_name='received_bank',blank=True)
    particular = models.CharField(max_length=200, null=True, blank=True)
    received_amount_date = models.DateField(null=True, blank=True)
    settle_from = models.CharField(max_length=60,choices=CHOOSE_RV_FROM,null=True,blank=True)
    
    tds = models.FloatField(default=0,blank=True)
    received_amount = models.FloatField(default=0,blank=True)
    advance_amount = models.FloatField(default=0,blank=True)
    total_recieved_amount = models.FloatField(default=0,blank=True)
    reciept_tds_amount = models.FloatField(default=0,blank=True)
    adjustment_amount = models.FloatField(default=0,blank=True)
    narration = models.CharField(max_length=200, null=True, blank=True)
    round_off_amount = models.FloatField(default=0,blank=True)
    net_amount = models.FloatField(default=0,blank=True)
    
    
    bank_charges = models.FloatField(default=0,blank=True)
    bank_charges_cgst = models.FloatField(default=0,blank=True)
    bank_charges_sgst = models.FloatField(default=0,blank=True)
    bank_charges_igst = models.FloatField(default=0,blank=True)
    bank_charges_tax = models.FloatField(default=0,blank=True)
    
    old_voucher = models.BooleanField(default=False)
    is_reversed = models.BooleanField(default=False)
    has_childs = models.BooleanField(default=False)
    rounded_off = models.BooleanField(default=False)
    
   
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory, default = 4, on_delete=models.SET_NULL,null=True,blank=True, related_name='rec_ledger_dr_category')
    cr_ledger_category = models.ForeignKey(LedgerCategory, default = 9, on_delete=models.SET_NULL,null=True,blank=True, related_name='rec_ledger_cr_category')
    tds_ledger_category = models.ForeignKey(LedgerCategory, default = 11, on_delete=models.SET_NULL,null=True,blank=True, related_name='rec_ledger_tds_category')
    adjustment_ledger_category = models.ForeignKey(LedgerCategory, default = 16, on_delete=models.SET_NULL,null=True,blank=True, related_name='rec_ledger_adjst_category')
    bank_charges_ledger_category = models.ForeignKey(LedgerCategory, default = 16, on_delete=models.SET_NULL,null=True,blank=True, related_name='rec_ledger_bank_charges')
    cgst_ledger_category = models.ForeignKey(LedgerCategory, default = 11,on_delete=models.SET_NULL,related_name='cgst_rec_category',blank=True, null=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory, default = 11,on_delete=models.SET_NULL,related_name='sgst_rec_category',blank=True, null=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory, default = 11,on_delete=models.SET_NULL,related_name='igst_rec_category',blank=True, null=True)

    def __str__(self):
        return f'{self.voucher_no}'
    
    def save(self,*args,**kwargs):
        if not self.voucher_no:
            current_year = datetime.now().year
            current_month = datetime.now().month
            if current_month < 4:
                current_year -= 1
            current_financial_date = date(current_year, 4, 1)
            current_length = RecieptVoucher.objects.filter(created_at__gte = current_financial_date).count()
            if current_length == 0:
                current_length = 1
            is_duplicate = True
            
            while is_duplicate:
                try:
                    voucher_no = self.company_type.pre_recieve_voucher + str(current_length).zfill(6)
                except:
                    voucher_no = "RV/" + str(current_length).zfill(6)
                    
                voucher = RecieptVoucher.objects.filter(voucher_no=voucher_no).count()
                if voucher == 0:
                    is_duplicate = False
                else:
                    current_length += 1
                    
            self.voucher_no = voucher_no
                            
        try:
            self.adjustment_ledger_category = LedgerCategory.objects.filter(id=26).first()
        except:
            pass
        
      
        if self.recieve_in == "CASH":
            self.dr_ledger_category = LedgerCategory.objects.filter(id=5).first()
            
        if self.old_voucher:
            self.dr_ledger_category = LedgerCategory.objects.filter(id=1).first()
                
        return super(RecieptVoucher,self).save(*args,**kwargs)
    
    class Meta:
        ordering = ('-id',)

class RecieptVoucherDetails(LogFolder):
    voucher = models.ForeignKey(RecieptVoucher,null=True,blank=True,on_delete=models.CASCADE,related_name="rec_voucher_detail")
    
    payment_type = models.CharField(max_length=20,choices=PAY_TYPE,null=True,blank=True)

    ledger = models.ForeignKey(LedgerMaster, on_delete=models.CASCADE,null=True,blank=True, related_name='reciept_ledger')
    party = models.ForeignKey(Party, on_delete=models.CASCADE,null=True,blank=True, related_name='reciept_party')
    party_address = models.ForeignKey(PartyAddress, on_delete=models.CASCADE,null=True,blank=True, related_name='reciept_party_address')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True, related_name='reciept_in_vendor')
    
    invoice = models.ForeignKey(InvoiceReceivable, null=True, blank=True,on_delete=models.CASCADE,related_name="reciept_rec_inv")

    party_type = models.CharField(max_length=30,default='Direct',choices=VOUCHER_TYPE,blank=True)

    date = models.DateField(auto_now_add=True,null=True,blank=True)
    received_amount = models.FloatField(default=0)
    pending_amount = models.FloatField(default=0)
    tds_amount = models.FloatField(default=0)
    adjustment_amount = models.FloatField(default=0)
    tds_claimed = models.BooleanField(default=False)
    tds_claim_date = models.DateField(null=True,blank=True)

VOUCHER_TYPE = (
    ('Direct','Direct'),
    ('Indirect','Indirect'),
)


SETTLE_FROM = (
    ('Y','Yes'),
    ('N','No'),
)
SETTLE_FROM = (
    ('Y','Yes'),
    ('N','No'),
)
SETTLE_FROM = (
    ('Y','Yes'),
    ('N','No'),
)
class PaymentVoucher(LogFolder):
    voucher = models.ForeignKey('self',on_delete=models.CASCADE,related_name="payment_voucer_advance",null=True,blank=True)
    voucher_no = models.CharField(max_length=200, null=True, blank=True)
    voucher_date = models.DateField( null=True, blank=True)
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="pay_voucher_company_type")
    payment_type = models.CharField(max_length=30,default='Direct',choices=VOUCHER_TYPE,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True, related_name='payment_vendor')
    party_name = models.ForeignKey(Party, on_delete=models.CASCADE,null=True,blank=True, related_name='payment_party_name')
    party_address = models.ForeignKey(PartyAddress, on_delete=models.CASCADE,null=True,blank=True, related_name='pay_party_address')
    pay_from = models.CharField(max_length=20,choices=CASH_BANK,default='Bank',blank=True)
    bank_clearing_date = models.DateField(null=True, blank=True)
    from_bank = models.ForeignKey(Bank,on_delete=models.SET_NULL, null=True, related_name='payment_bank',blank=True) # Old Field
    bank = models.ForeignKey(Bank,on_delete=models.SET_NULL, null=True, related_name='bank_payment',blank=True) # New Field
    cash = models.ForeignKey(Logistic,on_delete=models.SET_NULL, null=True, related_name='cash_payment',blank=True) # New Field
    instrument_no = models.CharField(max_length=200, null=True, blank=True)
    settle_from_advance = models.CharField(max_length=4,null=True,blank=True,choices=SETTLE_FROM)
    narration = models.CharField(max_length=200, null=True, blank=True)
    payment_tds_amount = models.FloatField(default=0,blank=True)
    paid_amount = models.FloatField(default=0,blank=True)
    net_amount = models.FloatField(default=0,blank=True)
    advance_amount = models.FloatField(default=0,blank=True)
    amm_no = models.IntegerField(default=0,blank=True)
    adjustment_amount = models.FloatField(default=0,blank=True)
    total_paid_amount = models.FloatField(default=0,blank=True)
    is_reversed = models.BooleanField(default=False)
    has_childs = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    bank_charges_cgst = models.FloatField(default=0,blank=True)
    bank_charges_sgst = models.FloatField(default=0,blank=True)
    bank_charges_igst = models.FloatField(default=0,blank=True)
    bank_charges_tax = models.FloatField(default=0,blank=True)
    bank_charges = models.FloatField(default=0,blank=True)
    rounded_off = models.BooleanField(default=False)

    
    
    old_voucher = models.BooleanField(default=False)
    
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory,default = 13, on_delete=models.SET_NULL,null=True,blank=True, related_name='payment_ledger_dr_category')
    cr_ledger_category = models.ForeignKey(LedgerCategory,default = 4, on_delete=models.SET_NULL,null=True,blank=True, related_name='payment_ledger_cr_category')
    tds_ledger_category = models.ForeignKey(LedgerCategory,default = 11, on_delete=models.SET_NULL,null=True,blank=True, related_name='payment_ledger_tds_category')
    adjustment_ledger_category = models.ForeignKey(LedgerCategory,default = 16, on_delete=models.SET_NULL,null=True,blank=True, related_name='payment_ledger_adjst_category')
    bank_charges_ledger_category = models.ForeignKey(LedgerCategory,default = 16, on_delete=models.SET_NULL,null=True,blank=True, related_name='payment_ledger_bank_charges')
    cgst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,related_name='cgst_pay_category',blank=True, null=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,related_name='sgst_pay_category',blank=True, null=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,related_name='igst_pay_category',blank=True, null=True)

    def __str__(self):
        return f'{self.voucher_no}'
    
    
    class Meta:
        ordering = ('-id',)
        
        
    
    def save(self,*args,**kwargs):
        if not self.voucher_no:
            current_year = datetime.now().year
            current_month = datetime.now().month
            if current_month < 4:
                current_year -= 1
            current_financial_date = date(current_year, 4, 1)
            current_length = PaymentVoucher.objects.filter(created_at__gte = current_financial_date).count()
            if current_length == 0:
                current_length = 1
            is_duplicate = True
            
            while is_duplicate:
                try:
                    voucher_no = self.company_type.pre_payment_voucher + str(current_length).zfill(6)
                except:
                    voucher_no = "PV/" + str(current_length).zfill(6)
                    
                voucher = PaymentVoucher.objects.filter(voucher_no=voucher_no).count()
                if voucher == 0:
                    is_duplicate = False
                else:
                    current_length += 1
                    
            self.voucher_no = voucher_no
        
        try:
            self.adjustment_ledger_category = LedgerCategory.objects.filter(id=26).first()
        except:
            pass

        if self.pay_from == "Cash":
            self.cr_ledger_category = LedgerCategory.objects.filter(id=5).first()
            
        if self.old_voucher:
            self.cr_ledger_category = LedgerCategory.objects.filter(id=1).first()
        
        return super(PaymentVoucher,self).save(*args,**kwargs)
    
class PaymentVoucherDetails(models.Model):
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    payment_type = models.CharField(max_length=20,choices=PAY_TYPE,null=True,blank=True)
    voucher = models.ForeignKey(PaymentVoucher,null=True,blank=True,on_delete=models.CASCADE,related_name="pay_voucher_detail")
    invoice = models.ForeignKey(InvoicePayable, null=True, blank=True,on_delete=models.CASCADE,related_name="pay_payment_inv")
    expense = models.ForeignKey(IndirectExpense, null=True, blank=True,on_delete=models.CASCADE,related_name="exp_payment_inv")

    ledger = models.ForeignKey(LedgerMaster, on_delete=models.CASCADE,null=True,blank=True, related_name='pay_ledger')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True, related_name='pay_voucher_vendor')
    party = models.ForeignKey(Party, on_delete=models.CASCADE,null=True,blank=True, related_name='pay_voucher_party_name')
    party_address = models.ForeignKey(PartyAddress, on_delete=models.CASCADE,null=True,blank=True, related_name='pay_voucher_party_address')

    party_type = models.CharField(max_length=30,default='Direct',choices=VOUCHER_TYPE,blank=True)
    paid_amount = models.FloatField(default=0)
    pending_amount = models.FloatField(default=0)
    tds_amount = models.FloatField(default=0)
    adjustment_amount = models.FloatField(default=0)
    
CONTRA_CHOICES = (
    ('B2B','Bank To Bank'),
    ('B2C','Bank To Cash'),
    ('C2B','Cash To Bank'),
)    
 
class ContraVoucher(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="contra_company_type")
    voucher_no = models.CharField(max_length=120,null=True,blank=True)
    voucher_date = models.DateField(null=True,blank=True)
    account_from = models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True,blank=True,related_name='contra_account_from')
    account_to = models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True,blank=True,related_name='contra_account_to')
    cash = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name='contra_cash')
    amount = models.FloatField(default=0)
    # journal = models.ForeignKey(Journal,on_delete=models.SET_NULL,null=True,blank=True,related_name="contra_journal")
    contra_choice = models.CharField(max_length=120,choices=CONTRA_CHOICES,default="Bank To Bank")
    instrument_no = models.CharField(max_length=200,null=True,blank=True)
    bank_clearing_date = models.DateField(null=True,blank=True)
    bank_charges = models.FloatField(default=0,blank=True)
    
    
    # Category
    bank_expense_ledger_category = models.ForeignKey(LedgerCategory,default=16 ,on_delete=models.SET_NULL,null=True,blank=True, related_name='contra_ledger_bank_charges_category')
    dr_ledger_category = models.ForeignKey(LedgerCategory,default=4 ,on_delete=models.SET_NULL,null=True,blank=True, related_name='contra_ledger_dr_category')
    cr_ledger_category = models.ForeignKey(LedgerCategory,default=4 ,on_delete=models.SET_NULL,null=True,blank=True, related_name='contra_ledger_cr_category')
    
    def save(self,*args,**kwargs):
        if self.contra_choice == "B2C":
            self.dr_ledger_category = LedgerCategory.objects.filter(id=5).first()
        
        if self.contra_choice == "C2B":
            self.cr_ledger_category = LedgerCategory.objects.filter(id=5).first()

        
        return super(ContraVoucher,self).save(*args,**kwargs)
        
        

   
    
PAYMENT = (
    ('PENDING','PENDING'),
    ('COMPLETED','COMPLETED')
)


class PettyCash(LogFolder):
    voucher = models.OneToOneField(ContraVoucher,on_delete=models.CASCADE,null=True,blank=True,related_name="petty_contra")
    rec_voucher = models.OneToOneField(RecieptVoucher,on_delete=models.CASCADE,null=True,blank=True,related_name="petty_reciept")
    date = models.DateField(null=True,blank=True)
    amount = models.FloatField(default=0)
    type = models.CharField(max_length=20,choices=DR_CR)
    description = models.TextField(null=True,blank=True)
    


class Manifest(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_company')
    job_no = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_job')
    manifest_no = models.CharField(max_length=50,null=True,blank=True)
    manifest_date = models.DateField(null=True,blank=True)
    manifest_currency = models.ForeignKey(currency,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_currency')
    manifest_ex_rate = models.FloatField(default=1)
    customer = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='manifest_customer')
    customer_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='manifest_customer_address')
    payment = models.CharField(max_length=60,default="PENDING",choices=PAYMENT)
    payment_date = models.DateField(null=True,blank=True)

    
class ManifestChargesToCollect(LogFolder):
    manifest = models.ForeignKey(Manifest,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_charges_collect')
    billing_head = models.ForeignKey(BillingHead,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_charges_collect_bh')
    curr = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True,related_name='manifest_charges_collect_curr')
    ex_rate = models.FloatField(default=1)
    rate = models.FloatField(default=0)
    total = models.FloatField(default=0)
    qty = models.FloatField(default=0)
  
class ManifestChargesToPay(LogFolder):
    manifest = models.ForeignKey(Manifest,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_charges_pay')
    billing_head = models.ForeignKey(BillingHead,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_charges_pay_bh')
    curr = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True,related_name='manifest_charges_pay_curr')
    ex_rate = models.FloatField(default=1)
    rate = models.FloatField(default=0)
    total = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    
class ManifestOurCharges(LogFolder):
    manifest = models.ForeignKey(Manifest,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_our_charges')
    billing_head = models.ForeignKey(BillingHead,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_our_charges_bh')
    curr = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True,related_name='manifest_our_charges_curr')
    ex_rate = models.FloatField(default=1)
    rate = models.FloatField(default=0)
    total = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    
class ManifestYourCharges(LogFolder):
    manifest = models.ForeignKey(Manifest,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_your_charges')
    billing_head = models.ForeignKey(BillingHead,on_delete=models.CASCADE,null=True,blank=True,related_name='manifest_your_charges_bh')
    curr = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True,related_name='manifest_your_charges_curr')
    ex_rate = models.FloatField(default=1)
    rate = models.FloatField(default=0)
    total = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    
    
class IrisInvoiceSetting(LogFolder):
    username = models.CharField(max_length=120,null=True,blank=True)
    email = models.CharField(max_length=120,null=True,blank=True)
    password = models.CharField(max_length=120,null=True,blank=True)
    token = models.TextField(null=True,blank=True)
    company_id = models.CharField(max_length=10,null=True,blank=True)
    token_date = models.DateTimeField(null=True,blank=True)
    password_expiry_date = models.DateField(null=True,blank=True)
    login_url = models.CharField(max_length=200,null=True,blank=True)
    add_inv_url = models.CharField(max_length=200,null=True,blank=True)
    cancel_irn_url = models.CharField(max_length=200,null=True,blank=True)
    get_inv_by_irn_url = models.CharField(max_length=200,null=True,blank=True)


LOAN_TYPE = (
    ("Secured","Secured"),
    ("Unsecured","Unsecured")
)

RATE_TYPE = (
    ("Flat","Flat"),
    ("Reducing","Reducing")
)

class Loan(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='loan_company')
    category = models.ForeignKey('masters.LedgerCategory',on_delete=models.CASCADE,null=True,blank=True,related_name='loan_category')
    loan_no = models.CharField(max_length=180,null=True,blank=True)
    loan_date = models.DateField(null=True,blank=True)
    loan_type = models.CharField(max_length=60,choices=LOAN_TYPE,null=True,blank=True)
    rate_type = models.CharField(max_length=60,choices=RATE_TYPE,blank=True,default="Flat")
    bank = models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True,related_name='loan_bank')
    loan_duration = models.IntegerField(default=0,blank=True)
    principal_amount = models.FloatField(default=0,blank=True)
    interest_rate = models.FloatField(default=0,blank=True)
    interest_amount = models.FloatField(default=0,blank=True)
    total_amount = models.FloatField(default=0,blank=True)
    monthly_emi = models.FloatField(default=0,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    pending_principal_amount = models.FloatField(default=0,blank=True)
    pending_interest_amount = models.FloatField(default=0,blank=True)
    pending_total_amount = models.FloatField(default=0,blank=True)
    bank_charges = models.FloatField(default=0,blank=True)
    cgst_charges = models.FloatField(default=0,blank=True)
    sgst_charges = models.FloatField(default=0,blank=True)
    igst_charges = models.FloatField(default=0,blank=True)
    paid_tenure = models.IntegerField(default=0,blank=True)
    file1 = models.FileField(null=True,blank=True)
    file2 = models.FileField(null=True,blank=True)
    file3 = models.FileField(null=True,blank=True)
    
   
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory,default = 4,on_delete=models.SET_NULL,null=True,blank=True,related_name='loan_ledger_dr_category')
    cr_ledger_category = models.ForeignKey(LedgerCategory,default = 21,on_delete=models.SET_NULL,null=True,blank=True,related_name='loan_ledger_cr_category')
    bank_expense_ledger_category = models.ForeignKey(LedgerCategory,default = 16,on_delete=models.SET_NULL,null=True,blank=True,related_name='loan_ledger_bank_expense_category')
    cgst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,null=True,blank=True,related_name='loan_ledger_bank_cgst_category')
    sgst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,null=True,blank=True,related_name='loan_ledger_bank_sgst_category')
    igst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,null=True,blank=True,related_name='loan_ledger_bank_igst_category')
    
    def __str__(self) -> str:
        return self.loan_no
    
    
    def save(self,*args,**kwargs):
        
        if self.loan_type == "Unsecured":
            self.cr_ledger_category = LedgerCategory.objects.filter(id=22).first()
            
        current_asset_category = LedgerCategories.objects.filter(name = 'Current Assets').first()
        if not current_asset_category:
            current_asset_category = LedgerCategories.objects.create(name="Current Assets",head_type="T",include_in="BS",type="Asset")
        
        liability_category = LedgerCategories.objects.filter(name = f'Loan Liability').first()
        if not liability_category:
            liability_category = LedgerCategories.objects.create(name=f'Loan Liability',head_type="T",include_in="BS",type="Liability")
        
        loan_liability_category = LedgerCategories.objects.filter(name = f'{self.loan_type}').first()
        if not loan_liability_category:
            loan_liability_category = LedgerCategories.objects.create(name=f'{self.loan_type}',parent=liability_category,head_type="S",include_in="BS",type="Liability")
        
        bank_ledger_category = LedgerCategories.objects.filter(name="Bank").first()
        if not bank_ledger_category:
            bank_ledger_category = LedgerCategories.objects.create(name="Bank",head_type="S",include_in="BS",type="Asset",parent=current_asset_category)
            
            
        cr_ledger = LedgerMaster.objects.filter(ledger_name=self.loan_no).first()
        if not cr_ledger:
            cr_ledger = LedgerMaster.objects.create(
                ledger_name = f"{self.loan_no}",
                ledger_under=loan_liability_category,
                auto_generated=True,
                party_type="Other",
                )
            
        self.cr_ledger = cr_ledger
        
        dr_ledger = LedgerMaster.objects.filter(bank=self.bank).first()
        if not dr_ledger:
            dr_ledger = LedgerMaster.objects.create(
                ledger_name = f"{self.bank.bank_name} ({self.bank.account_no})",
                ledger_under=bank_ledger_category,
                auto_generated=True,
                party_type="Bank",
                bank=self.bank
                )
            
        self.dr_ledger = dr_ledger
            
        expense_ledger_category = LedgerCategories.objects.filter(name="Indirect Expense").first()
        if not expense_ledger_category:
            expense_ledger_category = LedgerCategories.objects.create(name="Indirect Expense",head_type="S",include_in="PL",type="Nominal")
            
        bank_expense_ledger = LedgerMaster.objects.filter(ledger_name = "Bank Charges").first()
        if not bank_expense_ledger:
            bank_expense_ledger = LedgerMaster.objects.create(
                ledger_name = "Bank Charges",
                ledger_under=expense_ledger_category,
                auto_generated=True,
                party_type = "Other"
            )
            bank_expense_ledger

        self.bank_expense_ledger = bank_expense_ledger
        
        current_liability_category = LedgerCategories.objects.filter(name = 'Current Liability').first()
        if not current_liability_category:
            current_liability_category = LedgerCategories.objects.create(name="Current Liability",head_type="T",include_in="BS",type="Liability")
            
            
        duties_and_taxes = LedgerCategories.objects.filter(name = 'Duties & Taxes').first()
        if not duties_and_taxes:
            duties_and_taxes = LedgerCategories.objects.create(name="Duties & Taxes",parent=current_liability_category,head_type="S",include_in="BS",type="Liability")
        
        
        gst_ledger_category = LedgerCategories.objects.filter(name="GST Input").first()
        if not gst_ledger_category:
            gst_ledger_category = LedgerCategories.objects.create(name="GST Input",parent=duties_and_taxes,head_type="S",include_in="BS",type="Asset")
            
        
        cgst_ledger = LedgerMaster.objects.filter(ledger_name = "CGST Input").first()
        if not cgst_ledger:
            cgst_ledger = LedgerMaster.objects.create(ledger_name = "CGST Input",ledger_under=gst_ledger_category,auto_generated=True,party_type="Other")
            
        sgst_ledger = LedgerMaster.objects.filter(ledger_name = "SGST Input").first()
        if not sgst_ledger:
            sgst_ledger = LedgerMaster.objects.create(ledger_name = "SGST Input",ledger_under=gst_ledger_category,auto_generated=True,party_type="Other")
            
        igst_ledger = LedgerMaster.objects.filter(ledger_name = "IGST Input").first()
        if not igst_ledger:
            igst_ledger = LedgerMaster.objects.create(ledger_name = "IGST Input",ledger_under=gst_ledger_category,auto_generated=True,party_type="Other")
            
          
        self.cgst_ledger = cgst_ledger
        self.sgst_ledger = sgst_ledger
        self.igst_ledger = igst_ledger
        
        return super(Loan,self).save(*args,**kwargs)

class LoanPaymentRecord(LogFolder):
    loan = models.ForeignKey(Loan,on_delete=models.CASCADE,null=True,blank=True,related_name='loan_record')
    due_date = models.DateField(null=True,blank=True)
    payment_date = models.DateField(null=True,blank=True)
    principal_amount = models.FloatField(default=0)
    interest_rate = models.FloatField(default=0)
    interest_amount = models.FloatField(default=0)
    cgst = models.FloatField(default=0)
    sgst = models.FloatField(default=0)
    igst = models.FloatField(default=0)
    late_fee = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    instrument_no = models.CharField(max_length=255,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    
   
    # Category
    dr_ledger_category = models.ForeignKey(LedgerCategory,default = 21,on_delete=models.SET_NULL,null=True,related_name='repayment_loan_ledger_dr_category',blank=True)
    cr_ledger_category = models.ForeignKey(LedgerCategory,default = 4,on_delete=models.SET_NULL,null=True,related_name='repayment_loan_ledger_cr_category',blank=True)
    bank_expense_ledger_category = models.ForeignKey(LedgerCategory,default = 16,on_delete=models.SET_NULL,null=True,related_name='repayment_loan_ledger_bank_expense_category',blank=True)
    cgst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,null=True,related_name='repayment_loan_ledger_bank_cgst_category',blank=True)
    sgst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,null=True,related_name='repayment_loan_ledger_bank_sgst_category',blank=True)
    igst_ledger_category = models.ForeignKey(LedgerCategory,default = 11,on_delete=models.SET_NULL,null=True,related_name='repayment_loan_ledger_bank_igst_category',blank=True)
    
    
    def __str__(self) -> str:
        return self.loan.loan_no
    
    def save(self,*args,**kwargs):
        current_asset_category = LedgerCategories.objects.filter(name = 'Current Assets').first()
        if not current_asset_category:
            current_asset_category = LedgerCategories.objects.create(name="Current Assets",head_type="T",include_in="BS",type="Asset")
        
        return super(LoanPaymentRecord,self).save(*args,**kwargs)

class RevisedLoan(LogFolder):
    loan = models.ForeignKey(Loan,on_delete=models.CASCADE,null=True,blank=True,related_name='loan_revision')
    loan_duration = models.IntegerField(default=0)
    principal_amount = models.FloatField(default=0)
    interest_rate = models.FloatField(default=0)
    interest_amount = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    def __str__(self) -> str:
        return self.loan.loan_no





PAYMENT_STATUS = (
    ('Pending','Pending'),
    ('Paid','Paid'),
    ('Partial-Paid','Partial-Paid'),
    
)


class bill_of_payment(LogFolder):
    invoice_no = models.CharField(max_length=200,null=True,blank=True)
    invoice_year = models.CharField(max_length=50,null=True,blank=True)
    date_of_invoice=models.DateField(null=True,blank=True)
    # transactions = models.CharField(max_length=30,choices=TRANSACTIONS_TYPE)
    payment_status = models.CharField(max_length=30,choices=PAYMENT_STATUS,default="None")
    # details=models.CharField(max_length=255,null=True,blank=True)
    days_left=models.FloatField(default=0,null=True,blank=True)
    amount=models.FloatField(default=0)
    payments=models.FloatField(default=0)
    balance=models.FloatField(default=0,null=True,blank=True)
    # bop_file = models.FileField(null=True,blank=True,upload_to="bop/file/")
    due_date=models.DateField(null=True,blank=True)
    # bill_upload = models.ImageField(null=True,blank=True,upload_to="party/billupload/")
    bill_upload = models.FileField(null=True,blank=True,upload_to="party/billupload/")
   


    def __str__(self):
        return self.invoice_no
    

    def save(self, *args, **kwargs):
        self.balance = self.amount - self.payments

        if self.amount > 0 and self.payments == 0:
            self.payment_status = 'Pending'
        elif self.payments >= self.amount:
            self.payment_status = 'Paid'
        elif 0 < self.payments < self.amount:
            self.payment_status = 'Partial-Paid'
        else:
            self.payment_status = 'Pending'

        super().save(*args, **kwargs)

