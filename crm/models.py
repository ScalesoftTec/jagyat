from django.db import models
from masters.models import Party,PartyAddress,ShippingLines,Airlines,Location,LogFolder,BillingHead,currency,Ports,CHOICE_FREIGHT_TERM,CHOICE_MODULE,CHOICE_JOB_TYPE,CHOOSE_CONTAINER_TYPE,State
from dashboard.models import Logistic
from django.contrib.auth.models import User
# Create your models here.


class sales_person_party(LogFolder):
    party_name=models.CharField(max_length=200,null=True,blank=True)
    party_short=models.CharField(max_length=200,null=True,blank=True)
    contact_person=models.CharField(max_length=200,null=True,blank=True)
    contact_number=models.CharField(max_length=200,null=True,blank=True)
    contact_email=models.CharField(max_length=200,null=True,blank=True)
    states=models.ForeignKey(State,on_delete=models.SET_NULL,null=True,blank=True,related_name='states_data')
    address1=models.TextField(null=True,blank=True)
    address2=models.TextField(null=True,blank=True)
    address3=models.TextField(null=True,blank=True)
    sales_person=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.party_name




CHOOSE_SOURCE = (
    ('Online','Online'),
    ('Advertisement','Advertisement'),
    ('Cold Calling','Cold Calling'),
    ('Reference','Reference'),
)


CHOOSE_SOURCE = (
    ('Online','Online'),
    ('Advertisement','Advertisement'),
    ('Cold Calling','Cold Calling'),
    ('Reference','Reference'),
)

choose_status=(
    ('Qualified','Qualified'),
    ('Prospect','Prospect'),
    ('Business Won','Business Won'),
)

class Event(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name="event_branch")
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="event_user")
    assigned_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="event_asignee")
    title = models.CharField(max_length=200,null=True,blank=True)
    customer=models.ForeignKey(sales_person_party,on_delete=models.SET_NULL,null=True,blank=True,related_name="sales_customer_data")
    description = models.TextField(null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    manager_remarks = models.TextField(null=True,blank=True)
    status=models.CharField(max_length=20,choices=choose_status,default='Qualifie')
    remarks = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self,*args,**kwargs):
        
       

        return super(Event,self).save(*args,**kwargs)


class Lead(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name="lead_company_type")
    sales_person=models.CharField(max_length=200,null=True,blank=True)
    manager_remarks = models.TextField(max_length=200,null=True,blank=True)\
    
    def __str__(self):
        return self.sales_person


class Leads_Details(LogFolder):
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,null=True,blank=True,related_name='leads_details_data')
    company_name = models.CharField(max_length=120)
    contact_person = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=60,null=True,blank=True)
    phone=models.CharField(max_length=12,null=True,blank=True)
    location=models.CharField(max_length=120)
    remarks = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.company_name


CHOOSE_PRIORITY = (
    ('Normal','Normal'),
    ('Express','Express'),
)


class Inquiry(LogFolder):
    quotation_no = models.CharField(max_length=200)
    date_of_inquiry = models.DateField(blank=True, null=True)
    company_type = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name="inquiry_company_type")
    customer = models.ForeignKey(sales_person_party, on_delete=models.SET_NULL, null=True,related_name='sales_party')
   
    shipping_line = models.ForeignKey(ShippingLines, on_delete=models.SET_NULL, null=True, blank=True,related_name='inquiry_shipping_line')   
    airline = models.ForeignKey(Airlines, on_delete=models.SET_NULL, null=True, blank=True,related_name='inquiry_airline')
    valid_from = models.DateField()                        
    valid_till = models.DateField()                        
    pol = models.ForeignKey(Ports, on_delete=models.SET_NULL, null=True, blank=True,related_name='inquiry_pol')
    pod = models.ForeignKey(Ports, on_delete=models.SET_NULL, null=True, blank=True,related_name='inquiry_pod')
    origin = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,related_name='inquiry_origin')
    destination = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,related_name='inquiry_destination')
    priority = models.CharField(max_length=30,choices=CHOOSE_PRIORITY,default="Normal")
    freght_terms = models.CharField(max_length=60,choices=CHOICE_FREIGHT_TERM,null=True,blank=True)
    work_scope = models.CharField(max_length=80,choices=CHOICE_JOB_TYPE,null=True,blank=True)
    module = models.CharField(max_length=60,choices=CHOICE_MODULE,default="Sea Export")
    gross = models.CharField(max_length=50,null=True,blank=True)
    detention_at_origin = models.CharField(max_length=100,null=True,blank=True)
    detention_at_pod = models.CharField(max_length=100,null=True,blank=True)
    routing = models.CharField(max_length=120,null=True,blank=True)
    vessel_schedule = models.DateField(null=True,blank=True)                        
    container_type = models.CharField(max_length=80,choices=CHOOSE_CONTAINER_TYPE,null=True,blank=True)
    commodity = models.CharField(max_length=200,null=True,blank=True)
    commodity_type = models.CharField(max_length=200,null=True,blank=True)
    total_packages = models.CharField(max_length=100,null=True,blank=True)
    total_packages_type = models.CharField(max_length=200,null=True,blank=True)
    
    gross_amount = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    advance_amount = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    profit_amount = models.FloatField(default=0)
    remark = models.CharField(max_length=300, null=True, blank=True)
   
    def __str__(self):
        return str(self.quotation_no)


class InquiryDetail(LogFolder):
    inquiry = models.ForeignKey(Inquiry,related_name="inquiry_reference",null=True,on_delete=models.CASCADE)

    billing_head = models.ForeignKey(BillingHead,related_name='inquiry_billing_head',null=True, blank=True, on_delete=models.SET_NULL)
    
    currency = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True, blank=True,related_name='inquiry_currency')
    
    ex_rate = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    rate_rec = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    qty_unit = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    gst = models.FloatField(default=0)
    gst_amount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    
    