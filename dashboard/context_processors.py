from dashboard.models import Alerts
from accounting.models import InvoicePayable,InvoiceReceivable,PaymentVoucher,RecieptVoucher,CreditNote,DebitNote
from django.contrib.auth.models import User
from masters.models import BillingHead, JobMaster,City,currency,Country,Ports,State,Location,ShippingLines,Airlines,Party,LedgerCategories,UOM,TrailorBillingHead,Vendor,LedgerCategory,PartyType,Bank,PartyAddress,LedgerMaster
from dashboard.models import Logistic,TallyIpAdress
from hr.models import Department,Employee
from datetime import date
from django.db.models import Count

def alerts_messages(request):
    alerts = Alerts.objects.filter(completed=False).all()
    try:
        alerts_not_readed_by_user = Alerts.objects.filter(completed=False).exclude(user=request.user).count()
    except:
        alerts_not_readed_by_user = 0
    recievable_invoices = InvoiceReceivable.objects.count()
    payable_invoices = InvoicePayable.objects.count()
    payment_voucher = (PaymentVoucher.objects.count())
    global_ledgers = LedgerMaster.objects.all()
    receipt_voucher = (RecieptVoucher.objects.count())
    credit_note = (CreditNote.objects.count())
    debit_note = (DebitNote.objects.count())
    jobs = (JobMaster.objects.count())
    users = (User.objects.filter(is_superuser=False).count())
    staff_users = (User.objects.filter(is_staff=True).filter(is_superuser=False).count())
    emp_users = (User.objects.filter(is_staff=False).count())
    company_regions = Logistic.objects.all().values('region').annotate(count=Count('region'))
    
    countries = (Country.objects.count())
    states = State.objects.all()
    cities = (City.objects.count())
    currencies = (currency.objects.count())
    sea_ports = (Ports.objects.filter(type="Sea").count())
    air_ports = (Ports.objects.filter(type="Air").count())
    locations = Location.objects.all()
    shipping_lines = (ShippingLines.objects.count())
    global_shipping_lines = ShippingLines.objects.all()
    airlines = (Airlines.objects.count())
    billing_heads = (BillingHead.objects.count())
    parties = (Party.objects.count())
    global_parties = Party.objects.all()
    global_party_address = PartyAddress.objects.all()
    global_jobs = (JobMaster.objects.count())
    global_companies = Logistic.objects.all()
    global_ip_address = TallyIpAdress.objects.all()
    global_employees = Employee.objects.all()
    ledger_category_global_gth = (LedgerCategories.objects.count())
    
    MODULES = [
        'All',
        'Sea Export',
        'Sea Import',
        'Air Export',
        'Air Import',
        'Transportation',
    ]
    FREIGHT_TERMS = [
        {'name':"FOB"},
        {'name':"CIF"},
        {'name':"C&F"},
        {'name':"C&I"},
    ]
    SCHEME_TYPE = [
        {'name':"19 (DRAWBACK)"},
        {'name':"00 (DUTY FREE)"},
        {'name':"12 (EPCG)"},
        {'name':"43 (EPCG + DRAWBACK)"},
        {'name':"99 (NFIA)"},
        {'name':"ROAD TAP"},
        {'name':"DFIA"},
    ]
    
    job_container_types = [
        '20',
        '40',
        '45',
       
        ]
    job_container_mode = [
        'Dry',
        'Dry Standard',
        'Dry High Cube',
        'Tank',
        'Reefer',
        'Normal',
        ]

   
    return {'alerts':alerts,
            'alerts_not_readed_by_user':alerts_not_readed_by_user, 
            'MODULES':MODULES,
            'recievable_invoices_global_gth':recievable_invoices,
            'payable_invoices_global_gth':payable_invoices,
            'payment_voucher_global_gth':payment_voucher,
            'receipt_voucher_global_gth':receipt_voucher,
            'credit_note_global_gth':credit_note,
            'debit_note_global_gth':debit_note,
            'jobs_global_gth':jobs,
            'users_global_gth':users,
            'countries_global_gth':countries,
            'states_global_gth':(states),
            'all_states':states,
            'cities_global_gth':cities,
            'currencies_global_gth':currencies,
            'sea_ports_global_gth':sea_ports,
            'air_ports_global_gth':air_ports,
            'locations_global_gth':(locations),
            'global_locations':locations,
            'shipping_lines_global_gth':shipping_lines,
            'airlines_global_gth':airlines,
            'billing_heads_global_gth':billing_heads,
            'parties_global_gth':parties,
            'jobs_global_gth':global_jobs,
            'global_companies':global_companies,
            'global_ip_address':global_ip_address,
            'global_vendors':Vendor.objects.exclude(tally_group=None).all(),
            'global_ledgers':LedgerMaster.objects.exclude(tally_group=None).all(),
            'ledger_category_global_gth':ledger_category_global_gth,
            'staff_users':staff_users,
            'emp_users':emp_users,
            'global_employees':global_employees,
            'global_ports':Ports.objects.all(),
            'global_uom':UOM.objects.all(),
            'global_currencies':currency.objects.all(),
            'global_billing_head':BillingHead.objects.all(),
            'global_trailor_billing_head':TrailorBillingHead.objects.all(),
            'global_vendor':Vendor.objects.all(),
            'global_parties':global_parties,
            'global_voucher_parties':global_parties.exclude(tally_group=None).all(),
            'company_regions':company_regions,
            'global_party_type':PartyType.objects.all(),
            'global_banks':Bank.objects.all(),
            'global_party_address':global_party_address,
            'FREIGHT_TERMS':FREIGHT_TERMS,
            'SCHEME_TYPE':SCHEME_TYPE,
            'job_container_types':job_container_types,
            'job_container_mode':job_container_mode,
            'global_shipping_lines':global_shipping_lines,
            'global_category':LedgerCategory.objects.all(),
            
            'total_departments':(Department.objects.count()),
            }