from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from api.serializers import *
from masters.models import BillingHead, City,currency,JobMaster,LedgerMaster,PartyAddress,DSR,Vendor,JobHBL
from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from accounting.models import  RecieptVoucher,PaymentVoucher,InvoiceReceivable,InvoicePayable,IndirectExpense,ContraVoucher
from django_filters.rest_framework import DjangoFilterBackend,MultipleChoiceFilter
from rest_framework.filters import OrderingFilter
from crm.models import Inquiry,Event,sales_person_party
from django_filters import FilterSet,NumberFilter
from dashboard.models import Logistic
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# Create your views here.


class BillingHeadListView(ListAPIView):
    queryset = BillingHead.objects.all()
    serializer_class = BillingHeadSerializer
    permission_classes = (IsAuthenticated,)


class EventListView(ListAPIView):
    queryset = Event.objects.select_related('user','company_type','assigned_by').filter(is_deleted=False).all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','user','assigned_by','start','end']


class sales_customer_ListView(ListAPIView):
    queryset = sales_person_party.objects.all()
    serializer_class = sales_person_Serializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
  
    

class VendorListView(ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

class BillingHeadDetailView(RetrieveAPIView):
    queryset = BillingHead.objects.all()
    serializer_class = BillingHeadSerializer
    permission_classes = (IsAuthenticated,)

class CurrencyListView(ListAPIView):
    queryset = currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticated,)

class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated,)

class RecieptVoucherListView(ListAPIView):
    queryset = RecieptVoucher.objects.all()
    serializer_class = RecieptVoucherSerializer
    permission_classes = (IsAuthenticated,)


class RecieptVoucherUpdateView(RetrieveUpdateAPIView):
    queryset = RecieptVoucher.objects.all()
    serializer_class = RecieptVoucherSerializer
    permission_classes = (IsAuthenticated,)

class RecieptVoucherPartyWiseListView(ListAPIView):
    queryset = RecieptVoucher.objects.all()
    serializer_class = RecieptVoucherBillWiseSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['party_name','party_address']

class PaymentVoucherPartyWiseListView(ListAPIView):
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherBillWiseSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['party_name','party_address','vendor']

class InvoicePayablePurchaseList(ListAPIView):
    queryset = InvoicePayable.objects.all().values('purchase_invoice_no')
    serializer_class = InvoicePayablePurchaseSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    

class PaymentVoucherListView(ListAPIView):
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherSerializer
    permission_classes = (IsAuthenticated,)

class PaymentVoucherUpdateView(RetrieveUpdateAPIView):
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherSerializer
    permission_classes = (IsAuthenticated,)

class ContraVoucherUpdateView(RetrieveUpdateAPIView):
    queryset = ContraVoucher.objects.all()
    serializer_class = ContraVoucherSerializer
    permission_classes = (IsAuthenticated,)

 


class CompanyJobListView(ListAPIView):
    queryset = JobMaster.objects.all()
    serializer_class = CompanyJobsSerializer
    permission_classes = (IsAuthenticated,)
    
    filterset_fields = ['module']
    ordering_fields = ['id']
    def get_queryset(self):
        company = self.request.GET.get('company_type',None)
        if company:
            return JobMaster.objects.filter(Q(alternate_company__id = int(company)) | Q(company_type__id = int(company))).exclude(Q(job_status='Close') | Q(is_approved=False) | Q(is_deleted=True))
        else:
            return JobMaster.objects.exclude(Q(job_status='Close') | Q(is_approved=False) | Q(is_deleted=True))

class JobListView(ListAPIView):
    queryset = JobMaster.objects.all()
    serializer_class = JobMasterSerializer
    permission_classes = (IsAuthenticated,)
    
    filterset_fields = ['module']
    ordering_fields = ['id']
    def get_queryset(self):
        company = self.request.GET.get('company_type',None)
        if company:
            return JobMaster.objects.filter(Q(alternate_company__id = int(company)) | Q(company_type__id = int(company))).exclude(Q(job_status='Close') | Q(is_approved=False) | Q(is_deleted=True))
        else:
            return JobMaster.objects.exclude(Q(job_status='Close') | Q(is_approved=False) | Q(is_deleted=True))
        


class HBLListView(ListAPIView):
    queryset=JobHBL.objects.all()
    serializer_class=HBLMasterSerializer
    permission_classes = (IsAuthenticated,)


class InvoiceReceivableView(ListAPIView):
    queryset = InvoiceReceivable.objects.all()
    serializer_class = InvoiceReceivableSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_type','bill_to']
    
    def get_queryset(self):
        return InvoiceReceivable.objects.exclude(pending_amount=0).exclude(invoice_status="Cancel").exclude(is_einvoiced=False)  


class AllInvoiceReceivableView(ListAPIView):
    queryset = InvoiceReceivable.objects.all()
    serializer_class = InvoiceReceivableSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_type','bill_to']
    
    def get_queryset(self):
        return InvoiceReceivable.objects.exclude(is_einvoiced=False)  

class InvoiceReceivableDetailView(RetrieveAPIView):
    queryset = InvoiceReceivable.objects.all()
    serializer_class = InvoiceReceivableSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_type','bill_to']
    
    def get_queryset(self):
        return InvoiceReceivable.objects.exclude(is_einvoiced=False)  

class RecieptVoucherDetailListView(ListAPIView):

    queryset = RecieptVoucherDetails.objects.all()
    serializer_class = RecieptVoucherDetailSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['invoice']
    
    

class InvoiceReceivableReportView(ListAPIView):
    queryset = InvoiceReceivable.objects.all()
    serializer_class = InvoiceReceivableSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_type','invoice_status','due_date','job_no','pending_amount','bill_to_address','company_type__tax_policy']
    
    def get_queryset(self):
        return InvoiceReceivable.objects.exclude(is_einvoiced=False).exclude(invoice_status="Cancel")

class InvoiceReceivableGSTRView(ListAPIView):
    queryset = InvoiceReceivable.objects.all()
    serializer_class = InvoiceReceivableGSTSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'einvoice_date':['gte', 'lte', 'exact'],
        'id':['exact'],
        'is_einvoiced':['exact'],
        'old_invoice':['exact'],
        'company_type':['exact'],
        'due_date':['exact'],
        'due_date':['exact'],
        'pending_amount':['exact'],
        'pending_amount':['exact'],
        'bill_to_address':['exact'],
        'bill_to_address':['exact'],
        'company_type__tax_policy':['exact'],
        
        }
    

class InvoicePayableReportView(ListAPIView):
    queryset = InvoicePayable.objects.all()
    serializer_class = InvoicePayableSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_type','invoice_status','pending_amount','bill_from','bill_from_address']
    def get_queryset(self):
        return InvoicePayable.objects.exclude(pending_amount=0).exclude(invoice_status="Cancel").exclude(is_deleted=True)   

class IndirectExpenseReportView(ListAPIView):
    queryset = IndirectExpense.objects.all()
    serializer_class = IndirectExpenseSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_type','pending_amount','vendor']
    def get_queryset(self):
        return IndirectExpense.objects.exclude(pending_amount=0).exclude(is_deleted=True)   
    

class PartyAddressLimitedListView(ListAPIView):
    queryset = PartyAddress.objects.all()
    serializer_class = PartyAddressLimitedSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['party']
    
   
class PartyAddressListView(ListAPIView):
    queryset = PartyAddress.objects.all()
    serializer_class = PartyAddressSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['party']
    
   

class LedgerMasterListView(ListAPIView):
    queryset = LedgerMaster.objects.all()
    serializer_class = LedgerMasterSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_type']
    
  

class DSRListView(ListAPIView):
    queryset = DSR.objects.all()
    serializer_class = DSRSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job__job_no','job__is_deleted','job__account_address__corp_contact']
    
  
class InquiryView(ListAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    
  
class MBLView(ListAPIView):
    queryset = MBLMaster.objects.all()
    serializer_class = MBLMasterSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job_no']
    
class JobCostSheetView(ListAPIView):
    queryset = JobMaster.objects.all()
    serializer_class = JobCostSheetSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]

    filterset_fields = {
        'job_date':['gte', 'lte', 'exact'],
        'id':['exact'],
        'job_no':['exact'],
        'company_type__company_name':['exact'],
        'recievable_invoice_job__is_einvoiced':['exact'],
        'recievable_invoice_job__old_invoice':['exact'],
        
        }
    
  