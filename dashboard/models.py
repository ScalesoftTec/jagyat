from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField 
from django.contrib.auth.models import User
# Create your models here.

class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user',on_delete=models.CASCADE,default="")
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Alerts(models.Model):
    alert_title = models.CharField(max_length=200,null=True,blank=True)
    alert_date = models.DateField(null=True,blank=True)
    money_related = models.BooleanField(default=False)
    info_related = models.BooleanField(default=False)
    document_related = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    user = models.ManyToManyField(User,related_name='alert_user',blank=True)

    
  
    def __str__(self) -> str:
        return self.alert_title

TAX_PLOICIES = (
    ('GST','GST'),
    ('VAT','VAT'),
    ('NO TAX','NO TAX'),
    ('OTHERS','OTHERS'),
)
CHOOSE_REGION = (
    ('India','India'),
    ('Indonesia','Indonesia'),
    ('Thailand','Thailand'),
)


class Logistic(models.Model):
    company_name = models.CharField(max_length=200,null=True,blank=True)
    gstin_no = models.CharField(max_length=200,null=True,blank=True)
    legal_name = models.CharField(max_length=200,null=True,blank=True)
    cost_center_name = models.CharField(max_length=200,null=True,blank=True)
    address_line_1 = models.CharField(max_length=200,null=True,blank=True)
    address_line_2 = models.CharField(max_length=200,null=True,blank=True)
    pin_code = models.CharField(max_length=20,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    branch_name = models.CharField(max_length=200,null=True,blank=True)
    pre_job = models.CharField(max_length=30,null=True,blank=True)
    pre_recievable_invoice = models.CharField(max_length=30,null=True,blank=True)
    mbl_prefix = models.CharField(max_length=30,null=True,blank=True)
    pre_payable_invoice = models.CharField(max_length=30,null=True,blank=True)
    pre_payment_voucher = models.CharField(max_length=30,null=True,blank=True)
    pre_recieve_voucher = models.CharField(max_length=30,null=True,blank=True)
    pre_credit_note = models.CharField(max_length=30,null=True,blank=True)
    pre_debit_note = models.CharField(max_length=30,null=True,blank=True)
    pre_booking = models.CharField(max_length=30,null=True,blank=True)
    pre_inquiry = models.CharField(max_length=30,null=True,blank=True)
    for_company = models.CharField(max_length=200,null=True,blank=True)
    vgm_authorized_shipper = models.CharField(max_length=200,null=True,blank=True)
    company_gst_code = models.CharField(max_length=5,null=True,blank=True)
    created_on = models.DateField(auto_now_add=True,null=True,blank=True)
    logo = models.ImageField()
    stamp = models.ImageField()
    letter_head = models.ImageField()
    mbl_final_image = models.ImageField()
    tax_policy = models.CharField(max_length=20,default="GST",choices=TAX_PLOICIES)
    open_time = models.TimeField(null=True,blank=True)
    close_time = models.TimeField(null=True,blank=True)
    branch_email = models.CharField(max_length=120,null=True,blank=True)
    terms_and_conditions = RichTextUploadingField(null=True,blank=True)
    rec_email_content = RichTextUploadingField(null=True,blank=True)
    is_connected_to_tally = models.BooleanField(default=False)
    rcm_cn_prefix = models.CharField(max_length=120,null=True,blank=True)
    rcm_ri_prefix = models.CharField(max_length=120,null=True,blank=True)
    psr_report = models.BooleanField(default=False)
    is_job_approve_required = models.BooleanField(default=True)
    is_rec_inv_approve_required = models.BooleanField(default=True)
    is_pay_inv_approve_required = models.BooleanField(default=True)
    is_can_approve_required = models.BooleanField(default=True)
    is_do_approve_required = models.BooleanField(default=True)
    is_fc_approve_required = models.BooleanField(default=True)
    is_crn_approve_required = models.BooleanField(default=True)
    is_drn_approve_required = models.BooleanField(default=True)
    auto_journal = models.BooleanField(default=False)
    opening_invoice_no = models.IntegerField(default=0,blank=False)
    region = models.CharField(max_length=80,default="India",choices=CHOOSE_REGION)
    financial_from=models.DateField(null=True,blank=True)
    financial_to=models.DateField(null=True,blank=True)
    opening_mbl_no=models.IntegerField(default=0,blank=False)
    opening_job_no=models.IntegerField(default=0,blank=False)
    opening_crn=models.IntegerField(default=0,blank=False)

    cgst_in_ledger_name_5 = models.CharField(max_length=5,null=True,blank=True,default="CGST")
    cgst_out_ledger_name_5 = models.CharField(max_length=5,null=True,blank=True,default="CGST")
    sgst_in_ledger_name_5 = models.CharField(max_length=5,null=True,blank=True,default="SGST")
    sgst_out_ledger_name_5 = models.CharField(max_length=5,null=True,blank=True,default="SGST")
    igst_in_ledger_name_5 = models.CharField(max_length=5,null=True,blank=True,default="IGST")
    igst_out_ledger_name_5 = models.CharField(max_length=5,null=True,blank=True,default="IGST")
    
    cgst_in_ledger_name_12 = models.CharField(max_length=120,null=True,blank=True,default="CGST")
    cgst_out_ledger_name_12 = models.CharField(max_length=120,null=True,blank=True,default="CGST")
    sgst_in_ledger_name_12 = models.CharField(max_length=120,null=True,blank=True,default="SGST")
    sgst_out_ledger_name_12 = models.CharField(max_length=120,null=True,blank=True,default="SGST")
    igst_in_ledger_name_12 = models.CharField(max_length=120,null=True,blank=True,default="IGST")
    igst_out_ledger_name_12 = models.CharField(max_length=120,null=True,blank=True,default="IGST")
    
    cgst_in_ledger_name_18 = models.CharField(max_length=120,null=True,blank=True,default="CGST")
    cgst_out_ledger_name_18 = models.CharField(max_length=120,null=True,blank=True,default="CGST")
    sgst_in_ledger_name_18 = models.CharField(max_length=120,null=True,blank=True,default="SGST")
    sgst_out_ledger_name_18 = models.CharField(max_length=120,null=True,blank=True,default="SGST")
    igst_in_ledger_name_18 = models.CharField(max_length=120,null=True,blank=True,default="IGST")
    igst_out_ledger_name_18 = models.CharField(max_length=120,null=True,blank=True,default="IGST")
    
    cgst_in_ledger_name_28 = models.CharField(max_length=120,null=True,blank=True,default="CGST")
    cgst_out_ledger_name_28 = models.CharField(max_length=120,null=True,blank=True,default="CGST")
    sgst_in_ledger_name_28 = models.CharField(max_length=120,null=True,blank=True,default="SGST")
    sgst_out_ledger_name_28 = models.CharField(max_length=120,null=True,blank=True,default="SGST")
    igst_in_ledger_name_28 = models.CharField(max_length=120,null=True,blank=True,default="IGST")
    igst_out_ledger_name_28 = models.CharField(max_length=120,null=True,blank=True,default="IGST")
    
    round_off_ledger_name = models.CharField(max_length=120,null=True,blank=True,default="Round Off")
    unique_no = models.UUIDField(null=True,blank=True)

    
    
    
    def __str__(self) -> str:
        return self.branch_name
    
    class Meta:
        verbose_name = 'Company Setting'
        verbose_name_plural = 'Company Settings'
        ordering = ('branch_name',)
    
class TallyIpAdress(models.Model):
    ip_url = models.CharField(max_length=120,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.ip_url
    
    
