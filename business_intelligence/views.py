from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from masters.models import JobMaster,Party
from masters.views import check_permissions
from dashboard.models import Logistic
from datetime import datetime,date, timedelta
import calendar

from accounting.models import InvoiceReceivable,InvoicePayable,IndirectExpense,RecieptVoucher,PaymentVoucher,PaymentVoucherDetails,DebitNoteDetail, RecieptVoucherDetails, Vendor, Salary, DebitNote, Loan, LoanPaymentRecord, ContraVoucher

from django.db.models import Sum,Count
from django.db.models.functions import TruncYear,TruncMonth,TruncDate
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
import xlsxwriter
from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent

from collections import defaultdict
import json
from io import BytesIO


# Create your views here.



@login_required(login_url='handle_login')
def index(request, module):
    context = {}
    check_permissions(request, module)

    jobs = JobMaster.objects.exclude().select_related('created_by', 'shipper', 'company_type', 'consignee',
                                                      'port_of_loading', 'port_of_discharge', 'application_handler',
                                                      'alternate_company', 'shipping_line', 'booking_party',
                                                      'place_of_reciept', 'place_of_loading', 'place_of_unloading',
                                                      'account', 'account_address').prefetch_related('job_container').all()

    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()

    current_month = datetime.now().month
    current_year = datetime.now().year
    _, end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year, current_month, 1)
    to_date = date(current_year, current_month, end_day)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        # Safely retrieve bi_company without raising an error
        bi_company = request.POST.get('bi_company')
        if bi_company is not None:
            bi_company = int(bi_company)
            # Additional processing with bi_company if needed...

        jobs = jobs.filter(job_date__range=[from_date, to_date]).all()

    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user).all()

    account_manager_job_counts = (
    jobs.exclude(account_manager=None)
        .values('account_manager', 'account_manager__name', 'job_date__year')
        .annotate(job_count=Count('account_manager'))
      
)
    # print(account_manager_job_counts)
        # Process the data and create a list for JSON response
    graph_data = []
    for i in account_manager_job_counts:
        graph_data.append({
            'name': i['account_manager__name'],
            'date': i['job_date__year'],
            'counts': i['job_count']
        })



    

    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    invoices = InvoiceReceivable.objects.filter(is_deleted=False).all()

    years = []
    invoice_date = invoices.annotate(years=TruncYear('date_of_invoice')).values('years').annotate(year_amount = Sum('date_of_invoice')).order_by('years')
    for i in invoice_date:
        years.append(i['years'].strftime('%Y'))


    jobs = JobMaster.objects.all()
    selected_company = 'all'
    if request.method == 'POST':
        bi_company = int(request.POST.get('bi_company', 0))
        company = Logistic.objects.filter(id=bi_company).first()
        invoices = invoices.filter(company_type=company).all()
        jobs = jobs.filter(company_type=company).all()
        selected_company = bi_company

    if not request.user.user_account.see_global_data:
        invoices = invoices.filter(company_type=company).all()
        jobs = jobs.filter(company_type=company).all()

    total_sales = invoices.aggregate(Sum('net_amount'))
    if total_sales['net_amount__sum']:
        total_sales = round(total_sales['net_amount__sum'], 2)
    else:
        total_sales = 0

    recievable_pending_amount = invoices.aggregate(Sum('pending_amount'))
    if recievable_pending_amount['pending_amount__sum']:
        recievable_pending_amount = round(recievable_pending_amount['pending_amount__sum'], 2)
    else:
        recievable_pending_amount = 0

    today_sales = invoices.filter(date_of_invoice=date.today()).aggregate(Sum('net_amount'))
    if today_sales['net_amount__sum']:
        today_sales = round(today_sales['net_amount__sum'], 2)
    else:
        today_sales = 0

    recievable_collected_amount = round((total_sales - recievable_pending_amount), 2)

    year_wise_sales = invoices.annotate(year=TruncYear('date_of_invoice')).values('year').annotate(
        year_amount=Sum('net_amount')).values('year', 'year_amount')
    year_wise_sales_list = []
    for i in year_wise_sales:
        year_wise_sales_list.append({
            'year': i['year'].year,
            'amount': i['year_amount'],
        })

    year_wise_sales_list.reverse()

    year_wise_jobs = jobs.annotate(year=TruncYear('job_date')).values('year').annotate(
        year_count=Count('job_no')).values('year', 'year_count')
    year_wise_jobs_list = []
    for i in year_wise_jobs:
        year_wise_jobs_list.append({
            'year': i['year'].year,
            'count': i['year_count'],
        })

    year_wise_jobs_list.reverse()

    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    

    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user).all()
    
    
    # bill_to_counts = (
    #     invoices.exclude(bill_to=None).values('bill_to','bill_to__party_name')
    #         .annotate(job_count=Count('id'))
    #         .order_by('bill_to')
    # )
    # graph_dataa = []
    # for i in bill_to_counts:
    #     graph_dataa.append({
    #         'name':i['bill_to__party_name'],
    #         'counts' : i['job_count']
    #     })
    bill_to_counts = (
        invoices.exclude(bill_to=None)
        .annotate(date=TruncDate('date_of_invoice'))  # Replace 'date_of_invoice' with your actual date field
        .values('bill_to', 'bill_to__party_name', 'date')
        .annotate(job_count=Count('id'))
        .order_by('bill_to', 'date')
    )
    graph_dataa = []
    for i in bill_to_counts:
        try:
            graph_dataa.append({
                'name': i['bill_to__party_name'],
                'date': datetime.strftime(i['date'],"%Y-%m-%d"),
                'counts': i['job_count']
            })
        except:
            pass
  
    data_list=[]
    databse_query=JobMaster.objects.filter(module="Sea Import")
    for i in databse_query:
        data={"month":i.job_date.month,"year":i.job_date.year,"container":i.job_container.count()}
        data_list.append(data)
    context = {
        'years' : years,

        'data_list':data_list,
        'bill_to_data': graph_dataa,
        'account_manager_data': graph_data,
        'total_sales': total_sales,
        'today_sales': today_sales,
        'recievable_pending_amount': recievable_pending_amount,
        'recievable_collected_amount': recievable_collected_amount,
        'selected_company': selected_company,
        'year_wise_sales': year_wise_sales_list,
        'greeting': greeting,
        'module': module,
        'year_wise_jobs_list': year_wise_jobs_list,
        'job_count': len(jobs),
        'active_job_count': len(
            jobs.exclude(Q(job_status='Close') | Q(job_status='Cancel') | Q(is_deleted=True)).all()),
        'close_job_count': len(jobs.filter(Q(job_status='Close') | Q(job_status='Cancel')).all()),
        'deleted_job_count': len(jobs.filter(is_deleted=True).all()),
        'jobs': jobs,
        'module': module,
        'from_date': datetime.strptime(str(from_date), '%Y-%m-%d'),
        'to_date': datetime.strptime(str(to_date), '%Y-%m-%d')
    }

    return render(request, 'bi_report/index.html', context)




@login_required(login_url='home:handle_login')
def incompleted_jobs(request,module):
    context = {}
    check_permissions(request,module)
    selected_region = "A"
    selected_company = "A"
    selected_party = "A"

    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    jobs = JobMaster.objects.select_related('company_type','account','created_by').prefetch_related('recievable_invoice_job','recievable_invoice_job__company_type','payable_invoice_job','credit_note_job','credit_note_job__company_type','payable_invoice_job__company_type','gr_job','mbl_job','can_job','manifest_job','trailor_exp_job__company_type','trailor_exp_job__trailor_no','indirect_exp_job__company_type').all()

    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company = request.POST.get('company',"A")
        party = request.POST.get('party',"A")
        region = request.POST.get('region',"A")
       
        if not region == "A" and request.user.user_account.see_global_data:
            jobs = jobs.filter(company_type__region=region).all()
            selected_region = region
       
        if not company == "A" and request.user.user_account.see_global_data:
            jobs = jobs.filter(company_type=int(company)).all()
            selected_company = int(company)

        if not party == "A":
            jobs = jobs.filter(account=int(party)).all()
            selected_party = int(party)


    
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(company_type=request.user.user_account.office).all()
        
    
    jobs = jobs.annotate(receivable_sum=Sum('recievable_invoice_job__net_amount'),payable_sum=Sum('payable_invoice_job__net_amount')) 
    jobs = jobs.exclude(is_deleted=True).all()
    jobs = jobs.filter(job_date__range=[from_date,to_date]).all()

    context['jobs']= jobs
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    context['selected_region']=selected_region
    context['selected_company']=selected_company
    context['selected_party']=selected_party
    return render(request,'bi_report/jobs/incompleted_jobs.html',context)


@login_required(login_url='home:handle_login')
def jobs_p_and_l_status(request,module):
    context = {}
    check_permissions(request,module)
    selected_region = "A"
    selected_company = "A"
    selected_party = "A"
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    jobs = JobMaster.objects.select_related('company_type','account','created_by').prefetch_related('recievable_invoice_job','payable_invoice_job').all()
   
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company = request.POST.get('company',"A")
        party = request.POST.get('party',"A")
        region = request.POST.get('region',"A")
       
        if not region == "A":
            jobs = jobs.filter(company_type__region=region).all()
            selected_region = region
       
        if not company == "A":
            jobs = jobs.filter(company_type=int(company)).all()
            selected_company = int(company)

        if not party == "A":
            jobs = jobs.filter(account=int(party)).all()
            selected_party = int(party)

       
        
    jobs = jobs.filter(job_date__range=[from_date,to_date]).all()
        
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(company_type=company).all()
        
    jobs = jobs.annotate(receivable_sum=Sum('recievable_invoice_job__net_amount'),payable_sum=Sum('payable_invoice_job__net_amount'))   
    
    
    jobs = jobs.exclude(is_deleted=True).all()
    
    context['jobs']= jobs
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    context['selected_region']=selected_region
    context['selected_company']=selected_company
    context['selected_party']=selected_party
    return render(request,'bi_report/jobs/jobs_p_and_l_status.html',context)

@login_required(login_url='home:handle_login')
def jobs_psr(request,module):
    context = {}
    check_permissions(request,module)

    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
   
  
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    if request.method == 'POST':
        
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
            

    jobs = JobMaster.objects.prefetch_related('manifest_job','job_container','mbl_job','mbl_job__consigned_name','mbl_job__exporter_name').select_related('company_type','account','created_by','port_of_loading','port_of_discharge','final_destination','alternate_company').exclude(is_deleted=True).filter(Q(company_type__psr_report=True) | Q(alternate_company__psr_report=True)).filter(job_date__range=[from_date,to_date]).all()


    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()
 
   
    
    context['jobs']= jobs
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    return render(request,'bi_report/jobs/jobs_psr.html',context)

@login_required(login_url='home:handle_login')
def day_book(request,module):
    check_permissions(request,module)
    selected_company = request.user.user_account.office
    filter_date = date.today()
    date_type = 'EF'
    if request.method == 'POST':
        selected_company = request.POST['company']
        selected_company = Logistic.objects.filter(id=int(selected_company)).first()
        str_filter_date = request.POST['filter_date']
        filter_date = datetime.strptime(str(str_filter_date),"%Y-%m-%d").date()
        date_type = request.POST['date_type']
    
    all_sales = InvoiceReceivable.objects.filter(company_type=selected_company).filter(is_einvoiced=True).filter(is_deleted=False).filter(is_cancel=False).filter(old_invoice=False).all()
    day_sales = []
    for i in all_sales:
        if date_type == "EF":
            if i.einvoice_date.date() == filter_date:
                day_sales.append(i)
        else:
            if i.created_at.date() == filter_date:
                day_sales.append(i)

    
    day_purchase_data = InvoicePayable.objects.filter(company_type=selected_company).filter(is_deleted=False).all() 
    if date_type == "EF":
        day_purchase = day_purchase_data.filter(date_of_invoice=filter_date).all()
    else:
        day_purchase = []
        for i in day_purchase_data:
            if i.created_at.date() == filter_date:
                day_purchase.append(i)

    day_reciept_data = RecieptVoucher.objects.filter(company_type=selected_company).filter(is_deleted=False).all()
    if date_type == "EF":
        day_reciept = day_reciept_data.filter(voucher_date=filter_date).all()
    else:
        day_reciept = []
        for i in day_reciept_data:
            if i.created_at.date() == filter_date:
                day_reciept.append(i)

    day_payment_data = PaymentVoucher.objects.filter(company_type=selected_company).filter(is_deleted=False).all()
    if date_type == "EF":
        day_payment = day_payment_data.filter(voucher_date = filter_date).all()
    else:
        day_payment = []
        for i in day_payment_data:
            if i.created_at.date() == filter_date:
                day_payment.append(i)

    jobs_data = JobMaster.objects.filter(is_deleted=False).filter(Q(company_type=selected_company)|Q(alternate_company=selected_company)).all()
    if date_type == "EF":
        jobs = jobs_data.filter(job_date = filter_date).all()
    else:
        jobs = []
        for i in jobs_data:
            if i.created_at.date() == filter_date:
                jobs.append(i)


    context = {
        'module':module,
        'filter_date':filter_date,
        'selected_company':selected_company,
        'jobs':jobs,
        'day_sales':day_sales,
        'day_purchase':day_purchase,
        'day_reciept':day_reciept,
        'day_payment':day_payment,
        'date_type':date_type,
    }
    return render(request,'bi_report/daybook/daybook.html',context)


@login_required(login_url='home:handle_login')
def customer_details(request,module):
    context={}
    check_permissions(request,module)
    party_details=Party.objects.prefetch_related('party_address').all()   
    context['module'] = module
    context['parties'] = party_details

    return render(request,'bi_report/other/customer_detail.html',context)

@login_required(login_url='home:handle_login')
def csr_report(request,module):
    context={}
    check_permissions(request,module)

    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
      
        
        jobs = JobMaster.objects.select_related('port_of_loading','port_of_discharge','shipper','consignee','shipping_line','account_manager').prefetch_related('job_container').filter(job_date__gte=from_date).filter(job_date__lte=to_date).all()
        
        if not request.user.user_account.see_global_data:
            jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()

        context['jobs']= jobs
        context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
        context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()
    
    context['module']= module
    return render(request,'bi_report/csr/csr.html',context)

@login_required(login_url='home:handle_login')
def customer_report(request,module):
    context={}
    check_permissions(request,module)
    if request.method == 'POST':
        choose_company = request.POST['choose_company']
        invoices = InvoiceReceivable.objects.filter(company_type__id=choose_company).filter(is_einvoiced=True).filter(is_deleted=False).filter(is_cancel=False).values('bill_to__party_name','invoice_currency__short_name').annotate(sum=Sum('net_amount')).order_by('-sum')
        # print(invoices)
        context['invoices']= invoices
        context['choose_company']= choose_company
    context['module']= module
    return render(request,'bi_report/top_customers/top_customers.html',context)






@login_required(login_url='handle_login')
def get_sales_and_purchase_data(request, year, module):
    
    sales_invoices = InvoiceReceivable.objects.filter(is_child=False, is_deleted=False, date_of_invoice__year=year) \
        .annotate(month=TruncMonth('date_of_invoice')) \
        .values('month') \
        .annotate(month_amount=Sum('net_amount')) \
        .order_by('month')

    months = []
    sales = []
    for record in sales_invoices:
        months.append(record['month'].strftime('%b'))  # Short month name
        sales.append(record['month_amount'] or 0)

    # Get purchase invoices data
    purchase_invoices = InvoicePayable.objects.filter(is_deleted=False, date_of_invoice__year=year).annotate(month=TruncMonth('date_of_invoice')) \
                        .values('month').annotate(month_amount=Sum('net_amount')).order_by('month')

    
    purchases = []
    for record in purchase_invoices:
        purchases.append(record['month_amount'] or 0)

    return JsonResponse({
        'sales': sales,
        'purchases': purchases,
        'months': months,
        
    })


@login_required(login_url='handle_login')
def job_wise_data(request, year, module):
    job_masters = JobMaster.objects.filter(is_deleted = False).all()
    job_condition_wise = job_masters.filter(job_date__year = year) \
                                            .annotate(month=TruncMonth('job_date')) \
                                            .values('month') \
                                            .annotate(job_count=Count('id')) \
                                            .order_by('month')
        
    months = []
    jobs = []
    for record in job_condition_wise:
        months.append(record['month'].strftime('%b'))  # Short month name
        jobs.append(record['job_count'] or 0)  # Default to 0 if no sales

    return JsonResponse({
        'jobs': jobs,
        'months': months,
        
    })



@login_required(login_url='handle_login')
def profit_margin_date_wise(request, year, module):
    invoices = InvoiceReceivable.objects.filter(
        is_child=False,
        is_deleted=False,
        date_of_invoice__year=year
    ).prefetch_related('crn_ref_invoice')

    
    monthly_data = defaultdict(lambda: {'invoice_sum': 0, 'credit_note_sum': 0})

    
    for invoice in invoices:
        month = invoice.date_of_invoice.month
        
        monthly_data[month]['invoice_sum'] += invoice.net_amount
        
        
        credit_notes = invoice.crn_ref_invoice.all()
        for crn in credit_notes:
            monthly_data[month]['credit_note_sum'] += crn.net_amount

    
    result = {
        'months': [],
        'invoice_sum': [],
        'credit_note_sum': [],
        'net_invoice_amount': []
    }

    for month in range(1, 13):
        result['months'].append(month)
        invoice_sum = monthly_data[month]['invoice_sum']
        credit_note_sum = monthly_data[month]['credit_note_sum']
        net_invoice_amount = invoice_sum - credit_note_sum
        result['invoice_sum'].append(invoice_sum)
        result['credit_note_sum'].append(credit_note_sum)
        result['net_invoice_amount'].append(net_invoice_amount)

    json_result = json.dumps(result)

    
    return JsonResponse(result)



@login_required(login_url='handle_login')
def invoice_pay_margin_date_wise(request, year, module):
    invoice_payables = InvoicePayable.objects.filter(
        date_of_invoice__year=year
    )
    
    monthly_data = defaultdict(lambda: {'debit_note_sum': 0, 'payable_invoice_sum': 0})

    for invoice in invoice_payables:
        month = invoice.date_of_invoice.month
        
        related_debit_notes = DebitNote.objects.filter(invoice_no=invoice.invoice_no)
        
        for debit_note in related_debit_notes:
            monthly_data[month]['debit_note_sum'] += debit_note.net_amount
        
        
        monthly_data[month]['payable_invoice_sum'] += invoice.net_amount

    
    result = {
        'months': [],
        'debit_note_sum': [],
        'payable_invoice_sum': [],
        'net_debit_amount': []
    }

    
    for month in range(1, 13):
        result['months'].append(month)
        debit_note_sum = monthly_data[month]['debit_note_sum']
        payable_invoice_sum = monthly_data[month]['payable_invoice_sum']
        net_debit_amount = payable_invoice_sum - debit_note_sum  # Calculate the net debit amount
        result['debit_note_sum'].append(debit_note_sum)
        result['payable_invoice_sum'].append(payable_invoice_sum)
        result['net_debit_amount'].append(net_debit_amount)

    
    json_result = json.dumps(result)
    
    return JsonResponse(result)







@login_required(login_url='handle_login')
def CrudLogs(request, module):
    check_permissions(request, module)
    context = {}
    crud = CRUDEvent.objects.all()

    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    current_date = datetime.now().date()
    from_date = current_date - timedelta(days=2)

    crud = crud.filter(datetime__range=[from_date,current_date]).all()

    if request.method == 'POST':
        from_date = request.POST['from_date']
        current_date  = request.POST['to_date']
        crud = CRUDEvent.objects.all()
        crud = crud.filter(datetime__range=[from_date,current_date]).all()

    # for i in crud:
    #     print(i)
    for event in crud:
        # Parse JSON for changed fields
        if event.changed_fields:
            event.changes_dict = json.loads(event.changed_fields)
        else:
            event.changes_dict = None

    context['data'] = crud
    context['crudevents'] = crud
     
    context['module'] = module
    context['from_date'] = from_date
    context['to_date'] = current_date
    return render(request, 'bi_report/logs/crud_logs.html', context=context)