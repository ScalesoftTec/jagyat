from django.db import models
from django.contrib.auth.models import User
from home.models import UserAccount,DocumentHandler
from dashboard.models import Logistic
from datetime import date,datetime
from django.db.models import Count
from django.db.models import Q

class LogFolder(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='%(app_label)s_%(class)s_created_by')
    activity_name = models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(null=True,auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='%(app_label)s_%(class)s_updated_by')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='%(app_label)s_%(class)s_deleted_by')
    is_deleted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_journalised = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
    
   
# Create your models here.

        
CHOOSE_CONTAINER_TYPE = (
    ("20", "20"),
    ("40", "40"),  
    ("45", "45"),  
    ("20 HQ", "20 HQ"),
    ("20 GP", "20 GP"),
    ("40 HQ", "40 HQ"),
    ("45 HQ", "45 HQ"),
    ("40 GP", "40 GP"),
    ("20 FT", "20 FT"),
    ("20 HC", "20 HC"),
    ("40 HC", "40 HC"),
    ("20 DV", "20 DV"),
    ("40 DV", "40 DV"),
    ("20 OT", "20 OT"),
    ("40 OT", "40 OT"),
    ("20 FR", "20 FR"),
    ("40 FR", "40 FR"),
    ("20 RF", "20 RF"),
    ("40 RF", "40 RF"),
    ("20 DC", "20 DC"),
    ("40 DC", "40 DC"),
    ('Break Bulk', 'Break Bulk'),
    ('Tank', 'Tank'),
    ('LCL', 'LCL'),
    ('Air', 'Air'),
)


#=================== Category Master ==================================

CATEGORIES = (
    ('Income', 'Income'),
    ('Indirect Income', 'Indirect Income'),
    ('Other Income Type', 'Other Income Type'),
    ('Expense', 'Expense'),
    ('Indirect Expense', 'Indirect Expense'),
    ('Other Expenses Type', 'Other Expenses Type'),
    ('Assets', 'Assets'),
    ('Liabilities','Liabilities'),
    ('Stock Holders Equity','StockHolders Equity')
)

class CategoryMaster(LogFolder):
    name = models.CharField(max_length=200,null=False,blank=False,default="")
    description = models.CharField(max_length=200,null=True,blank=True,default="")
    under = models.CharField(max_length=200, null=False, blank=False, default="",choices=CATEGORIES)
    created_by = models.ForeignKey(UserAccount, null=True, blank=True, on_delete=models.CASCADE, related_name='category_created_by')

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']

# Currency List
class currency(LogFolder):
    name = models.CharField(max_length=100,null=True,blank=True)
    short_name = models.CharField(max_length=10,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.short_name}'
    
    class Meta:
        verbose_name = 'Currencies'
        verbose_name_plural = 'Currencies'

# Shipping Line
class ShippingLines(LogFolder):
    name = models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=10,null=True,blank=True,default='Sea')
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Shipping Line'
        verbose_name_plural = 'Shipping Lines'

# Air Line
class Airlines(LogFolder):
    name = models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=10,null=True,blank=True,default='Air')
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Air Line'
        verbose_name_plural = 'Air Lines'
        
# Country List
class Country(LogFolder):
    name = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'

PORT_TYPE = (
    ('Sea','Sea'),
    ('Air','Air'),
)

# Ports List
class Ports(LogFolder):
    name = models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=20,null=True,blank=True,choices=PORT_TYPE)
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Port'
        verbose_name_plural = 'Ports'
        ordering = ('name',)
        
# States List
class State(LogFolder):
    name = models.CharField(max_length=100,null=True,blank=True)
    gst_code = models.CharField(max_length=5,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'States'
        verbose_name_plural = 'States'
        
    
        
# --------------------- Commodity ------------------------------------


class Commodity(LogFolder):
    type = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Commodities'
        verbose_name_plural = 'Commodities'
    
        
# --------------------- Location ------------------------------------


class Location(LogFolder):
    name = models.CharField(max_length=200)

    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ('name',)
    
    
# --------------------- Billing Head ------------------------------------

BH_CATEGROY = (
    ('FREIGHT CHARGES','FREIGHT CHARGES'),
    ('TAXABLE CHARGES','TAXABLE CHARGES'),
    ('NON-TAXABLE CHARGES','NON-TAXABLE CHARGES'),
)

BH_UNDER = (
    ('Direct','Direct'),
    ('Indirect','Indirect '),    
)

class BillingHead(LogFolder):
    tally_group = models.ForeignKey('masters.LedgerCategory',on_delete=models.SET_NULL,null=True,blank=True,related_name='bh_category')
    billing_head = models.CharField(max_length=200)
    alias = models.CharField(max_length=60,null=True,blank=True)
    hsn_code = models.CharField(max_length=30, null=True, blank=True)
    is_transfered_to_tally = models.BooleanField(default=False)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name="bh_child")
    is_disabled = models.BooleanField(default=False,null=True, blank=True)
    gst = models.FloatField(default=0,null=True, blank=True)
    under= models.CharField(max_length=80,choices=BH_UNDER,default='Direct',null=True, blank=True)
    category= models.CharField(max_length=80,choices=BH_CATEGROY,default='TAXABLE CHARGES',null=True, blank=True)
    always_igst = models.BooleanField(default=False,null=True, blank=True)
    is_head = models.BooleanField(default=False,null=True, blank=True)
    is_service = models.BooleanField(default=True,null=True, blank=True)
    gst_applicable = models.BooleanField(default=True,null=True, blank=True)
    sales_head = models.CharField(max_length=200,null=True,blank=True)
    purchase_head = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self) -> str:
        if self.alias:
            return f'{self.billing_head}/{self.alias}'
        else:
            return f'{self.billing_head}'
    def __str__(self) -> str:
        if self.alias:
            return f'{self.billing_head}/{self.alias}'
        else:
            return f'{self.billing_head}'

    
    class Meta:
        verbose_name = 'Billing Heads'
        verbose_name_plural = 'Billing Heads'
        ordering = ('billing_head',)

# ---------------------Trailor Billing Head ------------------------------------

TRAILOR_BH_TYPE = (
    ('Direct','Direct'),
    ('Indirect','Indirect')
)

class TrailorBillingHead(LogFolder):
    billing_head = models.CharField(max_length=200)
    hsn_code = models.CharField(max_length=30, null=True, blank=True)
    gst = models.FloatField(default=0)
    always_igst = models.BooleanField(default=False)
    is_head = models.BooleanField(default=False,null=True, blank=True)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name="trailor_bh_child")
    type = models.CharField(max_length=10,default="Direct",choices=TRAILOR_BH_TYPE)
    def __str__(self) -> str:
        return f'{self.billing_head}'
    
    class Meta:
        verbose_name = 'Trailor Billing Heads'
        verbose_name_plural = 'Trailor Billing Heads'
     
# --------------------- Bank  ------------------------------------

DR_CR = (
    ('Debit','Debit'),
    ('Credit','Credit'),
)
class Bank(LogFolder):
    company_type = models.ForeignKey(Logistic,null=True,blank=True,on_delete=models.CASCADE,related_name="bank_company")
    account_no = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    branch_name = models.CharField(max_length=200, null=True, blank=True)
    ifsc_code = models.CharField(max_length=200, null=True, blank=True)
    beneficiary_name = models.CharField(max_length=200, null=True, blank=True)
    swift_code = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
     
    opening_balance = models.FloatField(default=0)
    opening_in = models.CharField(max_length=30,choices=DR_CR,default="Debit")
    opening_date = models.DateField(null=True,blank=True)
    tally_group = models.ForeignKey('masters.LedgerCategory',on_delete=models.SET_NULL,null=True,blank=True,related_name='bank_category')
    opening_ledger_category = models.ForeignKey('masters.LedgerCategory',default=1,null=True,blank=True,on_delete=models.SET_NULL,related_name='bank_opening_group')
    
    
    def __str__(self) -> str:
        return f'{self.account_no} / {self.bank_name}'
    
    class Meta:
        verbose_name = 'Bank Detail'
        verbose_name_plural = 'Bank Details'
    
         
# --------------------- UOM  ------------------------------------

class UOM(LogFolder):
    name = models.CharField(max_length=200, null=True, blank=True)
    short_name = models.CharField(max_length=200, null=True, blank=True)
    decimal_places = models.CharField(max_length=10,default="0")
    is_transfered_to_tally = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Unit Of Measurements'
        verbose_name_plural = 'Unit Of Measurements'
    


class City(LogFolder):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

class Battery(LogFolder):
    brand_name = models.CharField(max_length=120)
    model_name = models.CharField(max_length=120)
    vendor_name = models.CharField(max_length=120)
    battery_no = models.CharField(max_length=120)
    invoice_no = models.CharField(max_length=120)
    invoice_date = models.DateField()
    amount = models.CharField(max_length=120)
    def __str__(self) -> str:
        return f'{self.battery_name}'
    
    class Meta:
        verbose_name = 'Battery'
        verbose_name_plural = 'Batteries'

TYRE_TYPE = (
    ('HORSE','HORSE'),
    ('TROLLEY','TROLLEY'),
)

class Tyre(LogFolder):
    brand_name = models.CharField(max_length=120,null=True,blank=True)
    model_name = models.CharField(max_length=120,null=True,blank=True)
    vendor_name = models.CharField(max_length=120,null=True,blank=True)
    tyre_no = models.CharField(max_length=120,null=True,blank=True)
    invoice_no = models.CharField(max_length=120,null=True,blank=True)
    invoice_date = models.DateField(null=True,blank=True)
    amount = models.CharField(max_length=120,null=True,blank=True)
    type = models.CharField(max_length=120,choices=TYRE_TYPE,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.tyre_no} ({self.brand_name})'
    
    class Meta:
        verbose_name = 'Tyre'
        verbose_name_plural = 'Tires'
    



# -------------------------------Party Master--------------------------------------
FIN_NON_TYPE = (
    ('Financial', 'Financial'),
    ('Non Financial', 'Non Financial'),
    )

PROP_TYPE = (
    ('Private Limited', 'Private Limited'),
    ('Public Limited', 'Public Limited'),
    ('Company Limited', 'Company Limited'),
    ('Partnership', 'Partnership'),
    ('Proprieter', 'Proprieter'),
    ('Governement Firm', 'Governement Firm'),
    )



PRTY_UNDER = (
    ("Co-Loaders", "Co-Loaders"),
    ("Shipping Line", "Shipping Line"),
    ("Airlines", "Airlines"),
    ("Other Trade Creditors", "Other Trade Creditors"),
    ("Sundry Debtors", "Sundry Debtors"),
    ("Non Trade Creditors", "Non Trade Creditors"),
    ("Others", "Others")
    )
TDS = (
    ("TDS 194H", "TDS 194H"),
    ("TDS 194C", "TDS 194C"),
    ("TDS 194J", "TDS 194J"),
    ("TDS 194I", "TDS 194I"),
    ("TDS 1942", "TDS 1942"),
    )
RATE_TYPE = (
    ("As Agreed", "As Agreed"),
    ("As Actual", "As Actual"),
    )

PER = (
    ("Airwaybill", "Airwaybill"),
    ("Chargeable Weight", "Chargeable Weight"),
    ("General", "General"),
    ("Gross Weight", "Gross Weight"),
    )

TALLY_UNDER = (
    ('Sundry Debtors','Sundry Debtors'),
    ('Sundry Creditors','Sundry Creditors'),
 
)




class PartyType(models.Model):
    name = models.CharField(max_length=120,null=True,blank=True)
    def __str__(self) -> str:
        return self.name



PARTY_CREATION_CHOICES = [
    ('DELHI', 'DELHI'),
    ('MUMBAI', 'MUMBAI')
]

class Party(LogFolder):
    company_type = models.ForeignKey(Logistic,null=True,blank=True,on_delete=models.CASCADE,related_name="party_company")
    party_name = models.CharField(max_length=180)
    alias = models.CharField(max_length=100,null=True,blank=True)
    tally_group = models.ForeignKey('masters.LedgerCategory',on_delete=models.SET_NULL,null=True,blank=True,related_name='party_category')
    fin_non_fin = models.CharField(max_length=60, choices=FIN_NON_TYPE, null=True, blank=True)

    for_station = models.CharField(max_length=120,null=True,blank=True, choices=PARTY_CREATION_CHOICES)
    # for_station = models.CharField(max_length=120,null=True,blank=True)
    party_company_type = models.CharField(max_length=120, choices=PROP_TYPE, null=True, blank=True)
    party_type = models.ManyToManyField(PartyType)
    tally_under = models.CharField(max_length=80, choices=TALLY_UNDER, null=True, blank=True)
    under = models.CharField(max_length=120, choices=PRTY_UNDER, null=True, blank=True)
    account_manager = models.ForeignKey('hr.Employee',related_name='party_manager',on_delete=models.SET_NULL ,null=True, blank=True)
    bl_type = models.CharField(max_length=180, null=True, blank=True)
    contact_person=models.CharField(max_length=120,null=True,blank=True)
    party_short_name = models.CharField(max_length=120, null=True, blank=True)
    party_remarks = models.TextField( null=True, blank=True)
    iec_code = models.CharField(max_length=60, null=True, blank=True)
    cin_number = models.CharField(max_length=120, null=True, blank=True)
    registered_gst = models.CharField(max_length=120, null=True, blank=True)
    registered_address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    credit_days = models.FloatField(default=0)
    is_transfered_to_tally = models.BooleanField(default=False)
    kyc_form = models.FileField(null=True,blank=True,upload_to="party/kyc/")
    photo_id = models.FileField(null=True,blank=True,upload_to="party/kyc/")
    gst_certificate = models.FileField(null=True,blank=True,upload_to="party/kyc/")
    other_document = models.FileField(null=True,blank=True,upload_to="party/kyc/")
    opening_balance = models.FloatField(default=0)
    opening_in = models.CharField(max_length=30,choices=DR_CR,default="Debit")
    opening_date = models.DateField(null=True,blank=True)
    opening_ledger_category = models.ForeignKey('masters.LedgerCategory',default=1,null=True,blank=True,on_delete=models.SET_NULL,related_name='party_opening_group')

    def __str__(self) -> str:
        if self.alias:
            return f'{self.party_name} / {self.alias}'
        else:
            return f'{self.party_name}'


    class Meta:
        verbose_name = 'Parties'
        verbose_name_plural = 'Parties'
        ordering = ('party_name',)
        
        
class PartyAddress(LogFolder):
    party = models.ForeignKey(Party,on_delete=models.CASCADE,null=False,blank=False,related_name='party_address')
    branch = models.CharField(max_length=120,null=True,blank=True)
    corp_address_line1 = models.CharField(max_length=200,null=True,blank=True)
    corp_address_line2 = models.CharField(max_length=200,null=True,blank=True)
    corp_address_line3 = models.CharField(max_length=200,null=True,blank=True)
    corp_country = models.CharField(max_length=200,null=True,blank=True)
    corp_state = models.ForeignKey(State,on_delete=models.SET_NULL,related_name='party_state',null=True,blank=True)
    corp_city = models.CharField(max_length=120,null=True,blank=True)
    corp_tel = models.CharField(max_length=20, null=True, blank=True)
    corp_email = models.TextField(null=True, blank=True)
    corp_website = models.CharField(max_length=200, null=True, blank=True)
    corp_gstin = models.CharField(max_length=200,null=True, blank=True)
    corp_zip = models.CharField(max_length=200, null=True, blank=True)
    corp_fax = models.CharField(max_length=200, null=True, blank=True)
    corp_contact = models.CharField(max_length=200, null=True, blank=True)
    corp_pan = models.CharField(max_length=200, null=True, blank=True)
    corp_tan = models.CharField(max_length=200, null=True, blank=True)
    corp_contact_person = models.CharField(max_length=200,null=True,blank=True)
    

    def __str__(self) -> str:
        return f'{self.branch}'

    class Meta:
        verbose_name = 'Party Address'
        verbose_name_plural = 'Parties Adresses'
        ordering = ('-id',)
    
    def get_gst_code(self):
        return self.corp_state.gst_code
        
    


class Vendor(LogFolder):
    company_type = models.ForeignKey(Logistic,null=True,blank=True,on_delete=models.CASCADE,related_name="vendor_company")
    vendor_name = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=120)
    address_line2 = models.CharField(max_length=120)
    address_line3 = models.CharField(max_length=120)
    country = models.CharField(max_length=200,null=True,blank=True)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,related_name='vendor_fk_state',null=True,blank=True)
    city = models.CharField(max_length=120,null=True,blank=True)
    tel = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    gstin = models.CharField(max_length=20,null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    pan = models.CharField(max_length=20, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    opening_balance = models.FloatField(default=0)
    opening_in = models.CharField(max_length=30,choices=DR_CR,default="Debit")
    opening_date = models.DateField(null=True,blank=True)
    opening_ledger_category = models.ForeignKey('masters.LedgerCategory',default=1,null=True,blank=True,on_delete=models.SET_NULL,related_name='vendor_opening_group')
    tally_group = models.ForeignKey('masters.LedgerCategory',on_delete=models.SET_NULL,null=True,blank=True,related_name='vendor_category')

    
    
    
    def __str__(self) -> str:
        return f'{self.vendor_name}'

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ('vendor_name',)


# ---------------------Job Master-------------------------

CHOICE_JOB_TYPE = (

    ('Freight Forwarding','Freight Forwarding'),
    ('Custom Clearance','Custom Clearance'),
    ('Transportation','Transportation'),
)

class ScaleOfWork(models.Model):
    name = models.CharField(max_length=180,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name


CHOICE_FREIGHT_TERM = (
    ('Prepaid','Prepaid'),
    ('Collect','Collect'),
    ('Part-Prepaid/Collect','Part-Prepaid/Collect'), 
    ('C&F' ,'C&F'),
    ('CIF' ,'CIF'),  
    ('DAP' ,'DAP'),  
    ('DDP' ,'DDP'),  
    ('FOB' ,'FOB'),  
    ('EXW' ,'EXW'),  
)

CHOICE_MODULE = (
    ('Sea Export','Sea Export'),
    ('Sea Import','Sea Import'),
    ('Air Export','Air Export'),
    ('Air Import','Air Import'),
    ('Transport','Transport'),
)
CHOICE_JOB_STATUS = (
    ('Open','Open'),
    ('Received','Received'),
    ('Pending For Invoice','Pending For Invoice'),
    ('Under Custom Clearance','Under Custom Clearance'),
    ('Under Stuffing','Under Stuffing'),
    ('Railed Out','Railed Out'),
    ('Arrived on Port','Arrived on Port'),
    ('Sailed','Sailed'),
    ('Close','Close'),
    ('Cancel','Cancel'),
   
)
CHOICE_GOODS_RECIEPT = (
    ('Carting','Carting'),
    ('F-Stuffing','F-Stuffing'),
    ('Self Sealing','Self Sealing'),
    
   
)
CHOICE_CARGO_NATURE = (
    ('General','General'),
    ('Hazardous','Hazardous'),
  
)


OWNERHIRE = (
    ('Owned','Owned'),
    ('Hire','Hire'),
)


MBL_TYPE = (
    ('HBL','HBL'),
    ('MBL','MBL'),
)

BL_TYPE = (
    ('ORIGINAL','ORIGINAL'),
    ('SEAWAY','SEAWAY'),
)
commodities_type_data = (
    ('HAZARDOUS','HAZARDOUS'),
    ('GENERAL','GENERAL'),
    ('OTHER','OTHER'),

)

CHOICE_JOB_TYPE = (
    ('Central Office','Central Office'),
    ('Only Forwarding','Only Forwarding'),
    ('Baggaging','Baggaging'),
    ('Door To Door','Door To Door'),
    ('Only Clearance','Only Clearance'),
    ('Clearance and Forwarding','Clearance and Forwarding'),
    ('Clearing','Clearing'),
    ('Transport','Transport'),
)


HBL_LOCATION_STATUS = (
    ("Original Recived at Delhi","Original Recived at Delhi"),
    ("Original Recived at Port","Original Recived at Port"),
    ("TELEX OK","TELEX OK"),
    ("Pending","Pending"),
)


class BookingMaster(LogFolder):
    module = models.CharField(max_length=100,null=True,blank=True,choices=CHOICE_MODULE)
    company_type = models.ForeignKey(Logistic,on_delete=models.SET_NULL,related_name='booking_company',null=True,blank=True)
    booking_no = models.CharField(max_length=60,null=True,blank=True)
    booking_date = models.DateField(null=True,blank=True,default=date.today)
    ref_no = models.CharField(max_length=60,null=True,blank=True)
    shipper = models.ForeignKey(Party,on_delete=models.SET_NULL,related_name='booking_shipper',null=True,blank=True)
    consignee = models.ForeignKey(Party,on_delete=models.SET_NULL,related_name='booking_consignee',null=True,blank=True)
    agent = models.ForeignKey(Party,on_delete=models.SET_NULL,related_name='booking_agent',null=True,blank=True)
    pol = models.ForeignKey(Ports,on_delete=models.SET_NULL,related_name='booking_pol',null=True,blank=True)
    pod = models.ForeignKey(Ports,on_delete=models.SET_NULL,related_name='booking_pod',null=True,blank=True)
    fpod = models.ForeignKey(Ports,on_delete=models.SET_NULL,related_name='booking_fpod',null=True,blank=True)
    shipping_line = models.ForeignKey(ShippingLines,on_delete=models.SET_NULL,related_name='booking_sl',null=True,blank=True)
    container_size = models.CharField(max_length=20,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    no_of_container = models.CharField(max_length=250,null=True,blank=True)
    weight = models.CharField(max_length=250, null=True,blank=True)
    cbm = models.CharField(max_length=150,null=True,blank=True)
    mbl_no = models.CharField(max_length=150,null=True,blank=True)
    hbl_no = models.CharField(max_length=150,null=True,blank=True)
    buying_rate = models.CharField(max_length=150,null=True,blank=True)
    selling_rate = models.CharField(max_length=150,null=True,blank=True)
    etd = models.DateField(null=True,blank=True)
    sales_person = models.ForeignKey('hr.Employee',null=True,blank=True,on_delete=models.SET_NULL,related_name="booking_sales_person")
    
    
    #  Added on 7-Mar-2025 
    party_name = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)
    actual_weight = models.CharField(max_length=250, null=True,blank=True)
    volume_weight = models.CharField(max_length=200, blank=True, null=True)
    
    def save(self,*args,**kwargs):
        if not self.booking_no:
            
           
            booking_prefix =  self.company_type.pre_booking
            if not booking_prefix:
                booking_prefix = 'RK/'

            total_bookings = BookingMaster.objects.filter(created_at__gte = self.company_type.financial_from).filter(company_type=self.company_type).count() + 1 
            is_duplicate = True
            
            while is_duplicate:
                booking_no = booking_prefix + str(total_bookings).zfill(4)
                booking = BookingMaster.objects.filter(booking_no=booking_no).count()
                if booking == 0:
                    is_duplicate = False
                    self.booking_no = booking_no
                else:
                    total_bookings += 1
        
        
        super(BookingMaster, self).save(*args, **kwargs)
        
    def __str__(self):
        if self.ref_no:
            return f"{self.booking_no} ({self.ref_no})"
        return self.booking_no



SHIPMENT_TYPE_CHOICES = [
    ('FCL', 'FCL'),
    ('LCL', 'LCL'),
    ('AIR', 'AIR'),
    
]

class JobMaster(LogFolder):
    job_no = models.CharField(max_length=30,null=False,blank=True)
    booking = models.ForeignKey(BookingMaster,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_booking')
    job_date = models.DateField(null=False,blank=False,default=date.today)
    scale_of_work = models.ManyToManyField(ScaleOfWork,blank=True)
    work_scope = models.CharField(max_length=80,choices=CHOICE_JOB_TYPE,null=True,blank=True)
    line_freight = models.CharField(max_length=100,null=True,blank=True,choices=CHOICE_FREIGHT_TERM)
    freight_term = models.CharField(max_length=100,null=True,blank=True,choices=CHOICE_FREIGHT_TERM)
    module = models.CharField(max_length=100,null=True,blank=True,choices=CHOICE_MODULE)
    shipping_line = models.ForeignKey(ShippingLines,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_shipping_line')
    do_no = models.CharField(max_length=100,null=True,blank=True)
    mbl_no = models.CharField(max_length=100,null=True,blank=True)
    mbl_date = models.DateField(null=True,blank=True)
    handling_type = models.CharField(max_length=120,null=True,blank=True,choices=CHOICE_JOB_TYPE)
    hbl_no = models.CharField(max_length=100,null=True,blank=True)
    move_type = models.CharField(max_length=200,null=True,blank=True)
    account_manager = models.ForeignKey("hr.Employee",on_delete=models.SET_NULL,null=True,blank=True,related_name="job_manager")
    hbl_date = models.DateField(null=True,blank=True)
    container_return_date = models.DateField(null=True,blank=True)
    vessel_voy_name = models.CharField(max_length=200,null=True,blank=True)
    vessel_voy_date = models.DateField(null=True,blank=True)
    shipper_invoice_no = models.CharField(max_length=200,null=True,blank=True)
    via_no = models.CharField(max_length=200,null=True,blank=True)
    rotation_no = models.CharField(max_length=200,null=True,blank=True)
    container_count = models.IntegerField(default=0,null=True,blank=True)
    inquiry = models.ForeignKey('crm.Inquiry',on_delete=models.SET_NULL,null=True,blank=True,related_name='job_inquiry')
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='job_company_type')
    alternate_company = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_alternate_company')
    account = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_account_address')
    account_address = models.ForeignKey(PartyAddress,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_account')
    shipper = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_shipper')
    consignee = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_consignee')
    notify_party = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_notify_party')
    booking_party = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_buying_house')
    overseas_agent = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_overseas_agent')
    broker = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_broker')
    importer = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_importer')
    forwarder = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_forwarder')
    stuffing_type = models.CharField(max_length=150,null=True,blank=True)
    place_of_reciept = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_place_of_reciept')
    final_destination = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_final_destination')
    place_of_loading = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_place_of_loading')
    place_of_loading_date = models.DateField(null=True,blank=True)
    place_of_unloading = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_place_of_unloading')
    place_of_unloading_date = models.DateField(null=True,blank=True)
    port_of_loading = models.ForeignKey(Ports,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_pol')
    port_of_discharge = models.ForeignKey(Ports,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_pod')
    po_no = models.CharField(max_length=100,null=True,blank=True)
    commodity = models.CharField(max_length=200,null=True,blank=True)
    commodity_type = models.CharField(max_length=200,null=True,blank=True,choices=commodities_type_data)
    no_of_packages = models.CharField(max_length=20,null=True,blank=True)
    packages_type = models.CharField(max_length=200,null=True,blank=True)
    volume = models.CharField(max_length=200,null=True,blank=True)
    gross_weight = models.CharField(max_length=200,null=True,blank=True)
    net_weight = models.CharField(max_length=200,null=True,blank=True)
    cbm = models.CharField(max_length=200,null=True,blank=True)
    job_status = models.CharField(max_length=50,null=True,blank=True,choices=CHOICE_JOB_STATUS,default='Open')
    remarks = models.CharField(max_length=300,null=True,blank=True)
    charges = models.CharField(max_length=60,null=True,blank=True)
    imdg = models.CharField(max_length=60,null=True,blank=True)
    gigm = models.CharField(max_length=200,null=True,blank=True)
    ligm = models.CharField(max_length=200,null=True,blank=True)
    gate_open_date = models.DateField(null=True,blank=True)
    document_cutoff_date = models.DateField(null=True,blank=True)
    form13_cutoff_date = models.DateField(null=True,blank=True)
    gate_cutoff_date = models.DateField(null=True,blank=True)
    gigm_date = models.DateField(null=True,blank=True)
    ligm_date = models.DateField(null=True,blank=True)
    igm_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=200,null=True,blank=True)
    bl_type = models.CharField(max_length=100, null=True, blank=True,choices=BL_TYPE)
    mbl_type = models.CharField(max_length=200, null=True, blank=True,choices=MBL_TYPE)
    no_of_hbl = models.CharField(max_length=30, null=True, blank=True)
    part_bl = models.CharField(max_length=90, null=True, blank=True)
    railout_date = models.DateField(null=True,blank=True)
    # For Air
    docket_no = models.CharField(max_length=100,null=True,blank=True)
    air_line = models.ForeignKey(Airlines,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_air_line')
    awb_no = models.CharField(max_length=100,null=True,blank=True)
    flight_no = models.CharField(max_length=100,null=True,blank=True)
    igm_no = models.CharField(max_length=100,null=True,blank=True)
    awb_date = models.DateField(null=True,blank=True)
    flight_date = models.DateField(null=True,blank=True)
    clearance = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_clearance')
    container_pickup_location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_container_pickup')
    container_pickup_date = models.DateField(null=True,blank=True)
    container_no = models.TextField(null=True,blank=True)
    container_type = models.CharField(max_length=200,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    delivery = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_party')
    cfs_in_date = models.DateField(null=True,blank=True)
    cfs_out_date = models.DateField(null=True,blank=True)
    do_date = models.DateField(null=True,blank=True)
    shipper_invoice_date = models.DateField(null=True,blank=True)
    stuffing_date = models.DateField(null=True,blank=True)
    rail_out_date = models.DateField(null=True,blank=True)
    sailing_date = models.DateField(null=True,blank=True)
    sob_date = models.DateField(null=True,blank=True)
    fpod_date = models.DateField(null=True,blank=True)
    eta_date = models.DateField(null=True,blank=True)
   
    actual_arrival_pod_date = models.DateField(null=True,blank=True)
    port_out_date = models.DateField(null=True,blank=True)
    oc_date = models.DateField(null=True,blank=True)
    eway_date = models.DateField(null=True,blank=True)
    asessable_value = models.CharField(max_length=60,null=True,blank=True)
    
    transipment1_eta = models.DateField(null=True,blank=True)
    transipment1_etd = models.DateField(null=True,blank=True)
    transipment1_vessel = models.CharField(max_length=120,null=True,blank=True)
    transipment1_country = models.CharField(max_length=120,null=True,blank=True)
    
    transipment2_eta = models.DateField(null=True,blank=True)
    transipment2_etd = models.DateField(null=True,blank=True)
    transipment2_vessel = models.CharField(max_length=120,null=True,blank=True)
    transipment2_country = models.CharField(max_length=120,null=True,blank=True)
    
    # For Transport
    owned_hire = models.CharField(max_length=120,null=True,blank=True,choices=OWNERHIRE)
    gr_no = models.CharField(max_length=120,null=True,blank=True)
    bilty_no = models.CharField(max_length=120,null=True,blank=True)
    trailor_no = models.CharField(max_length=120,null=True,blank=True)
    l_seal = models.CharField(max_length=120,null=True,blank=True)
    ship_bill_no = models.CharField(max_length=60,null=True,blank=True)
    ship_bill_type = models.CharField(max_length=60,null=True,blank=True)
    ship_bill_date = models.DateField(null=True,blank=True)
    currency = models.ForeignKey(currency,on_delete=models.SET_NULL,null=True,blank=True)
    cfs = models.CharField(max_length=60,null=True,blank=True)
    invoice_no = models.CharField(max_length=60,null=True,blank=True)
    invoice_date = models.DateField(null=True,blank=True)
    invoice_value = models.CharField(max_length=60,null=True,blank=True)
    bl_type = models.CharField(max_length=60,null=True,blank=True)
    bl_no = models.CharField(max_length=60,null=True,blank=True)
    lc_no = models.CharField(max_length=60,null=True,blank=True)
    ams_no = models.CharField(max_length=60,null=True,blank=True)
    ams_date = models.DateField(null=True,blank=True)
    isf_no = models.CharField(max_length=60,null=True,blank=True)
    isf_date = models.DateField(null=True,blank=True)
    entry_cont_date = models.DateField(null=True,blank=True)
    booking_no = models.CharField(max_length=60,null=True,blank=True)
    ptc_mobile = models.CharField(max_length=120,null=True,blank=True)
    booking_date = models.DateField(null=True,blank=True)
    si_cut_off_date = models.DateField(null=True,blank=True)
    vgm_cut_off_date =  models.DateField(null=True,blank=True)
    etd_date =  models.DateField(null=True,blank=True)
    truck_no = models.CharField(max_length=60,null=True,blank=True)
    dispatch_date =  models.DateField(null=True,blank=True)
    hbl_recieved_date =  models.DateField(null=True,blank=True)
    # shipment_type = models.CharField(max_length=180,null=True,blank=True)
    shipment_type = models.CharField(max_length=180,null=True,blank=True, choices=SHIPMENT_TYPE_CHOICES)
    
    goods_reciept = models.CharField(max_length=120,null=True,blank=True,choices=CHOICE_GOODS_RECIEPT)
    cargo_nature = models.CharField(max_length=120,null=True,blank=True,choices=CHOICE_CARGO_NATURE)
    cfs_port_name = models.CharField(max_length=120,null=True,blank=True)
    class_name = models.CharField(max_length=120,null=True,blank=True)
    uin = models.CharField(max_length=120,null=True,blank=True)
    isf_filed_by = models.CharField(max_length=120,null=True,blank=True)
    hbl_status = models.CharField(max_length=120,null=True,blank=True,choices=HBL_LOCATION_STATUS)
    hbl_location = models.ForeignKey(City,on_delete=models.SET_NULL,related_name="job_hbl_location",null=True,blank=True)
    isf_filed_by = models.CharField(max_length=120,null=True,blank=True)
    agent_remarks = models.TextField(null=True,blank=True)
    customer_invoice_file = models.FileField(null=True, blank=True)
    packing_list_file = models.FileField(null=True, blank=True)
    do_file = models.FileField(null=True, blank=True)
    check_list_file = models.FileField(null=True, blank=True)
    leo_copy_file = models.FileField(null=True, blank=True)
    gatepass_copy_file = models.FileField(null=True, blank=True)
    vgm_file = models.FileField(null=True, blank=True)
    weighing_slip_file = models.FileField(null=True, blank=True)
    forwarding_note_file = models.FileField(null=True, blank=True)
    tr_copy_file = models.FileField(null=True, blank=True)
    shipping_instruction_file = models.FileField(null=True, blank=True)
    bl_file = models.FileField(null=True, blank=True)
    isf_file = models.FileField(null=True, blank=True)
    booking_copy = models.FileField(null=True, blank=True)
    application_handler = models.ForeignKey(DocumentHandler,on_delete=models.SET_NULL,null=True,blank=True,related_name="job_application_handler")
    is_approved = models.BooleanField(default=False)
    is_uploaded  = models.BooleanField(default=False,blank=True)
    
    # added on 7march 2025
    ata_date =  models.DateField(null=True,blank=True)
    atd_date =  models.DateField(null=True,blank=True)
    
    
    def __str__(self) -> str:
        return f'{self.job_no}'
    
    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Job Masters'
        ordering = ('-id',)

    def get_mbl_job(self):
        return self.mbl_job.select_related('exporter_name','consigned_name')

    def get_job_container(self):
        return self.job_container.all()
   
    def get_job_container_group(self):
        return self.job_container.all().values('container_type').annotate(count=Count('container_type'))

    def save(self,*args,**kwargs):
        if not self.job_no:
            
            current_year=datetime.now().year
            current_month=datetime.now().month
            job_prefix = str(current_year).zfill(2)[2:4] + str(current_month).zfill(2)  + self.company_type.pre_job

            total_jobs = JobMaster.objects.filter(created_at__month=current_month).filter(created_at__gte = self.company_type.financial_from).filter(company_type=self.company_type).count() + 1 + self.company_type.opening_job_no
            is_duplicate = True
            
            while is_duplicate:
                job_no = job_prefix + str(total_jobs).zfill(4)
                job = JobMaster.objects.filter(job_no=job_no).count()
                if job == 0:
                    is_duplicate = False
                    self.job_no = job_no
                else:
                    total_jobs += 1
        
        
        super(JobMaster, self).save(*args, **kwargs)

    

class JobTranshipment(models.Model):
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='job_transhipment')
    port = models.ForeignKey(Ports,on_delete=models.SET_NULL,null=True,blank=True,related_name='connecting_port')
    eta_date = models.DateField(null=True,blank=True)
    etd_date = models.DateField(null=True,blank=True)
    vessel_voyage = models.CharField(max_length=120,null=True,blank=True)

class JobInvoice(models.Model):
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='job_invoice')
    value = models.FloatField(default=0)
    curr = models.CharField(max_length=60,null=True,blank=True)
    invoice_no = models.CharField(max_length=120,null=True,blank=True)
    net_wt = models.CharField(max_length=120,null=True,blank=True)
    ship_bill_no = models.CharField(max_length=120,null=True,blank=True)
    ship_bill_type = models.CharField(max_length=120,null=True,blank=True)
    ship_bill_date =  models.DateField(null=True,blank=True)
    invoice_date = models.DateField(null=True,blank=True)
    
 
 
CONTAINER_BELONG = (
    ('Self','Self'),
    ('Other','Other'),
)

class JobHBL(models.Model):
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='job_hbl')
    job_hbl_no = models.CharField(max_length=120,null=True,blank=True)
    job_hbl_date = models.DateField(null=True,blank=True)
    hbl_account = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_hbl_account')
    hbl_shipper = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_hbl_shipper')
    hbl_consignee = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_hbl_consignee')
    mbl_no = models.CharField(max_length=100,null=True,blank=True)
    vessel_name = models.CharField(max_length=180,null=True,blank=True)
    commodity = models.TextField(null=True,blank=True)
    commodity_type = models.CharField(max_length=200,null=True,blank=True)
    no_of_packages = models.CharField(max_length=30,null=True,blank=True,default=0)
    packages_type = models.CharField(max_length=200,null=True,blank=True)
    volume = models.FloatField(default=0)
    net_weight = models.FloatField(default=0)
    gross_weight = models.FloatField(default=0)
    
    ''' Tmax weight 11 Nov'''
    chargeable_weight = models.FloatField(default = 0, null=True, blank=True)

    def __str__(self) -> str:
        return self.job_hbl_no

class JobContainer(models.Model):
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='job_container')
    hbl = models.ForeignKey(JobHBL,on_delete=models.CASCADE,null=True,blank=True,related_name="job_container_hbl")
    job_container_no = models.CharField(max_length=120,null=True,blank=True)
    container_type = models.CharField(max_length=60,null=True,blank=True)
    gross_wt = models.CharField(max_length=30,null=True,blank=True)
    net_wt = models.CharField(max_length=30,null=True,blank=True)
    total_package = models.CharField(max_length=30,null=True,blank=True)
    cbm = models.CharField(max_length=10,null=True,blank=True)
    line_seal = models.CharField(max_length=120,null=True,blank=True)
    trailor_no = models.CharField(max_length=120,null=True,blank=True)
    gta = models.CharField(max_length=120,null=True,blank=True)
    pickup_date = models.DateField(null=True,blank=True)
    excfs_date = models.DateField(null=True,blank=True)
    in_fac_date = models.DateField(null=True,blank=True)
    activity_date = models.DateField(null=True,blank=True)
    fac_out_date = models.DateField(null=True,blank=True)
    cfs_in_date = models.DateField(null=True,blank=True)
    return_date = models.DateField(null=True,blank=True)
    railout_date = models.DateField(null=True,blank=True)
    train_no = models.CharField(max_length=120,null=True,blank=True)
    shipper_seal_no = models.CharField(max_length=120,null=True,blank=True)
    new_seal_no = models.CharField(max_length=120,null=True,blank=True)
    stuffing_date = models.DateField(null=True,blank=True)
    icd_handover_date = models.DateField(null=True,blank=True)
    port_handover_date = models.DateField(null=True,blank=True)
    
    delivery_date = models.DateField(null=True,blank=True)
    sob_date = models.DateField(null=True,blank=True)
    eta_date = models.DateField(null=True,blank=True)
    belong_to = models.CharField(max_length=120,default="Self",choices=CONTAINER_BELONG)
    place_of_unloading = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name="container_load_loacation")
    place_of_loading = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name="container_unload_loacation")
    detention_from = models.DateField(null=True,blank=True)
    detention_to = models.DateField(null=True,blank=True)
    packaging = models.CharField(max_length=120,null=True,blank=True)
    def __str__(self):
        return str(self.id)
   

class DeliveryOrder(LogFolder):
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='do_job')
    date = models.DateField(null=True,blank=True)
    gigm_date = models.DateField(null=True,blank=True)
    ligm_date = models.DateField(null=True,blank=True)
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='do_company_type')
    
    manager_location = models.CharField(max_length=200,null=True,blank=True)
    manager_state = models.CharField(max_length=200,null=True,blank=True)
    desc_of_goods = models.CharField(max_length=200,null=True,blank=True)
    gigm = models.CharField(max_length=200,null=True,blank=True)
    ligm = models.CharField(max_length=200,null=True,blank=True)
    
    container_no = models.CharField(max_length=200,null=True,blank=True)
    container_type = models.CharField(max_length=200,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    weight = models.CharField(max_length=200,null=True,blank=True)
    total_packages = models.CharField(max_length=200,null=True,blank=True)
    
    hbl_date = models.DateField(null=True,blank=True)
    mbl_date = models.DateField(null=True,blank=True)
    hbl = models.CharField(max_length=200,null=True,blank=True)
    mbl = models.CharField(max_length=200,null=True,blank=True)
    vessel_voy_name = models.CharField(max_length=200,null=True,blank=True)
    vessel_voy_date = models.DateField(null=True,blank=True)
    mode_of_delivery = models.CharField(max_length=200,null=True,blank=True)
    
    consignee = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='do_consignee_name')
    hbl_options = models.ManyToManyField(JobHBL,blank=True,related_name='do_job_hbl')
    
    def __str__(self) -> str:
        return f'{self.job}'
    class Meta:
        verbose_name = 'Delivery Order'
        verbose_name_plural = 'Delivery Orders'
        ordering = ('-id',)
    
class FreightCertificate(LogFolder):
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='fc_job')
    gross_weight = models.CharField(max_length=50,null=True,blank=True)
    cbm = models.CharField(max_length=10,null=True,blank=True)
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='fc_company_type')
    ocean_freight = models.CharField(max_length=200,null=True,blank=True)
    consignee = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='fc_consignee')
    hbl_date = models.DateField(null=True,blank=True)
    mbl_date = models.DateField(null=True,blank=True)
    hbl = models.CharField(max_length=200,null=True,blank=True)
    mbl = models.CharField(max_length=200,null=True,blank=True)
    container_no = models.CharField(max_length=200,null=True,blank=True)
    container_type = models.CharField(max_length=200,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    hbl_options = models.ManyToManyField(JobHBL,blank=True,related_name='fc_job_hbl')
    def __str__(self) -> str:
        return f'{self.job}'
    
    class Meta:
        verbose_name = 'Freight Certifictae'
        verbose_name_plural = 'Freight Certificates'
        ordering = ('-id',)
    
    
CHOOSE_DSR_MODE = (
    ('Sea','Sea'),
    ('Air','Air'),
    ('LCL','LCL'),
    ('ETD','ETD'),
    ('Export','Export'),
)

CHOOSE_DSR_STATUS = (
    ('Open','Open'),
    ('Close','Close'),
    
)
    
    
class DSR(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='dsr_company_type')
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='dsr_job')
    invoice = models.CharField(max_length=180,null=True,blank=True)
    container_inv_date = models.DateField(null=True,blank=True)
    s_bill_no = models.CharField(max_length=180,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    egm_date = models.DateField(null=True,blank=True)
    no = models.CharField(max_length=180,null=True,blank=True)
    pfi_no = models.CharField(max_length=180,null=True,blank=True)
    shipment_term = models.CharField(max_length=180,null=True,blank=True)
    consignee = models.ForeignKey(Party,on_delete=models.CASCADE,null=True,blank=True,related_name='dsr_consignee')
    shipper = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='dsr_shipper')
    no_of_container = models.CharField(max_length=120,null=True,blank=True)
    pol = models.ForeignKey(Ports,on_delete=models.SET_NULL,null=True,blank=True,related_name='dsr_pol')
    fd = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='dsr_final_destination')
    pod = models.ForeignKey(Ports,on_delete=models.CASCADE,null=True,blank=True,related_name='dsr_pod')
    net_qty = models.CharField(max_length=30,null=True,blank=True)
    desp_date = models.DateField(null=True,blank=True)
    doc_rec_date = models.DateField(null=True,blank=True)
    cont_hold_date = models.DateField(null=True,blank=True)
    cont_release_date = models.DateField(null=True,blank=True)
    rail_out_date = models.DateField(null=True,blank=True)
    port_in_date = models.DateField(null=True,blank=True)
    vessel_name = models.CharField(max_length=180,null=True,blank=True)
    vessel_sailed =  models.DateField(null=True,blank=True)
    eta_date = models.DateField(null=True,blank=True)
    bl_release_date = models.DateField(null=True,blank=True)
    mbl_no = models.CharField(max_length=180,null=True,blank=True)
    hbl_no = models.CharField(max_length=180,null=True,blank=True)
    bl_instr_given_to_line = models.CharField(max_length=255,null=True,blank=True)
    shipping_line = models.ForeignKey(ShippingLines,on_delete=models.CASCADE,null=True,blank=True,related_name='dsr_shipping_line')
    doc_scan_date = models.DateField(null=True,blank=True)
    dsr_status = models.CharField(max_length=20,default='Open',choices=CHOOSE_DSR_STATUS) 
    remarks = models.CharField(max_length=300,null=True,blank=True)
    status=models.CharField(max_length=200,null=True,blank=True)
   
    def __str__(self) -> str:
        return f'{self.job}'
    
    class Meta:
        verbose_name = 'DSR'
        verbose_name_plural = 'DSR'
        ordering = ('-id',)
    
    
VGM_TYPE = (
    ('Normal','Normal'),
    ('Reefer','Reefer'),
    ('Hazardous','Hazardous'),
    ('Others','Others'),
)
    
class VGMMaster(LogFolder):
    job = models.ForeignKey(JobMaster,on_delete=models.SET_NULL,null=True,blank=False,related_name="vgm_job")
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="vgm_company_type")
    shipper = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=False,related_name="vgm_shipper_party")
    shipper_licence_no = models.CharField(max_length=200,null=True,blank=True)
    auth_shipper_name = models.CharField(max_length=200,null=True,blank=True)
    auth_shipper_designation = models.CharField(max_length=200,null=True,blank=True)
    shipper_contact = models.CharField(max_length=200,null=True,blank=True)
    vgm_type = models.CharField(max_length=50,null=True,blank=True,choices=VGM_TYPE)
    vgm_class = models.CharField(max_length=200,null=True,blank=True)
    booking_cont_no = models.CharField(max_length=200,null=True,blank=True)
    container_size = models.CharField(max_length=100,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    max_permissible_weight = models.CharField(max_length=100,null=True,blank=True)
    verified_gross_mass = models.CharField(max_length=100,null=True,blank=True)
    date_of_weighing = models.DateField(null=True,blank=True)
    time_of_weighing = models.TimeField()
    weighing_slip_no = models.CharField(max_length=200,null=True,blank=True)
    weighbridge_register_no = models.CharField(max_length=200,null=True,blank=True)
    weighbridge_address = models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        ordering = ('-id',)


Freight = (
    ("Collect", "Collect"),
    ("Part Prepaid/Collect", "Part Prepaid/Collect"),
    ("Prepaid", "Prepaid")
    )

FREIGHT_TYPE = (
    ('Prepaid','Prepaid'),
    ('Collect','Collect'),
)
MBL_TYPE2 = (
    ('Draft','Draft'),
    ('Final','Final'),
    ('Shipping Instruction','Shipping Instruction'),
)
       
class MBLMaster(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=False,related_name="mbl_company_type")
    mbl_no = models.CharField(max_length=100, null=True, blank=True)
    is_awb = models.BooleanField(default=False)
    date =  models.DateField(null=True,blank=True)
    mbl_Document_no = models.CharField(max_length=100, null=True, blank=True)
    job_no = models.ForeignKey(JobMaster, on_delete=models.SET_NULL, null=True,blank=True,related_name="mbl_job")

    exporter_name = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, related_name='exporter_mbl', blank=True)
    exporter_address = models.CharField(max_length=500, null=True, blank=True)

    consigned_name = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, related_name='consignee_mbl', blank=True)
    consigned_address = models.CharField(max_length=500, null=True, blank=True)
    
   
    bl_type = models.CharField(max_length=100, null=True, blank=True,choices=BL_TYPE)

    notify_party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True,blank=True, related_name='notfi_party_mbl')
    notify_party_address = models.TextField(null=True, blank=True)

    mtd_number = models.CharField(max_length=200, null=True, blank=True)
    shipment_ref_no = models.CharField(max_length=200, null=True, blank=True)

    type = models.CharField(max_length=200, null=True, blank=True,choices=MBL_TYPE)
    executed_at = models.CharField(max_length=200, null=True, blank=True)
    shipper_board_date = models.DateField(null=True, blank=True)
    by = models.CharField(max_length=200, null=True, blank=True)
    movement_type = models.CharField(max_length=200, null=True, blank=True)
    
    freight_type = models.CharField(max_length=100, null=True, blank=True,choices=CHOICE_FREIGHT_TERM)
    total_weight = models.CharField(max_length=100, null=True, blank=True)
    total_packages = models.CharField(max_length=100, null=True, blank=True)

    carrier = models.ForeignKey(ShippingLines, on_delete=models.SET_NULL, null=True, related_name='mbl_shipping', blank=True)
    currency = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True, related_name='mbl_currency', blank=True)
    freight = models.CharField(max_length=200,null=True, blank=True)

  

    no_of_o_mtd = models.CharField(max_length=100, null=True, blank=True)
    freight_charge_amt = models.CharField(max_length=100, null=True, blank=True)
    freight_payable_at = models.CharField(max_length=200, null=True, blank=True)

    export_references = models.TextField(null=True, blank=True)
    forwarding_agent = models.TextField(null=True, blank=True)

    point_and_country_of_origin = models.CharField(max_length=200, null=True, blank=True)
    loading_pier = models.CharField(max_length=200, null=True, blank=True)

    domestic_routing = models.TextField(null=True, blank=True)

    pre_carriage_by = models.CharField(max_length=200, null=True, blank=True)
    ocean_vessel = models.CharField(max_length=200, null=True, blank=True)
    port_of_loading_export = models.ForeignKey(Ports, on_delete=models.SET_NULL, null=True, related_name='port_of_loading_mbl', blank=True)
    place_of_delivery = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,related_name='mbl_place_of_delivery')
    place_of_receipt = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,related_name='mbl_place_of_receipt')
    voyage_no = models.CharField(max_length=200, null=True, blank=True)
    port_of_discharge = models.ForeignKey(Ports, on_delete=models.SET_NULL, null=True, related_name='port_of_discharge_mbl', blank=True)
    agent_name = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, related_name='mbl_agent', blank=True)
    agent_address = models.TextField( null=True, blank=True)

    marks_and_number = models.TextField(null=True, blank=True)
    no_of_packages = models.TextField(null=True, blank=True)
    description_of_commodities = models.TextField(null=True, blank=True)
    gross_weight = models.TextField(null=True, blank=True)
    measurement = models.TextField(null=True, blank=True)
    
    
    mbl_type = models.CharField(max_length=50,null=True,blank=True,choices=MBL_TYPE2,default='Draft')
    mbl_file = models.FileField(null=True,blank=True)
    hbl_file = models.FileField(null=True,blank=True)
    is_duplicate=models.BooleanField(default=False)
    duplicate_check=models.BooleanField(default=False)
    container_options=models.ManyToManyField(JobContainer,blank=True,related_name='job_container_options')

    # Air
    airline = models.ForeignKey(Airlines,on_delete=models.SET_NULL,null=True,blank=True,related_name="awb_airline")
    flight_no = models.CharField(max_length=120,null=True,blank=True)
    flight_date = models.DateField(null=True,blank=True)
    departure_date = models.DateField(null=True,blank=True)
    departure_airport = models.CharField(max_length=150,null=True,blank=True)
    destination_airport = models.CharField(max_length=150,null=True,blank=True)
    accounting_information = models.TextField(null=True,blank=True)
    handling_information = models.TextField(null=True,blank=True)
    chargeable_weight = models.TextField(null=True, blank=True)
    rate_charges = models.TextField(null=True, blank=True)
    total_charges = models.TextField(null=True, blank=True)
    declared_value = models.CharField(max_length=200, null=True, blank=True)
    declared_value_customs = models.CharField(max_length=200, null=True, blank=True)
    valuation_charge = models.CharField(max_length=200, null=True, blank=True)
    other_charge_due_agent = models.CharField(max_length=200, null=True, blank=True)
    other_charge_due_carrier = models.CharField(max_length=200, null=True, blank=True)
    account_no = models.CharField(null=True,blank=True,max_length=120)
    agent_iata_code = models.CharField(null=True,blank=True,max_length=120)
    origin_to = models.CharField(max_length=120,null=True,blank=True)
    airline_address = models.TextField(null=True,blank=True)
    carrier_name = models.CharField(max_length=120,null=True,blank=True)
    signature_company = models.CharField(max_length=255,null=True,blank=True, default='JAGYAT GLOBAL TRANSPORT AND LOGISTICS PVT. LTD.')
    signature_for = models.CharField(max_length=255,null=True,blank=True,default='Signature of Shipper of his Agent')
    class Meta:
        ordering = ('-id',)
    
    def __str__(self) -> str:
        return f'{self.mbl_no}'
    

    def save(self,*args,**kwargs):
        if not self.mbl_no:
            current_year=datetime.now().year
            current_month=datetime.now().month
            mbl_prefix = self.company_type.mbl_prefix + str(current_year).zfill(2)[2:4] + str(current_month).zfill(2)
            old_month = current_month - 1
            old_year = current_year
            if old_month == 0:
                old_month = 12
                old_year = old_year - 1
            
            old_mbl_prefix = self.company_type.mbl_prefix + str(old_year).zfill(2)[2:4] + str(old_month).zfill(2)
            
            total_mbl = MBLMaster.objects.filter(created_at__gte = self.company_type.financial_from).filter(company_type=self.company_type).filter(is_duplicate=False).count() + 1 + self.company_type.opening_mbl_no
            is_duplicate = True
            
            while is_duplicate:
                mbl_no = mbl_prefix + str(total_mbl).zfill(4)
                old_mbl_no = old_mbl_prefix + str(total_mbl).zfill(4)
                job = MBLMaster.objects.filter(Q(mbl_no=mbl_no)|Q(mbl_no=old_mbl_no)).count()
                if job == 0:
                    is_duplicate = False
                    self.mbl_no = mbl_no
                else:
                    total_mbl += 1
        
        
        super(MBLMaster, self).save(*args, **kwargs)

  
class CargoArrivalNotice(LogFolder):
    job = models.ForeignKey(JobMaster,on_delete=models.CASCADE,null=True,blank=True,related_name='can_job')
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='can_company_type')
    shipper = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_shipper_name')
    consignee = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_consignee_name')
    pol = models.ForeignKey(Ports,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_pol_name')
    pod = models.ForeignKey(Ports,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_pod_name')
    date = models.DateField(null=True,blank=True)
    
    move_type = models.CharField(max_length=200,null=True,blank=True)
    arrival_notice_no = models.CharField(max_length=200,null=True,blank=True)
    it_location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_it_loc')
    final_destination = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_fd')
    it_no = models.CharField(max_length=200,null=True,blank=True)
    it_date = models.DateField(null=True,blank=True)
    eta = models.DateField(null=True,blank=True)
    etd = models.DateField(null=True,blank=True)
    ams_hbl = models.CharField(max_length=200,null=True,blank=True)
    notify_party_1 = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_notify_1')
    notify_party_2 = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_notify_2')
    freight_location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='can_fl')
    consignee_location = models.TextField(null=True,blank=True)
    notify_party_1_location = models.TextField(null=True,blank=True)
    notify_party_2_location = models.TextField(null=True,blank=True)
    freight_address = models.TextField(null=True,blank=True)
    firm_code = models.CharField(max_length=120,null=True,blank=True)
    firm_phone = models.CharField(max_length=120,null=True,blank=True)
    no_of_packages = models.TextField(null=True,blank=True)
    desc_of_packages = models.TextField(null=True,blank=True)
    gross_weight = models.TextField(null=True,blank=True)
    measurement = models.TextField(null=True,blank=True)
    marks = models.TextField(null=True,blank=True)
    
    hbl_date = models.DateField(null=True,blank=True)
    mbl_date = models.DateField(null=True,blank=True)
    pod_date = models.DateField(null=True,blank=True)
    fpd_date = models.DateField(null=True,blank=True)
    vessel_voyage = models.CharField(max_length=200,null=True,blank=True)
    seal_no = models.CharField(max_length=200,null=True,blank=True)
    gigm = models.CharField(max_length=200,null=True,blank=True)
    hbl = models.ForeignKey(MBLMaster,on_delete=models.SET_NULL,null=True,blank=True,related_name="can_hbl")
    
    mbl = models.CharField(max_length=200,null=True,blank=True)
    ligm = models.CharField(max_length=200,null=True,blank=True)
    shipping_line = models.ForeignKey(ShippingLines,on_delete=models.CASCADE,null=True,blank=True,related_name='can_shipping_line')
    air_line = models.ForeignKey(Airlines,on_delete=models.CASCADE,null=True,blank=True,related_name='can_air_line')
    container_no = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return f'{self.job.job_no}'
    
    class Meta:
        verbose_name = 'CAN'
        verbose_name_plural = 'Cargo Arrival Notice'
        ordering = ('-id',)
        


CHOICE_YES_NO = (
    ('Yes','Yes'),
    ('No','No')
)

CHOICE_HAZ_LEVEL = (
    ('General','General'),
    ('Hazardous','Hazardous'),
    ('Non-Hazardous','Non-Hazardous')
)

class TransportBooking(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=False,related_name="transport_booking_company_type")
    job_no = models.ForeignKey(JobMaster,null=True,blank=True,on_delete=models.SET_NULL,related_name="booking_job")
    booking_no = models.CharField(max_length=120)
    booking_date = models.DateField()
    shipping_line = models.ForeignKey(ShippingLines,null=True,blank=True,on_delete=models.SET_NULL,related_name='booking_shipping_line')
    vessel_no = models.CharField(max_length=120,null=True,blank=True)
    voyage_no = models.CharField(max_length=120,null=True,blank=True)
    forwarder = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_forwarder")
    send_to_party = models.CharField(max_length=5,default='Yes',choices=CHOICE_YES_NO)
    date_of_sent = models.DateField(null=True,blank=True)
    pickup_location = models.ForeignKey(Location,null=True,blank=True,on_delete=models.SET_NULL,related_name="pickup_location")
    booking_location = models.ForeignKey(Location,null=True,blank=True,on_delete=models.SET_NULL,related_name="booking_location")
    stuffice_place = models.ForeignKey(Location,null=True,blank=True,on_delete=models.SET_NULL,related_name="stuffing_place")
    is_hazardous = models.CharField(max_length=30,default='General',choices=CHOICE_HAZ_LEVEL)
    class_name = models.CharField(max_length=120,null=True,blank=True)
    isf_by = models.CharField(max_length=120,null=True,blank=True)
    bl_type = models.CharField(max_length=120,null=True,blank=True)
    term = models.CharField(max_length=120,null=True,blank=True)
    qty = models.CharField(max_length=120,null=True,blank=True)
    uin = models.CharField(max_length=120,null=True,blank=True)
    pol = models.ForeignKey(Ports,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_pol")
    pod = models.ForeignKey(Ports,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_pod")
    fpd = models.ForeignKey(Ports,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_fpd")
    shipper = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_shipper")
    
    consignee = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_consignee")
    broker = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_broker")
    client = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_client")
    cha = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_cha")
    buyer = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_buyer")
    overseas_agent = models.ForeignKey(Party,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_oa")
    is_cig_involved = models.CharField(max_length=5,default='Yes',choices=CHOICE_YES_NO)
    is_tpt_involved = models.CharField(max_length=5,default='Yes',choices=CHOICE_YES_NO)
    is_isf = models.CharField(max_length=5,default='Yes',choices=CHOICE_YES_NO)
    sales_person = models.CharField(max_length=120,null=True,blank=True)
    eta_destination = models.ForeignKey(Location,null=True,blank=True,on_delete=models.SET_NULL,related_name="eta_destination")
    cs_remarks = models.CharField(max_length=200,null=True,blank=True)
    etd = models.DateField(null=True,blank=True)
    cargo_type = models.CharField(max_length=150,null=True,blank=True)
    stuffing_type = models.CharField(max_length=150,null=True,blank=True)
    
    no_of_container_1 = models.CharField(max_length=30,null=True,blank=True)
    container_size_1 = models.CharField(max_length=60,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    gross_weight_1 = models.CharField(max_length=30,null=True,blank=True)
    commodity_1 = models.CharField(max_length=150,null=True,blank=True)
    
    no_of_container_2 = models.CharField(max_length=30,null=True,blank=True)
    container_size_2 = models.CharField(max_length=60,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    gross_weight_2 = models.CharField(max_length=30,null=True,blank=True)
    commodity_2 = models.CharField(max_length=150,null=True,blank=True)
    
    trans_port_1 = models.ForeignKey(Ports,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_port_1")
    trans_port_2 = models.ForeignKey(Ports,null=True,blank=True,on_delete=models.SET_NULL,related_name="transport_port_2")
    eta_1 = models.DateField(null=True,blank=True)
    eta_2 = models.DateField(null=True,blank=True)
    etd_1 = models.DateField(null=True,blank=True)
    etd_2 = models.DateField(null=True,blank=True)
    conn_1 = models.CharField(max_length=120,null=True,blank=True)
    conn_2 = models.CharField(max_length=120,null=True,blank=True)
    vessel_1 = models.CharField(max_length=120,null=True,blank=True)
    vessel_2 = models.CharField(max_length=120,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Transport Booking'
        verbose_name_plural = 'Transport Bookings'
   
        ordering = ('-id',)
        
        

class DriverMaster(LogFolder):
    driver_name = models.CharField(max_length=120,null=True,blank=True)
    phone_1 = models.CharField(max_length=30,null=True,blank=True)
    phone_2 = models.CharField(max_length=30,null=True,blank=True)
    address_1 = models.CharField(max_length=255,null=True,blank=True)
    address_2 = models.CharField(max_length=255,null=True,blank=True)
    address_3 = models.CharField(max_length=255,null=True,blank=True)
    address_4 = models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    driving_licence_no = models.CharField(max_length=255,null=True,blank=True)
    lic_date = models.DateField(null=True,blank=True)
    account_no = models.CharField(max_length=255,null=True,blank=True)
    bank_name = models.CharField(max_length=255,null=True,blank=True)
    bank_ifsc = models.CharField(max_length=255,null=True,blank=True)
    bank_address = models.CharField(max_length=255,null=True,blank=True)
    aadhar_no = models.CharField(max_length=255,null=True,blank=True)
    driver_dob = models.DateField(null=True,blank=True)
    nominee_name = models.CharField(max_length=255,null=True,blank=True)
    nominee_bank = models.CharField(max_length=255,null=True,blank=True)
    nominee_account = models.CharField(max_length=255,null=True,blank=True)
    nominee_dob = models.DateField(null=True,blank=True)
    relation = models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=255,null=True,blank=True)
    joining_date = models.DateField(null=True,blank=True)
    pan_file = models.FileField(null=True,blank=True,upload_to="driver/kyc/")
    lic_file = models.FileField(null=True,blank=True,upload_to="driver/kyc/")
    kyc1_file = models.FileField(null=True,blank=True,upload_to="driver/kyc/")
    kyc2_file = models.FileField(null=True,blank=True,upload_to="driver/kyc/")
    kyc3_file = models.FileField(null=True,blank=True,upload_to="driver/kyc/")
    photo = models.ImageField(null=True,blank=True,upload_to="driver/kyc/")
    
    def __str__(self) -> str:
        return f'{self.driver_name}'
    class Meta:
        ordering = ('-id',)
     

EXPORT_IMPORT = (
    ('IMPORT','IMPORT'),
    ('EXPORT','EXPORT'),
)    

def GR_AUTO():
    gr = GRMaster.objects.count()
    return str(gr+1).zfill(5)

GR_JOB_TYPE = (
   ('EMPTY CONTAINER','EMPTY CONTAINER'), 
   ('LOADED CONTAINER','LOADED CONTAINER'), 
   ('LOOSE CARGO','LOOSE CARGO'), 
)

GR_BACKLOAD = (
   ('YES','YES'), 
   ('NO','NO'), 

)

class GRMaster(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name="gr_company_type")
    job = models.ForeignKey(JobMaster,on_delete=models.SET_NULL,null=True,blank=False,related_name="gr_job")
    gr_no = models.CharField(max_length=20,default=GR_AUTO,null=True,blank=True)
    seal_no = models.CharField(max_length=150,null=True,blank=True)
    trailor_no = models.CharField(max_length=150,null=True,blank=True)
    trailor_type = models.CharField(max_length=150,null=True,blank=True)
    container_no = models.CharField(max_length=150,null=True,blank=True)
    container_type = models.CharField(max_length=150,choices=CHOOSE_CONTAINER_TYPE,null=True,blank=True)
    consignee = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_consignee")
    consignee_address = models.TextField(null=True,blank=True)
    consignor = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_consignor")
    driver = models.ForeignKey(DriverMaster,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_driver")
    fpd = models.ForeignKey(Ports,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_fpd")
    consignor_address = models.TextField(null=True,blank=True)
    consignee_back_load = models.CharField(max_length=150,null=True,blank=True)
    consignee_bl_address = models.TextField(null=True,blank=True)
    is_backloaded = models.BooleanField(default=False)
    gr_backloaded = models.BooleanField(default=False)
    
    consignor_back_load = models.CharField(max_length=150,null=True,blank=True)
    consignor_bl_address = models.TextField(null=True,blank=True)
    factory_address = models.TextField(null=True,blank=True)
    import_export = models.CharField(max_length=30,default='EXPORT',choices=EXPORT_IMPORT)
    
    gr_date = models.DateField(null=True,blank=True)
    stuffing_date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    pickup_from = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_pickup")
    drop_location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_drop")
    person_name = models.CharField(max_length=150,null=True,blank=True)
    mobile_no = models.CharField(max_length=150,null=True,blank=True)

    remarks = models.TextField(null=True,blank=True)
    
    job_type = models.CharField(max_length=60,choices=GR_JOB_TYPE,null=True,blank=True)
    gross_wt = models.CharField(max_length=60,null=True,blank=True)
    delivery_address = models.CharField(max_length=180,null=True,blank=True)
    container_pickup_from = models.CharField(max_length=180,null=True,blank=True)
    container_pickup_date = models.DateField(null=True,blank=True)
    back_loading = models.CharField(max_length=60,choices=GR_BACKLOAD,default="NO")
    loading_address = models.CharField(max_length=180,null=True,blank=True)
    unloading_address = models.CharField(max_length=180,null=True,blank=True)
    date_load = models.DateField(null=True,blank=True)
    offload_date = models.DateField(null=True,blank=True)
    gr_customer = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_customer")
    billing_party = models.ForeignKey(Party,on_delete=models.SET_NULL,null=True,blank=True,related_name="gr_bp")
    no_lr = models.CharField(max_length=20,null=True,blank=True)
    date_lr = models.DateField(null=True,blank=True)
    bp_date = models.DateField(null=True,blank=True)
    commision = models.FloatField(default=0)
    advance = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    cheque = models.CharField(max_length=60,null=True,blank=True)
    gross_wt_2 = models.CharField(max_length=60,null=True,blank=True)
    cargo = models.CharField(max_length=180,null=True,blank=True)
    
    def __str__(self) -> str:
        return f'{self.gr_no}'
    
    class Meta:
        verbose_name = 'GR'
        verbose_name_plural = 'GRs'
        
        ordering = ('-id',)
        
   
class TrailorMaster(LogFolder):
    invoice_no = models.CharField(max_length=120,null=True,blank=True)
    invoice_date = models.DateField(null=True,blank=True)
    trailor_no = models.CharField(max_length=120,null=True,blank=True)
    registration_no = models.CharField(max_length=120,null=True,blank=True)
    finance_bank = models.CharField(max_length=120,null=True,blank=True)
    model_no = models.CharField(max_length=120,null=True,blank=True)
    
    engine_no = models.CharField(max_length=120,null=True,blank=True)
    rto_office = models.CharField(max_length=120,null=True,blank=True)
    tax_details = models.CharField(max_length=120,null=True,blank=True)
    valid_upto = models.DateField(null=True,blank=True)
    chasis_no = models.CharField(max_length=120,null=True,blank=True)
    fast_card_no = models.CharField(max_length=120,null=True,blank=True)
    diesel_card_no = models.CharField(max_length=120,null=True,blank=True)
    average = models.CharField(max_length=120,null=True,blank=True)
    
    
    def __str__(self) -> str:
        return f'{self.trailor_no}'
    


    
class TrailorDriver(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_driver_ref")
    driver = models.ForeignKey(DriverMaster,on_delete=models.CASCADE,related_name="trailor_driver")
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.driver}"
    
    
class TrailorTyreHorse(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_ht_ref")
    tyre = models.ForeignKey(Tyre,on_delete=models.CASCADE,related_name="trailor_horse_tyre")
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.tyre}"
    
    
class TrailorTyreTrolley(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_tt_ref")
    tyre = models.ForeignKey(Tyre,on_delete=models.CASCADE,related_name="trailor_trolley_tyre")
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.tyre}"
    
class TrailorFitness(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_fit_ref")
    fitness_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.fitness_no}"
    
    
class TrailorNationalPermit(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name='trailor_np_ref')
    permit_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.permit_no}"
    
    
class TrailorNationalGoodPermit(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name='trailor_ng_ref')
    permit_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.permit_no}"
    
class TrailorInsurance(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_ins_ref")
    insurance_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.insurance_no}"
    
    
class TrailorRoadTax(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name='trailor_road_tax_ref')
    permit_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.permit_no}"
    
    
class TrailorPUC(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name='trailor_puc_ref')
    permit_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.permit_no}"
    
class TrailorRC(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name='trailor_rc_ref')
    permit_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.permit_no}"
    
    
    
    
class TrailorOrgInv(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name='trailor_orginv_ref')
    permit_no = models.CharField(max_length=255,null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.permit_no}"
    

CHOOSE_ACESSORY = (
    ('Battery','Battery'),
    ('Bumper Stand','Bumper Stand'),
    ('Chain','Chain'),
    ('Hydraulic Jack & Rod','Hydraulic Jack & Rod'),
)

class TrailorAcessory(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_accesory_ref")
    acessory = models.CharField(max_length=255,null=True,blank=True,choices=CHOOSE_ACESSORY)
    price = models.FloatField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.acessory}"




class TrailorEventBook(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_event_ref")
    event_remarks = models.CharField(max_length=255,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.event_remarks}"
    

class TrailorService(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_service_ref")
    service_date = models.DateField(null=True,blank=True)
    next_due_date = models.DateField(null=True,blank=True)
    place = models.CharField(max_length=255,null=True,blank=True)
    expense_amount = models.FloatField(default=0)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.event_remarks}"


class TrailorLocation(LogFolder):
    trailor = models.ForeignKey(TrailorMaster,on_delete=models.CASCADE,related_name="trailor_location_ref")
    location = models.ForeignKey(Location,null=True,blank=True,on_delete=models.SET_NULL,related_name='location_trailor')
    from_date = models.DateField(null=True,blank=True)
    employee = models.ForeignKey('hr.Employee',null=True,blank=True,on_delete=models.SET_NULL,related_name='location_employee')
    remarks = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.id} {self.trailor} {self.remarks}"

LEDGER_TYPE = (
    ("Asset","Asset"),
    ("Liability","Liability"),
    ("Nominal","Nominal"),
)
ACCOUNT_CATEGORY = (
    ('BS','Balance Sheet'),
    ('PL','Profit & Loss'),
    ('B','Both')
)
HEAD_CATEGORY = (
    ('T','TOP'),
    ('S','SUB'),
    ('C','CHILD')
)


class LedgerCategory(models.Model):
    name = models.CharField(max_length=120,null=True,blank=True)
    child = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name="parent")
    nominal = models.BooleanField(default=False)
    liability = models.BooleanField(default=False)
    asset = models.BooleanField(default=False)
    depth = models.IntegerField(default=1,blank=True)
    
    def __str__(self) -> str:
        return f"{self.name}"



class LedgerCategories(LogFolder):
    name = models.CharField(max_length=120,null=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,related_name='category_parent',null=True,blank=True)
    type = models.CharField(max_length=30,default="Asset",choices=LEDGER_TYPE)
    include_in = models.CharField(max_length=100,null=True,blank=True,choices=ACCOUNT_CATEGORY)
    head_type = models.CharField(max_length=100,null=True,blank=True,choices=HEAD_CATEGORY)
    
   
    def __str__(self) -> str:
        return self.name
    
class LedgerSubCategories(LogFolder):
    name = models.CharField(max_length=120,null=True,blank=True)
    category = models.ForeignKey(LedgerCategories,null=True,blank=True,on_delete=models.SET_NULL,related_name="ledger_under")
    account_category = models.CharField(max_length=100,null=True,blank=True,choices=ACCOUNT_CATEGORY)
    def __str__(self) -> str:
        return self.name

DR_CR = (
    ('Debit','Debit'),
    ('Credit','Credit'),
)


PARTY_TYPE_LEDGER = (
    ('Direct','Direct'),
    ('Indirect','Indirect'),
    ('Bank','Bank'),
    ('Other','Other'),
)

DR_CR = (
    ('Debit','Debit'),
    ('Credit','Credit'),
)


PARTY_TYPE_LEDGER = (
    ('Direct','Party'),
    ('Indirect','Vendor'),
    ('Bank','Bank'),
    ('Other','Other'),
)

class LedgerMaster(LogFolder):
    company_type = models.ForeignKey(Logistic,null=True,blank=True,on_delete=models.CASCADE,related_name="ledger_company")
    ledger_name = models.CharField(max_length=180,null=True,blank=True)
    tally_group = models.ForeignKey(LedgerCategory,on_delete=models.SET_NULL,related_name="tally_category",null=True,blank=True)
    balance_in = models.CharField(max_length=30,choices=DR_CR,default="Debit")
    opening_date = models.DateField(null=True,blank=True)
    opening_balance = models.FloatField(default=0)
    auto_generated = models.BooleanField(default=False,null=True,blank=True)
    opening_ledger_category = models.ForeignKey('masters.LedgerCategory',default=1,null=True,blank=True,on_delete=models.SET_NULL,related_name='ledger_opening_group')
    
    class Meta:
        ordering = ['ledger_name']
    
    def __str__(self) -> str:
        return self.ledger_name
    
 
    
class LedgerMasterOpeningBalanceDetails(models.Model):
    ledger = models.ForeignKey(LedgerMaster,on_delete=models.CASCADE,related_name="ledger_opening_details",null=True,blank=True)
    invoice_no = models.CharField(max_length=120,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    amount = models.FloatField(default=0,blank=True)
    invoice_payable = models.ForeignKey('accounting.InvoicePayable',on_delete=models.CASCADE,null=True,blank=True,related_name='opening_invoice_payable')
    indirect_expense = models.ForeignKey('accounting.IndirectExpense',on_delete=models.CASCADE,null=True,blank=True,related_name='opening_invoice_payable')
    invoice = models.ForeignKey('accounting.InvoiceReceivable',on_delete=models.CASCADE,null=True,blank=True,related_name='opening_invoice')
    reciept_voucher = models.ForeignKey('accounting.RecieptVoucher',on_delete=models.CASCADE,null=True,blank=True,related_name='opening_invoice')
    payment_voucher = models.ForeignKey('accounting.PaymentVoucher',on_delete=models.CASCADE,null=True,blank=True,related_name='opening_invoice')
    balance_in = models.CharField(max_length=30,choices=DR_CR,default="Debit")
    is_final = models.BooleanField(default=False)
    sales_invoice = models.BooleanField(default=False)
    purchase_invoice = models.BooleanField(default=False)
    ind_expense = models.BooleanField(default=False)
    rec_voucher = models.BooleanField(default=False)
    pay_voucher = models.BooleanField(default=False)
    

    
AC_TYPE = (
    ('NAC','NAC'),
    ('FAK','FAK'),
)

class RateMaster(LogFolder):
    carrier = models.ForeignKey(ShippingLines,null=True,blank=True,related_name="shipping_rate",on_delete=models.SET_NULL)
    ac_type = models.CharField(max_length=80,default="NAC",choices=AC_TYPE)
    size = models.CharField(max_length=80,null=True,blank=True,choices=CHOOSE_CONTAINER_TYPE)
    pol = models.ForeignKey(Ports,null=True,blank=True,related_name="rate_pol",on_delete=models.SET_NULL)
    pod = models.ForeignKey(Ports,null=True,blank=True,related_name="rate_pod",on_delete=models.SET_NULL)
    fpd = models.ForeignKey(Ports,null=True,blank=True,related_name="rate_fpd",on_delete=models.SET_NULL)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    ammendment = models.CharField(max_length=20,null=True,blank=True)
    basic_charges = models.FloatField(default=0)
    oth_charges = models.FloatField(default=0)
    ramp_charges = models.FloatField(default=0)
    line_door_charges = models.FloatField(default=0)
    trucking_charges = models.FloatField(default=0)
    net_charges = models.FloatField(default=0)
    rate_file = models.FileField(upload_to='rates/',null=True,blank=True)
    
    def __str__(self) -> str:
        return f'{self.pol.name} To {self.pod.name}'
    
BH_TYPE = (
    ("BASIC","BASIC"),
    ("RAMP","RAMP"),
    ("OTH","OTH"),
    ("LINE-DOOR","LINE-DOOR"),
    ("TRUCKING","TRUCKING"),
)

class RateMasterDetails(models.Model):
    rate = models.ForeignKey(RateMaster,related_name='rate_details',null=True,blank=True,on_delete=models.CASCADE)
    billing_head = models.ForeignKey(BillingHead,on_delete=models.SET_NULL,null=True,blank=True,related_name='rate_bh')
    bh_type = models.CharField(max_length=80,default="BASIC",choices=BH_TYPE)
    amount = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    




