from django.contrib import admin

from masters.models import Bank, CargoArrivalNotice, Commodity, Country, DeliveryOrder, Location, Party, State, currency,BillingHead,UOM,FreightCertificate,DSR,City,JobMaster,MBLMaster,CategoryMaster,DriverMaster,TrailorTyreTrolley,LedgerMaster,TrailorNationalPermit,Ports,Airlines,Vendor,TrailorAcessory,PartyType,LedgerCategories,JobContainer,JobTranshipment,JobInvoice,PartyAddress,GRMaster,TrailorBillingHead,ScaleOfWork,LedgerMasterOpeningBalanceDetails,State,ShippingLines,Logistic,JobHBL,LedgerCategory
from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget,DateWidget,DateTimeWidget

# Register your models here.



class JobResource(resources.ModelResource):
    
    account_address = fields.Field(
        column_name='account_address',
        attribute='account_address',
        widget=ForeignKeyWidget(PartyAddress, field='party__party_name'))
    
    account = fields.Field(
        column_name='account',
        attribute='account',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    flight_date = fields.Field(
        attribute="flight_date",
        column_name="flight_date",
        widget=DateWidget("%d-%b-%Y")
    )
    
    created_at = fields.Field(
        attribute="created_at",
        column_name="created_at",
        widget=DateWidget("%d-%b-%Y")
    )
    
    job_date = fields.Field(
        attribute="job_date",
        column_name="job_date",
        widget=DateWidget("%d-%b-%Y")
    )

    do_date = fields.Field(
        attribute="do_date",
        column_name="do_date",
        widget=DateWidget("%d-%b-%Y")
    )
    
    hbl_date = fields.Field(
        attribute="hbl_date",
        column_name="hbl_date",
        widget=DateWidget("%d-%b-%Y")
    )
    
    mbl_date = fields.Field(
        attribute="mbl_date",
        column_name="mbl_date",
        widget=DateWidget("%d-%b-%Y")
    )
   
    eta_date = fields.Field(
        attribute="eta_date",
        column_name="eta_date",
        widget=DateWidget("%d-%b-%Y")
    )
    etd_date = fields.Field(
        attribute="etd_date",
        column_name="etd_date",
        widget=DateWidget("%d-%b-%Y")
    )
    actual_arrival_pod_date = fields.Field(
        attribute="actual_arrival_pod_date",
        column_name="actual_arrival_pod_date",
        widget=DateWidget("%d-%b-%Y")
    )
    port_out_date = fields.Field(
        attribute="port_out_date",
        column_name="port_out_date",
        widget=DateWidget("%d-%b-%Y")
    )
   
    vessel_voy_date = fields.Field(
        attribute="vessel_voy_date",
        column_name="vessel_voy_date",
        widget=DateWidget("%d-%b-%Y")
    )
    updated_at = fields.Field(
        attribute="updated_at",
        column_name="updated_at",
        widget=DateWidget("%d-%b-%Y")
    )
    dispatch_date = fields.Field(
        attribute="dispatch_date",
        column_name="dispatch_date",
        widget=DateWidget("%d-%b-%Y")
    )

    container_handover_location = fields.Field(
        column_name='container_handover_location',
        attribute='container_handover_location',
        widget=ForeignKeyWidget(Location, field='name'))

    place_of_reciept = fields.Field(
        column_name=' place_of_reciept',
        attribute=' place_of_reciept',
        widget=ForeignKeyWidget(Location, field='name'))
    
   
    
    consignee = fields.Field(
        column_name='consignee',
        attribute='consignee',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    notify_party = fields.Field(
        column_name='notify_party',
        attribute='notify_party',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    forwarder = fields.Field(
        column_name='forwarder',
        attribute='forwarder',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    final_destination = fields.Field(
        column_name='final_destination',
        attribute='final_destination',
        widget=ForeignKeyWidget(Location, field='name'))
    
    port_of_loading = fields.Field(
        column_name='port_of_loading',
        attribute='port_of_loading',
        widget=ForeignKeyWidget(Ports, field='name'))
    
    port_of_discharge = fields.Field(
        column_name='port_of_discharge',
        attribute='port_of_discharge',
        widget=ForeignKeyWidget(Ports, field='name'))
    

    shipper = fields.Field(
        column_name='shipper',
        attribute='shipper',
        widget=ForeignKeyWidget(Party, field='party_name'))
    

    shipping_line = fields.Field(
        column_name='shipping_line',
        attribute='shipping_line',
        widget=ForeignKeyWidget(ShippingLines, field='name'))
    
    overseas_agent = fields.Field(
        column_name='overseas_agent',
        attribute='overseas_agent',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    company_type = fields.Field(
        column_name='company_type',
        attribute='company_type',
        widget=ForeignKeyWidget(Logistic, field='company_name'))
    
    alternate_company = fields.Field(
        column_name='alternate_company',
        attribute='alternate_company',
        widget=ForeignKeyWidget(Logistic, field='company_name'))
    
    
    class Meta:
        model = JobMaster
        
        fields = ("id","job_no","job_date","scale_of_work","freight_term","module","shipping_line","do_no","mbl_no","mbl_date","hbl_no","account_manager","hbl_date","container_return_date","vessel_voy_name","vessel_voy_date","shipper_invoice_no","container_count","inquiry","company_type","alternate_company","account","account_address","shipper","consignee","notify_party","booking_party","overseas_agent","broker","importer","forwarder","stuffing_type","place_of_reciept","final_destination","place_of_loading","place_of_loading_date","place_of_unloading","place_of_unloading_date","port_of_loading","port_of_discharge","po_no","commodity","commodity_type","no_of_packages","packages_type","volume","gross_weight","net_weight","cbm","job_status","remarks","charges","imdg","gigm","ligm","gate_open_date","gigm_date","ligm_date","igm_date","status","docket_no","air_line","awb_no","flight_no","igm_no","awb_date","flight_date","clearance","container_pickup_location","container_pickup_date","container_no","container_type","delivery","cfs_in_date","do_date","shipper_invoice_date","stuffing_date","rail_out_date","sailing_date","eta_date","actual_arrival_pod_date","port_out_date","oc_date","eway_date","asessable_value","owned_hire","gr_no","bilty_no","trailor_no","l_seal","ship_bill_no","ship_bill_type","ship_bill_date","currency","cfs","invoice_no","invoice_date","invoice_value","bl_type","bl_no","lc_no","ams_no","ams_date","isf_no","isf_date","entry_cont_date","booking_no","ptc_mobile","booking_date","si_cut_off_date","vgm_cut_off_date","etd_date","truck_no","dispatch_date","shipment_type","goods_reciept","cargo_nature","cfs_port_name","class_name","uin","isf_filed_by","is_approved","created_at","updated_at","rounting","atd_date","ata_date","container_handover_date","container_arrival_date","shipon_board_date","container_handover_location","transit_time","free_detention_at_origin","free_detention_at_pod","vsl_schedule","is_uploaded")


class JobAdmin(ImportExportModelAdmin):
    resource_class = JobResource
    list_display = ['job_no','module','company_type','created_by', 'is_deleted','is_approved']
    list_per_page = 100
    
    class Meta:
        fields = "__all__"




class ImportAdmin(ImportExportModelAdmin):
    class Meta:
        fields = '__all__'


class PartyAddressResource(resources.ModelResource):
    party = fields.Field(
        column_name='party',
        attribute='party',
        widget=ForeignKeyWidget(Party, field='party_name'))
    
    corp_state = fields.Field(
        column_name='corp_state',
        attribute='corp_state',
        widget=ForeignKeyWidget(State, field='name'))

    class Meta:
        model = PartyAddress
        import_id_fields = ['party','corp_state']
        fields = ('party','corp_state','branch','corp_address_line1','corp_address_line2','corp_address_line3','corp_country','corp_city','corp_email','corp_gstin','corp_zip','corp_contact','corp_pan')
       

class StateResource(resources.ModelResource):
    class Meta:
        model=State
        fields=('name','gst_code')

class StateAdmin(ImportExportModelAdmin):
    resource_class=StateResource
    class Meta:
        fields='__all__'


class PartyAddressAdmin(ImportExportModelAdmin):
    resource_class = PartyAddressResource
    
    class Meta:
        fields = '__all__'
  
     
    
class PartyResource(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = Party
        fields = ('party_name',)
        import_id_fields = ('party_name',)
        skip_unchanged = True
    
class TrailorBillingHeadResource(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = TrailorBillingHead
        fields = '__all__'

class JobList(admin.ModelAdmin):
    list_display = ['job_no','module','company_type','created_by', 'is_deleted']
    list_filter = ['module','company_type','created_by', 'is_deleted']
    list_per_page = 100

class LedgerCategoriesList(admin.ModelAdmin):
    list_display = ['name','parent','type','include_in', 'head_type']
    list_per_page = 100

class LedgerMasterOpeningBalanceList(admin.ModelAdmin):
    list_display = ['ledger',]
    list_filter = ['sales_invoice','purchase_invoice','ind_expense', 'rec_voucher','pay_voucher']
    list_per_page = 100

class LedgerCategoryList(admin.ModelAdmin):
    list_display = ["name","child","nominal","liability","asset","depth"]
    list_per_page = 100

admin.site.register(Party,PartyResource)
admin.site.register(TrailorBillingHead,TrailorBillingHeadResource)
admin.site.register(ScaleOfWork)
admin.site.register(currency,ImportAdmin)
admin.site.register(Country,ImportAdmin)
admin.site.register(State,ImportAdmin)
admin.site.register(Commodity,ImportAdmin)
admin.site.register(BillingHead,ImportAdmin)
admin.site.register(Bank)
admin.site.register(UOM)
admin.site.register(CargoArrivalNotice)
admin.site.register(DeliveryOrder)
admin.site.register(FreightCertificate)
admin.site.register(Location,ImportAdmin)
admin.site.register(Ports,ImportAdmin)
admin.site.register(DSR)
admin.site.register(City)
admin.site.register(JobMaster,JobAdmin)
admin.site.register(CategoryMaster)
admin.site.register(MBLMaster)
admin.site.register(DriverMaster)
admin.site.register(TrailorTyreTrolley)
admin.site.register(TrailorNationalPermit)
admin.site.register(LedgerMaster)
admin.site.register(Airlines)
admin.site.register(Vendor)
admin.site.register(TrailorAcessory)
admin.site.register(PartyType)
admin.site.register(JobContainer)
admin.site.register(JobHBL)
admin.site.register(JobTranshipment)
admin.site.register(JobInvoice)
admin.site.register(PartyAddress,PartyAddressAdmin)
admin.site.register(LedgerMasterOpeningBalanceDetails,LedgerMasterOpeningBalanceList)
admin.site.register(GRMaster)
admin.site.register(LedgerCategory,LedgerCategoryList)
admin.site.register(LedgerCategories,LedgerCategoriesList)