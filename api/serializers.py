
from masters.models import currency,BillingHead,City,JobMaster,LedgerMaster,PartyAddress,DSR,State,Party,MBLMaster,Vendor,JobHBL
from rest_framework.serializers import ModelSerializer
from accounting.models import RecieptVoucher,PaymentVoucher,RecieptVoucherDetails,InvoiceReceivable,InvoicePayable,IndirectExpense,InvoiceReceivableDetail,ContraVoucher
from crm.models import Inquiry,InquiryDetail,Event,sales_person_party
from dashboard.models import Logistic
from rest_framework import serializers

class sales_person_Serializer(serializers.ModelSerializer):
    class Meta:
        model=sales_person_party
        fields='__all__'

class EventSerializer(serializers.ModelSerializer):
    customer = sales_person_Serializer(read_only=True)
    class Meta:
        model = Event
 
        # fields = ['id','description','customer']
        fields = '__all__'


class InquiryDetailSerializer(ModelSerializer):
    class Meta:
        
        model = InquiryDetail
        fields = '__all__'

class InquirySerializer(ModelSerializer):
    inquiry_reference = InquiryDetailSerializer(many=True)
    class Meta:
        model = Inquiry
        fields = '__all__'

class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id','vendor_name']
        
class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ['name','gst_code']

class PartySerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = [
            'id',
            'party_name',
            'credit_days'
        ]


class PartyAddressSerializer(ModelSerializer):
    party = PartySerializer(many=False)
    corp_state = StateSerializer(many=False)
    class Meta:
        model = PartyAddress
        fields = ['name','gst_code']

class PartyLimitedSerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = ['id','credit_days','party_name']

class PartyAddressLimitedSerializer(ModelSerializer):
    party = PartyLimitedSerializer(many=False)
    class Meta:
        model = PartyAddress
        fields = ['id','party','branch']


class PartyAddressSerializer(ModelSerializer):
    party = PartySerializer(many=False)
    corp_state = StateSerializer(many=False)
    class Meta:
        model = PartyAddress
        fields = ['id','branch','party','corp_state']


class CompanyJobsSerializer(ModelSerializer):
    
    class Meta:
        model = JobMaster
        fields = ['id','job_no','module','company_type','alternate_company']

class JobMasterSerializer(ModelSerializer):
    account_address = PartyAddressSerializer(many=False)
    class Meta:
        model = JobMaster
        fields = '__all__'

class HBLMasterSerializer(ModelSerializer):
    class Meta:
        model = JobHBL
        fields = '__all__'


        
class DSRSerializer(ModelSerializer):
    job = JobMasterSerializer(many=False)
    
    class Meta:
        model = DSR
        fields = '__all__'

class CurrencySerializer(ModelSerializer):
    class Meta:
        model = currency
        fields = '__all__'

class BillingHeadSerializer(ModelSerializer):
    class Meta:
        model = BillingHead
        fields = '__all__'

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class RecieptVoucherBillWiseSerializer(ModelSerializer):
    class Meta:
        model = RecieptVoucher
        fields = [
            'party_name',
            'party_address',
            'id',
            'voucher_no',
            'advance_amount',
            'instrument_no'
        ]

class PaymentVoucherBillWiseSerializer(ModelSerializer):
    class Meta:
        model = PaymentVoucher
        fields = [
            'party_name',
            'party_address',
            'vendor',
            'id',
            'voucher_no',
            'advance_amount',
            'instrument_no'
        ]

class RecieptVoucherSerializer(ModelSerializer):
    class Meta:
        model = RecieptVoucher
        fields = '__all__'

class PaymentVoucherSerializer(ModelSerializer):
    class Meta:
        model = PaymentVoucher
        fields = '__all__'

class ContraVoucherSerializer(ModelSerializer):
    class Meta:
        model = ContraVoucher
        fields = '__all__'


        
class JobMasterLessSerializer(ModelSerializer):
    class Meta:
        model = JobMaster
        fields = ['job_no','id','module']

class InvoiceReceivableSerializer(ModelSerializer):
    class Meta:
        model = InvoiceReceivable
        fields = '__all__'

class RecieptVoucherDetailSerializer(ModelSerializer):
    invoice = InvoiceReceivableSerializer(many=False)
    class Meta:
        model = RecieptVoucherDetails
        fields = '__all__'

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Logistic
        fields = ['company_gst_code','company_name']


class PartyLessSerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = ['party_name']
        
class PartyAddressLessSerializer(ModelSerializer):
    corp_state = StateSerializer(many=False)
    class Meta:
        model = PartyAddress
        fields = ['corp_state','corp_gstin','branch']
        
class BillingHeadLessSerializer(ModelSerializer):
    class Meta:
        model = BillingHead
        fields = ['always_igst']

class InvoiceRecDetails(ModelSerializer):
    billing_head = BillingHeadLessSerializer(many=False)
    class Meta:
        model = InvoiceReceivableDetail
        fields = [
            'billing_head',
            'gst',
            'gst_amount',
            'total',
            'amount',
         
        ]
        read_only_fields = fields
        
class InvoiceReceivableGSTSerializer(ModelSerializer):
    company_type = CompanySerializer(many=False)
    job_no = JobMasterLessSerializer(many=False)
    bill_to = PartyLessSerializer(many=False)
    bill_to_address = PartyAddressLessSerializer(many=False)
    recievable_invoice_reference = InvoiceRecDetails(many=True)
    invoice_currency = CurrencySerializer(many=False)
    class Meta:
        model = InvoiceReceivable
        fields = ['id','job_no','final_invoice_no','invoice_no','date_of_invoice','einvoice_date','net_amount','gross_amount','gst_amount','bill_to','bill_to_address','company_type','invoice_currency','currency_ex_rate','type_of_invoice','category','recievable_invoice_reference','old_invoice','is_cancel']
        read_only_fields = fields
        

class InvoicePayablePurchaseSerializer(ModelSerializer):
    class Meta:
        model = InvoicePayable
        fields = ['purchase_invoice_no']

class InvoicePayableSerializer(ModelSerializer):
    class Meta:
        model = InvoicePayable
        fields = '__all__'

class IndirectExpenseSerializer(ModelSerializer):
    class Meta:
        model = IndirectExpense
        fields = '__all__'

class LedgerMasterSerializer(ModelSerializer):
    class Meta:
        model = LedgerMaster
        fields = '__all__'
        
class MBLMasterSerializer(ModelSerializer):
    class Meta:
        model = MBLMaster
        fields = '__all__'
        
        
        
class CurrencyShortName(ModelSerializer):
    class Meta:
        model = currency
        fields = ('short_name',)
        
class PartyNameSerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = ('party_name',)
        
class IRJobCostSheetSerializer(ModelSerializer):
    invoice_currency = CurrencyShortName(many=False)
    class Meta:
        model = InvoiceReceivable
        fields = (
            'is_einvoiced',
            'old_invoice',
            'net_amount',
            'gross_amount',
            'gst_amount',
            'invoice_currency',
            'currency_ex_rate'
        )

class IDPJobCostSheetSerializer(ModelSerializer):
    invoice_currency = CurrencyShortName(many=False)
    class Meta:
        model = InvoicePayable
        fields = (
            'net_amount',
            'gross_amount',
            'gst_amount',
            'invoice_currency',
            'currency_ex_rate'
        )
class INDPJobCostSheetSerializer(ModelSerializer):
    class Meta:
        model = IndirectExpense
        fields = (
            'net_amount',
            'gross_amount',
            'gst_amount',
        )
class TrailorJobCostSheetSerializer(ModelSerializer):
    class Meta:
        model = IndirectExpense
        fields = (
            'net_amount',
           
        )
        
class LogisticSerializer(ModelSerializer):
    class Meta:
        model = Logistic
        fields = (
            'company_name',
           
        )
        

class JobCostSheetSerializer(ModelSerializer):
    recievable_invoice_job = IRJobCostSheetSerializer(many=True)
    payable_invoice_job = IDPJobCostSheetSerializer(many=True)
    indirect_exp_job = INDPJobCostSheetSerializer(many=True)
    trailor_exp_job = TrailorJobCostSheetSerializer(many=True)
    company_type = LogisticSerializer(many=False)
    alternate_company = LogisticSerializer(many=False)
    account = PartyNameSerializer(many=False)
    class Meta:
        model = JobMaster
        fields = (
            'id',
            'job_no',
            'company_type',
            'alternate_company',
            'account',
            'job_date',
            'module',
            'recievable_invoice_job',
            'payable_invoice_job',
            'indirect_exp_job',
            'trailor_exp_job',
            
        )
        read_only_fields = fields