from django.shortcuts import  render,redirect
from accounting.forms import  *
from accounting.models import  *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from masters.models import Bank, BillingHead, JobMaster, Party,PartyAddress,TrailorBillingHead,Vendor,JobContainer
from dashboard.models import Logistic
from masters.views import check_permissions
from json import loads
from datetime import date, datetime, timedelta
from time import localtime
from django.db.models import Count,Sum, Q, Case, When,F,FloatField
import calendar
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.template import loader
from accounting.utils import generate_pdf
import xlsxwriter
from collections import defaultdict
from itertools import chain
from django.urls import reverse
from hr.models import Employee
from itertools import chain,zip_longest
# Create your views here.


@login_required(login_url='home:handle_login')
def mis_report(request,module):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Report')
    
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']
        company = None

        invoice_rec = InvoiceReceivable.objects.select_related('job_no','company_type').prefetch_related('recievable_invoice_reference','recievable_invoice_reference__billing_head').filter(job_no__job_date__range=[from_date,to_date]).all()
        invoice_pay = InvoicePayable.objects.select_related('job_no','company_type').prefetch_related('payable_invoice_reference','payable_invoice_reference__billing_head').filter(job_no__job_date__range=[from_date,to_date]).all()
        
        jobs = JobMaster.objects.select_related('company_type').prefetch_related('job_container').filter(job_date__range = [from_date,to_date]).all()

        if not choose_company == "All":
            company = Logistic.objects.filter(id=int(choose_company)).first()
            invoice_rec = invoice_rec.filter(company_type = company).all()
            invoice_pay = invoice_pay.filter(company_type = company).all()
            invoice_pay = invoice_pay.filter(company_type = company).all()
            jobs = jobs.filter(company_type = company).all()

        if Logistic.objects.count() == 1:
            company = Logistic.objects.first()

        income_heads = []
        expense_heads = []
        for i in invoice_rec:
            for j in i.recievable_invoice_reference.all():
                if not j.billing_head.billing_head in income_heads:
                    income_heads.append(j.billing_head.billing_head)
        
        for i in invoice_pay:
            for j in i.payable_invoice_reference.all():
                try:
                    if not j.billing_head.billing_head in expense_heads:
                        expense_heads.append(j.billing_head.billing_head)
                except:
                    pass

        cell_format_bold = workbook.add_format({'bold': True,'font_size':10, 'font_color': 'black','border':1,'bg_color':"#ffffff",'border_color':"black","align":"left"})

        cell_format_without_border = workbook.add_format({ 'font_color': 'black',"align":"left"})
        cell_format = workbook.add_format({ 'font_color': 'black','border':1,'bg_color':"#ffffff",'border_color':"black","align":"left"})
        income_cell_format_color = workbook.add_format({'bold': True, 'font_color': 'black','border':1,'bg_color':"#ffff00",'border_color':"black","align":"left"})
        expense_cell_format_color = workbook.add_format({'bold': True, 'font_color': 'black','border':1,'bg_color':"#aad000",'border_color':"black","align":"left"})
        global_y = 1
        
        if company:
            worksheet.merge_range(f"A{global_y}:C{global_y}",f"{company.legal_name}",cell_format_bold)
            global_y += 1
            worksheet.merge_range(f"A{global_y}:C{global_y}",f"{company.address_line_1}",cell_format)
            global_y += 1
            worksheet.merge_range(f"A{global_y}:C{global_y}",f"{company.address_line_2}",cell_format)
            global_y += 1

        
        worksheet.merge_range(f"A{global_y}:C{global_y}","Sales Register",cell_format_bold)
        global_y += 1
        
        worksheet.merge_range(f"A{global_y}:C{global_y}",f"{datetime.strptime(str(from_date),'%Y-%m-%d').date()} To {datetime.strptime(str(to_date),'%Y-%m-%d').date()}",cell_format)

        income_side = 5 + len(income_heads) + 1
        if len(income_heads) > 1:
            worksheet.merge_range(global_y-1,5,global_y-1,income_side-1,f"INCOME SIDE",income_cell_format_color)
        else:
            worksheet.write(global_y-1,income_side,f"INCOME SIDE",income_cell_format_color)

        if len(expense_heads) > 1:
            worksheet.merge_range(global_y-1,income_side,global_y-1,income_side+len(expense_heads),f"EXPENSE SIDE",expense_cell_format_color)
        else:
            worksheet.write(global_y-1,income_side,f"EXPENSE SIDE",expense_cell_format_color)


        
        global_y += 1
        first_row = global_y
        worksheet.write(f"A{global_y}","Sr. No.",cell_format_bold)
        worksheet.write(f"B{global_y}","Particulars",cell_format_bold)
        worksheet.write(f"C{global_y}","Voucher Type",cell_format_bold)
        worksheet.write(f"D{global_y}","No. of Containers",cell_format_bold)
        worksheet.write(f"E{global_y}","Job No.",cell_format_bold)
        worksheet.freeze_panes(global_y, 5)
        income_x = 5
        for head in income_heads:
            worksheet.write(global_y-1,income_x,f"{head}",cell_format_bold)
            income_x += 1

        worksheet.write(global_y-1,income_x,f"TOTAL INCOME",cell_format_bold)
        income_x += 1
        
        
        for head in expense_heads:
            worksheet.write(global_y-1,income_x,f"{head}",cell_format_bold)
            income_x += 1

        worksheet.write(global_y-1,income_x,f"TOTAL EXPENSE",cell_format_bold)
        income_x += 1
        worksheet.write(global_y-1,income_x,f"MARGIN",cell_format_bold)
        income_x += 1

        worksheet.set_column(0, income_x, 20)  
        global_y+=1
        for index,data in enumerate(jobs):
            worksheet.write(f"A{global_y}",f"{index+1}",cell_format_bold)
            worksheet.write(f"B{global_y}",f"{data.account}",cell_format)
            worksheet.write(f"C{global_y}",f"Sales",cell_format)
            worksheet.write(f"D{global_y}",f"{data.job_container.count()}",cell_format)
            worksheet.write(f"E{global_y}",f"{data.job_no}",cell_format)

            income_obj={}
            visited_income_heads = []
            rec_inv = invoice_rec.filter(job_no__id=data.id).all()
            total_income = 0
            if rec_inv.count() > 0:
                for inv in rec_inv:
                    for head in inv.recievable_invoice_reference.all():
                        total_income += head.amount
                        if not head.billing_head.billing_head in visited_income_heads:
                            visited_income_heads.append(head.billing_head.billing_head)
                            income_obj[f"{income_heads.index(f'{head.billing_head.billing_head}')}"]=head.amount
                        else:
                            income_obj[f"{income_heads.index(f'{head.billing_head.billing_head}')}"]+=head.amount

                            
                        worksheet.write(global_y-1,income_heads.index(f'{head.billing_head.billing_head}')+5,income_obj[f"{income_heads.index(f'{head.billing_head.billing_head}')}"],cell_format_without_border)
            
            worksheet.write(global_y-1,len(income_heads)+5,total_income,cell_format_without_border)
            
            expense_obj={}
            visited_expense_heads = []
            total_expense = 0
            pay_inv = invoice_pay.filter(job_no__id=data.id).all()
            if pay_inv.count() > 0:
                for inv in pay_inv:
                    
                    for head in inv.payable_invoice_reference.all():
                        try:
                            if  head.billing_head:
                                total_expense += head.amount
                                if not head.billing_head in visited_expense_heads:
                                    visited_expense_heads.append(head.billing_head)
                                    expense_obj[f"{expense_heads.index(f'{head.billing_head}')}"]=head.amount
                                else:
                                    expense_obj[f"{expense_heads.index(f'{head.billing_head}')}"]+=head.amount

                                
                                worksheet.write(global_y-1,1+expense_heads.index(f'{head.billing_head}')+5+len(income_heads),expense_obj[f"{expense_heads.index(f'{head.billing_head}')}"],cell_format_without_border)
                        except:
                            pass
                    
            worksheet.write(global_y-1,1+len(expense_heads)+5+len(income_heads),total_expense,cell_format_without_border)
            worksheet.write(global_y-1,2+len(expense_heads)+5+len(income_heads),total_income-total_expense,cell_format_without_border)

            global_y += 1

       
        
        workbook.close()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = f'attachment;filename="mis{from_date}to{to_date}.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response
    
    context = {
        'module':module
    }
    return render(request,'bi_report/mis/mis.html',context)

# Journal Books
@login_required(login_url='home:handle_login')
def sales_invoice_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(sales_invoice=None).filter(sales_invoice__einvoice_date__date__gte=from_date).filter(sales_invoice__einvoice_date__date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(sales_invoice__company_type__id=int(choose_company))

    vouchers = vouchers.values('sales_invoice__id','sales_invoice__company_type', 'sales_invoice__final_invoice_no','sales_invoice__bill_to__party_name', 'category__name','dr_cr','amount','sales_invoice__einvoice_date').annotate(
        count=Count('sales_invoice__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["sales_invoice__id"]}'].append(i)
        
    print(report)

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/sales.html',context)

@login_required(login_url='home:handle_login')
def crn_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(crn=None).filter(crn__einvoice_date__date__gte=from_date).filter(crn__einvoice_date__date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(crn__company_type__id=int(choose_company))

    vouchers = vouchers.values('crn__id','crn__company_type','crn__reference_invoice__final_invoice_no', 'crn__final_invoice_no','crn__bill_to__party_name', 'category__name','dr_cr','amount','crn__einvoice_date').annotate(
        count=Count('crn__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["crn__id"]}'].append(i)
        
    print(report)

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/crn.html',context)

@login_required(login_url='home:handle_login')
def purchase_invoice_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(purchase_invoice=None).filter(purchase_invoice__date_of_invoice__gte=from_date).filter(purchase_invoice__date_of_invoice__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(purchase_invoice__company_type__id=int(choose_company))

    vouchers = vouchers.values('purchase_invoice__id','purchase_invoice__company_type', 'purchase_invoice__purchase_invoice_no','purchase_invoice__bill_from__party_name', 'category__name','dr_cr','amount','purchase_invoice__date_of_invoice').annotate(
        count=Count('purchase_invoice__id'),
        total = Sum('amount')
    )

   
    report = defaultdict(lambda: {'dr_sum': 0, 'cr_sum': 0, 'records': []})
    for i in vouchers:
        key = i["purchase_invoice__id"]  # Group by purchase_invoice ID
        report[key]['records'].append(i)  # Store record details

        if i['dr_cr'] == "Debit":
            report[key]['dr_sum'] += round(i['total'],2)
        else:
            report[key]['cr_sum'] += round(i['total'],2)
    
    unmatched_value_dr = 0
    unmatched_value_cr = 0
    for key, data in report.items():
        data['dr_sum'] = round(data['dr_sum'], 2)
        data['cr_sum'] = round(data['cr_sum'], 2)
        data['difference'] = ((data['dr_sum'] - data['dr_sum']))

        if data['dr_sum'] != data['cr_sum']:
            unmatched_value_dr += data['dr_sum']
            unmatched_value_cr += data['cr_sum']

    # Print unmatched debit and credit values
    print("Total Unmatched:", unmatched_value_dr - unmatched_value_cr)
    


    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/purchase.html',context)

@login_required(login_url='home:handle_login')
def drn_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(drn=None).filter(drn__date_of_note__gte=from_date).filter(drn__date_of_note__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(drn__company_type__id=int(choose_company))

    vouchers = vouchers.values('drn__id','drn__company_type', 'drn__debit_note_no','drn__invoice_no','drn__bill_from__party_name', 'category__name','dr_cr','amount','drn__date_of_note').annotate(
        count=Count('drn__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["drn__id"]}'].append(i)
        
    print(report)

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/drn.html',context)

@login_required(login_url='home:handle_login')
def indirect_expense_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(indirect_expense=None).filter(indirect_expense__bill_date__gte=from_date).filter(indirect_expense__bill_date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(indirect_expense__company_type__id=int(choose_company))

    vouchers = vouchers.values('indirect_expense__id','indirect_expense__company_type', 'indirect_expense__bill_no','indirect_expense__vendor__vendor_name', 'category__name','dr_cr','amount','indirect_expense__bill_date').annotate(
        count=Count('indirect_expense__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["indirect_expense__id"]}'].append(i)
        
    print(report)

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/indirect_expense.html',context)

@login_required(login_url='home:handle_login')
def reciept_voucher_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(receipt=None).filter(receipt__voucher_date__gte=from_date).filter(receipt__voucher_date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(receipt__company_type__id=int(choose_company))

    vouchers = vouchers.values('receipt__id','receipt__company_type', 'receipt__voucher_no','receipt__instrument_no','receipt__party_name__party_name', 'category__name','dr_cr','amount','receipt__voucher_date').annotate(
        count=Count('receipt__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["receipt__id"]}'].append(i)
        

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/receipt.html',context)

@login_required(login_url='home:handle_login')
def payment_voucher_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(payment=None).filter(payment__voucher_date__gte=from_date).filter(payment__voucher_date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(payment__company_type__id=int(choose_company))

    vouchers = vouchers.values('payment__id','payment__company_type', 'payment__voucher_no','payment__instrument_no','payment__party_name__party_name','payment__vendor__vendor_name', 'category__name','dr_cr','amount','payment__voucher_date').annotate(
        count=Count('payment__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["payment__id"]}'].append(i)
        

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/payment.html',context)


@login_required(login_url='home:handle_login')
def contra_voucher_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(contra=None).filter(contra__voucher_date__gte=from_date).filter(contra__voucher_date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(contra__company_type__id=int(choose_company))

    vouchers = vouchers.values('contra__id','contra__company_type', 'contra__voucher_no','contra__instrument_no','contra__account_from__bank_name','contra__account_to__bank_name','contra__cash__company_name', 'category__name','dr_cr','amount','contra__voucher_date','contra__contra_choice').annotate(
        count=Count('contra__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["contra__id"]}'].append(i)
        

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/contra.html',context)


@login_required(login_url='home:handle_login')
def loan_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(loan=None).filter(loan__loan_date__gte=from_date).filter(loan__loan_date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(loan__company_type__id=int(choose_company))

    vouchers = vouchers.values('loan__id','loan__company_type', 'loan__loan_no','loan__loan_date','category__name','dr_cr','amount',).annotate(
        count=Count('loan__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["loan__id"]}'].append(i)
        

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/loan.html',context)


@login_required(login_url='home:handle_login')
def loan_record_journal(request,module):
    context = {'module':module}

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    choose_company = "All"

    if request.method == "POST":
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

    vouchers = Voucher.objects.exclude(loan_record=None).filter(loan_record__payment_date__gte=from_date).filter(loan_record__payment_date__lte=to_date).order_by('-dr_cr')

    if not choose_company == "All":
        vouchers = vouchers.filter(loan_record__loan__company_type__id=int(choose_company))

    vouchers = vouchers.values('loan_record__id','loan_record__loan__company_type', 'loan_record__loan__loan_no','loan_record__payment_date','category__name','dr_cr','amount',).annotate(
        count=Count('loan_record__id'),
        total = Sum('amount')
    )

    report = defaultdict(list)
    for i in vouchers:
        report[f'{i["loan_record__id"]}'].append(i)
        

    context['report'] = dict(report)
    context['choose_company'] = choose_company
    context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()

    return render(request,'report/journal_book/loan_payment_record.html',context)

@login_required(login_url='home:handle_login')
def job_cost_sheet_detail(request,module):
    context ={}
    check_permissions(request,module)
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    
        
    selected_company = "A"
    selected_party = "A"
    job_status = "A"
    job_date_filter = "J"
    report = False
    selected_region = None
    if request.method == 'POST':
        list_selected = int(request.POST['list_selected'])
        if list_selected == 1:
            selected_fields = request.POST['selected_fields']
            selected_fields = str(selected_fields).split(",")
            error_list = []
        
            for i in selected_fields:
                try:
                    job = JobMaster.objects.filter(id=int(i)).first()
                    job.job_status = "Close"
                    job.save()
                except:
               
                    error_list.append(f"{i}")
                    
            if len(error_list) > 0:
                messages.error(request,f'{error_list} Not Found...')
                
        report = True
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company = request.POST['company']
        party = request.POST['party']
        job_status = request.POST['job_status']
        selected_region = request.POST['region']
        job_date_filter = request.POST['job_date_filter']
        
        
        jobs = JobMaster.objects.select_related('company_type','alternate_company','created_by','account','booking_party','shipping_line','port_of_loading').prefetch_related('job_hbl').filter(is_deleted=False).all()
            
        if job_date_filter == "J":
            jobs = jobs.filter(job_date__gte=from_date).filter(job_date__lte=to_date).all()
        
        if not company == "A":
            selected_company = int(company)
            jobs = jobs.filter(Q(company_type=selected_company)|Q(alternate_company=selected_company)).all()
           

        if not party == "A":
            selected_party = int(party)
            jobs = jobs.filter(account__id=selected_party).all()
            
        if job_status == "O":
            jobs = jobs.exclude(job_status="Close").all()
            
        if job_status == "C":
            jobs = jobs.filter(job_status="Close").all()
            
        report_list = []

        for i in jobs:
            report_data = {
                'job':i,
            }
            invoice_recievable_sum = 0
            invoice_recievable_data = []
            recievable_invoice = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','invoice_currency','job_no').filter(company_type__region=selected_region).prefetch_related('recievable_invoice_reference','recievable_invoice_reference__billing_head','reciept_rec_inv','reciept_rec_inv__voucher','reciept_rec_inv__invoice').filter(is_deleted=False).filter(is_cancel=False).filter(job_no=i).all()
            if job_date_filter == "I":
                recievable_invoice = recievable_invoice.filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).all()
                if recievable_invoice.count() == 0:
                    continue
            
            if not company == "A":
                recievable_invoice = recievable_invoice.filter(company_type=company).all()

            for invoice in recievable_invoice:
                data = []
                for head in invoice.recievable_invoice_reference.all():
                    data.append({
                        'billing_head':head.billing_head,
                        'qty_unit':head.qty_unit,
                        'ex_rate':head.ex_rate,
                        'rate':head.rate,
                        'amount':head.amount,
                        'gst':head.gst,
                        'gst_amount':head.gst_amount,
                        'total':head.total,
                    })

                voucher_data = []
                for head in invoice.reciept_rec_inv.all():
                    voucher_data.append({
                        'voucher':head.voucher,
                        'net_amount':head.invoice.net_amount,
                        'received_amount':head.received_amount,
                        'tds_amount':head.tds_amount,
                        'adjustment_amount':head.adjustment_amount,
                        'pending_amount':head.pending_amount,
                    })

                invoice_recievable_data.append({
                    'invoice':invoice,
                    'data':data,
                    'vouchers':voucher_data
                })

                ex_rate = 1
                if not invoice.invoice_currency.short_name == "INR":
                    ex_rate = invoice.currency_ex_rate
                    
                invoice_recievable_sum += (float(invoice.gross_amount) * float(ex_rate))

            report_data['sales_invoice'] = {
                'sum':invoice_recievable_sum,
                'data':invoice_recievable_data
            }
            
                
            invoice_payable_sum = 0
            invoice_payable_data = []
            payable_invoice = InvoicePayable.objects.select_related('company_type','bill_from','bill_from_address','invoice_currency','job_no').prefetch_related('payable_invoice_reference','payable_invoice_reference__billing_head','pay_payment_inv','pay_payment_inv__voucher','pay_payment_inv__invoice').filter(job_no=i).filter(company_type__region=selected_region).filter(is_deleted=False).all()
            if not company == "A":
                payable_invoice = payable_invoice.filter(company_type=company).all()
            for invoice in payable_invoice:

                data = []
                for head in invoice.payable_invoice_reference.select_related('billing_head').all():
                    data.append({
                        'billing_head':head.billing_head,
                        'qty_unit':head.qty_unit,
                        'ex_rate':head.ex_rate,
                        'rate':head.rate,
                        'amount':head.amount,
                        'gst':head.gst,
                        'gst_amount':head.gst_amount,
                        'total':head.total,
                    })

                voucher_data = []
                for head in invoice.pay_payment_inv.all():
                    voucher_data.append({
                        'voucher':head.voucher,
                        'net_amount':head.invoice.net_amount,
                        'paid_amount':head.paid_amount,
                        'tds_amount':head.tds_amount,
                        'adjustment_amount':head.adjustment_amount,
                        'pending_amount':head.pending_amount,
                    })

                invoice_payable_data.append({
                    'invoice':invoice,
                    'data':data,
                    'vouchers':voucher_data
                })

                ex_rate = 1
                if not invoice.invoice_currency.short_name == "INR":
                    ex_rate = invoice.currency_ex_rate
                    
                invoice_payable_sum += (float(invoice.gross_amount) * float(ex_rate))

            report_data['purchase_invoice'] = {
                'sum':invoice_payable_sum,
                'data':invoice_payable_data,

            }

            credit_note_sum = 0
            crn_data = []
            credit_note = CreditNote.objects.select_related('company_type','bill_to','bill_to_address','invoice_currency','job_no').prefetch_related('credit_note_reference','credit_note_reference__billing_head').filter(company_type__region=selected_region).filter(job_no=i).filter(is_cancel=False).all()
            if not company == "A":
                credit_note = credit_note.filter(company_type=company).all()
            for invoice in credit_note:

                data = []
                for head in invoice.credit_note_reference.all():
                    data.append({
                        'billing_head':head.billing_head,
                        'qty_unit':head.qty_unit,
                        'ex_rate':head.ex_rate,
                        'rate':head.rate,
                        'amount':head.amount,
                        'gst':head.gst,
                        'gst_amount':head.gst_amount,
                        'total':head.total,
                    })

                crn_data.append({
                    'invoice':invoice,
                    'data':data
                })
                ex_rate = 1
                if not invoice.invoice_currency.short_name == "INR":
                    ex_rate = invoice.currency_ex_rate
                    
                credit_note_sum += (float(invoice.gross_amount) * float(ex_rate))

            report_data['credit_note'] = {
                'sum':credit_note_sum,
                'data':crn_data
            }
        
            debit_note_sum = 0
            drn_data = []
            debit_note = DebitNote.objects.select_related('company_type','bill_from','bill_from_address','invoice_currency','job_no').prefetch_related('debit_note_reference','debit_note_reference__billing_head').filter(company_type__region=selected_region).filter(job_no=i).all()
            if not company == "A":
                credit_note = credit_note.filter(company_type=company).all()
            for invoice in debit_note:

                data = []
                for head in invoice.debit_note_reference.all():
                    data.append({
                        'billing_head':head.billing_head,
                        'qty_unit':head.qty_unit,
                        'ex_rate':head.ex_rate,
                        'rate':head.rate,
                        'amount':head.amount,
                        'gst':head.gst,
                        'gst_amount':head.gst_amount,
                        'total':head.total,
                    })

                drn_data.append({
                    'invoice':invoice,
                    'data':data
                })
                ex_rate = 1
                if not invoice.invoice_currency.short_name == "INR":
                    ex_rate = invoice.currency_ex_rate
                    
                debit_note_sum += (float(invoice.gross_amount) * float(ex_rate))

            report_data['debit_note'] = {
                'sum':debit_note_sum,
                'data':drn_data
            }
        
            indirect_expense = IndirectExpense.objects.select_related('company_type','vendor','job_no').prefetch_related('indirect_expense_reference','indirect_expense_reference__billing_head').filter(company_type__region=selected_region).filter(job_no__job_no=i.job_no).all()
            indirect_expense_sum = 0
            indirect_expense_data = []

            if not company == "A":
                indirect_expense = indirect_expense.filter(company_type=company).filter(job_no__job_no=i.job_no).all()
            
            for invoice in indirect_expense:
                data = []
                for head in invoice.indirect_expense_reference.all():
                    data.append({
                        'billing_head':head.billing_head,
                        'total':head.total
                    })

                indirect_expense_data.append({
                    'invoice':invoice,
                    'data':data
                })
                indirect_expense_sum += invoice.gross_amount


            report_data['indirect_expense'] = {
                'sum':indirect_expense_sum,
                'data':indirect_expense_data
            }

            trailor_expense = TrailorExpense.objects.select_related('company_type','trailor_no','job_no').prefetch_related('trailor_expense_reference','trailor_expense_reference__billing_head','trailor_expense_reference__vendor').filter(company_type__region=selected_region).filter(job_no__job_no=i.job_no).all()
            trailor_expense_sum = 0
            trailor_expense_data = []

            if not company == "A":
                trailor_expense = trailor_expense.filter(company_type=company).all()

            for invoice in trailor_expense:
                data = []
                for head in invoice.trailor_expense_reference.all():
                    data.append({
                        'billing_head':head.billing_head,
                        'vendor':head.vendor,
                        'payment_type':head.payment_type,
                        'charges':head.charges
                    })
                    
                trailor_expense_data.append({
                    'invoice':invoice,
                    'data':data
                })
                trailor_expense_sum += invoice.net_amount

            report_data['trailor_expense'] = {
                'sum':trailor_expense_sum,
                'data':trailor_expense_data
            }
                
        
          
            
            profit_loss = round((invoice_recievable_sum + debit_note_sum) - (invoice_payable_sum + indirect_expense_sum + trailor_expense_sum + credit_note_sum),2)
            profit_percent = 0
            try:
                profit_percent = round(((profit_loss/invoice_recievable_sum)*100),2)
            except:
                pass
            total_purchase = round((invoice_payable_sum + indirect_expense_sum + trailor_expense_sum - debit_note_sum),2)
            recievable_invoice = round(invoice_recievable_sum,2)
            if recievable_invoice > 0 or total_purchase > 0:
                report_list.append(
                    {
                        **report_data,
                        'total_purchase':total_purchase,
                        'profit_loss':profit_loss,
                        'profit_percent':profit_percent
                    }
                )
            
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d") 
        context['report_list']= report_list
    
    
    context['report']= report
    context['selected_region']= selected_region
    context['selected_company']= selected_company
    context['selected_party']= selected_party
    context['job_status']= job_status
    context['job_date_filter']= job_date_filter
    context['module']= module
    return render(request,'report/job_cost_sheet/job_cost_sheet_report.html',context)


@login_required(login_url='home:handle_login')
def sale_person_performance_sheet(request,module):
    context = {}
    if request.method == "POST":
        from_date = request.POST['from_date']    
        to_date = request.POST['to_date']    
        company = request.POST['company']
        
        from_date = datetime.strptime(str(from_date),"%Y-%m-%d").date()    
        to_date = datetime.strptime(str(to_date),"%Y-%m-%d").date()    
        
        container_count = JobContainer.objects.filter(job__job_date__gte=from_date).filter(job__job_date__lte=to_date).filter(job__is_deleted=False).values("job__account_manager","container_type").annotate(count=Count('container_type'))
        
        inr_invoice = InvoiceReceivable.objects.select_related('company_type','bill_to','job_no','bill_to_address').filter(is_einvoiced=True).filter(is_cancel=False).filter(is_deleted=False).filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).filter(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum('gross_amount'),net_amount=Sum('net_amount'))
        
       
        
        non_inr_invoice = InvoiceReceivable.objects.select_related('company_type','bill_to','job_no','bill_to_address').filter(is_einvoiced=True).filter(is_cancel=False).filter(is_deleted=False).filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).exclude(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum(F('gross_amount')*F('currency_ex_rate')),net_amount=Sum(F('gross_amount')*F('currency_ex_rate')))
        
        inr_crn = CreditNote.objects.select_related('company_type','bill_to','job_no','bill_to_address').filter(is_einvoiced=True).filter(is_cancel=False).filter(is_deleted=False).filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).filter(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum('gross_amount'),net_amount=Sum('net_amount'))
        
        non_inr_crn = CreditNote.objects.select_related('company_type','bill_to','job_no','bill_to_address').filter(is_einvoiced=True).filter(is_cancel=False).filter(is_deleted=False).filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).exclude(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum(F('gross_amount')*F('currency_ex_rate')),net_amount=Sum(F('gross_amount')*F('currency_ex_rate')))
        
        inr_purchase = InvoicePayable.objects.select_related('company_type','bill_from','job_no','bill_from_address').filter(is_deleted=False).filter(date_of_invoice__gte=from_date).filter(date_of_invoice__lte=to_date).filter(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum('gross_amount'),net_amount=Sum('net_amount'))
        
        non_inr_purchase = InvoicePayable.objects.select_related('company_type','bill_from','job_no','bill_from_address').filter(is_deleted=False).filter(date_of_invoice__gte=from_date).filter(date_of_invoice__lte=to_date).exclude(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum(F('gross_amount')*F('currency_ex_rate')),net_amount=Sum(F('gross_amount')*F('currency_ex_rate')))
        
        inr_indirect_expense = IndirectExpense.objects.select_related('company_type','vendor','invoice_currency').filter(is_deleted=False).filter(bill_date__gte=from_date).filter(bill_date__lte=to_date).filter(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum('gross_amount'),net_amount=Sum('net_amount'))
        
        non_inr_indirect_expense = IndirectExpense.objects.select_related('company_type','vendor','job_no','invoice_currency').filter(is_deleted=False).filter(bill_date__gte=from_date).filter(bill_date__lte=to_date).exclude(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum(F('gross_amount')*F('currency_ex_rate')),net_amount=Sum(F('gross_amount')*F('currency_ex_rate')))
        
        inr_drn = DebitNote.objects.select_related('company_type','bill_from','job_no','bill_from_address').filter(is_deleted=False).filter(date_of_note__gte=from_date).filter(date_of_note__lte=to_date).filter(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum('gross_amount'),net_amount=Sum('net_amount'))
        
        non_inr_drn = DebitNote.objects.select_related('company_type','bill_from','job_no','bill_from_address').filter(is_deleted=False).filter(date_of_note__gte=from_date).filter(date_of_note__lte=to_date).exclude(invoice_currency__short_name="INR").values("job_no__account_manager").annotate(gross_sum=Sum(F('gross_amount')*F('currency_ex_rate')),net_amount=Sum(F('gross_amount')*F('currency_ex_rate')))
        
        sale_persons = Employee.objects.filter(Q(role__name__contains="SALE") | Q(department__name__contains ="SALE")).all()
        report = []
        for i in sale_persons:
            print(i)
            gross_profit = 0
            net_profit = 0
            report_data = {
                'person':i,
                'sales':{'gross':0,'net':0},
                'sales_return':{'gross':0,'net':0},
                'purchase':{'gross':0,'net':0},
                'expense':{'gross':0,'net':0},
                'purchase_return':{'gross':0,'net':0},
                'profit':{'gross':0,'net':0},
                'total_container':{'count':0,'details':[]},
            }
            net_sum = 0
            gross_sum = 0
            inr_invoice_ = list(filter(lambda inr_invoice: inr_invoice['job_no__account_manager'] == i.id, inr_invoice))
            non_inr_invoice_ = list(filter(lambda non_inr_invoice: non_inr_invoice['job_no__account_manager'] == i.id, non_inr_invoice))
            all_invoice_rec = inr_invoice_ + non_inr_invoice_
            print(all_invoice_rec)
            for invoice in all_invoice_rec:
                try:
                    gross_sum += invoice['gross_sum']
                    net_sum += invoice['net_amount']
                    gross_profit += invoice['gross_sum']
                    net_profit += invoice['net_amount']
                except:
                    pass
            
            report_data['sales']['gross'] = gross_sum
            report_data['sales']['net'] = net_sum
            print("Sales Gross - ",gross_sum)
            
            net_sum = 0
            gross_sum = 0
            inr_crn_ = list(filter(lambda inr_crn: inr_crn['job_no__account_manager'] == i.id, inr_crn))
            non_inr_crn_ = list(filter(lambda non_inr_crn: non_inr_crn['job_no__account_manager'] == i.id, non_inr_crn))
            all_sale_return = inr_crn_ + non_inr_crn_
            for invoice in all_sale_return:
                try:
                    gross_sum += invoice['gross_sum']
                    net_sum += invoice['net_amount']
                    gross_profit -= invoice['gross_sum']
                    net_profit -= invoice['net_amount']
                except:
                    pass
            
            report_data['sales_return']['gross'] = gross_sum
            report_data['sales_return']['net'] = net_sum
            
            net_sum = 0
            gross_sum = 0
            inr_purchase_ = list(filter(lambda inr_purchase: inr_purchase['job_no__account_manager'] == i.id, inr_purchase))
            non_inr_purchase_ = list(filter(lambda non_inr_purchase: non_inr_purchase['job_no__account_manager'] == i.id, non_inr_purchase))
            all_purchase = inr_purchase_ + non_inr_purchase_
            for invoice in all_purchase:
                try:
                    gross_sum += invoice['gross_sum']
                    net_sum += invoice['net_amount']
                    gross_profit -= invoice['gross_sum']
                    net_profit -= invoice['net_amount']
                except:
                    pass
            
            report_data['purchase']['gross'] = gross_sum
            report_data['purchase']['net'] = net_sum
            
            
            net_sum = 0
            gross_sum = 0
            inr_drn_ = list(filter(lambda inr_drn: inr_drn['job_no__account_manager'] == i.id, inr_drn))
            non_inr_drn_ = list(filter(lambda non_inr_drn: non_inr_drn['job_no__account_manager'] == i.id, non_inr_drn))
            all_purchase_return = inr_drn_ + non_inr_drn_
            for invoice in all_purchase_return:
                try:
                    gross_sum += invoice['gross_sum']
                    net_sum += invoice['net_amount']
                    
                    gross_profit += invoice['gross_sum']
                    net_profit += invoice['net_amount']
                except:
                    pass
            
            report_data['purchase_return']['gross'] = gross_sum
            report_data['purchase_return']['net'] = net_sum
           
            count = 0
            details = []
            container_count_ = list(filter(lambda container_count: container_count['job__account_manager'] == i.id, container_count))
            for invoice in container_count_:
                try:
                    count += invoice['count']
                    details.append({'container_type':invoice['container_type'],'count':invoice['count']})
                    
                except:
                    pass
            
            report_data['total_container']['count'] = count
            report_data['total_container']['details'] = details
           
            net_sum = 0
            gross_sum = 0
            inr_indirect_expense = list(filter(lambda inr_indirect_expense: inr_indirect_expense['job_no__account_manager'] == i.id, inr_indirect_expense))
            non_inr_indirect_expense = list(filter(lambda non_inr_indirect_expense: non_inr_indirect_expense['job_no__account_manager'] == i.id, non_inr_indirect_expense))
            all_inndirect_exp = inr_indirect_expense + non_inr_indirect_expense
            for invoice in all_inndirect_exp:
                try:
                    gross_sum += invoice['gross_sum']
                    net_sum += invoice['net_amount']
                    gross_profit -= invoice['gross_sum']
                    net_profit -= invoice['net_amount']
                except:
                    pass
            
            report_data['expense']['gross'] = gross_sum
            report_data['expense']['net'] = net_sum
            
            report_data['profit']['gross'] = gross_profit
            report_data['profit']['net'] = net_profit
            
            report.append(report_data)
        
        # none_data = [{"id":None}]
        # for i in none_data:
        #     gross_profit = 0
        #     net_profit = 0
        #     report_data = {
        #         'person':i,
        #         'sales':{'gross':0,'net':0},
        #         'sales_return':{'gross':0,'net':0},
        #         'purchase':{'gross':0,'net':0},
        #         'expense':{'gross':0,'net':0},
        #         'purchase_return':{'gross':0,'net':0},
        #         'profit':{'gross':0,'net':0}
        #     }
        #     net_sum = 0
        #     gross_sum = 0
        #     inr_invoice = list(filter(lambda inr_invoice: inr_invoice['job_no__account_manager'] == i.id, inr_invoice))
        #     non_inr_invoice = list(filter(lambda non_inr_invoice: non_inr_invoice['job_no__account_manager'] == i.id, non_inr_invoice))
        #     all_invoice_rec = inr_invoice + non_inr_invoice
        #     for invoice in all_invoice_rec:
        #         try:
        #             gross_sum += invoice['gross_sum']
        #             net_sum += invoice['net_amount']
        #             gross_profit += invoice['gross_profit']
        #             net_profit += invoice['net_profit']
        #         except:
        #             pass
            
        #     report_data['sales']['gross'] = gross_sum
        #     report_data['sales']['net'] = net_sum
            
        #     net_sum = 0
        #     gross_sum = 0
        #     inr_crn = list(filter(lambda inr_crn: inr_crn['job_no__account_manager'] == i.id, inr_crn))
        #     non_inr_crn = list(filter(lambda non_inr_crn: non_inr_crn['job_no__account_manager'] == i.id, non_inr_crn))
        #     all_sale_return = inr_crn + non_inr_crn
        #     for invoice in all_sale_return:
        #         try:
        #             gross_sum += invoice['gross_sum']
        #             net_sum += invoice['net_amount']
        #             gross_profit -= invoice['gross_sum']
        #             net_profit -= invoice['net_amount']
        #         except:
        #             pass
            

            
        context['report'] = report
        context['from_date'] = from_date
        context['to_date'] = to_date
        context['company'] = company
        
    
        
    context['module'] = module
    return render(request,'report/sale_person_performance_sheet/sale_person_report.html',context)
    
@login_required(login_url='home:handle_login')
def job_cost_sheet_pdf(request,id):
    template_path = 'report/job_cost_sheet/pdf2.html'
    
    domain = Site.objects.get_current().domain
    job = JobMaster.objects.filter(id=int(id)).first()
    invoice_rec = InvoiceReceivable.objects.prefetch_related('recievable_invoice_reference','recievable_invoice_reference__billing_head').filter(job_no__id=id).filter(is_deleted=False).all()
    invoice_rec_gross = invoice_rec.aggregate(sum=Sum('gross_amount'))
    invoice_rec_net = invoice_rec.aggregate(sum=Sum('net_amount'))
    
    invoice_rec_gst_amount = invoice_rec.aggregate(sum=Sum('gst_amount'))
    invoice_pay = InvoicePayable.objects.prefetch_related('payable_invoice_reference','payable_invoice_reference__billing_head').filter(job_no__id=id).filter(is_deleted=False).all()
    invoice_pay_net = invoice_pay.aggregate(sum=Sum('net_amount'))
    if not invoice_pay_net['sum']:
        invoice_pay_net['sum'] = 0

    invoice_crn = CreditNote.objects.filter(job_no__id=id).filter(is_deleted=False).all()
    invoice_crn_net = invoice_crn.aggregate(sum=Sum('gross_amount'))
    if not invoice_crn_net['sum']:
        invoice_crn_net['sum'] = 0

    invoice_drn = DebitNote.objects.filter(job_no__id=id).filter(is_deleted=False).all()
    invoice_drn_net = invoice_drn.aggregate(sum=Sum('gross_amount'))
    if not invoice_drn_net['sum']:
        invoice_drn_net['sum'] = 0
    invoice_pay_gst = invoice_pay.aggregate(sum=Sum('gst_amount'))
    if not invoice_pay_gst['sum']:
        invoice_pay_gst['sum'] = 0
    invoice_pay_gross = invoice_pay.aggregate(sum=Sum('gross_amount'))
    if not invoice_pay_gross['sum']:
        invoice_pay_gross['sum'] = 0

    if invoice_rec_net['sum']:    
        invoice_rec_net = round(invoice_rec_net['sum'],2)
    else:
        invoice_rec_net = 0
   
    if invoice_rec_gross['sum']:    
        invoice_rec_gross = round(invoice_rec_gross['sum'],2)
    else:
        invoice_rec_net = 0
   
    if invoice_rec_gst_amount['sum']:    
        invoice_rec_gst_amount = round(invoice_rec_gst_amount['sum'],2)
    else:
        invoice_rec_gst_amount = 0

    billing_head_summary = []
    hsn = []
    net_wot_sales = 0
    net_wt_sales = 0
    net_wot_purchase = 0
    net_wt_purchase = 0
    for invoice in invoice_rec:
        for i in invoice.recievable_invoice_reference.all():
            if not i.billing_head in hsn:
                hsn.append(i.billing_head)
                obj = {
                    'billing_head':i.billing_head,
                    'ex_rate':i.ex_rate,
                    'sale_qty':i.qty_unit,
                    'sale_rate':i.rate,
                    'pay_rate':0,
                    'pay_qty':0,
                    'pay_amount':0,
                    'sale_amount':i.amount,
                    'net_amount':i.amount,
                    'pay_gst_amount':0,
                    'sale_gst_amount':i.gst_amount,
                    'pay_total':0,
                    'sale_total':i.total,
                    'net_total':i.total,
                }
                net_wot_sales += i.amount
                net_wt_sales += i.total
                billing_head_summary.append(obj)
            
            else:
                for j in billing_head_summary:
                    if i.billing_head == j['billing_head']:
                        j['sale_qty'] += i.qty_unit
                
                        j['sale_amount'] += i.amount
                        j['net_amount'] += i.amount
                        j['sale_gst_amount'] += i.gst_amount
                        j['sale_total'] += i.total
                        j['net_total'] += i.total

                        net_wot_sales += i.amount
                        net_wt_sales += i.total

    for invoice in invoice_pay:
        for i in invoice.payable_invoice_reference.all():
            if not i.billing_head in hsn:
                hsn.append(i.billing_head)
                obj = {
                    'billing_head':i.billing_head,
                    'ex_rate':i.ex_rate,
                    'pay_qty':i.qty_unit,
                    'sale_qty':0,
                    'sale_rate':0,
                    'pay_rate':i.rate,
                    'sale_amount':0,
                    'pay_amount':i.amount,
                    'net_amount':i.amount,
                    'sale_gst_amount':0,
                    'pay_gst_amount':i.gst_amount,
                    'sale_total':0,
                    'pay_total':i.total,
                    'net_total':i.total,
                }
                net_wot_purchase += i.amount
                net_wt_purchase += i.total
                billing_head_summary.append(obj)
            
            else:
                for j in billing_head_summary:
                    if i.billing_head == j['billing_head']:
                        j['pay_qty'] += i.qty_unit
                        j['pay_amount'] += i.amount
                        j['net_amount'] -= i.amount
                        j['pay_gst_amount'] += i.gst_amount
                        j['pay_total'] += i.total
                        j['net_total'] -= i.total
                        j['pay_rate'] = i.rate

                        net_wot_purchase += i.amount
                        net_wt_purchase += i.total


    

    invoice_pay_net = round(invoice_pay_net['sum'],2)
    invoice_pay_gst = round(invoice_pay_gst['sum'],2)
    invoice_pay_gross = round(invoice_pay_gross['sum'],2)
    invoice_crn_net = round(invoice_crn_net['sum'],2)
    invoice_drn_net = round(invoice_drn_net['sum'],2)
    job_costing_amount = invoice_rec_gross - invoice_pay_gross - invoice_crn_net + invoice_drn_net
    context = {
        'job':job,
        'data':job.recievable_invoice_job.first(),
        'invoice_rec_net':invoice_rec_net,
        'invoice_rec_gross':invoice_rec_gross,
        'invoice_rec_gst_amount':invoice_rec_gst_amount,
        'invoice_pay_net':invoice_pay_net,
        'invoice_pay_gst':invoice_pay_gst,
        'invoice_pay_gross':invoice_pay_gross,
        'invoice_crn_net':invoice_crn_net,
        'invoice_drn_net':invoice_drn_net,
        'job_costing_amount':job_costing_amount,
        'recievable_invoices':InvoiceReceivable.objects.filter(job_no__id=id).filter(is_deleted=False).all(),
        'payable_invoices':InvoicePayable.objects.filter(job_no__id=id).filter(is_deleted=False).all(),
        'billing_head_summary' : billing_head_summary,
        'net_wot_sales' : net_wot_sales,
        'net_wt_sales' : net_wt_sales,
        
        'net_wot_purchase' : net_wot_purchase,
        'net_wt_purchase' : net_wt_purchase,
        'domain':domain
        
    }
    return generate_pdf(request,template_path,context)
   
@login_required(login_url='home:handle_login')
def sale_purchase_profit_loss(request,module):
    context ={}
    check_permissions(request,module)
    purch_finalize_bill = 'A'
    finalize_bill = 'A'
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        finalize_bill = request.POST['finalize_bill']
        purch_finalize_bill = request.POST['purch_finalize_bill']
        job_type = request.POST['job_type']
        location = request.POST['location']
       
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)
        invoices = InvoiceReceivable.objects.filter(is_deleted=False).filter(old_invoice=False).filter(Q(date_of_invoice__range=[from_date,from_to_date]) | Q(einvoice_date__range=[from_date,to_date])).select_related('bill_to','job_no','company_type','invoice_currency').all()

        purchase_invoices = InvoicePayable.objects.filter(is_deleted=False).filter(date_of_invoice__range=[from_date,to_date]).select_related('bill_from','job_no','company_type','invoice_currency').all()

        indirect_expense = IndirectExpense.objects.filter(is_deleted=False).filter(bill_date__range=[from_date,to_date]).select_related('vendor','job_no','company_type','invoice_currency').all()

        if purch_finalize_bill == "F":
            purchase_invoices = purchase_invoices.filter(is_approved=True).all()
        
        if purch_finalize_bill == "U":
            purchase_invoices = purchase_invoices.filter(is_approved=False).all()


        if finalize_bill == "F":
            invoices = invoices.filter(is_einvoiced=True).filter(einvoice_date__range=[from_date,to_date]).all()
            
        if finalize_bill == "U":
            invoices = invoices.filter(is_einvoiced=False).filter(date_of_invoice__range=[from_date,to_date]).all()

        if not job_type == "A":
            invoices = invoices.filter(job_no__module = job_type).all()
            purchase_invoices = purchase_invoices.filter(job_no__module = job_type).all()
            indirect_expense = indirect_expense.filter(job_no__module = job_type).all()

        if not location == "A":
            location = int(location)
            invoices = invoices.filter(company_type__id = int(location)).all()
            purchase_invoices = purchase_invoices.filter(company_type__id = int(location)).all()
            indirect_expense = indirect_expense.filter(company_type__id = int(location)).all()

      
        context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
        context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()
        context['finalize_bill'] = finalize_bill
        context['purch_finalize_bill'] = purch_finalize_bill
        context['job_type'] = job_type
        context['location'] = location
        
        context['invoices'] = invoices
        context['purchase_invoices'] = purchase_invoices
        context['indirect_expense'] = indirect_expense


    context['module']= module
    return render(request,'report/register/sales_purchase_profit_loss.html',context)

import datetime as dtime


# Party Ledger
@login_required(login_url='home:handle_login')
def PartyLedger(request,module,generate_report_pdf=0):
    context ={}
    include_options = ['Sales', 'CRN', 'Purchase', 'DRN', 'Trailor', 'Journal', 'Payment', 'Receipt']
    include = ['Sales', 'CRN', 'Purchase', 'DRN', 'Trailor', 'Journal', 'Payment', 'Receipt']
    context['include_options'] = include_options
    context['include'] = include
    check_permissions(request,module)
    
    current_year = datetime.now().year
    to_current_year = datetime.now().year + 1
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
        to_current_year -= 1

    from_date = dtime.date(current_year, 4, 1)
    to_date = dtime.date.today()
    

    opening_balance = 0
    p_opening_balance = 0
    total_rec = 0
    total_pay = 0
    total_rec_vou = 0
    total_pay_vou = 0
    round_off = "Y"
    show_details = "N"
    ledger_name = ""
    region = request.user.user_account.office.region

    if request.method == "POST":
        if generate_report_pdf == 1:
            choose_company = request.POST['choose_company_pdf']
            selected_region = request.POST['region_pdf']
            from_date = request.POST['from_date_pdf']
            ledger = request.POST['ledger_pdf'].split('_')
            to_date = request.POST['to_date_pdf']
            round_off = request.POST['round_off_pdf']
            show_details = request.POST['show_details_pdf']
            context['selected_ledger'] =  request.POST['ledger_pdf']
            context['company_name'] =  Logistic.objects.first().company_name
        else:
            selected_region = request.POST['region']
            selected_module = request.POST['selected_module']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            choose_company = request.POST['choose_company']
            include = request.POST.getlist('include')
            ledger = request.POST['ledger'].split('_')
            round_off = request.POST['round_off']
            show_details = request.POST['show_details']

            context['selected_ledger'] = request.POST['ledger']


        ledger_type = ledger[0]
        ledger_id = int(ledger[1])

        party = None
        vendor = None
        ledger = None

        credit_balance = 0
        debit_balance = 0
        
        
        if ledger_type == "V":
            vendor = Vendor.objects.filter(id=ledger_id).first()
            ledger_name = vendor.vendor_name
            if vendor.opening_in == "Debit":
                opening_balance += vendor.opening_balance
                debit_balance += vendor.opening_balance
            else:
                opening_balance -= vendor.opening_balance
                credit_balance += vendor.opening_balance

            context['vendor'] = vendor
            context['party_name'] = vendor.vendor_name

        if ledger_type == "P":
            party = Party.objects.filter(id=ledger_id).first()
            ledger_name = party.party_name
            context['party'] = party
            context['party_name'] = party.party_name

            if party.opening_in == "Debit":
                opening_balance += party.opening_balance
                debit_balance += party.opening_balance
            else:
                opening_balance -= party.opening_balance
                credit_balance += party.opening_balance

            
        if ledger_type == "L":
            ledger = LedgerMaster.objects.filter(id=ledger_id).first()
            ledger_name = ledger.ledger_name
            context['ledger'] = ledger
            context['party_name'] = ledger.ledger_name

            if ledger.balance_in == "Debit":
                opening_balance += ledger.opening_balance
                debit_balance += ledger.opening_balance
            else:
                opening_balance -= ledger.opening_balance
                credit_balance += ledger.opening_balance

        
        report = []
        opening_invoices_rec = []
        invoices_rec = []
        opening_credit_notes = []
        credit_notes = []
        opening_invoices_pay = []
        invoices_pay = []
        opening_rec_voucher = []
        rec_voucher = []
        opening_pay_voucher = []
        pay_voucher = []
        opening_debit_note = []
        debit_note = []
        opening_trailor_expense = []
        trailor_expense = []
        opening_journals = []
        journals = []

        region_filter = {'company_type__region': selected_region}
        date_filter = {'gte': from_date, 'lte': to_date}
        opening_date_filter = {'lt': from_date}
        company = None
        if choose_company != "All":
            company = Logistic.objects.filter(id=int(choose_company)).first()
            company_filter = {'company_type__id': company.id}
            journal_company_filter = {'voucher__company_type__id': company.id}
            trailor_company_filter = {'expense__company_type__id': company.id}
        else:
            company_filter = {}
            journal_company_filter = {}
            trailor_company_filter = {}

        # Journal
        journals_queryset = JournalEntry.objects.filter(
            voucher__company_type__region=selected_region,
            **journal_company_filter
        )

        # Purchase Invoice
        purchase_invoice_queryset = InvoicePayable.objects.select_related(
            'bill_from', 'company_type', 'bill_from_address', 'invoice_currency', 'job_no'
        ).prefetch_related(
            'payable_invoice_reference', 'payable_invoice_reference__billing_head'
        ).filter(
            
            is_deleted=False,
            old_invoice=False,
            
            **region_filter,
            **company_filter
        )
    
        # Debit Note
        debit_note_queryset = DebitNote.objects.select_related(
            'bill_from', 'company_type', 'bill_from_address', 'invoice_currency'
        ).prefetch_related(
            'debit_note_reference', 'debit_note_reference__billing_head'
        ).filter(
            is_deleted=False,
            **region_filter,
            **company_filter
        )

        # Receipt Voucher
        receipt_voucher_queryset = RecieptVoucher.objects.select_related(
            'company_type', 'voucher', 'bank', 'cash'
        ).prefetch_related(
            'rec_voucher_detail','rec_voucher_detail__party', 'rec_voucher_detail__invoice', 'rec_voucher_detail__voucher'
        ).filter(
            old_voucher=False,
            **region_filter,
            **company_filter
        )

        # Payment Voucher
        payment_voucher_queryset = PaymentVoucher.objects.select_related(
            'party_name', 'company_type', 'party_address', 'voucher', 'from_bank', 'voucher__from_bank'
        ).filter(
            **region_filter,
            **company_filter
        )
    
        # Trailor Expense
        trailor_expense_queryset = TrailorExpenseDetail.objects.select_related(
            'expense__job_no', 'expense__trailor_no', 'expense__company_type','party','invoice'
        ).filter(
            expense__company_type__region=selected_region,
            **trailor_company_filter
        )

        # Sales Invoice
        sales_invoices_queryset = InvoiceReceivable.objects.select_related(
            'bill_to', 'company_type', 'bill_to_address', 'invoice_currency', 'job_no'
        ).prefetch_related(
            'reciept_rec_inv', 'reciept_rec_inv__voucher', 'recievable_invoice_reference', 'recievable_invoice_reference__billing_head'
        ).filter(
            
            is_einvoiced=True,
            old_invoice=False
        ).filter(
            Q(is_deleted=False) | Q(is_cancel=False),
            
            **region_filter,
            **company_filter
        )

        # Credit Notes
        credit_note_queryset = CreditNote.objects.select_related(
            'bill_to', 'company_type', 'bill_to_address', 'invoice_currency', 'job_no', 'reference_invoice'
        ).prefetch_related(
            'credit_note_reference', 'credit_note_reference__billing_head'
        ).filter(
            is_einvoiced=True,
            is_deleted=False,
            is_cancel=False,
            **region_filter,
            **company_filter
        )
        
        
        if ledger_type == "P":
            trailor_expense_queryset = trailor_expense_queryset.filter(party=party)
            journals_queryset = journals_queryset.filter(party=party)
            sales_invoices_queryset = sales_invoices_queryset.filter(bill_to__id=party.id)
            credit_note_queryset = credit_note_queryset.filter(bill_to__id=party.id)
            purchase_invoice_queryset = purchase_invoice_queryset.filter(bill_from__id=party.id)
            debit_note_queryset = debit_note_queryset.filter(bill_from__id=party.id)
            receipt_voucher_queryset = receipt_voucher_queryset.filter(rec_voucher_detail__party__id=party.id)
            payment_voucher_queryset = payment_voucher_queryset.filter(pay_voucher_detail__party__id=party.id)
        
        if ledger_type == "V":
            trailor_expense_queryset = trailor_expense_queryset.filter(vendor=vendor)
            journals_queryset = journals_queryset.filter(vendor=vendor)
            purchase_invoice_queryset = purchase_invoice_queryset.filter(vendor__id=vendor.id)
            debit_note_queryset = debit_note_queryset.filter(bill_from_vendor__id=vendor.id)
            receipt_voucher_queryset = receipt_voucher_queryset.filter(rec_voucher_detail__vendor__id=vendor.id)
            payment_voucher_queryset = payment_voucher_queryset.filter(pay_voucher_detail__vendor__id=vendor.id)
        
        if ledger_type == "L":
            journals_queryset = journals_queryset.filter(ledger=ledger)
            receipt_voucher_queryset = receipt_voucher_queryset.filter(rec_voucher_detail__ledger__id=ledger.id)
            payment_voucher_queryset = payment_voucher_queryset.filter(pay_voucher_detail__ledger__id=ledger.id)
        
        # Current Date Range
        journals = journals_queryset.filter(voucher__date__range=(from_date, to_date))
        invoices_rec = sales_invoices_queryset.filter(einvoice_date__range=(from_date, to_date))
        invoices_pay = purchase_invoice_queryset.filter(date_of_invoice__range=(from_date, to_date))
        credit_notes = credit_note_queryset.filter(einvoice_date__range=(from_date, to_date))
        debit_note = debit_note_queryset.filter(date_of_note__range=(from_date, to_date))
        rec_voucher = receipt_voucher_queryset.filter(voucher_date__range=(from_date, to_date))
        pay_voucher = payment_voucher_queryset.filter(voucher_date__range=(from_date, to_date))
        trailor_expense = trailor_expense_queryset.filter(date__range=(from_date, to_date))

        # Opening
        opening_journals = journals_queryset.filter(voucher__date__lt=from_date)
        opening_invoices_rec = sales_invoices_queryset.filter(einvoice_date__lte=from_date)
        opening_invoices_pay = purchase_invoice_queryset.filter(date_of_invoice__lt=from_date)
        opening_credit_notes = credit_note_queryset.filter(einvoice_date__lte=from_date)
        opening_debit_note = debit_note_queryset.filter(date_of_note__lt=from_date)
        opening_rec_voucher = receipt_voucher_queryset.filter(voucher_date__lt=from_date)
        opening_pay_voucher = payment_voucher_queryset.filter(voucher_date__lt=from_date)
        opening_trailor_expense = trailor_expense_queryset.filter(date__lt=from_date)



        

        if ledger_type == "L":
            invoices_pay = []
            opening_invoices_pay = []
        
            debit_note = []
            opening_debit_note = []

            invoices_rec = []
            opening_invoices_rec = []
        
            credit_notes = []
            opening_credit_notes = []

        if ledger_type == "V":
            invoices_rec = []
            opening_invoices_rec = []
        
            credit_notes = []
            opening_credit_notes = []
        
        if not "Journal" in include:
            journals = []
            opening_journals = []
       
        if not "Sales" in include:
            invoices_rec = []
            opening_invoices_rec = []
        
        if not "CRN" in include:
            credit_notes = []
            opening_credit_notes = []
        
        if not "DRN" in include:
            debit_note = []
            opening_debit_note = []
        
        if not "Purchase" in include:
            invoices_pay = []
            opening_invoices_pay = []
        
        if not "Receipt" in include:
            rec_voucher = []
            opening_rec_voucher = []
        
        if not "Payment" in include:
            pay_voucher = []
            opening_pay_voucher = []
        
        if not "Trailor" in include:
            trailor_expense = []
            opening_trailor_expense = []
            
        # Journals
        for i in opening_journals:
            if i.dr_cr == "Debit":
                debit_balance += (i.amount)
                opening_balance += (i.amount)
            else:
                opening_balance -= (i.amount)
                credit_balance += (i.amount)



            
                

        for i in journals:
            invoice_no = i.particular
            dr_amount = 0
            cr_amount = 0
            to_by = "To"
            if i.dr_cr == "Debit":
                to_by = "TO"
                debit_balance += (i.amount)
                dr_amount = (i.amount)
            else:
                to_by = "BY"
                cr_amount = (i.amount)
                credit_balance += (i.amount)

            if i.voucher.date:
                report.append({
                    'date':i.voucher.date,
                    'invoice_no':f"Journal",
                    'by_to':to_by,
                    'voucher_no':"",
                    'url':reverse('accounting:journal_update',kwargs={'module':module,'id':i.voucher.id}),
                    'particulars':f"{invoice_no}",
                    'cr_amount':cr_amount ,
                    'dr_amount':dr_amount,
                    'tds_rec':0,
                    'tds_pay':0,
                    'adjustment':0,
                    'remarks':f'{i.voucher.description}',
                })

        receipts = []
        # Sales Invoices
        for i in opening_invoices_rec:
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR":
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass
                
            total_rec += i.net_amount * currency_ex_rate
            
                
            opening_balance += (i.net_amount * currency_ex_rate)
            debit_balance += (i.net_amount * currency_ex_rate)
            
            for j in i.reciept_rec_inv.all():
                opening_balance -= ( j.tds_amount + j.adjustment_amount)
                credit_balance += ( j.tds_amount + j.adjustment_amount)
                
        for i in invoices_rec:
            currency_ex_rate = 1
            job_no = ""
            bl_no = ""
            if i.job_no:
                job_no = i.job_no
                bl_no = i.job_no.booking_no

            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR":
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass
                
            total_rec += i.net_amount * currency_ex_rate
            invoice_no = i.final_invoice_no
            if not invoice_no:
                invoice_no = i.invoice_no
            
            if i.einvoice_date:
                einvoice_date = i.einvoice_date.date() 
            else:
                einvoice_date = i.date_of_invoice
        
                
            debit_balance += (i.net_amount * currency_ex_rate)
            report.append({
                'date':einvoice_date,
                'particulars':"SALES INVOICE",
                'by_to':"TO",
                'url':reverse('accounting:recievable_invoice_pdf',kwargs={'id':i.id}),
                'invoice_no':f"{invoice_no}",
                'voucher_no':"",
                'bl_no':bl_no,
                'dr_amount':i.net_amount * currency_ex_rate,
                'cr_amount':0,
                'tds_rec':0,
                'tds_pay':0,
                'adjustment':0,
                'remarks':f'JOB NO. = {job_no}'
            })
            
            for j in i.recievable_invoice_reference.all():
                report.append({
                    'date':einvoice_date,
                    'invoice_no':f"",
                    'particulars':f"{j.billing_head.billing_head}",
                    'by_to':"",
                    'voucher_no':"",
                    'dr_amount':0,
                    'cr_amount':0,
                    'tds_rec':0,
                    'bl_no':bl_no,
                    'tds_pay':0,
                    'adjustment':0,
                    'remarks':f'Amount - {j.total}',
                    'color':'#d3e0b4'
                })
                
                
            for j in i.reciept_rec_inv.all():
            
                credit_balance += (  j.adjustment_amount)
               
                if j.adjustment_amount > 0:
                    report.append({
                        'date':j.voucher.voucher_date,
                        'invoice_no':invoice_no,
                        'particulars':f"Adjusted Amount",
                        'by_to':"BY",
                        'voucher_no':f"{j.voucher.voucher_no}",
                        'dr_amount':0,
                        'bl_no':bl_no,
                        'cr_amount':j.adjustment_amount,
                        'tds_rec':j.tds_amount,
                        'tds_pay':0,
                        'adjustment':j.adjustment_amount,
                        'remarks':"",
                        'color':'#c6e0b4'
                    })
           
        # Credit Notes
        for i in opening_credit_notes:
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR":
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass
            
            total_rec_vou += i.net_amount * currency_ex_rate
            credit_balance += (i.net_amount * currency_ex_rate)  
            opening_balance -= (i.net_amount * currency_ex_rate)

        for i in credit_notes:
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR":
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass
            
            total_rec_vou += i.net_amount * currency_ex_rate
            credit_note_no = i.final_invoice_no
            if not credit_note_no:
                credit_note_no = i.final_invoice_no
            
            
            if i.einvoice_date:
                einvoice_date = i.einvoice_date.date() 
            else:
                einvoice_date = i.date_of_invoice
                
            credit_balance += (i.net_amount * currency_ex_rate)  
            job_no = ""
            bl_no = ""
            if i.job_no:
                job_no = i.job_no 
                bl_no = i.job_no.booking_no 
            report.append({
                'date':einvoice_date,
                'invoice_no':f"{credit_note_no} - (#{i.invoice_no})",
                'particulars':"CREDIT NOTE",
                'by_to':"BY",
                'url':reverse('accounting:credit_note_pdf',kwargs={'id':i.id}),
                'bl_no':bl_no,
                'voucher_no':"",
                'dr_amount':0,
                'cr_amount':i.net_amount * currency_ex_rate,
                'tds_rec':0,
                'tds_pay':0,
                'adjustment':0,
                'remarks':f'JOB NO. = {job_no}',
            })
            
            for j in i.credit_note_reference.all():
                report.append({
                    'date':einvoice_date,
                    'invoice_no':f"",
                    'particulars':f"{j.billing_head.billing_head}",
                    'by_to':"",
                    'bl_no':bl_no,
                    'voucher_no':"",
                    'dr_amount':0,
                    'cr_amount':0,
                    'tds_rec':0,
                    'tds_pay':0,
                    'adjustment':0,
                    'remarks':f'Amount - {j.total}',
                    'color':'#d3e0b4'
                })
                
         
        opening_bills = []          
        for i in opening_rec_voucher:
            if not i.id in opening_bills:
                opening_bills.append(i.id)
                total_recieved_amount = 0
                
                if i.advance_amount:
                    opening_balance -= i.net_amount
                    credit_balance += i.net_amount
                   

        # Receipt Voucher
        for i in rec_voucher:
            if not i.id in receipts:
                receipts.append(i.id)
                total_recieved_amount = 0
                recieve_in = "BANK"
                instrument_no = ""
                head_particular = "HEAD"
                
                if i.recieve_in == "CASH":
                    recieve_in = "CASH"
                    instrument_no = i.instrument_no
                    head_particular = f"{i.cash.branch_name}"

                if recieve_in == "BANK":
                    if i.bank:
                        instrument_no = i.instrument_no
                        head_particular = f"{i.bank.bank_name}_{i.bank.account_no}" 

                try:
                    instrument_no = i.instrument_no
                    head_particular = f"{i.bank.bank_name}_{i.bank.account_no}" 
                except:
                    pass

                
                head_reciept = {
                    'date':i.voucher_date,
                    'invoice_no':"",
                    'by_to':"BY",
                    'url':reverse('accounting:reciept_voucher_update',kwargs={'module':module,'id':i.id}),
                    'particulars':head_particular,
                    'voucher_no':f'{i.narration}',
                    'dr_amount':0,
                    'cr_amount':0,
                    'tds_rec':0,
                    'tds_pay':0,
                    'adjustment':0,
                    'remarks' : f'{instrument_no}',
                    'adjustments':[]
                    
                }
                voucher = i
                head_amount = 0
                for j in i.rec_voucher_detail.all():



                    if j.payment_type == "OAC":
                        particulars = f'On A/C'
                    else:
                        particulars = f'Agst Ref.'

                    invoice_no = ""
                    bl_no = ""
                    if j.invoice:
                        currency_ex_rate = 1
                        try:
                            if j.invoice.invoice_currency.short_name != 'INR':
                                currency_ex_rate = j.invoice.currency_ex_rate
                        except:
                            pass
                        
                        invoice_no = j.invoice.final_invoice_no
                        try:
                            bl_no = j.invoice.job_no.booking_no
                        except:
                            pass
                      
                    if j.received_amount > 0:
                        head_amount +=  (j.received_amount * currency_ex_rate)
                        credit_balance += ( j.received_amount * currency_ex_rate)
                        head_reciept['cr_amount'] += (j.received_amount * currency_ex_rate)
                        
                        head_reciept['adjustments'].append({
                            'date':voucher.voucher_date,
                            'invoice_no':invoice_no,
                            'particulars':particulars,
                            'bl_no':bl_no,
                            'by_to':"BY",
                            'voucher_no':f"{voucher.voucher_no}",
                            'dr_amount':0,
                            'cr_amount':j.received_amount * currency_ex_rate,
                            'tds_rec':0,
                            'tds_pay':0,
                            'adjustment':0,
                            'remarks':f"{voucher.instrument_no}",
                            'color':'#c6e0b4'
                        })
                    
                    if j.tds_amount > 0:
                        credit_balance += ( j.tds_amount * currency_ex_rate)
                        report.append({
                            'date':voucher.voucher_date,
                            'invoice_no':j.invoice and j.invoice.final_invoice_no or None,
                            'particulars':f"TDS Recievable",
                            'by_to':"BY",
                            'bl_no':bl_no,
                            'voucher_no':f"{voucher.voucher_no}",
                            'dr_amount':0,
                            'cr_amount':j.tds_amount * currency_ex_rate,
                            'tds_rec':j.tds_amount * currency_ex_rate,
                            'tds_pay':0,
                            'adjustment':0,
                            'remarks':"",
                            'color':'#c6e0b4'
                        })
                    
                    
        
                if i.round_off_amount:
                    credit_balance += i.round_off_amount
                    total_recieved_amount += i.round_off_amount
                    head_reciept['adjustments'].append({
                        'date':i.voucher_date,
                        'invoice_no':"Round Off",
                        'particulars':"Round Off",
                        'by_to':"BY",
                        'bl_no':bl_no,
                        'voucher_no':f"{i.voucher_no}",
                        'dr_amount':0,
                        'cr_amount':i.round_off_amount,
                        'tds_rec':0,
                        'tds_pay':0,
                        'adjustment':0,
                        'remarks':""
                    })
                    head_reciept['cr_amount'] += i.round_off_amount

                if head_amount > 0:
                    report.append(head_reciept)
        
        #  Trailor Expense
        for i in opening_trailor_expense:
            opening_balance -= (i.charges)
            credit_balance += (i.charges)
            
        for i in trailor_expense:
            if i.date:
                date = i.date
            else:
                date = i.created_at.date()

            credit_balance += (i.charges)
            job_no = ""
            if i.expense.job_no:
                job_no = i.expense.job_no
            particulars = ''
            remarks = ''
            if i.party:
                particulars = 'Advance Paid - '
                if i.invoice:
                    remarks = f", Invoice No. - {i.invoice}"
            report.append({
                'date':date,
                'invoice_no':f"{i.expense.trailor_no}",
                'by_to':"BY",
                'voucher_no':"",
                'particulars':particulars+"TRAILOR EXPENSE",
                'cr_amount':i.charges ,
                'dr_amount':0,
                'tds_rec':0,
                'tds_pay':0,
                'adjustment':0,
                'remarks':f'JOB NO. = {job_no}'+ remarks,
            })

        # Purchase Invoice
        for i in opening_invoices_pay:
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR" :
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass
            
            total_pay += i.net_amount * currency_ex_rate
            opening_balance -= (i.net_amount * currency_ex_rate)
            credit_balance += (i.net_amount * currency_ex_rate)
            
            if i.tds_payable > 0:
                debit_balance += (i.tds_payable)
                opening_balance += (i.tds_payable)
                
        for i in invoices_pay:
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR" :
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass
            job_no = ""
            bl_no = ""
            if i.job_no:
                job_no = i.job_no
                bl_no = i.job_no.booking_no


            particular = "PURCHASE INVOICE"
            try:
                particular = i.payable_invoice_reference.first().billing_head
            except:
                pass

            total_pay += i.net_amount * currency_ex_rate
            credit_balance += (i.net_amount * currency_ex_rate)
            report.append({
                'date':i.date_of_invoice,
                'invoice_no':f"{i.purchase_invoice_no} - Purchase",
                'voucher_no':f'',
                'bl_no':bl_no,
                'particulars':particular,
                'url':reverse('accounting:invoice_payable_update',kwargs={'module':module,'id':i.id}),
                'by_to':"BY",
                'dr_amount':0,
                'cr_amount':i.net_amount * currency_ex_rate,
                'tds_rec':0,
                'tds_pay':0,
                'adjustment':0,
                'remarks':f'JOB NO. = {job_no}',
                'link':"{% url 'dashboard:invoice_payable_pdf' %}"
            })
            
            
            for j in i.payable_invoice_reference.all():
                report.append({
                    'date':i.date_of_invoice,
                    'invoice_no':f"",
                    'particulars':f"{j.billing_head.billing_head}",
                    'by_to':"",
                    'bl_no':bl_no,
                    'voucher_no':"",
                    'dr_amount':0,
                    'cr_amount':0,
                    'tds_rec':0,
                    'tds_pay':0,
                    'adjustment':0,
                    'remarks':f'Amount - {j.total}',
                    'color':'#d3e0b4'
                })

            if i.tds_payable > 0:
                debit_balance += (i.tds_payable)
                report.append({
                    'date':i.date_of_invoice,
                    'invoice_no':f"TDS Payable - {i.purchase_invoice_no}",
                    'voucher_no':"TDS Payable",
                    'particulars':"TDS Payable",
                    'by_to':"To",
                    'bl_no':bl_no,
                    'dr_amount':i.tds_payable,
                    'cr_amount':0,
                    'tds_rec':0,
                    'tds_pay':0,
                    'adjustment':0,
                    'remarks':f'JOB NO. = {job_no}'
                })
    
        # Debit Note 
        for i in opening_debit_note:
            currency_ex_rate = 1
            
            if i.currency_ex_rate:
                currency_ex_rate = i.currency_ex_rate
                
            if i.invoice_currency.short_name == "INR" :
                currency_ex_rate = 1
                
            opening_balance += i.net_amount * currency_ex_rate
            total_pay += i.net_amount * currency_ex_rate
            debit_balance += (i.net_amount * currency_ex_rate)
            
        for i in debit_note:
            currency_ex_rate = 1
            
            if i.currency_ex_rate:
                currency_ex_rate = i.currency_ex_rate
                
            if i.invoice_currency.short_name == "INR" :
                currency_ex_rate = 1
                
                
            job_no = ""
            bl_no = ""
            if i.job_no:
                job_no = i.job_no
                bl_no = i.job_no.booking_no
            total_pay += i.net_amount * currency_ex_rate
            debit_balance += (i.net_amount * currency_ex_rate)
            report.append({
                'date':i.date_of_note,
                'invoice_no':f"{i.invoice_no} - Debit Note #{i.debit_note_no}",
                'url':reverse('accounting:debit_note_update',kwargs={'module':module,'id':i.id}),
                'voucher_no':"",
                'bl_no':bl_no,
                'particulars':"DEBIT NOTE",
                'by_to':"TO",
                'cr_amount':0,
                'dr_amount':i.net_amount * currency_ex_rate,
                'tds_rec':0,
                'tds_pay':0,
                'adjustment':0,
                'remarks':f'JOB NO. = {job_no}'
            })
            
            for j in i.debit_note_reference.all():
                report.append({
                    'date':i.date_of_note,
                    'invoice_no':f"",
                    'bl_no':bl_no,
                    'particulars':f"{j.billing_head.billing_head}",
                    'by_to':"",
                    'voucher_no':"",
                    'dr_amount':0,
                    'cr_amount':0,
                    'tds_rec':0,
                    'tds_pay':0,
                    'adjustment':0,
                    'remarks':f'Amount - {j.total}',
                    'color':'#d3e0b4'
                })
    
        
        opening_bills = []          
        for i in opening_pay_voucher:
            if not i.id in opening_bills:
                opening_bills.append(i.id)
                total_paid_amount = 0
                
                if i.net_amount:
                    opening_balance += i.net_amount
                    debit_balance += i.net_amount
                    total_paid_amount += i.net_amount
                    

        bills = []
        for i in pay_voucher:
            if not i.id in bills:
                if i.voucher_date:
                    voucher_date = i.voucher_date
                else:
                    voucher_date = i.created_at.date()

                bills.append(i.id)
                pay_from = i.pay_from
                
                if i.pay_from == "Cash":
                    pay_from = f'{pay_from}_{i.company_type.branch_name}'
                else:
                    pay_from = f'{pay_from}_{i.bank.bank_name}_{i.bank.account_no}'

                total_paid_amount = 0
                
                head_pay = {
                    'date':voucher_date,
                    'invoice_no':f"{i.narration}",
                    'particulars':f"{pay_from}",
                    'url':reverse('accounting:payment_voucher_update',kwargs={'module':module,'id':i.id}),
                    'remarks':f"{i.instrument_no}",
                    'voucher_no':i.voucher_no,
                    'dr_amount':0,
                    'cr_amount':0,
                    'by_to':"TO",
                    'tds_rec':0,
                    'tds_pay':0,
                    'adjustment':0,
                
                    'adjustments':[]
                }
                    
                for j in i.pay_voucher_detail.all():
                    total_pay_vou += j.paid_amount + j.tds_amount
                    invoice_no = ""
                    bl_no = ""
                    if j.invoice:
                        invoice_no = j.invoice.purchase_invoice_no
                        try:
                            bl_no = j.invoice.job_no.booking_no
                        except:
                            pass
                    if j.expense:
                        invoice_no = j.expense.bill_no
                    debit_balance += (j.paid_amount + j.tds_amount + j.adjustment_amount)
                    total_paid_amount += (j.paid_amount + j.tds_amount + j.adjustment_amount)

                    if i.is_reversed:
                        head_pay['color'] = '#e0b4b4'
                        head_pay['invoice_no'] = i.paid_amount

                    if j.paid_amount > 0 or i.is_reversed:
                        head_pay['adjustments'].append({
                            'date':i.voucher_date,
                            'invoice_no':invoice_no,
                            'particulars':f"Agst Ref. Paid",
                            'voucher_no':f"{i.voucher_no}",
                            'dr_amount':(j.paid_amount),
                            'bl_no':bl_no,
                            'by_to':"TO",
                            'cr_amount':0,
                            'tds_rec':0,
                            'tds_pay':j.tds_amount,
                            'adjustment':j.adjustment_amount,
                            'remarks':""
                        })
                        head_pay['dr_amount'] += j.paid_amount
                    
                    if j.tds_amount > 0:
                        report.append({
                            'date':i.voucher_date,
                            'invoice_no':invoice_no,
                            'particulars':f"TDS Payable",
                            'voucher_no':f"{i.voucher_no}",
                            'dr_amount':(j.tds_amount),
                            'by_to':"TO",
                            'bl_no':bl_no,
                            'cr_amount':0,
                            'tds_rec':0,
                            'tds_pay':j.tds_amount,
                            'adjustment':j.adjustment_amount,
                            'remarks':""
                        })
                    
                    if j.adjustment_amount > 0:
                        report.append({
                            'date':i.voucher_date,
                            'invoice_no':invoice_no,
                            'particulars':f"Adjusted Payable",
                            'voucher_no':f"{i.voucher_no}",
                            'dr_amount':(j.adjustment_amount),
                            'by_to':"TO",
                            'bl_no':bl_no,
                            'cr_amount':0,
                            'tds_rec':0,
                            'tds_pay':j.tds_amount,
                            'adjustment':j.adjustment_amount,
                            'remarks':""
                        })
                    
                
                report.append(head_pay)
       
        if not choose_company == "All":
            company = Logistic.objects.filter(id=int(choose_company)).first()
            context['choose_company'] = company.id
        else:
            context['choose_company'] = "All"
            
        report.sort(key=lambda item:item['date'])
        current_balance = opening_balance
        
        for i in report:
            current_balance += i['dr_amount']
            current_balance -= i['cr_amount']
    
            if current_balance < 0:
                i['current_balance'] =current_balance
                i['balance_in'] = 'Cr.'
            else:
                i['current_balance'] = current_balance
                i['balance_in'] = 'Dr.'

       
        
        context['ledger_name'] = ledger_name
        
        context['include'] = include
        context['report'] = report
        context['company'] = Logistic.objects.first()
        context['total_pay'] = total_pay + p_opening_balance
        context['total_pay_vou'] = total_pay_vou
        context['total_rec'] = total_rec + opening_balance
        context['total_rec_vou'] = total_rec_vou
        context['opening_balance'] = opening_balance
        context['p_opening_balance'] = p_opening_balance 
        context['debit_balance'] = debit_balance 
        context['credit_balance'] = credit_balance 
        context['show_details'] = show_details 
        context['total_balance'] = (total_rec + opening_balance) - total_rec_vou -  (total_pay + p_opening_balance) + total_pay_vou
    
    
    if round_off == "Y":
        context['round_off_value'] = 0
    else:
        context['round_off_value'] = 2
        
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()
        
    context['round_off'] = round_off
  
    context['module']= module
    context['selected_region']= region
    context['show_details'] = show_details

    if generate_report_pdf == 1:
        template_path = "report/party_ledger/party_ledger_pdf.html"
        return generate_pdf(request,template_path,context)
    
    return render(request,'report/party_ledger/party_ledger.html',context)




@login_required(login_url='home:handle_login')
def reciept_tds(request,module):
    context ={}
    check_permissions(request,module)
    
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company = request.POST['company']
        date_filter_from = request.POST['date_filter_from']
        company = Logistic.objects.filter(id=int(company)).first()
        
        vouchers = RecieptVoucherDetails.objects.filter(tds_amount__gt = 0).filter(voucher__company_type=company).select_related('voucher','voucher__party_name','voucher__party_address','invoice','invoice__job_no','voucher__company_type').all()
        if date_filter_from == "Input":
            vouchers = vouchers.filter(voucher__voucher_date__gte=from_date).filter(voucher__voucher_date__lte=to_date).all()
        
        if date_filter_from == "Claimed":
            vouchers = vouchers.filter(tds_claim_date__gte=from_date).filter(tds_claim_date__lte=to_date).all()
        
        context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
        context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()
        context['report']= vouchers
        context['company']= company
        context['date_filter_from']= date_filter_from
  
    context['module']= module
    
    return render(request,'report/reciept_tds/reciept_tds.html',context)

@login_required(login_url='home:handle_login')
def reciept_tds_claim_action(request,module):
    if request.method == "POST":
        status = request.POST['status']
        claim_date = request.POST['claim_date']
        selected_fields = request.POST['selected_fields']
        list_selected = request.POST['list_selected']
        
        if status == "F":
            status = True
        
        else:
            status = False
        
        if list_selected == "0":
            return redirect("dashboard:reciept_tds",module=module)
        
        selected_fields = selected_fields.split(",")
        for i in selected_fields:
            voucher = RecieptVoucherDetails.objects.filter(id=int(i)).first()
            voucher.tds_claimed = status
            if status:
                voucher.tds_claim_date = claim_date
                
            voucher.save()
            
    return redirect("dashboard:reciept_tds",module=module)
            
@login_required(login_url='home:handle_login')
def payment_tds(request,module):
    context ={}
    check_permissions(request,module)
    report = []
    sections = [
        'All',
        '192',
        '192A',
        '194C',
        '194H',
        '194I',
        '194J',
        'PPH23',
        'PP',
        'WHT',
    ]
    tds_section = "All"
    if request.method == 'POST':
        tds_section = request.POST['tds_section']
        from_date = datetime.strptime(str(request.POST['from_date']),"%Y-%m-%d").date()
        to_date = datetime.strptime(str(request.POST['to_date']),"%Y-%m-%d").date()
        
        company = request.POST['company']
        company = Logistic.objects.filter(id=int(company)).first()
        
       
        invoice_payables = InvoicePayable.objects.select_related('company_type','bill_from','bill_from_address').prefetch_related('pay_payment_inv').filter(date_of_invoice__gte=from_date).filter(date_of_invoice__lte=to_date).filter(company_type=company).filter(is_deleted=False).all()
        
        if not tds_section == "All":
            invoice_payables = invoice_payables.filter(tds_section=tds_section).all()
            
        for data in invoice_payables:
            tds = data.tds_payable
            try:
                for i in data.pay_payment_inv.filter(voucher__is_deleted=False).all():
                    tds += i.tds_amount
               
            except:
                pass
            
            if tds > 0:
                report.append({
                    'tds':tds,
                    'invoice':data,
                    "type":"Direct"
                })
        
       

        context['company']= int(company.id)
        context['invoice_payables']= invoice_payables
        context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
        context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()

    context['module']= module
    context['report']= report
    context['tds_section']= tds_section
    context['sections']= sections
    
    return render(request,'report/payment_tds/payment_tds.html',context)


# @login_required(login_url='home:handle_login')
# def gstr1_hsn_recievable(request,module):
#     context ={}
#     check_permissions(request,module)
#     choose_company = "All"
#     companies_gst_code = Logistic.objects.filter(tax_policy="GST").all().values('company_gst_code').annotate(**{'count':Count('company_gst_code')})
#     rcm_include = "N"
#     if request.method == "POST":
#         from_date = request.POST['from_date']
#         to_date = request.POST['to_date']
#         choose_company = request.POST['choose_company']
#         act_to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date() + timedelta(days=1)
#         rcm_include = request.POST['rcm_include']

        
#         invoices = InvoiceReceivableDetail.objects.filter(invoice_receivable__old_invoice=False).filter(invoice_receivable__is_cancel=False).filter(invoice_receivable__is_einvoiced=True).filter(invoice_receivable__einvoice_date__range=[from_date,act_to_date]).filter(invoice_receivable__company_type__tax_policy="GST").all()
        
#         if not choose_company == "All":
#             invoices = invoices.filter(invoice_receivable__company_type__company_gst_code=choose_company).all()
        
#         if rcm_include == "N":
#             invoices = invoices.exclude(invoice_receivable__type_of_invoice='RCM').all()
#         if rcm_include == "R":
#             invoices = invoices.filter(invoice_receivable__type_of_invoice='RCM').all()
    
        
#         report = invoices.values(
#                                 'billing_head__hsn_code',
#                                 'billing_head__billing_head',
#                                 'gst',
                           
#                                 ).annotate(**{'invoice_count' : Count('invoice_receivable'),
#                                 'gst_amount_sum': Sum('gst_amount'),
#                                 'csgst_amount_sum': Sum(Case(
#                                      When (
                                         
#                                              Q(
#                                                  Q(invoice_receivable__bill_to_address__corp_state__gst_code=F('invoice_receivable__company_type__company_gst_code'))
#                                              ) & Q(billing_head__always_igst=False)
#                                          ,
                                           
#                                         then=(F('gst_amount')*F("invoice_receivable__currency_ex_rate")) / 2,
#                                         ),
#                                     output_field=FloatField(),
#                                     default = 0
#                                      )
#                                     ),
#                                 'igst_amount_sum': Sum(Case(
#                                      When (
                                       
#                                              Q(
#                                                  ~Q(invoice_receivable__bill_to_address__corp_state__gst_code=F('invoice_receivable__company_type__company_gst_code'))
#                                              ) | Q(billing_head__always_igst=True)
#                                          ,
#                                            then=(F('gst_amount')*F("invoice_receivable__currency_ex_rate")),
#                                         ),
#                                     output_field=FloatField(),
#                                     default = 0
#                                      )
#                                     ),
#                                 'taxable_value': Sum(F('amount')*F("invoice_receivable__currency_ex_rate"))}
#                                 )


#         credit_notes = CreditNoteDetail.objects.filter(credit_note__is_einvoiced=True).filter(credit_note__einvoice_date__range=[from_date,to_date]).filter(credit_note__company_type__tax_policy="GST").filter(credit_note__is_cancel=False).all()
#         if rcm_include == "N":
#             credit_notes = credit_notes.exclude(credit_note__is_rcm=True).all()
#         if rcm_include == "R":
#             credit_notes = credit_notes.filter(credit_note__is_rcm=True).all()
    
#         if not choose_company == "All":
#             credit_notes = credit_notes.filter(credit_note__company_type__company_gst_code=choose_company).all()
        
#         crn_report = credit_notes.values(
#                                 'billing_head__hsn_code',
#                                 'billing_head__billing_head',
#                                 'gst',
#                                 ).annotate(**{'crn_count' : Count('credit_note'),
#                                 'gst_amount_sum': Sum('gst_amount'),
#                                 'csgst_amount_sum': Sum(Case(
#                                      When (
                                         
#                                              Q(
#                                                  Q(credit_note__bill_to_address__corp_state__gst_code=F('credit_note__company_type__company_gst_code'))
#                                              ) & Q(billing_head__always_igst=False)
#                                          ,
                                           
                                           
#                                         then=(F('gst_amount')*F("credit_note__currency_ex_rate")) / 2,

#                                         ),
#                                     output_field=FloatField(),
#                                     default = 0
#                                      )
#                                     ),
#                                 'igst_amount_sum': Sum(Case(
#                                      When (
                                         
#                                              Q(
#                                                  ~Q(credit_note__bill_to_address__corp_state__gst_code=F('credit_note__company_type__company_gst_code'))
#                                              ) | Q(billing_head__always_igst=True)
#                                          ,
#                                            then=(F('gst_amount')*F("credit_note__currency_ex_rate")),
#                                         ),
#                                     output_field=FloatField(),
#                                     default = 0
#                                      )
#                                     ),
#                                 'taxable_value':  Sum(F('amount')*F("credit_note__currency_ex_rate")),}
#                                 )

    
#         visited_list = []
#         for i in report:
#             for j in crn_report:
#                 if i['billing_head__billing_head'] == j['billing_head__billing_head'] and i['gst'] == j['gst']:
#                     i['taxable_value'] -= j['taxable_value']
#                     if i['csgst_amount_sum'] > 0 or j['csgst_amount_sum'] > 0:
                       
#                         i['csgst_amount_sum'] -= j['csgst_amount_sum']
#                         visited_list.append(j)
                        
#                     if i['igst_amount_sum'] > 0 or j['igst_amount_sum'] > 0:
#                         i['igst_amount_sum'] -= j['igst_amount_sum']
#                         visited_list.append(j)
        
       
                    
        
      
#         context['report'] = report
#         context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
#         context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")
        
       
#         context['choose_company']= choose_company
      
    
#     context['module'] = module
#     context['companies_gst_code'] = companies_gst_code
#     context['rcm_include'] = rcm_include

#     return render(request,'report/gstr1_recievable/gstr1_hsn_recievable.html',context)
    

@login_required(login_url='home:handle_login')
def gstr1_hsn_recievable(request,module):
    context ={}
    check_permissions(request,module)
    choose_company = "All"
    companies_gst_code = Logistic.objects.filter(tax_policy="GST").all().values('company_gst_code').annotate(**{'count':Count('company_gst_code')})
    rcm_include = "N"
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']
        act_to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date() + timedelta(days=1)
        rcm_include = request.POST['rcm_include']

        
        invoices = InvoiceReceivableDetail.objects.filter(invoice_receivable__old_invoice=False).filter(invoice_receivable__is_cancel=False).filter(invoice_receivable__is_einvoiced=True).filter(invoice_receivable__einvoice_date__range=[from_date,to_date]).filter(invoice_receivable__company_type__tax_policy="GST").all()
        
        if not choose_company == "All":
            invoices = invoices.filter(invoice_receivable__company_type__company_gst_code=choose_company).all()
        
        if rcm_include == "N":
            invoices = invoices.exclude(invoice_receivable__type_of_invoice='RCM').all()
        if rcm_include == "R":
            invoices = invoices.filter(invoice_receivable__type_of_invoice='RCM').all()
    
        
        report = invoices.values(
                                'billing_head__hsn_code',
                                'billing_head__billing_head',
                                'gst',
                           
                                ).annotate(**{'invoice_count' : Count('invoice_receivable'),
                                'gst_amount_sum': Sum('gst_amount'),
                                'csgst_amount_sum': Sum(Case(
                                     When (
                                         
                                             Q(
                                                 Q(invoice_receivable__bill_to_address__corp_state__gst_code=F('invoice_receivable__company_type__company_gst_code'))
                                             ) & Q(billing_head__always_igst=False)
                                         ,
                                           
                                        then=(F('gst_amount')*F("invoice_receivable__currency_ex_rate")) / 2,
                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                'igst_amount_sum': Sum(Case(
                                     When (
                                       
                                             Q(
                                                 ~Q(invoice_receivable__bill_to_address__corp_state__gst_code=F('invoice_receivable__company_type__company_gst_code'))
                                             ) | Q(billing_head__always_igst=True)
                                         ,
                                           then=(F('gst_amount')*F("invoice_receivable__currency_ex_rate")),
                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                'taxable_value': Sum(Case(
                                     When (
                                       
                                        Q(gst__gt=0)
                                             
                                         ,
                                           then=(F('amount')*F("invoice_receivable__currency_ex_rate")),
                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                'non_taxable_value': Sum(Case(
                                     When (
                                       
                                        Q(gst=0)
                                             
                                         ,
                                           then=(F('amount')*F("invoice_receivable__currency_ex_rate")),
                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                # 'taxable_value': Sum(F('amount')*F("invoice_receivable__currency_ex_rate"))
                                }
                                )


        credit_notes = CreditNoteDetail.objects.filter(credit_note__is_einvoiced=True).filter(credit_note__einvoice_date__range=[from_date,to_date]).filter(credit_note__company_type__tax_policy="GST").filter(credit_note__is_cancel=False).all()
        if rcm_include == "N":
            credit_notes = credit_notes.exclude(credit_note__is_rcm=True).all()
        if rcm_include == "R":
            credit_notes = credit_notes.filter(credit_note__is_rcm=True).all()
    
        if not choose_company == "All":
            credit_notes = credit_notes.filter(credit_note__company_type__company_gst_code=choose_company).all()

        
    

        crn_report = credit_notes.values(
                                'billing_head__hsn_code',
                                'billing_head__billing_head',
                                'gst',
                                ).annotate(**{'crn_count' : Count('credit_note'),
                                'gst_amount_sum': Sum('gst_amount'),
                                'csgst_amount_sum': Sum(Case(
                                     When (
                                         
                                             Q(
                                                 Q(credit_note__bill_to_address__corp_state__gst_code=F('credit_note__company_type__company_gst_code'))
                                             ) & Q(billing_head__always_igst=False)
                                         ,
                                           
                                           
                                        then=(F('gst_amount')*F("credit_note__currency_ex_rate")) / 2,

                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                'igst_amount_sum': Sum(Case(
                                     When (
                                         
                                             Q(
                                                 ~Q(credit_note__bill_to_address__corp_state__gst_code=F('credit_note__company_type__company_gst_code'))
                                             ) | Q(billing_head__always_igst=True)
                                         ,
                                           then=(F('gst_amount')*F("credit_note__currency_ex_rate")),
                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                    'taxable_value': Sum(Case(
                                     When (
                                       
                                        Q(gst__gt=0)
                                             
                                         ,
                                           then=(F('amount')*F("credit_note__currency_ex_rate")),
                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                'non_taxable_value': Sum(Case(
                                     When (
                                       
                                        Q(gst=0)
                                             
                                         ,
                                           then=(F('amount')*F("credit_note__currency_ex_rate")),
                                        ),
                                    output_field=FloatField(),
                                    default = 0
                                     )
                                    ),
                                # 'taxable_value':  Sum(F('amount')*F("credit_note__currency_ex_rate")),
                                }
                                )

    
        visited_list = []
        for i in report:
            crn_count = 0
            for j in crn_report:
                if i['billing_head__billing_head'] == j['billing_head__billing_head'] and i['gst'] == j['gst']:
                    crn_count = j['crn_count']
                    i['taxable_value'] -= j['taxable_value']
                    i['non_taxable_value'] -= j['non_taxable_value']
                    if i['csgst_amount_sum'] > 0 or j['csgst_amount_sum'] > 0:
                       
                        i['csgst_amount_sum'] -= j['csgst_amount_sum']
                        visited_list.append(j)
                        
                    if i['igst_amount_sum'] > 0 or j['igst_amount_sum'] > 0:
                        i['igst_amount_sum'] -= j['igst_amount_sum']
                        visited_list.append(j)
                    break

            i['crn'] = crn_count
        
       
                    
        
      
        context['report'] = report
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")
        
       
        context['choose_company']= choose_company
      
    
    context['module'] = module
    context['companies_gst_code'] = companies_gst_code
    context['rcm_include'] = rcm_include

    return render(request,'report/gstr1_recievable/gstr1_hsn_recievable.html',context)
    



@login_required(login_url='home:handle_login')
def gstr1_recievable(request,module):
    context ={}
    check_permissions(request,module)
    filter_percent = "All"
    report = False
    if request.method == 'POST':
        report = True
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        invoices = InvoiceReceivable.objects.filter(is_einvoiced = True).filter(company_type__tax_policy = "GST").filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).filter(old_invoice=False).all()
        filter_percent = request.POST['filter_percent']
        context['invoices']= invoices
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")
        
  
    context['filter_percent']= filter_percent
    context['module']= module

    context['report']= report
    
    return render(request,'report/gstr1_recievable/gstr1_recievable.html',context)

@login_required(login_url='home:handle_login')
def gstr1_recievable_server_side(request,module):
    context ={}
    check_permissions(request,module)
    filter_percent = "All"
    report = False
    rcm_include = "N"
    company_gst_code = "A"
    
    if request.method == 'POST':
        report = True
        from_date = request.POST['from_date']
        rcm_include = request.POST['rcm_include']

        to_date = request.POST['to_date']
        act_to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date() + timedelta(days=1)
        company_gst_code = request.POST['company_gst_code']

        invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','invoice_currency','job_no','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference','recievable_invoice_reference__billing_head').filter(is_einvoiced = True).filter(company_type__tax_policy = "GST").filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=act_to_date).filter(old_invoice=False).all()
        
            
                
        credit_notes = CreditNote.objects.select_related('company_type','bill_to','bill_to_address','invoice_currency','job_no','bill_to_address__corp_state').prefetch_related('credit_note_reference','credit_note_reference__billing_head').filter(is_einvoiced = True).filter(company_type__tax_policy = "GST").filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=act_to_date).all()

        if not company_gst_code == "A":
            invoices = invoices.filter(company_type__company_gst_code=company_gst_code).all()
            credit_notes = credit_notes.filter(company_type__company_gst_code=company_gst_code).all()

        if rcm_include == "R":
            invoices = invoices.filter(type_of_invoice='RCM').all()
            credit_notes = credit_notes.filter(is_rcm=True).all()

        if rcm_include == "N":
            invoices = invoices.exclude(type_of_invoice='RCM').all()
            credit_notes = credit_notes.exclude(is_rcm=True).all()
      
        
        report = []
        error_report = []
        crn_report = []
        error_crn_report = []
       
        for invoice in invoices:
            try:
                
                
                customer_gst_code = "00"
                if invoice.bill_to_address:
                    customer_gst_code = invoice.bill_to_address.corp_state.gst_code
               

                non_taxable_amount = 0
                taxable_5 = 0
                taxable_12 = 0
                taxable_18 = 0
                cs_5 = 0
                cs_12 = 0
                cs_18 = 0
                i_5 = 0
                i_12 = 0
                i_18 = 0
                error_flag = 0
                for i in invoice.recievable_invoice_reference.all():
                    company_gst_code_check = invoice.company_type.company_gst_code
                    billing_head = i.billing_head
                    if i.gst == 0:
                        non_taxable_amount += i.amount

                    if i.gst == 5:
                        taxable_5 += i.amount
                        if invoice.bill_to_address:
                            if customer_gst_code == company_gst_code_check and not billing_head.always_igst:
                                cs_5 += round((i.gst_amount / 2),2)
                            else:
                                i_5 += i.gst_amount
                        else:
                            error_flag = 1

                    if i.gst == 12:
                        taxable_12 += i.amount
                        if invoice.bill_to_address:
                            if customer_gst_code == company_gst_code_check and not billing_head.always_igst:
                                cs_12 += round((i.gst_amount / 2),2)
                            else:
                                i_12 += i.gst_amount
                        else:
                            error_flag = 1

                    if i.gst == 18:
                        taxable_18 += i.amount
                        if invoice.bill_to_address:
                            if customer_gst_code == company_gst_code_check and not billing_head.always_igst:
                                cs_18 += round((i.gst_amount / 2),2)
                            else:
                                i_18 += i.gst_amount
                        else:
                            error_flag = 1
                
                if error_flag == 0:
                    report.append({
                        'invoice':invoice,
                        'non_taxable_amount':non_taxable_amount,
                        'taxable_5':taxable_5,
                        'taxable_12':taxable_12,
                        'taxable_18':taxable_18,
                        'cs_5':cs_5,
                        'cs_12':cs_12,
                        'cs_18':cs_18,
                        'i_5':i_5,
                        'i_12':i_12,
                        'i_18':i_18,
                    })
                else:
                    error_report.append(invoice)
            
            except:
                error_report.append(invoice)
            
        
        for invoice in credit_notes:
            try:
                customer_gst_code = "00"
                if invoice.bill_to_address:
                    customer_gst_code = invoice.bill_to_address.corp_state.gst_code

                non_taxable_amount = 0
                taxable_5 = 0
                taxable_12 = 0
                taxable_18 = 0
                cs_5 = 0
                cs_12 = 0
                cs_18 = 0
                i_5 = 0
                i_12 = 0
                i_18 = 0
                error_flag = 0
                for i in invoice.credit_note_reference.all():
                    company_gst_code_check = invoice.company_type.company_gst_code
                    if i.gst == 0:
                        non_taxable_amount += i.amount

                    if i.gst == 5:
                        taxable_5 += i.amount
                        if invoice.bill_to_address:
                            if customer_gst_code == company_gst_code_check:
                                cs_5 += round((i.gst_amount / 2),2)
                            else:
                                i_5 += i.gst_amount
                        else:
                            error_flag = 1

                    if i.gst == 12:
                        taxable_12 += i.amount
                        if invoice.bill_to_address:
                            if customer_gst_code == company_gst_code_check:
                                cs_12 += round((i.gst_amount / 2),2)
                            else:
                                i_12 += i.gst_amount
                        else:
                            error_flag = 1

                    if i.gst == 18:
                        taxable_18 += i.amount
                        if invoice.bill_to_address:
                            if customer_gst_code == company_gst_code_check:
                                cs_18 += round((i.gst_amount / 2),2)
                            else:
                                i_18 += i.gst_amount
                        else:
                            error_flag = 1
                
                if error_flag == 0:
                    crn_report.append({
                        'invoice':invoice,
                        'non_taxable_amount':non_taxable_amount,
                        'taxable_5':taxable_5,
                        'taxable_12':taxable_12,
                        'taxable_18':taxable_18,
                        'cs_5':cs_5,
                        'cs_12':cs_12,
                        'cs_18':cs_18,
                        'i_5':i_5,
                        'i_12':i_12,
                        'i_18':i_18,
                    })
                else:
                    error_crn_report.append(invoice)
            
            except:
                error_crn_report.append(invoice)
        
        
        context['report'] = report
        context['crn_report'] = crn_report
        context['error_report'] = error_report
        context['error_crn_report'] = error_crn_report
        filter_percent = request.POST['filter_percent']
        context['invoices']= invoices
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

        
    companies_gst_code = Logistic.objects.filter(tax_policy="GST").all().values('company_gst_code').annotate(**{'count':Count('company_gst_code')})
    context['companies_gst_code']= companies_gst_code
    context['filter_percent']= filter_percent
    context['company_gst_code']= company_gst_code
    context['module']= module
    context['rcm_include']= rcm_include
 

    context['report']= report
    
    return render(request,'report/gstr1_recievable_server/gstr1_recievable.html',context)

@login_required(login_url='home:handle_login')
def gstr2_payable(request,module):
    context ={}
    check_permissions(request,module)
    companies_gst_code = Logistic.objects.filter(tax_policy="GST").all().values('company_gst_code').annotate(**{'count':Count('company_gst_code')})
    filter_percent = "All"
    report_status = False
    report = []
    error_report = []
    company_gst_code = "A"
    invoice_status = "A"
    if request.method == 'POST':
        report_status = True
        
        invoice_status = request.POST['invoice_status']
        from_date = request.POST['from_date']

        to_date = request.POST['to_date']
        act_to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date() + timedelta(days=1)
        company_gst_code = request.POST['company_gst_code']
        claim_date = request.POST['claim_date']
            

        filter_percent = request.POST['filter_percent']
        list_selected = int(request.POST['list_selected'])
        invoices = InvoicePayable.objects.select_related('company_type','bill_from','bill_from_address','bill_from_address__corp_state','invoice_currency','job_no').prefetch_related('payable_invoice_reference','payable_invoice_reference__billing_head').filter(date_of_invoice__gte=from_date).filter(date_of_invoice__lte=to_date).filter(company_type__tax_policy = "GST").filter(is_deleted=False).all()
        
        debit_notes = DebitNote.objects.select_related('company_type','bill_from','bill_from_address','bill_from_address__corp_state','invoice_currency','job_no').prefetch_related('debit_note_reference','debit_note_reference__billing_head').filter(date_of_note__gte=from_date).filter(date_of_note__lte=to_date).filter(company_type__tax_policy = "GST").filter(is_deleted=False).all()
        
        expenses = IndirectExpense.objects.select_related('company_type','vendor','job_no','vendor__state').filter(bill_date__gte=from_date).prefetch_related('indirect_expense_reference','indirect_expense_reference__billing_head').filter(company_type__tax_policy = "GST").filter(bill_date__lte=to_date).filter(gst_amount__gt=0).filter(is_deleted=False).filter(is_transfered=False).all()
        
        payment_voucher = PaymentVoucher.objects.select_related('company_type','from_bank').filter(voucher_date__gte=from_date).filter(company_type__tax_policy = "GST").filter(voucher_date__lte=to_date).filter(bank_charges_tax__gt=0).filter(is_deleted=False).all()

        if not company_gst_code == "A":
            invoices = invoices.filter(company_type__company_gst_code=company_gst_code).all()
            expenses = expenses.filter(company_type__company_gst_code=company_gst_code).all()
        
        if invoice_status == "F":
            invoices = invoices.filter(is_final=True).all()
            expenses = expenses.filter(is_final=True).all()
            debit_notes = debit_notes.filter(is_final=True).all()
        
        if invoice_status == "U":
            invoices = invoices.filter(is_final=False).all()
            expenses = expenses.filter(is_final=False).all()
            debit_notes = debit_notes.filter(is_final=False).all()
        
        if list_selected == 1:
            selected_fields = request.POST['selected_fields']
            status = request.POST['status']
            selected_fields = "[" + selected_fields + "]"
            selected_fields = loads(selected_fields)
         
            for i in selected_fields:
                if i['type'] == "D":
                    invoice = invoices.filter(id=int(i['id'])).first()
                    if status == "F":
                        invoice.is_final = True
                        invoice.claim_date = claim_date
                    else:
                        invoice.is_final = False
                        invoice.claim_date = None
                    invoice.save()
                
                if i['type'] == "N":
                    note = debit_notes.filter(id=int(i['id'])).first()
                    if status == "F":
                        note.is_final = True
                        note.claim_date = claim_date
                    else:
                        note.is_final = False
                        note.claim_date = None
                    note.save()
                    
                if i['type'] == "I":
                    invoice = expenses.filter(id=int(i['id'])).first()
                    if status == "F":
                        invoice.is_final = True
                        invoice.claim_date = claim_date
                    else:
                        invoice.is_final = False
                        invoice.claim_date = None
                        
                    invoice.save()
    
        for invoice in payment_voucher:
            
            try:
                non_taxable_amount = 0
                taxable_5 = 0
                taxable_12 = 0
                taxable_18 = 0
                taxable_28 = 0
                cs_5 = 0
                cs_12 = 0
                cs_18 = invoice.bank_charges_sgst
                cs_28 = 0
                i_5 = 0
                i_12 = 0
                i_18 = invoice.bank_charges_igst
                i_28 = 0
                error_flag = 0
                currency_ex_rate = 1
                
                report.append({
                        'type':'OTH',
                        'invoice':invoice,
                        'non_taxable_amount':non_taxable_amount,
                        'taxable_5':taxable_5,
                        'taxable_12':taxable_12,
                        'taxable_18':taxable_18,
                        'taxable_28':taxable_28,
                        'cs_5':0,
                        'cs_12':0,
                        'cs_18':0,
                        'cs_28':0,
                        'i_5':0,
                        'i_12':0,
                        'i_18':0,
                        'i_28':0,
                        'other_cs_5':(cs_5),
                        'other_cs_12':(cs_12),
                        'other_cs_18':(cs_18),
                        'other_cs_28':(cs_28),
                        'other_i_5':(i_5),
                        'other_i_12':(i_12),
                        'other_i_18':(i_18),
                        'other_i_28':(i_28),
                    })
               

                
            except:
                error_report.append(invoice)
            
        for invoice in debit_notes:
            if not invoice.claim_date and invoice.is_final:
                invoice.claim_date = invoice.date_of_note
                invoice.save()

            try:
                non_taxable_amount = 0
                taxable_5 = 0
                taxable_12 = 0
                taxable_18 = 0
                taxable_28 = 0
                cs_5 = 0
                cs_12 = 0
                cs_18 = 0
                cs_28 = 0
                i_5 = 0
                i_12 = 0
                i_18 = 0
                i_28 = 0
                other_cs_5 = 0
                other_cs_12 = 0
                other_cs_18 = 0
                other_cs_28 = 0
                other_i_5 = 0
                other_i_12 = 0
                other_i_18 = 0
                other_i_28 = 0
                error_flag = 0
                currency_ex_rate = 1
                try:
                    if not invoice.invoice_currency.short_name == "INR":
                        currency_ex_rate = invoice.currency_ex_rate
                except:
                    pass

                for i in invoice.debit_note_reference.all():
                    amount = round(i.amount * currency_ex_rate,2)
                    if company_gst_code == "A":
                        company_gst_code_temp = invoice.company_type.company_gst_code
                    else:
                        company_gst_code_temp = company_gst_code
                        
                    if i.gst == 0:
                        non_taxable_amount += amount

                    if i.gst == 5:
                        taxable_5 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_5 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_5 += round((i.gst_amount / 2),2)

                            else:
                                if invoice.job_no:
                                    i_5 += i.gst_amount
                                else:
                                    other_i_5 += i.gst_amount

                        else:
                            error_flag = 1

                    if i.gst == 12:
                        taxable_12 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_12 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_12 += round((i.gst_amount / 2),2)

                            else:
                                if invoice.job_no:
                                    i_12 += i.gst_amount
                                else:
                                    other_i_12 += i.gst_amount

                        else:
                            error_flag = 1

                    if i.gst == 18:
                        taxable_18 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_18 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_18 += round((i.gst_amount / 2),2)

                            else:
                                if invoice.job_no:
                                    i_18 += i.gst_amount
                                else:
                                    other_i_18 += i.gst_amount

                        else:
                            error_flag = 1
                            
                    if i.gst == 28:
                        taxable_28 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_28 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_28 += round((i.gst_amount / 2),2)

                            else:
                                if invoice.job_no:
                                    i_28 += i.gst_amount
                                else:
                                    other_i_28 += i.gst_amount

                        else:
                            error_flag = 1
                
                if error_flag == 0:
                    report.append({
                        'type':'N',
                        'invoice':invoice,
                        'non_taxable_amount':non_taxable_amount,
                        'taxable_5':taxable_5,
                        'taxable_12':taxable_12,
                        'taxable_18':taxable_18,
                        'taxable_28':taxable_28,
                        'cs_5':(cs_5),
                        'cs_12':(cs_12),
                        'cs_18':(cs_18),
                        'cs_28':(cs_28),
                        'i_5':(i_5),
                        'i_12':(i_12),
                        'i_18':(i_18),
                        'i_28':(i_28),
                        'other_cs_5':(other_cs_5),
                        'other_cs_12':(other_cs_12),
                        'other_cs_18':(other_cs_18),
                        'other_cs_28':(other_cs_28),
                        'other_i_5':(other_i_5),
                        'other_i_12':(other_i_12),
                        'other_i_18':(other_i_18),
                        'other_i_28':(other_i_28),
                    })
                else:
                    error_report.append(invoice)
            
            except:
                error_report.append(invoice)
            
        
        for invoice in invoices:
            if not invoice.claim_date and invoice.is_final:
                invoice.claim_date = invoice.date_of_invoice
                invoice.save()

            try:
                non_taxable_amount = 0
                taxable_5 = 0
                taxable_12 = 0
                taxable_18 = 0
                taxable_28 = 0
                cs_5 = 0
                cs_12 = 0
                cs_18 = 0
                cs_28 = 0
                i_5 = 0
                i_12 = 0
                i_18 = 0
                i_28 = 0
                other_cs_5 = 0
                other_cs_12 = 0
                other_cs_18 = 0
                other_cs_28 = 0
                other_i_5 = 0
                other_i_12 = 0
                other_i_18 = 0
                other_i_28 = 0
                error_flag = 0
                currency_ex_rate = 1
                try:
                    if not invoice.invoice_currency.short_name == "INR":
                        currency_ex_rate = invoice.currency_ex_rate
                except:
                    pass

                for i in invoice.payable_invoice_reference.all():
                    amount = round(i.amount * currency_ex_rate,2)
                    if company_gst_code == "A":
                        company_gst_code_temp = invoice.company_type.company_gst_code
                    else:
                        company_gst_code_temp = company_gst_code
                        
                    if i.gst == 0:
                        non_taxable_amount += amount

                    if i.gst == 5:
                        taxable_5 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_5 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_5 += round((i.gst_amount / 2),2)
                            else:
                                if invoice.job_no:
                                    i_5 += i.gst_amount
                                else:
                                    other_i_5 += i.gst_amount
                        else:
                            error_flag = 1

                    if i.gst == 12:
                        taxable_12 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_12 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_12 += round((i.gst_amount / 2),2)
                            else:
                                if invoice.job_no:
                                    i_12 += i.gst_amount
                                else:
                                    other_i_12 += i.gst_amount
                        else:
                            error_flag = 1

                    if i.gst == 18:
                        taxable_18 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_18 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_18 += round((i.gst_amount / 2),2)
                            else:
                                if invoice.job_no:
                                    i_18 += i.gst_amount
                                else:
                                    other_i_18 += i.gst_amount
                        else:
                            error_flag = 1
                            
                    if i.gst == 28:
                        taxable_28 += amount
                        if invoice.bill_from_address:
                            if invoice.bill_from_address.corp_state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_28 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_28 += round((i.gst_amount / 2),2)
                            else:
                                if invoice.job_no:
                                    i_28 += i.gst_amount
                                else:
                                    other_i_28 += i.gst_amount
                        else:
                            error_flag = 1
                
                if error_flag == 0:
                    report.append({
                        'type':'D',
                        'invoice':invoice,
                        'non_taxable_amount':non_taxable_amount,
                        'taxable_5':taxable_5,
                        'taxable_12':taxable_12,
                        'taxable_18':taxable_18,
                        'taxable_28':taxable_28,
                        'cs_5':cs_5,
                        'other_cs_5':other_cs_5,
                        'cs_12':cs_12,
                        'other_cs_12':other_cs_12,
                        'cs_18':cs_18,
                        'other_cs_18':other_cs_18,
                        'cs_28':cs_28,
                        'other_cs_28':other_cs_28,
                        'i_5':i_5,
                        'other_i_5':other_i_5,
                        'i_12':i_12,
                        'other_i_12':other_i_12,
                        'i_18':i_18,
                        'other_i_18':other_i_18,
                        'i_28':i_28,
                        'other_i_28':other_i_28
                    })
                else:
                    error_report.append(invoice)
            
            except:
                error_report.append(invoice)
               
        for invoice in expenses:
            if not invoice.claim_date and invoice.is_final:
                invoice.claim_date = invoice.bill_date
                invoice.save()
            try:
                non_taxable_amount = 0
                taxable_5 = 0
                taxable_12 = 0
                taxable_18 = 0
                taxable_28 = 0
                cs_5 = 0
                cs_12 = 0
                cs_18 = 0
                cs_28 = 0
                i_5 = 0
                i_12 = 0
                i_18 = 0
                i_28 = 0
                other_cs_5 = 0
                other_cs_12 = 0
                other_cs_18 = 0
                other_cs_28 = 0
                other_i_5 = 0
                other_i_12 = 0
                other_i_18 = 0
                other_i_28 = 0
                error_flag = 0
                for i in invoice.indirect_expense_reference.all():
                    if company_gst_code == "A":
                        company_gst_code_temp = invoice.company_type.company_gst_code
                    else:
                        company_gst_code_temp = company_gst_code
                        
                    if i.gst == 0:
                        non_taxable_amount += i.amount

                    if i.gst == 5:
                        taxable_5 += i.amount
                        if invoice.vendor:
                            if invoice.vendor.state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_5 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_5 += round((i.gst_amount / 2),2)
                            else:
                                if invoice.job_no:
                                    i_5 += i.gst_amount
                                else:
                                    other_i_5 += i.gst_amount

                        else:
                            error_flag = 1

                    if i.gst == 12:
                        taxable_12 += i.amount
                        if invoice.vendor:
                            
                            if invoice.vendor.state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_12 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_12 += round((i.gst_amount / 2),2)
                            else:
                                if invoice.job_no:
                                    i_12 += i.gst_amount
                                else:
                                    other_i_12 += round((i.gst_amount),2)
                        else:
                            error_flag = 1

                    if i.gst == 18:
                        taxable_18 += i.amount
                        if invoice.vendor:
                            if invoice.vendor.state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_18 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_18 += round((i.gst_amount / 2),2)

                            else:
                                if invoice.job_no:
                                    i_18 += i.gst_amount
                                else:
                                    other_i_18 += i.gst_amount

                        else:
                            error_flag = 1
                            
                    if i.gst == 28:
                        taxable_28 += i.amount
                        if invoice.vendor:
                            if invoice.vendor.state.gst_code == company_gst_code_temp and not i.billing_head.always_igst:
                                if invoice.job_no:
                                    cs_28 += round((i.gst_amount / 2),2)
                                else:
                                    other_cs_28 += round((i.gst_amount / 2),2)

                            else:
                                if invoice.job_no:
                                    i_28 += i.gst_amount
                                else:
                                    other_i_28 += i.gst_amount

                        else:
                            error_flag = 1
                
                if error_flag == 0:
                    report.append({
                        'type':'I',
                        'invoice':invoice,
                        'non_taxable_amount':non_taxable_amount,
                        'taxable_5':taxable_5,
                        'taxable_12':taxable_12,
                        'taxable_18':taxable_18,
                        'taxable_28':taxable_28,
                        'cs_5':cs_5,
                        'other_cs_5':other_cs_5,
                        'cs_12':cs_12,
                        'other_cs_12':other_cs_12,
                        'cs_18':cs_18,
                        'other_cs_18':other_cs_18,
                        'cs_28':cs_28,
                        'other_cs_28':other_cs_28,
                        'i_5':i_5,
                        'other_i_5':other_i_5,
                        'i_12':i_12,
                        'other_i_12':other_i_12,
                        'i_18':i_18,
                        'other_i_18':other_i_18,
                        'i_28':i_28,
                        'other_i_28':other_i_28,
                    })
                else:
                    error_report.append(invoice)
            
            except:
                error_report.append(invoice)
            
        
        context['invoices']= invoices
        context['expenses']= expenses
        context['debit_notes']= debit_notes
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")
                
    context['filter_percent']= filter_percent
  
    context['module']= module
    context['companies_gst_code']= companies_gst_code
    context['report_list']= report
    context['report']= report_status
    context['company_gst_code']= company_gst_code
    context['invoice_status']= invoice_status
    context['today_date']= date.today()
   
    
    return render(request,'report/gstr2_payable/gstr2_payable.html',context)

@login_required(login_url='home:handle_login')
def gstr3b(request,module):
    context ={}
    check_permissions(request,module)
    report = False
    companies_gst_code = Logistic.objects.filter(tax_policy="GST").all().values('company_gst_code').annotate(**{'count':Count('company_gst_code')})
    if request.method == "POST":
        report = True
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        next_to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date() + timedelta(days=1)
        current_year = datetime.now().year
        last_month = datetime.strptime(from_date,'%Y-%m-%d').date().replace(day=1) - timedelta(days=1)
        _,end_day = calendar.monthrange(current_year, last_month.month)
        old_from_date = date(current_year,last_month.month,1)
        old_to_date = date(current_year,last_month.month,end_day)
     
        company_gst_code = request.POST['company_gst_code']
        all_invoice_rec = InvoiceReceivable.objects.select_related('company_type','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference','recievable_invoice_reference__billing_head').filter(is_einvoiced = True).filter(company_type__tax_policy = "GST").filter(company_type__company_gst_code=company_gst_code).filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=next_to_date).filter(is_single=True).filter(is_cancel=False).filter(is_deleted=False).all()
        
    
        
        all_invoice_pay = InvoicePayable.objects.select_related('company_type','bill_from_address','bill_from_address__corp_state').prefetch_related('payable_invoice_reference','payable_invoice_reference__billing_head').filter(is_final=True).filter(company_type__tax_policy = "GST").filter(company_type__company_gst_code=company_gst_code).filter(claim_date__gte=from_date).filter(claim_date__lte=next_to_date).filter(is_deleted=False).all()
    
        
        old_invoice_pay_rcm = InvoicePayable.objects.select_related('company_type','bill_from_address','bill_from_address__corp_state').prefetch_related('payable_invoice_reference','payable_invoice_reference__billing_head').filter(is_final=True).filter(company_type__tax_policy = "GST").filter(company_type__company_gst_code=company_gst_code).filter(claim_date__gte=old_from_date).filter(claim_date__lte=old_to_date).filter(is_rcm=True).filter(is_deleted=False).all()
        
        all_expense_pay = IndirectExpense.objects.select_related('company_type','vendor').prefetch_related('indirect_expense_reference','indirect_expense_reference__billing_head').filter(is_final=True).filter(company_type__tax_policy = "GST").filter(company_type__company_gst_code=company_gst_code).filter(is_deleted=False).filter(claim_date__gte=from_date).filter(claim_date__lte=next_to_date).filter(is_transfered=False).all()
        
        all_crn = CreditNote.objects.select_related('company_type','bill_to_address').prefetch_related('credit_note_reference','credit_note_reference__billing_head').filter(is_einvoiced=True).filter(company_type__tax_policy = "GST").filter(company_type__company_gst_code=company_gst_code).filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=next_to_date).filter(is_cancel=False).filter(is_deleted=False).all()

        all_drn = DebitNote.objects.select_related('company_type','bill_from_address').prefetch_related('debit_note_reference','debit_note_reference__billing_head').filter(date_of_note__gte=from_date).filter(company_type__tax_policy = "GST").filter(company_type__company_gst_code=company_gst_code).filter(date_of_note__lte=next_to_date).filter(is_deleted=False).all()
        
        out_total_cs5 = 0
        out_total_i5 = 0
        out_total_cs12 = 0
        out_total_i12 = 0
        out_total_cs18 = 0
        out_total_i18 = 0
        out_total_cs28 = 0
        out_total_i28 = 0
        out_total_rcm_cs5 = 0
        out_total_rcm_i5 = 0
        
        in_total_cs5 = 0
        in_total_i5 = 0
        in_total_cs12 = 0
        in_total_i12 = 0
        in_total_cs18 = 0
        in_total_i18 = 0
        in_total_cs28 = 0
        in_total_i28 = 0
        in_total_rcm_cs5 = 0
        in_total_rcm_i5 = 0
        
        cr_out_total_cs5 = 0
        cr_in_total_cs5 = 0
        cr_out_total_i5 = 0
        cr_in_total_i5 = 0
        cr_out_total_cs12 = 0
        cr_in_total_cs12 = 0
        cr_out_total_i12 = 0
        cr_in_total_i12 = 0
        cr_out_total_cs18 = 0
        cr_in_total_cs18 = 0
        cr_out_total_cs28 = 0
        cr_in_total_cs28 = 0
        cr_out_total_i18 = 0
        cr_in_total_i18 = 0
        cr_out_total_i28 = 0
        cr_in_total_i28 = 0
        cr_out_total_rcm_cs5 = 0
        cr_in_total_rcm_cs5 = 0
        cr_out_total_rcm_i5 = 0
        cr_in_total_rcm_i5 = 0
        
        dr_out_total_cs5 = 0
        dr_in_total_cs5 = 0
        dr_out_total_i5 = 0
        dr_in_total_i5 = 0
        dr_out_total_cs12 = 0
        dr_in_total_cs12 = 0
        dr_out_total_i12 = 0
        dr_in_total_i12 = 0
        dr_out_total_cs18 = 0
        dr_in_total_cs18 = 0
        dr_out_total_cs28 = 0
        dr_in_total_cs28 = 0
        dr_out_total_i18 = 0
        dr_in_total_i18 = 0
        dr_out_total_i28 = 0
        dr_in_total_i28 = 0
        dr_out_total_rcm_cs5 = 0
        dr_in_total_rcm_cs5 = 0
        dr_out_total_rcm_i5 = 0
        dr_in_total_rcm_i5 = 0
        
        
        
        for invoice in all_invoice_rec:
            for i in invoice.recievable_invoice_reference.all():
                if i.gst == 5:
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_cs5 += round((i.gst_amount/2),2)
                    
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_i5 += i.gst_amount
                    
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and  invoice.type_of_invoice == "RCM":
                        # out_total_rcm_cs5 += round((i.gst_amount/2),2)
                        out_total_rcm_cs5 += 0
                    
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and  invoice.type_of_invoice == "RCM":
                        out_total_rcm_i5 += 0
                        # out_total_rcm_i5 += i.gst_amount
                
                if i.gst == 12:
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_cs12 += round((i.gst_amount/2),2)
                    
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_i12 += i.gst_amount
                    
                
                if i.gst == 18:
                   
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_cs18 += round((i.gst_amount/2),2)
                    
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_i18 += i.gst_amount
                    
                if i.gst == 28:
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_cs28 += round((i.gst_amount/2),2)
                    
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.type_of_invoice == "RCM":
                        out_total_i28 += i.gst_amount
                    
        
        for invoice in all_crn:
          
            # mode = ""
            mode = "O"
           
            
            for i in invoice.credit_note_reference.all():
                
                if i.gst == 5:
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.is_rcm:
                        
                        cr_out_total_cs5 += round((i.gst_amount/2),2)
                        
                    
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.is_rcm:
                        
                        cr_out_total_i5 += round((i.gst_amount),2)
                        
                   
                    
                  
                
                if i.gst == 12:
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not  invoice.is_rcm:
                    
                        cr_out_total_cs12 += round((i.gst_amount/2),2)
                        
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not  invoice.is_rcm:
                    
                        cr_out_total_i12 += round((i.gst_amount),2)
                        
                
                if i.gst == 18:
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not  invoice.is_rcm:
                        
                        cr_out_total_cs18 += round((i.gst_amount/2),2)
                        
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not  invoice.is_rcm:
                        
                        cr_out_total_i18 += round((i.gst_amount),2)
                
                if i.gst == 28:
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not  invoice.is_rcm:
                        
                        cr_out_total_cs28 += round((i.gst_amount/2),2)
                        
                    if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not  invoice.is_rcm:
                        
                        cr_out_total_i28 += round((i.gst_amount),2)
                        
              
    
    
        for invoice in all_drn:
            
            for i in invoice.debit_note_reference.all():
                try:
                    if i.gst == 5:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst :
                            
                            dr_in_total_cs5 += round((i.gst_amount/2),2)
                            
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                            
                            dr_in_total_i5 += round((i.gst_amount),2)
                           
                    
                    if i.gst == 12:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                            dr_in_total_cs12 += round((i.gst_amount/2),2)
                                                   
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                          
                            dr_in_total_i12 += round((i.gst_amount),2)
                           
                    
                    if i.gst == 18:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                            dr_in_total_cs18 += round((i.gst_amount/2),2)
                            
                        
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                            dr_in_total_i18 += round((i.gst_amount),2)
                    
                    if i.gst == 28:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                            dr_in_total_cs28 += round((i.gst_amount/2),2)
                            
                        
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                            dr_in_total_i28 += round((i.gst_amount),2)
                           
                except:
                    pass
    
    
                    
        # for invoice in old_invoice_pay_rcm:
        #     for i in invoice.payable_invoice_reference.all():
            
        #         if i.gst == 5 and invoice.is_rcm:
        #             if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and invoice.is_rcm:
        #                 in_total_rcm_cs5 += round((i.gst_amount/2),2)
                    
        #             if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and invoice.is_rcm:
        #                 in_total_rcm_i5 += i.gst_amount
                    
        for invoice in all_invoice_pay:
           
            for i in invoice.payable_invoice_reference.all():
                try:
                    if i.gst == 5 and not invoice.is_rcm:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                            in_total_cs5 += round((i.gst_amount/2),2)
                        
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                            in_total_i5 += i.gst_amount
                        
                    
                    if invoice.is_rcm:
                        gst_amount = round(((invoice.gross_amount*5) / 100),2)
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and invoice.is_rcm:
                            in_total_rcm_cs5 += round((gst_amount/2),2)
                            out_total_rcm_cs5 += round((gst_amount/2),2)
                        
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and invoice.is_rcm:
                            in_total_rcm_i5 += gst_amount
                            out_total_rcm_i5 += gst_amount


                    # if i.gst == 5 and invoice.is_rcm:
                    #     if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and invoice.is_rcm:
                    #         out_total_rcm_cs5 += round((i.gst_amount/2),2)
                        
                    #     if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and invoice.is_rcm:
                    #         out_total_rcm_i5 += i.gst_amount
                        
                    
                    
                    if i.gst == 12:
                     
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.is_rcm:
                            in_total_cs12 += round((i.gst_amount/2),2)
                        
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.is_rcm:
                            in_total_i12 += i.gst_amount
                        
                    
                    if i.gst == 18:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.is_rcm:
                            in_total_cs18 += round((i.gst_amount/2),2)
                        
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.is_rcm:
                            in_total_i18 += i.gst_amount
                            
                    if i.gst == 28:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst and not invoice.is_rcm:
                            in_total_cs28 += round((i.gst_amount/2),2)
                        
                        if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst and not invoice.is_rcm:
                            in_total_i28 += i.gst_amount
                except:
                    pass
                    
        for invoice in all_expense_pay:
            for i in invoice.indirect_expense_reference.all():
                if i.gst == 5:
                    if invoice.vendor.state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst :
                        in_total_cs5 += round((i.gst_amount/2),2)
                    
                    if not invoice.vendor.state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst :
                        in_total_i5 += i.gst_amount
                    
                    if invoice.vendor.state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                        in_total_rcm_cs5 += round((i.gst_amount/2),2)
                    
                    if not invoice.vendor.state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst :
                        in_total_rcm_i5 += i.gst_amount
                
                if i.gst == 12:
                    if invoice.vendor.state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                        in_total_cs12 += round((i.gst_amount/2),2)
                    
                    if not invoice.vendor.state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst :
                        in_total_i12 += i.gst_amount
                    
                
                if i.gst == 18:
                    if invoice.vendor.state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                        in_total_cs18 += round((i.gst_amount/2),2)
                    
                    if not invoice.vendor.state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst :
                        in_total_i18 += i.gst_amount
                    
                
                if i.gst == 28:
                    if invoice.vendor.state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                        in_total_cs28 += round((i.gst_amount/2),2)
                    
                    if not invoice.vendor.state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst :
                        in_total_i28 += i.gst_amount
                    
                
        total_out_sales = round((out_total_cs5 + out_total_cs5 + out_total_i5 + out_total_cs12 + out_total_cs12 + out_total_i12 + out_total_cs18 +out_total_cs18 +out_total_cs28 + out_total_i18 + out_total_i28 + out_total_rcm_cs5 + out_total_rcm_cs5 + out_total_rcm_i5),2)
                    
        total_cr_out_sales = round((cr_out_total_cs5 + cr_out_total_cs5 + cr_out_total_i5 + cr_out_total_cs12 + cr_out_total_cs12 + cr_out_total_i12 + cr_out_total_cs18 + cr_out_total_cs18 + cr_out_total_i18 + cr_out_total_cs28 + cr_out_total_cs28 + cr_out_total_i28 + cr_out_total_rcm_cs5 + cr_out_total_rcm_i5),2)
                    
        total_cr_in_sales = round((cr_in_total_cs5 + cr_in_total_cs5 + cr_in_total_i5 + cr_in_total_cs12 + cr_in_total_cs12 + cr_in_total_i12 + cr_in_total_cs18 +cr_in_total_cs18 + cr_in_total_cs28 + + cr_in_total_i28 + cr_in_total_i18 + cr_in_total_rcm_cs5 + cr_in_total_rcm_cs5 + cr_in_total_rcm_i5),2)
                    
        total_dr_out_sales = round((dr_out_total_cs5 + dr_out_total_cs5 + dr_out_total_i5 + dr_out_total_cs12 + dr_out_total_cs12 + dr_out_total_i12 + dr_out_total_cs18 + dr_out_total_cs18 + dr_out_total_i18 + dr_out_total_rcm_cs5+ dr_out_total_cs28 + dr_out_total_i28 + dr_out_total_rcm_i5),2)
                    
        total_dr_in_sales = round((dr_in_total_cs5 + dr_in_total_cs5 + dr_in_total_i5 + dr_in_total_cs12 + dr_in_total_cs12 + dr_in_total_i12 + dr_in_total_cs18 +dr_in_total_cs18 + dr_in_total_i18 + dr_in_total_rcm_cs5 + dr_in_total_rcm_cs5 + dr_in_total_rcm_i5  + dr_in_total_rcm_cs5+ dr_in_total_cs28 ),2)
                    
        total_in_purchase = round((in_total_cs5 + in_total_cs5 + in_total_i5 + in_total_cs12 + in_total_cs12 + in_total_i12 + in_total_cs18 +in_total_cs18 + in_total_i18 + in_total_rcm_cs5 + in_total_rcm_cs5 + in_total_rcm_i5 + in_total_cs28 + in_total_i28),2)
        
        
        context['selected_gst_code']= company_gst_code
        context['out_total_cs5']= out_total_cs5
        context['out_total_i5']= out_total_i5
        context['out_total_cs12']= out_total_cs12
        context['out_total_i12']= out_total_i12
        context['out_total_cs18']= out_total_cs18
        context['out_total_cs28']= out_total_cs28
        context['out_total_i18']= out_total_i18
        context['out_total_i28']= out_total_i28
        context['out_total_rcm_cs5']= out_total_rcm_cs5
        context['out_total_rcm_i5']= out_total_rcm_i5
        context['in_total_cs5']= in_total_cs5
        context['in_total_i5']= in_total_i5
        context['in_total_rcm_cs5']= in_total_rcm_cs5
        context['in_total_rcm_i5']= in_total_rcm_i5
        context['in_total_cs12']= in_total_cs12
        context['in_total_i12']= in_total_i12
        context['in_total_cs18']= in_total_cs18
        context['in_total_cs28']= in_total_cs28
        context['in_total_i18']= in_total_i18
        context['in_total_i28']= in_total_i28
        context['total_out_sales']= total_out_sales
        context['total_in_purchase']= total_in_purchase
        
        context['cr_out_total_cs5'] = cr_out_total_cs5
        context['cr_in_total_cs5'] = cr_in_total_cs5
        context['cr_out_total_i5'] = cr_out_total_i5
        context['cr_in_total_i5'] = cr_in_total_i5
        context['cr_out_total_cs12'] = cr_out_total_cs12
        context['cr_in_total_cs12'] = cr_in_total_cs12
        context['cr_out_total_i12'] = cr_out_total_i12
        context['cr_in_total_i12'] = cr_in_total_i12
        context['cr_out_total_cs18'] = cr_out_total_cs18
        context['cr_in_total_cs18'] = cr_in_total_cs18
        context['cr_out_total_cs28'] = cr_out_total_cs28
        context['cr_in_total_cs28'] = cr_in_total_cs28
        context['cr_out_total_i18'] = cr_out_total_i18
        context['cr_in_total_i18'] = cr_in_total_i18
        context['cr_out_total_i28'] = cr_out_total_i28
        context['cr_in_total_i28'] = cr_in_total_i28
        context['cr_out_total_rcm_cs5'] = cr_out_total_rcm_cs5
        context['cr_in_total_rcm_cs5'] = cr_in_total_rcm_cs5
        context['cr_out_total_rcm_i5'] = cr_out_total_rcm_i5
        context['cr_in_total_rcm_i5'] = cr_in_total_rcm_i5
    
        context['dr_out_total_cs5'] = dr_out_total_cs5
        context['dr_in_total_cs5'] = dr_in_total_cs5
        context['dr_out_total_i5'] = dr_out_total_i5
        context['dr_in_total_i5'] = dr_in_total_i5
        context['dr_out_total_cs12'] = dr_out_total_cs12
        context['dr_in_total_cs12'] = dr_in_total_cs12
        context['dr_out_total_i12'] = dr_out_total_i12
        context['dr_in_total_i12'] = dr_in_total_i12
        context['dr_out_total_cs18'] = dr_out_total_cs18
        context['dr_in_total_cs18'] = dr_in_total_cs18
        context['dr_out_total_cs28'] = dr_out_total_cs28
        context['dr_in_total_cs28'] = dr_in_total_cs28
        context['dr_out_total_i18'] = dr_out_total_i18
        context['dr_in_total_i18'] = dr_in_total_i18
        context['dr_in_total_i28'] = dr_in_total_i28
        context['dr_out_total_i28'] = dr_out_total_i28
        context['dr_out_total_rcm_cs5'] = dr_out_total_rcm_cs5
        context['dr_in_total_rcm_cs5'] = dr_in_total_rcm_cs5
        context['dr_out_total_rcm_i5'] = dr_out_total_rcm_i5
        context['dr_in_total_rcm_i5'] = dr_in_total_rcm_i5
        
        context['total_cr_out_sales'] = total_cr_out_sales
        context['total_cr_in_sales'] = total_cr_in_sales
        context['total_dr_out_sales'] = total_dr_out_sales
        context['total_dr_in_sales'] = total_dr_in_sales
        context['total_out'] = round(((total_out_sales - total_cr_out_sales) + total_dr_out_sales),2)
        context['total_in'] = round(((total_in_purchase + total_cr_in_sales) - total_dr_in_sales),2)
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

    context['module']= module
    context['report'] = report
    context['companies_gst_code'] = companies_gst_code
    
    return render(request,'report/gstr3b/gstr3b.html',context)

@login_required(login_url='home:handle_login')
def ageing_analysis(request,module):
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()

    selected_company = ''
    selected_region = request.user.user_account.office.region
    result = []
    report_type = 'D'
    if request.method == 'POST':
        selected_region = request.POST['region']
            
        today = date.today()
        recievables = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','invoice_currency','bill_to__account_manager','bill_to__account_manager__role').prefetch_related('reciept_rec_inv').filter(company_type__region=selected_region).filter(is_einvoiced=True).filter(is_deleted=False).filter(is_cancel=False).all()
        advance_vouchers = RecieptVoucherDetails.objects.select_related('voucher','voucher__company_type').filter(voucher__company_type__region=selected_region).filter(payment_type='OAC').all()
        credit_note = CreditNote.objects.select_related('company_type','invoice_currency','bill_to','bill_to_address').filter(company_type__region=selected_region).filter(is_cancel=False).filter(is_deleted=False).filter(is_einvoiced=True).all()
    
        direct_payables = InvoicePayable.objects.filter(company_type__region=selected_region).filter(is_deleted=False).all()
        payment_advance_vouchers = PaymentVoucherDetails.objects.select_related('voucher','voucher__company_type').filter(voucher__company_type__region=selected_region).filter(payment_type='OAC').all()

        debit_note = DebitNote.objects.select_related('company_type','invoice_currency','bill_from','bill_from_address').filter(company_type__region=selected_region).filter(is_deleted=False).all()
        

        if not request.POST['company'] == 'overall':
            company = Logistic.objects.filter(id=int(request.POST['company'])).first()
            selected_company = company
            recievables = recievables.filter(company_type=company).all()
            advance_vouchers = advance_vouchers.filter(company_type=company).all()
            credit_note = credit_note.filter(company_type=company).all()
            direct_payables = direct_payables.filter(company_type=company).all()
            payment_advance_vouchers = payment_advance_vouchers.filter(voucher__company_type=company).all()
            debit_note = debit_note.filter(company_type=company).all()
            
        for i in recievables:
            count_days = abs((today - i.einvoice_date.date()).days)
            
            flag = 0
            recieved_amount = 0
            for j in i.reciept_rec_inv.all():
                recieved_amount += j.received_amount
                recieved_amount += j.tds_amount
                recieved_amount += j.adjustment_amount
            
            
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR":
                    currency_ex_rate = float(i.currency_ex_rate)
            except:
                pass
        
            net_amount = float(i.net_amount * currency_ex_rate) - float(recieved_amount)
            if net_amount > 0:
                data = list(filter(lambda result: result['party'] == i.bill_to and result['address'] == i.bill_to_address, result))
                for j in data:
                    if j['party'] == i.bill_to and j['address'] == i.bill_to_address:
                        j['invoice'].append(i)
                        flag = 1
                        if count_days >= 0 and count_days < 15:
                            
                            j['start'] = float(j['start']) + float(net_amount)
                        if count_days >= 15 and count_days < 30:
                            j['medium'] = float(j['medium']) + float(net_amount)
                        if count_days >= 30 and count_days < 45:
                            j['high'] = float(j['high']) + float(net_amount)
                        if count_days >= 45:
                            j['greater'] = float(j['greater']) + float(net_amount)
                        
                        j['total'] += float(net_amount)
                        
                        
                if flag == 0:
                    j = {"invoice":[i],"party":i.bill_to,"address":i.bill_to_address,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}
                    
                    if count_days >= 0 and count_days < 15:
                        j['start'] = float(j['start']) + float(net_amount)
                    if count_days >= 15 and count_days < 30:
                    
                        j['medium'] = float(j['medium']) + float(net_amount)
                    if count_days >= 30 and count_days < 45:
                    
                        j['high'] = float(j['high']) + float(net_amount)
                    if count_days >= 45:
                    
                        j['greater'] = float(j['greater']) + float(net_amount)
                        
                    j['total'] = float(net_amount)
                    result.append(j)
            
        for advance in advance_vouchers:
            count_days = abs((today - advance.voucher.voucher_date).days)
            flag = 0
            net_amount = advance.received_amount * (-1)
            data = list(filter(lambda result: result['party'] == advance.party and result['address'] == advance.party_address, result))
            for i in data:
                if i['party'] == advance.party and i['address'] == advance.party_address:
                    flag = 1
                    if count_days >= 0 and count_days < 15:
                        i['start'] = float(i['start']) + float(net_amount)
                    if count_days >= 15 and count_days < 30:
                        i['medium'] = float(i['medium']) + float(net_amount)
                    if count_days >= 30 and count_days < 45:
                        i['high'] = float(i['high']) + float(net_amount)
                    if count_days >= 45:
                        i['greater'] = float(i['greater']) + float(net_amount)
                    
                    i['total'] += float(net_amount)
                    
            if flag == 0:
                i = {"invoice":[i],"party":advance.party,"address":advance.party_address,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}
                
                if count_days >= 0 and count_days < 15:
                    i['start'] = float(i['start']) + float(net_amount)
                if count_days >= 15 and count_days < 30:
                
                    i['medium'] = float(i['medium']) + float(net_amount)
                if count_days >= 30 and count_days < 45:
                
                    i['high'] = float(i['high']) + float(net_amount)
                if count_days >= 45:
                    i['greater'] = float(i['greater']) + float(net_amount)
                    
                i['total'] = float(net_amount)
                result.append(i)
        
        for note in credit_note:
            try:
                if not note.invoice_currency.short_name == "INR":
                    net_amount = (note.net_amount * note.currency_ex_rate)
                else:
                    net_amount = note.net_amount
            except:
                net_amount = note.net_amount
                    
            count_days = abs((today - note.einvoice_date.date()).days)
            flag = 0
            net_amount = net_amount * (-1)
            data = list(filter(lambda result: result['party'] == note.bill_to and result['address'] == note.bill_to_address, result))
            for i in data:
                if i['party'] == note.bill_to and i['address'] == note.bill_to_address:
                    flag = 1
                    if count_days >= 0 and count_days < 15:
                        i['start'] = float(i['start']) + float(net_amount)
                    if count_days >= 15 and count_days < 30:
                        i['medium'] = float(i['medium']) + float(net_amount)
                    if count_days >= 30 and count_days < 45:
                        i['high'] = float(i['high']) + float(net_amount)
                    if count_days >= 45:
                        i['greater'] = float(i['greater']) + float(net_amount)
                    
                    i['total'] += float(net_amount)
                    
            if flag == 0:
                i = {"invoice":[i],"party":note.bill_to,"address":note.bill_to_address,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}
                
                if count_days >= 0 and count_days < 15:
                    i['start'] = float(i['start']) + float(net_amount)
                if count_days >= 15 and count_days < 30:
                
                    i['medium'] = float(i['medium']) + float(net_amount)
                if count_days >= 30 and count_days < 45:
                
                    i['high'] = float(i['high']) + float(net_amount)
                if count_days >= 45:
                    i['greater'] = float(i['greater']) + float(net_amount)
                    
                i['total'] = float(net_amount)
                result.append(i)
        
        for i in direct_payables:
            count_days = abs((today - i.date_of_invoice).days)                
            flag = 0
            paid_amount = 0

            for j in i.pay_payment_inv.all():
                paid_amount += j.paid_amount
                paid_amount += j.tds_amount
                paid_amount += j.adjustment_amount
            
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == "INR":
                    currency_ex_rate = float(i.currency_ex_rate)
            except:
                pass
        
            net_amount = float(i.net_amount * currency_ex_rate * -1) + float(paid_amount)

            

            if not net_amount == 0:
                if i.party_type == "Direct":
                    data = list(filter(lambda result: result['party'] == i.bill_from and result['address'] == i.bill_from_address, result))
                else:
                    data = list(filter(lambda result: result['party'] == i.vendor, result))

                for j in data:
                    if i.party_type == "Direct":
                        if j['party'] == i.bill_from and j['address'] == i.bill_from_address:
                            j['invoice'].append(i)
                            flag = 1
                            if count_days >= 0 and count_days < 15:
                                
                                j['start'] = float(j['start']) + float(net_amount)
                            if count_days >= 15 and count_days < 30:
                                j['medium'] = float(j['medium']) + float(net_amount)
                            if count_days >= 30 and count_days < 45:
                                j['high'] = float(j['high']) + float(net_amount)
                            if count_days >= 45:
                                j['greater'] = float(j['greater']) + float(net_amount)
                            
                            j['total'] += float(net_amount)
                    
                    if i.party_type == "Indirect":
                        if j['party'] == i.vendor:
                            j['invoice'].append(i)
                            flag = 1
                            if count_days >= 0 and count_days < 15:
                                
                                j['start'] = float(j['start']) + float(net_amount)
                            if count_days >= 15 and count_days < 30:
                                j['medium'] = float(j['medium']) + float(net_amount)
                            if count_days >= 30 and count_days < 45:
                                j['high'] = float(j['high']) + float(net_amount)
                            if count_days >= 45:
                                j['greater'] = float(j['greater']) + float(net_amount)
                            
                            j['total'] += float(net_amount)
                        
                        
                if flag == 0:
                    if i.party_type == "Direct":
                        j = {"invoice":[i],"party":i.bill_from,"address":i.bill_from_address,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}
                    else:
                        j = {"invoice":[i],"party":i.vendor,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}

                    
                    if count_days >= 0 and count_days < 15:
                        j['start'] = float(j['start']) + float(net_amount)
                    if count_days >= 15 and count_days < 30:
                    
                        j['medium'] = float(j['medium']) + float(net_amount)
                    if count_days >= 30 and count_days < 45:
                    
                        j['high'] = float(j['high']) + float(net_amount)
                    if count_days >= 45:
                    
                        j['greater'] = float(j['greater']) + float(net_amount)
                        
                    j['total'] = float(net_amount)
                    result.append(j)
        
        for advance in payment_advance_vouchers:
            count_days = abs((today - advance.voucher.voucher_date).days)
            flag = 0
            net_amount = advance.paid_amount
            if advance.party_type == "Direct":
                data = list(filter(lambda result: result['party'] == advance.party and result['address'] == advance.party_address, result))
            if advance.party_type == "Indirect":
                data = list(filter(lambda result: result['party'] == advance.vendor, result))

            for i in data:
                if advance.party_type == "Direct":
                    if i['party'] == advance.party and i['address'] == advance.party_address:
                        flag = 1
                        if count_days >= 0 and count_days < 15:
                            i['start'] = float(i['start']) + float(net_amount)
                        if count_days >= 15 and count_days < 30:
                            i['medium'] = float(i['medium']) + float(net_amount)
                        if count_days >= 30 and count_days < 45:
                            i['high'] = float(i['high']) + float(net_amount)
                        if count_days >= 45:
                            i['greater'] = float(i['greater']) + float(net_amount)
                        
                        i['total'] += float(net_amount)
                if advance.party_type == "Indirect":
                    if i['party'] == advance.vendor:
                        flag = 1
                        if count_days >= 0 and count_days < 15:
                            i['start'] = float(i['start']) + float(net_amount)
                        if count_days >= 15 and count_days < 30:
                            i['medium'] = float(i['medium']) + float(net_amount)
                        if count_days >= 30 and count_days < 45:
                            i['high'] = float(i['high']) + float(net_amount)
                        if count_days >= 45:
                            i['greater'] = float(i['greater']) + float(net_amount)
                        
                        i['total'] += float(net_amount)
                    
            if flag == 0:
                if advance.party_type == "Direct":
                    i = {"invoice":[i],"party":advance.party,"address":advance.party_address,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}

                if advance.party_type == "Indirect":
                    i = {"invoice":[i],"party":advance.vendor,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}
                
                if count_days >= 0 and count_days < 15:
                    i['start'] = float(i['start']) + float(net_amount)
                if count_days >= 15 and count_days < 30:
                
                    i['medium'] = float(i['medium']) + float(net_amount)
                if count_days >= 30 and count_days < 45:
                
                    i['high'] = float(i['high']) + float(net_amount)
                if count_days >= 45:
                    i['greater'] = float(i['greater']) + float(net_amount)
                    
                i['total'] = float(net_amount)
                result.append(i)
        
        for note in debit_note:
            try:
                if not note.invoice_currency.short_name == "INR":
                    net_amount = (note.net_amount * note.currency_ex_rate)
                else:
                    net_amount = note.net_amount
            except:
                net_amount = note.net_amount
                    
            count_days = abs((today - note.date_of_note).days)
            flag = 0
            net_amount = net_amount
            if note.party_type == "Direct":
                data = list(filter(lambda result: result['party'] == note.bill_from and result['address'] == note.bill_from_address, result))
            else:
                data = list(filter(lambda result: result['party'] == note.bill_from_vendor, result))

            for i in data:
                if note.party_type == "Direct":
                    if i['party'] == note.bill_from and i['address'] == note.bill_from_address:
                        flag = 1
                        if count_days >= 0 and count_days < 15:
                            i['start'] = float(i['start']) + float(net_amount)
                        if count_days >= 15 and count_days < 30:
                            i['medium'] = float(i['medium']) + float(net_amount)
                        if count_days >= 30 and count_days < 45:
                            i['high'] = float(i['high']) + float(net_amount)
                        if count_days >= 45:
                            i['greater'] = float(i['greater']) + float(net_amount)
                        
                        i['total'] += float(net_amount)
                    
                else:
                    if i['party'] == note.bill_from_vendor:
                        flag = 1
                        if count_days >= 0 and count_days < 15:
                            i['start'] = float(i['start']) + float(net_amount)
                        if count_days >= 15 and count_days < 30:
                            i['medium'] = float(i['medium']) + float(net_amount)
                        if count_days >= 30 and count_days < 45:
                            i['high'] = float(i['high']) + float(net_amount)
                        if count_days >= 45:
                            i['greater'] = float(i['greater']) + float(net_amount)
                        
                        i['total'] += float(net_amount)

            if flag == 0:
                if note.party_type == "Direct":
                    i = {"invoice":[i],"party":note.bill_from,"address":note.bill_from_address,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}
                else:
                    i = {"invoice":[i],"party":note.bill_from_vendor,"start":0,"medium":0,"high":0,"greater":0,"total":0,"advance_amount":0,"credit_note":0}

                
                if count_days >= 0 and count_days < 15:
                    i['start'] = float(i['start']) + float(net_amount)
                if count_days >= 15 and count_days < 30:
                
                    i['medium'] = float(i['medium']) + float(net_amount)
                if count_days >= 30 and count_days < 45:
                
                    i['high'] = float(i['high']) + float(net_amount)
                if count_days >= 45:
                    i['greater'] = float(i['greater']) + float(net_amount)
                    
                i['total'] = float(net_amount)
                result.append(i)
        
     
                
    try:
        company_detail = Logistic.objects.filter(id=selected_company.id).first().id
    except:
        company_detail = "A"

    context = {
        'module':module,
        'result':result,
        'report_type':report_type,
        'company_detail':company_detail,
        
        'selected_company':selected_company,
        'selected_region':selected_region,
    }
    return render(request,'report/ageing_analysis/ageing_analysis.html',context)

@login_required(login_url='home:handle_login')
def ageing_analysis_details(request,module,type,company,party,range):
    range_map = {
        '1':{'start':0,"end":15},
        '2':{'start':15,"end":30},
        '3':{'start':30,"end":45},
        '4':{'start':45,"end":0},
    }

    if range_map[range]['end'] == 0:
        from_date = datetime.strptime(str(date.today()),'%Y-%m-%d').date() - timedelta(days=range_map[range]['start'])
        to_date = datetime.strptime(str(date.today()),'%Y-%m-%d').date() - timedelta(days=range_map[range]['start'])
    
    else:
        from_date = datetime.strptime(str(date.today()),'%Y-%m-%d').date() - timedelta(days=range_map[range]['end'])
        to_date = datetime.strptime(str(date.today()),'%Y-%m-%d').date() - timedelta(days=range_map[range]['start'])

    

   

    if type == "IC":
        

        party = Vendor.objects.filter(id=int(party)).first()
        bills = IndirectExpense.objects.select_related('company_type','vendor','job_no','invoice_currency').filter(pending_amount__gt=0).filter(vendor__id=party.id).filter(old_invoice=False).filter(is_deleted=False).all()
        if from_date == to_date:
            bills = bills.filter(bill_date__lte=from_date).all()
        else:
            bills = bills.filter(bill_date__range=[from_date,to_date]).all()


    
    elif type == "D":
        party = Party.objects.filter(id=int(party)).first()
        bills = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','invoice_currency','job_no').filter(pending_amount__gt=0).filter(is_einvoiced=True).filter(bill_to__id=party.id).filter(is_deleted=False).filter(is_cancel=False).filter(old_invoice=False).all()
        if from_date == to_date:
            bills = bills.filter(einvoice_date__lt=from_date).all()
        else:
            bills = bills.filter(einvoice_date__range=[from_date,to_date]).all()



    
    elif type == "C":
        party = Party.objects.filter(id=int(party)).first()
        bills = InvoicePayable.objects.select_related('company_type','bill_from','bill_from_address','invoice_currency','job_no').filter(pending_amount__gt=0).filter(bill_from__id=party.id).filter(old_invoice=False).filter(is_deleted=False).all()
        if from_date == to_date:
            bills = bills.filter(date_of_invoice__lt=from_date).all()
        else:
            bills = bills.filter(date_of_invoice__range=[from_date,to_date]).all()

    if not company == "A":
        company = Logistic.objects.filter(id=int(company)).first()
        bills = bills.filter(company_type=company).all()

   
    context = {
        'module':module,
        'bills':bills,
        'type':type,
        'party':party,
        'range':range_map[range]
    }
    return render(request,'report/ageing_analysis/ageing_analysis_details.html',context)

@login_required(login_url='home:handle_login')
def ledger_report(request,module):
    current_year = date.today().year
    accounts = LedgerMaster.objects.all()
    companies = Logistic.objects.all()
    context = {
        'accounts':accounts,
        'current_year':current_year,
        'companies':companies,
        
    }
    selected_company = "All"
    if request.method == 'POST':
        # current_year = request.POST['year']
        company = request.POST['company']
        selected_company = company
       
        if selected_company == "All":
            journal = JournalEntry.objects.filter(account__id = int(request.POST['accounts'])).all()
        else:
            journal = JournalEntry.objects.filter(journal_entry__company_type__id=company).filter(account__id = int(request.POST['accounts'])).all()
            
        total_dr_amount = 0
        total_cr_amount = 0
        
        ledger = LedgerMaster.objects.filter(id=int(request.POST['accounts'])).first()
        
        
        
        for item in journal:
            if item.dr_cr == "Debit":
                total_dr_amount += float(item.amount)
            if item.dr_cr == "Credit":
                total_cr_amount += float(item.amount)
        
        if ledger.balance_in == 'Debit':
            total_dr_amount += ledger.opening_balance
        else:
            total_cr_amount += ledger.opening_balance
            
        
        
        context['journal'] = journal
        
        context['total_dr_amount'] = total_dr_amount
        context['total_cr_amount'] = total_cr_amount
        context['current_year'] = current_year
   
    context['today_date'] = date.today()
    context['module'] = module
    context['selected_company'] = selected_company

    return render(request,'report/ledger/ledger_report.html',context)

@login_required(login_url='home:handle_login')
def purchase_account(request,module):
    context ={}
    check_permissions(request,module)
    choose_company = "All"
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']
        invoices = InvoicePayableDetail.objects.filter(invoice_payable__date_of_invoice__gte=from_date).filter(invoice_payable__date_of_invoice__lte=to_date).filter(invoice_payable__party_type="Direct").all()
        
        indirect_expense = InvoicePayableDetail.objects.filter(invoice_payable__date_of_invoice__gte=from_date).filter(invoice_payable__date_of_invoice__lte=to_date).filter(invoice_payable__party_type="Indirect").all()
       
        if not choose_company == "All":
            choose_company = int(choose_company)
            invoices = invoices.filter(invoice_payable__company_type__id=int(choose_company)).all()
        report = invoices.values(
                    'billing_head__category',
                    'billing_head__billing_head',
                    ).annotate(**{
                    
                    
                    'non_taxable_amount': Sum(Case(
                            When (
                            gst=0,
                            then=F('amount'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    'taxable_intra_amount': Sum(Case(
                            When (
                            invoice_payable__bill_from_address__corp_state__gst_code=F('invoice_payable__company_type__company_gst_code'),
                                then=F('amount'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    'taxable_inter_amount': Sum(Case(
                            When (
                            ~Q(invoice_payable__bill_from_address__corp_state__gst_code=F('invoice_payable__company_type__company_gst_code')),
                                then=F('amount'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    }
            )
        
        indirect_expense_report = indirect_expense.values(
                    'billing_head__category',
                    'billing_head__billing_head',
                    ).annotate(**{
                    
                    
                    'non_taxable_amount': Sum(Case(
                            When (
                            gst=0,
                            then=F('amount'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    'taxable_intra_amount': Sum(Case(
                            When (
                            invoice_payable__bill_from_address__corp_state__gst_code=F('invoice_payable__company_type__company_gst_code'),
                                then=F('amount'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    'taxable_inter_amount': Sum(Case(
                            When (
                            ~Q(invoice_payable__bill_from_address__corp_state__gst_code=F('invoice_payable__company_type__company_gst_code')),
                                then=F('amount'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    }
            )
        
        final_report = [
            {
                'head_name':'NON TAXABLE',
                'amount':0,
                'items':[],
            },
            {
                'head_name':'TAXABLE INTER',
                'amount':0,
                'items':[],
            },
            {
                'head_name':'TAXABLE INTRA',
                'amount':0,
                'items':[],
            },
        ]
        
        final_report_indirect = [
            {
                'head_name':'NON TAXABLE',
                'amount':0,
                'items':[],
            },
            {
                'head_name':'TAXABLE INTER',
                'amount':0,
                'items':[],
            },
            {
                'head_name':'TAXABLE INTRA',
                'amount':0,
                'items':[],
            },
        ]
        
        direct_expense_sum = 0
        for i in report:
           
            for j in final_report:
                if j['head_name'] == 'NON TAXABLE' and i['non_taxable_amount'] > 0:
                    direct_expense_sum += i['non_taxable_amount']
                    j['amount'] += i['non_taxable_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['non_taxable_amount'],
                        })               
                if  j['head_name'] == 'TAXABLE INTRA' and i['taxable_intra_amount'] > 0:
                    direct_expense_sum += i['taxable_intra_amount']
                    j['amount'] += i['taxable_intra_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['taxable_intra_amount'],
                        })    
                   
                    
                if  j['head_name'] == 'TAXABLE INTER' and i['taxable_inter_amount'] > 0:
                    direct_expense_sum += i['taxable_inter_amount']
                    j['amount'] += i['taxable_inter_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['taxable_inter_amount'],
                    })    
        indirect_expense_sum = 0        
        for i in indirect_expense_report:
           
            for j in final_report_indirect:
                if j['head_name'] == 'NON TAXABLE' and i['non_taxable_amount'] > 0:
                    indirect_expense_sum += i['non_taxable_amount']
                    j['amount'] += i['non_taxable_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['non_taxable_amount'],
                        })               
                if  j['head_name'] == 'TAXABLE INTRA' and i['taxable_intra_amount'] > 0:
                    indirect_expense_sum += i['taxable_intra_amount']
                    j['amount'] += i['taxable_intra_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['taxable_intra_amount'],
                        })    
                   
                    
                if  j['head_name'] == 'TAXABLE INTER' and i['taxable_inter_amount'] > 0:
                    indirect_expense_sum += i['taxable_inter_amount']
                    j['amount'] += i['taxable_inter_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['taxable_inter_amount'],
                    })    
                    
        context['direct_expense_sum'] = direct_expense_sum
        context['indirect_expense_sum'] = indirect_expense_sum
        context['report'] = final_report
        context['final_report_indirect'] = final_report_indirect
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")
       
       
        context['choose_company']= choose_company
      
    
    context['module'] = module


    return render(request,'report/purchase_account/purchase.html',context)
    
@login_required(login_url='home:handle_login')
def sales_account(request,module):
    context ={}
    check_permissions(request,module)
    choose_company = "All"
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']
        invoices = InvoiceReceivableDetail.objects.filter(invoice_receivable__einvoice_date__gte=from_date).filter(invoice_receivable__einvoice_date__lte=to_date).all()
        
        if not choose_company == "All":
            choose_company = int(choose_company)
            invoices = invoices.filter(invoice_receivable__company_type__id=int(choose_company)).all()
            
        report = invoices.values(
                    'billing_head__category',
                    'billing_head__billing_head',
                    ).annotate(**{
                    
                    
                    'non_taxable_amount': Sum(Case(
                            When (
                            gst=0,
                            then=F('amount') * F('invoice_receivable__currency_ex_rate'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    'taxable_intra_amount': Sum(Case(
                            When (
                            invoice_receivable__bill_to_address__corp_state__gst_code=F('invoice_receivable__company_type__company_gst_code'),
                                then=F('amount') * F('invoice_receivable__currency_ex_rate'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    'taxable_inter_amount': Sum(Case(
                            When (
                            ~Q(invoice_receivable__bill_to_address__corp_state__gst_code=F('invoice_receivable__company_type__company_gst_code')),
                                then=F('amount') * F('invoice_receivable__currency_ex_rate'),
                            ),
                        output_field=FloatField(),
                        default = 0
                            )
                        ),
                    }
            )
        
        final_report = [
            {
                'head_name':'NON TAXABLE',
                'amount':0,
                'items':[],
            },
            {
                'head_name':'TAXABLE INTER',
                'amount':0,
                'items':[],
            },
            {
                'head_name':'TAXABLE INTRA',
                'amount':0,
                'items':[],
            },
        ]
        
        
       
        for i in report:
           
            for j in final_report:
                if j['head_name'] == 'NON TAXABLE' and i['non_taxable_amount'] > 0:
                   
                    j['amount'] += i['non_taxable_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['non_taxable_amount'],
                        })               
                if  j['head_name'] == 'TAXABLE INTRA' and i['taxable_intra_amount'] > 0:
                    
                    j['amount'] += i['taxable_intra_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['taxable_intra_amount'],
                        })    
                   
                    
                if  j['head_name'] == 'TAXABLE INTER' and i['taxable_inter_amount'] > 0:
                   
                    j['amount'] += i['taxable_inter_amount']
                    j['items'].append({
                            'item_name':i['billing_head__billing_head'],
                            'amount':i['taxable_inter_amount'],
                    })    
       
            
        
      
        context['report'] = final_report
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")
       
       
        context['choose_company']= choose_company
      
    
    context['module'] = module


    return render(request,'report/sales_account/sales.html',context)


@login_required(login_url='home:handle_login')
def ledger_category_transactions(request,module,company,from_date,to_date,id,profit_loss=None,detail_id=None,detail=0,type=None,expanded=0):
    id_list = [id]

    if profit_loss == "DP":
        # 14 = Direct Expenses
        # 15 = Direct Income
        # 16 = Indirect Expenses
        # 17 = Indirect Income
        # 23 = Direct Purchase
        # 24 = Direct Sales
        id_list = [14,23]

    if profit_loss == "DS":
        id_list = [15,24]
   
    if profit_loss == "IE":
        id_list = [16]
    
    if profit_loss == "II":
        id_list = [17]
    
    if profit_loss == "A":
        id_list = [14,15,16,17,23,24]

    transactions = Voucher.objects.filter(category__id__in=id_list).filter(date__gte=from_date).filter(date__lte=to_date).select_related('salary','salary__employee','indirect_expense','indirect_expense__vendor','sales_invoice','sales_invoice__bill_to','sales_invoice__bill_to_address','purchase_invoice','purchase_invoice__bill_from','purchase_invoice__bill_from_address','crn','crn__bill_to','crn__bill_to_address','drn','drn__bill_from','drn__bill_from_address','receipt','receipt__party_name','receipt__party_address','receipt__vendor','payment','payment__party_name','payment__party_address','contra','contra__account_from','contra__account_to','contra__cash','loan','loan_record')
    if not (company) == "ALL" or not company == "All" or not company == "A":
        try:
            transactions = transactions.filter(company_type__id=int(company))
        except:
            pass

    dr_total = 0
    cr_total = 0

    empty_transactions = transactions
    for i in empty_transactions:
        if i.party or i.vendor or i.bank or i.cash:
            empty_transactions = empty_transactions.exclude(id=i.id)

    
    if detail_id and type:
        for i in id_list:
            category = LedgerCategory.objects.filter(id=int(i)).first()
            if category.liability or category.asset:
                if str(type).endswith('P'):
                    transactions = transactions.filter(party__id=detail_id)
                    empty_transactions = empty_transactions.filter(Q(sales_invoice__bill_to__id=detail_id)|Q(crn__bill_to__id=detail_id)|Q(drn__bill_from__id=detail_id)|Q(purchase_invoice__bill_from__id=detail_id))
                if str(type).endswith('V'):
                    transactions = transactions.filter(vendor__id=detail_id)
                    empty_transactions = empty_transactions.filter(Q(drn__bill_from_vendor__id=detail_id)|Q(purchase_invoice__vendor__id=detail_id))
                if str(type).endswith('B'):
                    transactions = transactions.filter(bank__id=detail_id)
                if str(type).endswith('C'):
                    transactions = transactions.filter(cash__id=detail_id)
                
                if str(type).endswith('L'):
                    transactions = transactions.filter(ledger__id=detail_id)
                
                transactions = list(set(chain(empty_transactions,transactions)))

            if category.nominal:
                if str(type).endswith('SE'):
                    transactions = transactions.filter(salary__employee__id=detail_id)
                if str(type).endswith('SP') or str(type).endswith('CRNP'):
                    transactions = transactions.filter(Q(crn_details__billing_head__id=detail_id)|Q(sales_invoice_details__billing_head__id=detail_id))
                
                if str(type).endswith('DRNP') or str(type).endswith('PP') or str(type).endswith('DRNV') or str(type).endswith('PV') :
                    transactions = transactions.filter(Q(drn_details__billing_head__id=detail_id)|Q(purchase_invoice_details__billing_head__id=detail_id))
                
           
        

    report_dict = defaultdict(lambda: {'data': None, 'id': "", 'particulars': "", 'voucher_type': '', 'debit': 0, 'credit': 0,'type':'','url':''})

    for data in transactions:

        if data.party_opening:
            if detail == 0:
                particulars = f'{data.party}'
                obj = report_dict[particulars]
                obj['id'] = data.party.id
                obj['type'] = "P"
               

            else:
                particulars =  f"{data.party}"
                obj = report_dict[particulars]
                obj['id'] = data.party.id
                obj['url'] = reverse('masters:party_update',kwargs={'module':module,'id':data.party.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Opening'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.ledger_opening:
            if detail == 0:
                particulars = f'{data.ledger}'
                obj = report_dict[particulars]
                obj['id'] = data.ledger.id
                obj['type'] = "L"
               

            else:
                particulars =  f"{data.ledger}"
                obj = report_dict[particulars]
                obj['id'] = data.ledger.id
                obj['url'] = reverse('masters:ledger_update',kwargs={'module':module,'id':data.ledger.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Opening'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
       
        if data.bank_opening:
            if detail == 0:
                particulars = f'{data.bank}'
                obj = report_dict[particulars]
                obj['id'] = data.bank.id
                obj['type'] = "B"
               

            else:
                particulars =  f"{data.bank}"
                obj = report_dict[particulars]
                obj['id'] = data.bank.id
                obj['url'] = reverse('masters:bank_update',kwargs={'module':module,'id':data.bank.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Opening'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.vendor_opening:
            if detail == 0:
                particulars = f'{data.vendor}'
                obj = report_dict[particulars]
                obj['id'] = data.vendor.id
                obj['type'] = "V"
               

            else:
                particulars =  f"{data.vendor}"
                obj = report_dict[particulars]
                obj['id'] = data.vendor.id
                obj['url'] = reverse('masters:vendor_update',kwargs={'module':module,'id':data.vendor.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Opening'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.journal_entry:
            if detail == 0:
                if data.ledger:
                    particulars = f'{data.ledger}'
                if data.party:
                    particulars = f'{data.party}'
                if data.vendor:
                    particulars = f'{data.vendor}'
                obj = report_dict[particulars]

                if data.ledger:
                    obj['id'] = data.ledger.id
                    obj['type'] = "L"
                if data.party:
                    obj['id'] = data.party.id
                    obj['type'] = "P"
                if data.vendor:
                    obj['id'] = data.vendor.id
                    obj['type'] = "V"

            else:
                if data.ledger:
                    particulars = f'{data.ledger}'
                if data.party:
                    particulars = f'{data.party}'
                if data.vendor:
                    particulars = f'{data.vendor}'

                obj = report_dict[f'{particulars}-{data.journal_entry.id}']
                if data.ledger:
                    obj['id'] = data.ledger.id
                    obj['type'] = "L"
                if data.party:
                    obj['id'] = data.party.id
                    obj['type'] = "P"
                if data.vendor:
                    obj['id'] = data.vendor.id
                    obj['type'] = "V"


                obj['url'] = reverse('accounting:journal_update',kwargs={'module':module,'id':data.journal.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Journal'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount        
       
        if data.sales_invoice:

            if detail == 0:
                particulars = f'{data.sales_invoice.bill_to}'
                obj = report_dict[particulars]

                obj['id'] = data.sales_invoice.bill_to.id
                obj['type'] = "SP"
            else:
                particulars =  f"{data.sales_invoice.final_invoice_no}"
                obj = report_dict[f'{particulars}-{data.id}']

                obj['id'] = data.sales_invoice.id

                obj['url'] = reverse('accounting:recievable_invoice_pdf',kwargs={'id':data.sales_invoice.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Sales Invoice'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.sales_invoice_details:

            if detail == 0:
                if data.gst_type:
                    particulars = f'{data.gst_type}'
                    obj = report_dict[particulars]
                    # obj['id'] = data.sales_invoice_details.billing_head.id
                    obj['type'] = "SP"
                else:
                    particulars = f'{data.sales_invoice_details.billing_head}'
                    obj = report_dict[particulars]

                    obj['id'] = data.sales_invoice_details.billing_head.id
                    obj['type'] = "SP"
            else:
                particulars =  f"{data.sales_invoice_details.invoice_receivable.final_invoice_no}"
                obj = report_dict[particulars]

                obj['id'] = data.sales_invoice_details.invoice_receivable.id

                obj['url'] = reverse('accounting:recievable_invoice_pdf',kwargs={'id':obj['id']})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Sales Invoice'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount

        if data.crn:
            if detail == 0:
                particulars = f'{data.crn.bill_to}'
                obj = report_dict[particulars]

                obj['id'] = data.crn.bill_to.id
                obj['type'] = "CRNP"
            else:
                particulars = f"{data.crn.final_invoice_no}"

                obj = report_dict[f'{particulars}-{data.id}']
                obj['id'] = data.crn.id
                obj['url'] = reverse('accounting:credit_note_pdf',kwargs={'id':data.crn.id,'print':0})
                
            obj['data'] = data
            
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Credit Note'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.crn_details:
            if detail == 0:
                if data.gst_type:
                    particulars = f'{data.gst_type}'
                    obj = report_dict[particulars]
                    # obj['id'] = data.sales_invoice_details.billing_head.id
                    obj['type'] = "CRNP"
                else:

                    particulars = f'{data.crn_details.billing_head}'
                    obj = report_dict[particulars]

                    obj['id'] = data.crn_details.billing_head.id
                    obj['type'] = "CRNP"
            else:
                particulars = f"{data.crn_details.credit_note.final_invoice_no}"

                obj = report_dict[particulars]
                obj['id'] = data.crn_details.credit_note.id
                obj['url'] = reverse('accounting:credit_note_pdf',kwargs={'id':data.crn_details.credit_note.id,'print':0})
                
            obj['data'] = data
            
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Credit Note'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        
        if data.drn:
            if detail == 0:
                if data.drn.party_type == "Direct":
                    particulars = f'{data.drn.bill_from}'
                else:
                    particulars = f'{data.drn.bill_from_vendor}'

                obj = report_dict[particulars]

                if data.drn.party_type == "Direct":
                    obj['id'] = data.drn.bill_from.id
                    obj['type'] = "DRNP"
                else:
                    obj['id'] = data.drn.bill_from_vendor.id
                    obj['type'] = "DRNV"

            else:
                particulars = f"{data.drn.debit_note_no}"
                obj = report_dict[f'{particulars}-{data.id}']
                obj['id'] = data.drn.id
                obj['url'] = reverse('accounting:debit_note_update',kwargs={'module':module,'id':data.drn.id})

            obj['data'] = data

            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Debit Note'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] = data.amount
                cr_total += data.amount
    
        if data.drn_details:
            if detail == 0:
                if data.gst_type:
                    particulars = f'{data.gst_type}'
                    obj = report_dict[particulars]
                    # obj['id'] = data.sales_invoice_details.billing_head.id
                    obj['type'] = "DRNP"
                else:

                    particulars = f'{data.drn_details.billing_head}'
                    obj = report_dict[particulars]

                    obj['id'] = data.drn_details.billing_head.id
                    obj['type'] = "DRNP"
            else:
                particulars = f"{data.drn_details.debit_note.debit_note_no}"

                obj = report_dict[particulars]
                obj['id'] = data.drn_details.debit_note.id
                obj['url'] = reverse('accounting:credit_note_pdf',kwargs={'id':obj['id'],'print':0})
                
            obj['data'] = data
            
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Debit Note'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        
        if data.purchase_invoice:
            if detail == 0:
                if data.tds_section:
                    particulars = f'{data.tds_section}'
                    obj = report_dict[particulars]
                    # obj['id'] = data.sales_invoice_details.billing_head.id
                    obj['type'] = "PV"
                else:
                    if data.purchase_invoice.party_type == "Direct":
                        particulars = f'{data.purchase_invoice.bill_from}'
                    else:
                        particulars = f'{data.purchase_invoice.vendor}'

                    obj = report_dict[particulars]

                    if data.purchase_invoice.party_type == "Direct":
                        obj['id'] = data.purchase_invoice.bill_from.id
                        obj['type'] = "PP"
                    else:
                        obj['id'] = data.purchase_invoice.vendor.id
                        obj['type'] = "PV"

            else:
                particulars =  f"{data.purchase_invoice.purchase_invoice_no}"
                obj = report_dict[f'{particulars}-{data.id}']
                obj['id'] = data.purchase_invoice.id
                obj['url'] = reverse('accounting:invoice_payable_update',kwargs={'module':module,'id':data.purchase_invoice.id})

            

            obj['data'] = data
            

            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Purchase Invoice'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.purchase_invoice_details:
            if detail == 0:
                if data.gst_type:
                    particulars = f'{data.gst_type}'
                    obj = report_dict[particulars]
                    # obj['id'] = data.sales_invoice_details.billing_head.id
                    obj['type'] = "PV"

                elif data.tds_section:
                    particulars = f'{data.tds_section}'
                    obj = report_dict[particulars]
                    # obj['id'] = data.sales_invoice_details.billing_head.id
                    obj['type'] = "PV"

                else:
                    particulars = f'{data.purchase_invoice_details.billing_head}'
                    obj = report_dict[particulars]
                    obj['id'] = data.purchase_invoice_details.billing_head.id
                    obj['type'] = "PV"

            else:
                particulars =  f"{data.purchase_invoice_details.invoice_payable.purchase_invoice_no}"
                obj = report_dict[f'{particulars}-{data.id}']
                obj['id'] = data.purchase_invoice_details.invoice_payable.id
                obj['url'] = reverse('accounting:invoice_payable_update',kwargs={'module':module,'id':data.purchase_invoice_details.invoice_payable.id})

            obj['data'] = data
            
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Purchase Invoice C.'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.receipt:
            flag = False
            if detail == 0:
                if data.party:
                    particulars = f'{data.party}'
                elif data.bank:
                    particulars = f'{data.bank}'
                elif data.cash:
                    particulars = f'{data.cash}'
                elif data.vendor:
                    particulars = f'{data.vendor}'
                elif data.ledger:
                    particulars = f'{data.ledger}'
                elif data.tds_section:
                    particulars = f'{data.tds_section}'
                else:
                    particulars = f"{data.receipt.instrument_no}"
                    flag = True
                   
                obj = report_dict[particulars]

                if flag:
                    obj['id'] = data.receipt.id
                    obj['url'] = reverse('accounting:reciept_voucher_update',kwargs={'module':module,'id':data.receipt.id})


                if data.party:
                    obj['id'] = data.party.id
                    obj['type'] = "RVP"
                elif data.bank:
                    obj['id'] = data.bank.id
                    obj['type'] = "RVB"
                elif data.ledger:
                    obj['id'] = data.ledger.id
                    obj['type'] = "RVL"
                elif data.vendor:
                    obj['id'] = data.vendor.id
                    obj['type'] = "RVV"
                

            else:
                particulars =  f"{data.receipt.instrument_no}"
                obj = report_dict[f'{particulars}-{data.id}']
                obj['id'] = data.receipt.id
                obj['url'] = reverse('accounting:reciept_voucher_update',kwargs={'module':module,'id':data.receipt.id})

            

            obj['data'] = data
            
            obj['particulars'] = f"{particulars}"
        
            obj['voucher_type'] = 'Reciept'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
    
        if data.payment:
            flag = False
            if detail == 0:
                if data.party:
                    particulars = f'{data.party}'
                elif data.bank:
                    particulars = f'{data.bank}'
                elif data.cash:
                    particulars = f'{data.cash}'
                elif data.vendor:
                    particulars = f'{data.vendor}'
                elif data.ledger:
                    particulars = f'{data.ledger}'
                elif data.tds_section:
                    particulars = f'{data.tds_section}'
                else:
                    particulars = f"{data.payment.instrument_no}"
                    flag = True


                obj = report_dict[particulars]

                if flag:
                    obj['id'] = data.payment.id
                    obj['url'] = reverse('accounting:payment_voucher_update',kwargs={'module':module,'id':data.payment.id})


                if data.party:
                    obj['id'] = data.party.id
                    obj['type'] = "PVP"
                elif data.bank:
                    obj['id'] = data.bank.id
                    obj['type'] = "PVB"
                elif data.ledger:
                    obj['id'] = data.ledger.id
                    obj['type'] = "PVL"
                elif data.vendor:
                    obj['id'] = data.vendor.id
                    obj['type'] = "PVV"

            else:
                particulars =  f"{data.payment.instrument_no}"
                obj = report_dict[f'{particulars}-{data.id}']
                obj['id'] = data.payment.id
                obj['url'] = reverse('accounting:payment_voucher_update',kwargs={'module':module,'id':data.payment.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"
            obj['voucher_type'] = 'Payment'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
        if data.contra:
            if detail == 0:
                if data.bank:
                    particulars = f'{data.bank}'
                elif data.cash:
                    particulars = f'{data.cash}'
                else:
                    particulars = "Contra Voucher"

                obj = report_dict[particulars]

                if data.bank:
                    obj['id'] = f'{data.bank.id}'
                    obj['type'] = f'CB'
                if data.cash:
                    obj['id'] = f'{data.cash.id}'
                    obj['type'] = f'CC'



            else:
                particulars = f'{data.contra.instrument_no}'
                obj = report_dict[f'{particulars}-{data.id}']
                obj['id'] = f'{data.contra.id}'
                obj['url'] = reverse('accounting:contra_voucher_update',kwargs={'module':module,'id':data.contra.id})

            obj['data'] = data
            obj['particulars'] = f"{particulars}"

            obj['voucher_type'] = 'Contra'
            if data.dr_cr == "Debit":
                obj['debit'] += data.amount
                dr_total += data.amount
            else:
                obj['credit'] += data.amount
                cr_total += data.amount
        
       
    report = list(report_dict.values())

    if expanded == 1:
        return report
    
    context = {
        'module':module,
        'dr_total':dr_total,
        'cr_total':cr_total,
        'report':report,
        'transactions':transactions,
        'to_date':datetime.strptime(str(to_date),"%Y-%m-%d").date(),
        'from_date':datetime.strptime(str(from_date),"%Y-%m-%d").date(),
        'company':company,
        'detail':detail,
        'profit_loss':profit_loss,
 
    }

    if id:
        context['category'] = LedgerCategory.objects.filter(id=int(id)).first()
      
   
    return render(request,'report/ledger_category_transaction/transactions.html',context)



def set_expanded_ledger(request,module,company,from_date,to_date,report_list,c_depth=0,total_report=None):
    for i in report_list:
        ledger_report = ledger_category_transactions(request,module,company,from_date,to_date,id=i['category'].id,detail_id=None,detail=0,expanded=1)
        
        
       
        if total_report:
            
            total_report['debit'] += i['dr_total']
            total_report['credit'] += i['cr_total']

            if i['opening_in'] == "Debit":
                total_report['opening'] += i['opening']
            else:
                total_report['opening'] -= i['opening']
           
            if i['closing_in'] == "Debit":
                total_report['closing'] += i['closing']
            else:
                total_report['closing'] -= i['closing']

        

        
        i['ledger_report'] = ledger_report
        
        set_expanded_ledger(request,module,company,from_date,to_date,i['report'],c_depth)

def get_child_ctageories(category,company,from_date,to_date,report,depth=0,category_obj=None):
    current_category = {
        'category':category,
        'dr_total':0,
        'cr_total':0,
        'total':0,
        'opening':0,
        'closing':0,
        'closing_in':"Debit",
        'opening_in':"Debit",
        'balance_in':"Debit",
        'depth':depth,
        'report':[],
        'parent':1
    }
    # Before From Date Query
    opening_dr_vouchers = Voucher.objects.filter(category=category).filter(date__lt=from_date).filter(dr_cr='Debit').aggregate(total=Sum('amount'))
    opening_cr_vouchers = Voucher.objects.filter(category=category).filter(date__lt=from_date).filter(dr_cr='Credit').aggregate(total=Sum('amount'))
    
    # To Get Transaction Between From date and to date
    dr_vouchers = Voucher.objects.filter(category=category).filter(date__gte=from_date).filter(date__lte=to_date).filter(dr_cr='Debit').aggregate(total=Sum('amount'))
    cr_vouchers = Voucher.objects.filter(category=category).filter(date__gte=from_date).filter(date__lte=to_date).filter(dr_cr='Credit').aggregate(total=Sum('amount'))
    
    opening_dr_sum = 0
    opening_cr_sum = 0
    
    closing_dr_sum = 0
    closing_cr_sum = 0
    
    dr_sum = 0
    cr_sum = 0

    # Calculating Opening Debit and Credit Sum With Opening balance
    try:
        opening_dr_sum = opening_dr_vouchers['total'] or 0
    except:
        pass
    try:
        opening_cr_sum = opening_cr_vouchers['total'] or 0
    except:
        pass
    
    opening_balance = opening_dr_sum - opening_cr_sum
    if opening_balance >= 0:
        current_category['opening'] = round(opening_balance,2)
       
    else:
        current_category['opening_in'] = "Credit"
        current_category['opening'] = round(abs(opening_balance),2)
   
    # Calculating actual transaction Debit and Credit Sum
    try:
        dr_sum = dr_vouchers['total'] or 0
    except:
        pass
    try:
        cr_sum = cr_vouchers['total'] or 0
    except:
        pass

    balance = dr_sum - cr_sum
    current_category['dr_total'] = round(dr_sum,2)
    current_category['cr_total'] =  round(abs(cr_sum),2)

    # if balance >= 0:
    #     current_category['total'] = round(balance,2)
    # else:
    #     current_category['balance_in'] = "Credit"
    #     current_category['total'] = round(abs(balance),2)
       

    # Calculating closing balance between opening and actual transactions Debit and Credit
    closing_balance = opening_balance + balance
    if closing_balance >= 0:
        current_category['closing_in'] = "Debit"
        current_category['closing'] = round(closing_balance,2)
       
    else:
        current_category['closing_in'] = "Credit"
        current_category['closing'] = round(abs(closing_balance),2)
       

    report.append(current_category)
   
    if category_obj:
        parent_opening_dr = 0
        parent_opening_cr = 0

        if category_obj['opening_in'] == "Debit":
            parent_opening_dr += category_obj['opening']
        else:
            parent_opening_cr += category_obj['opening']

        if opening_balance >= 0:
            parent_opening_dr += round(opening_balance,2)
        
        else:
            parent_opening_cr += round(abs(opening_balance),2)

        parent_opeing_balance = parent_opening_dr - parent_opening_cr

       
        if parent_opeing_balance >= 0:
            category_obj['opening'] = round(parent_opeing_balance,2)
            category_obj['opening_in'] = "Debit"
        else:
            category_obj['opening'] = round(abs(parent_opeing_balance),2)
            category_obj['opening_in'] = "Credit"
    

    if category_obj:
        parent_dr = round(category_obj['dr_total'] + (dr_sum),2)
        category_obj['dr_total'] = round(parent_dr,2)
        parent_cr = abs(round(category_obj['cr_total'] + (cr_sum),2))
        category_obj['cr_total'] = round(abs(parent_cr),2)

        # if parent_balance >= 0:
        #     category_obj['total'] = round(parent_balance,2)
        #     category_obj['balance_in'] = "Debit"
        # else:
        #     category_obj['total'] = round(abs(parent_balance),2)
        #     category_obj['balance_in'] = "Credit"



    if category_obj:
        parent_closing_dr = 0
        parent_closing_cr = 0

        if category_obj['closing_in'] == "Debit":
            parent_closing_dr += category_obj['closing']
        else:
            parent_closing_cr += category_obj['closing']

        if closing_balance >= 0:
            parent_closing_dr += round(closing_balance,2)
        
        else:
            parent_closing_cr += round(abs(closing_balance),2)

        parent_closing_balance = parent_closing_dr - parent_closing_cr

       
        if parent_closing_balance >= 0:
            category_obj['closing'] = round(parent_closing_balance,2)
            category_obj['closing_in'] = "Debit"
        else:
            category_obj['closing'] = round(abs(parent_closing_balance),2)
            category_obj['closing_in'] = "Credit"

    # print(depth*" ",category.name,current_category['closing'])
    
    for i in category.parent.all():

        get_child_ctageories(i,company,from_date,to_date,current_category['report'],depth=depth+1,category_obj=current_category)

def get_balance_sheet_child_ctageories(category,company,from_date,to_date,report,depth=0,category_obj=None,type=None,reverse=False):
    current_category = {
        'category':category,
        'dr_total':0,
        'cr_total':0,
        'total':0,
        'opening':0,
        'closing':0,
        'closing_in':"Debit",
        'opening_in':"Debit",
        'balance_in':"Debit",
        'depth':depth,
        'report':[],
        'parent':1
    }
    # Before From Date Query
    
    
    # To Get Transaction Between From date and to date
    dr_vouchers = Voucher.objects.filter(category=category).filter(date__gte=from_date).filter(date__lte=to_date).filter(dr_cr='Debit').aggregate(total=Sum('amount'))
    cr_vouchers = Voucher.objects.filter(category=category).filter(date__gte=from_date).filter(date__lte=to_date).filter(dr_cr='Credit').aggregate(total=Sum('amount'))
    
    dr_sum = 0
    cr_sum = 0

    # Calculating actual transaction Debit and Credit Sum
    try:
        dr_sum = dr_vouchers['total'] or 0
    except:
        pass
    try:
        cr_sum = cr_vouchers['total'] or 0
    except:
        pass

    if type == "L" or reverse:
        balance = cr_sum - dr_sum
    else:
        balance = dr_sum - cr_sum

    current_category['dr_total'] = round(dr_sum,2)
    current_category['cr_total'] =  round((cr_sum),2)
    current_category['total'] = round(balance,2)

    
    # Calculating closing balance between opening and actual transactions Debit and Credit
    
    report.append(current_category)
   
        

    if category_obj:
        category_obj['total'] = round((category_obj['total'] + balance),2)
       

      
    # print(depth*" ",category.name,current_category['closing'])
    
    for i in category.parent.all():
        get_balance_sheet_child_ctageories(i,company,from_date,to_date,current_category['report'],depth=depth+1,category_obj=current_category,type=type)


# Trial Balance Report
@login_required(login_url='home:handle_login')
def trial_balance_report_category(request,module):
    for i in InvoiceReceivable.objects.filter(is_deleted=False):
        i.save()
    for i in InvoicePayable.objects.filter(is_deleted=False).all():
        i.save()
    for i in CreditNote.objects.filter(is_deleted=False).filter(is_einvoiced=True):
        i.save()
    for i in DebitNote.objects.filter(is_deleted=False):
        i.save()

    for i in Journal.objects.filter(is_deleted=False):
        i.save()
    for i in PaymentVoucher.objects.filter(is_deleted=False):
        i.save()
    for i in RecieptVoucher.objects.filter(is_deleted=False):
        i.save()
    for i in ContraVoucher.objects.filter(is_deleted=False):
        i.save()
    
    current_year = datetime.now().year
    to_current_year = datetime.now().year + 1
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
        to_current_year -= 1

    from_date = datetime.strptime(f'{current_year}-04-01',"%Y-%m-%d").date()
    to_date = datetime.strptime(f'{to_current_year}-03-31',"%Y-%m-%d").date()
    
    
    report_list = []
    company = "ALL"
    expanded = 0
    if request.method == 'POST':
        
        
        report_list = []
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company = request.POST['company']
        expanded = int(request.POST['expanded'])

        if not company == "ALL":
            company = Logistic.objects.filter(id=int(company)).first()
        
        all_ledger = LedgerCategory.objects.select_related('child').filter(child=None).prefetch_related('parent').all()
        
        for i in all_ledger:
            get_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=report_list)

        if expanded == 1:
            c_depth = 0
            set_expanded_ledger(request,module,company,from_date,to_date,report_list,c_depth)

    context = {
        
        'expanded':expanded,
        'report_list':report_list,
        'module':module,
        'to_date':datetime.strptime(str(to_date),"%Y-%m-%d").date(),
        'from_date':datetime.strptime(str(from_date),"%Y-%m-%d").date(),
        'company':company,
 
    }
   
    return render(request,'report/trial_balance_report/trial_balance_report.html',context)



# Profit Loss Report
@login_required(login_url='home:handle_login')
def profit_loss_report(request,module):
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    from_date = date(current_year,4,1)
    to_date = date(current_year+1,3,31)
    company = request.user.user_account.office.id
    
    selected_region = request.user.user_account.office.region
    
    context = {
        'current_year':current_year,
        'module':module,
        'selected_region':selected_region
    }
    context['company'] = company
    direct_sales_report_list = []
    direct_purchase_report_list = []
    indirect_sales_report_list = []
    indirect_purchase_report_list = []

    direct_sales_total_report = {'debit':0,'credit':0,'closing':0,'opening':0}
    direct_purchase_total_report = {'debit':0,'credit':0,'closing':0,'opening':0}
    indirect_sales_total_report = {'debit':0,'credit':0,'closing':0,'opening':0}
    indirect_purchase_total_report = {'debit':0,'credit':0,'closing':0,'opening':0}

    gross = 0
    net = 0

    expanded = 0
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company = request.POST['company']
        expanded = int(request.POST['expanded'])
        
        # 14 = Direct Expenses
        # 15 = Direct Income
        # 16 = Indirect Expenses
        # 17 = Indirect Income
        # 23 = Direct Purchase
        # 24 = Direct Sales
        profit_loss_ids = [14,15,16,17,23,24]
     
        sales_nominal_ledger = LedgerCategory.objects.filter(nominal=True).filter(child=None).select_related('child').prefetch_related('voucher_category','parent').filter(id__in=[15,24]).all()
        
        purchase_nominal_ledger = LedgerCategory.objects.filter(nominal=True).filter(child=None).select_related('child').prefetch_related('voucher_category','parent').filter(id__in=[14,23]).all()
       
        indirect_income_nominal_ledger = LedgerCategory.objects.filter(nominal=True).filter(child=None).select_related('child').prefetch_related('voucher_category','parent').filter(id=17).all()
       
        indirect_expense_nominal_ledger = LedgerCategory.objects.filter(nominal=True).filter(child=None).select_related('child').prefetch_related('voucher_category','parent').filter(id=16).all()

        
        for i in sales_nominal_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=direct_sales_report_list,reverse=True)
        
        for i in purchase_nominal_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=direct_purchase_report_list)
        
        for i in indirect_income_nominal_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=indirect_sales_report_list,reverse=True)
        
        for i in indirect_expense_nominal_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=indirect_purchase_report_list)
        
        
        set_expanded_ledger(request,module,company,from_date,to_date,direct_sales_report_list,total_report=direct_sales_total_report)
        set_expanded_ledger(request,module,company,from_date,to_date,direct_purchase_report_list,total_report=direct_purchase_total_report)
        set_expanded_ledger(request,module,company,from_date,to_date,indirect_sales_report_list,total_report=indirect_sales_total_report)
        set_expanded_ledger(request,module,company,from_date,to_date,indirect_purchase_report_list,total_report=indirect_purchase_total_report)


        total_direct_sales = round(direct_sales_total_report['credit'] - direct_sales_total_report['debit'],2)
        total_direct_purchase = round(direct_purchase_total_report['debit'] - direct_purchase_total_report['credit'],2)
        total_indirect_sales = round(indirect_sales_total_report['credit'] - indirect_sales_total_report['debit'],2)
        total_indirect_purchase = round(indirect_purchase_total_report['debit'] - indirect_purchase_total_report['credit'],2)

        gross = round(total_direct_sales - total_direct_purchase,2)
        net = gross - (total_indirect_sales - total_indirect_purchase)

            


        print(direct_sales_report_list)
       

       
        context['expanded'] = expanded
        context['total_direct_sales'] = total_direct_sales
        context['total_direct_purchase'] = total_direct_purchase
        context['total_indirect_sales'] = total_indirect_sales
        context['total_indirect_purchase'] = total_indirect_purchase
        context['direct_sales_report_list'] = direct_sales_report_list
        context['direct_purchase_report_list'] = direct_purchase_report_list
        context['indirect_sales_report_list'] = indirect_sales_report_list
        context['indirect_purchase_report_list'] = indirect_purchase_report_list
        if not company == "All":
            context['company'] = int(company)

    context['gross'] = gross
    context['net'] = net
    context['from_date'] = datetime.strptime(str(from_date),"%Y-%m-%d").date()
    context['to_date'] = datetime.strptime(str(to_date),"%Y-%m-%d").date()
    result_status = "No Profit, No Loss"
    return render(request,'report/profit_loss/profit_loss_report.html',context)

# Balance Sheet Report
@login_required(login_url='home:handle_login')
def balance_sheet_report_category(request,module):
    current_year = datetime.now().year
    to_current_year = datetime.now().year + 1
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
        to_current_year -= 1

    from_date = datetime.strptime(f'{current_year}-04-01',"%Y-%m-%d").date()
    to_date = datetime.strptime(f'{to_current_year}-03-31',"%Y-%m-%d").date()
    
    expanded = 0
    report_list = []
    company = request.user.user_account.office
    assets_report_list = []
    liability_report_list = []
    assets_total = 0
    liability_total = 0
    profit_loss = 0
    if request.method == 'POST':
        
        
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company = request.POST['company']
        expanded = int(request.POST['expanded'])

        if not company == "ALL":
            company = Logistic.objects.get(id=int(company))
        
        all_ledger = LedgerCategory.objects.select_related('child').prefetch_related('parent').all()
        assets_ledger = all_ledger.filter(asset=True).filter(child=None).all()
        liability_ledger = all_ledger.filter(liability=True).filter(child=None).all()
        nominal_ledger = all_ledger.filter(nominal=True).filter(child=None).prefetch_related('voucher_category').all()
        
        for i in assets_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=assets_report_list)


        if expanded == 1:
            c_depth = 0
            set_expanded_ledger(request=request,module=module,company=company,from_date=from_date,to_date=to_date,c_depth=c_depth,report_list=assets_report_list)

       
        for i in liability_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=liability_report_list,type="L")

        if expanded == 1:
            c_depth = 0
            set_expanded_ledger(request=request,module=module,company=company,from_date=from_date,to_date=to_date,c_depth=c_depth,report_list=liability_report_list)


        for i in nominal_ledger:
            for j in i.voucher_category.filter(date__gte=from_date).filter(date__lte=to_date).all():
                if j.dr_cr == "Debit":
                    profit_loss -= j.amount
                if j.dr_cr == "Credit":
                    profit_loss += j.amount
        
        for i in liability_report_list:
            liability_total += i['total']
        
        for i in assets_report_list:
            assets_total += i['total']

    context = {
        
        'module':module,
        'assets_report_list':assets_report_list,
        'liability_report_list':liability_report_list,
        'to_date':datetime.strptime(str(to_date),"%Y-%m-%d").date(),
        'from_date':datetime.strptime(str(from_date),"%Y-%m-%d").date(),
        'company':company,
        'liability_total':liability_total + profit_loss,
        'assets_total':assets_total,
        'profit_loss':profit_loss,
        'expanded':expanded,
    }
   
    return render(request,'report/balance_sheet_report_category/balance_sheet_report.html',context)


@login_required(login_url='home:handle_login')
def balance_sheet_pdf(request,module):
   
    report_list = []
    company = request.user.user_account.office
    assets_report_list = []
    liability_report_list = []
    assets_total = 0
    liability_total = 0
    profit_loss = 0
    assets_total_report = {'debit':0,'credit':0,'closing':0,'opening':0}
    liability_total_report = {'debit':0,'credit':0,'closing':0,'opening':0}
    if request.method == 'POST':
        
        
        from_date = request.POST['from_date2']
        to_date = request.POST['to_date2']
        company = request.POST['company2']

        if not company == "ALL":
            company = Logistic.objects.get(id=int(company))
        
        all_ledger = LedgerCategory.objects.select_related('child').prefetch_related('parent').all()
        assets_ledger = all_ledger.filter(asset=True).filter(child=None).all()
        liability_ledger = all_ledger.filter(liability=True).filter(child=None).all()
        nominal_ledger = all_ledger.filter(nominal=True).filter(child=None).prefetch_related('voucher_category').all()
        
        for i in assets_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=assets_report_list)

        c_depth = 0
        set_expanded_ledger(request=request,module=module,company=company,from_date=from_date,to_date=to_date,c_depth=c_depth,report_list=assets_report_list,total_report=assets_total_report)


       
        for i in liability_ledger:
            get_balance_sheet_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=liability_report_list,type="L")

       
        set_expanded_ledger(request=request,module=module,company=company,from_date=from_date,to_date=to_date,c_depth=c_depth,report_list=liability_report_list,total_report=liability_total_report)


        for i in nominal_ledger:
            for j in i.voucher_category.filter(date__gte=from_date).filter(date__lte=to_date).all():
                if j.dr_cr == "Debit":
                    profit_loss -= j.amount
                if j.dr_cr == "Credit":
                    profit_loss += j.amount
        
        for i in liability_report_list:
            liability_total += i['total']
        
        for i in assets_report_list:
            assets_total += i['total']

        context = {
            
            'module':module,
            'assets_report_list':assets_report_list,
            'liability_report_list':liability_report_list,
            'report_list':zip_longest(assets_report_list,liability_report_list),
            'to_date':datetime.strptime(str(to_date),"%Y-%m-%d").date(),
            'from_date':datetime.strptime(str(from_date),"%Y-%m-%d").date(),
            'company':company,
            'liability_total':liability_total + profit_loss,
            'assets_total':assets_total,
            'profit_loss':profit_loss,
        }
        template_path = 'report/balance_sheet_report_category/pdf/balance_sheet_pdf.html'
        return generate_pdf(request,template_path,context)


@login_required(login_url='home:handle_login')
def trial_balance_pdf(request,module):
    report_list = []
    total_report = {'debit':0,'credit':0,'closing':0,'opening':0}
    company = "ALL"
    if request.method == 'POST':
        report_list = []
        from_date = request.POST['from_date2']
        to_date = request.POST['to_date2']
        company = request.POST['company2']

        if not company == "ALL":
            company = Logistic.objects.filter(id=int(company)).first()
        
        all_ledger = LedgerCategory.objects.select_related('child').filter(child=None).prefetch_related('parent').all()
        
        for i in all_ledger:
            get_child_ctageories(category=i, company=company, from_date=from_date, to_date=to_date,report=report_list)

        template_path = 'report/trial_balance_report/pdf/trial_balance_pdf.html'
        c_depth = 0
        set_expanded_ledger(request,module,company,from_date,to_date,report_list,c_depth,total_report)
        
        if company == "ALL":
            company = Logistic.objects.first()
        

        context = {
            'data':report_list,
            'company':company,
            'to_date':datetime.strptime(str(to_date),"%Y-%m-%d").date(),
            'from_date':datetime.strptime(str(from_date),"%Y-%m-%d").date(),
            'total_report':total_report
            
        }
        
        return generate_pdf(request,template_path,context)





@login_required(login_url='home:handle_login')
def bank_report(request,module):
    context = {}
    banks = Bank.objects.all()
    opening_balance_type = "WOP"
    if request.method == 'POST':
        report = []
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        opening_balance_type = request.POST['opening_balance_type']
        bank = request.POST['bank']
        status = request.POST['status']
        bank = banks.filter(id=int(bank)).first()

        closing_balance = 0

        
        opening_bank_balance = bank.opening_balance
        opening_bank_balance_in = bank.opening_in
        opening_bank_balance_date = bank.opening_date

        reciepts = RecieptVoucher.objects.select_related('company_type','party_name','party_address','bank').filter(bank=bank).filter(is_deleted=False).filter().select_related('bank','company_type').prefetch_related('rec_voucher_detail','rec_voucher_detail__party','rec_voucher_detail__ledger','rec_voucher_detail__vendor','rec_voucher_detail__invoice').filter(recieve_in="BANK")

        payments = PaymentVoucher.objects.select_related('company_type','bank').filter(is_deleted=False).filter(bank=bank).prefetch_related('pay_voucher_detail','pay_voucher_detail__party','pay_voucher_detail__ledger','pay_voucher_detail__vendor','pay_voucher_detail__invoice').filter(pay_from="Bank")
        
    
        contra = ContraVoucher.objects.select_related('account_from','account_to','company_type').filter(is_deleted=False).all()

        if not status == "A":
            if status == "OC":
                reciepts = reciepts.exclude(bank_clearing_date=None)
                payments = payments.exclude(bank_clearing_date=None)
                contra = contra.exclude(bank_clearing_date=None)

                opening_reciepts = reciepts.filter(bank_clearing_date__lt=from_date).all()
                reciepts = reciepts.filter(bank_clearing_date__gte=from_date).filter(bank_clearing_date__lte=to_date).all()
                opening_payments = payments.filter(bank_clearing_date__lt=from_date).all()
                payments = payments.filter(bank_clearing_date__gte=from_date).filter(bank_clearing_date__lte=to_date).all()
                opening_contra = contra.filter(bank_clearing_date__lt=from_date).all()
                contra = contra.filter(bank_clearing_date__gte=from_date).filter(bank_clearing_date__lte=to_date).all()

                
            if status == "OUC":
                reciepts = reciepts.filter(bank_clearing_date=None)
                payments = payments.filter(bank_clearing_date=None)
                contra = contra.filter(bank_clearing_date=None)

        if status == "A" or status == "OUC":  
            opening_reciepts = reciepts.filter(voucher_date__lt=from_date).all()
            reciepts = reciepts.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).all()
            opening_payments = payments.filter(voucher_date__lt=from_date).all()
            payments = payments.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).all()
            opening_contra = contra.filter(voucher_date__lt=from_date).all()
            contra = contra.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).all()
              
                
        net_balance = 0
        opening_balance = 0
        for data in reciepts:
            obj = {
                'id':data.id,
                'company':data.company_type,
                'customer':'',
                'no':data.instrument_no,
                'date':data.voucher_date,
                'type':'Debit',
                'amount':round(data.received_amount,2),
                'clearing_date':data.bank_clearing_date,
                'data':data,
                'details':[]
            }
            closing_balance += data.received_amount
            party_name = ''
            for i in data.rec_voucher_detail.all():
                if i.party:
                    party_name += f'{i.party} /'
                elif i.vendor:
                    party_name += f'{i.vendor} /'

                elif i.ledger:
                    party_name += f'{i.ledger} /'

                obj['details'].append({
                    'party':i.party or i.ledger or i.vendor,
                    'payment_type':i.payment_type,
                    'amount':round(i.received_amount,2),
                })

                

            party_name = party_name[:-1]
            obj['customer'] = party_name
           
            if data.bank_charges > 0:
                net_balance -= data.bank_charges
                closing_balance -= data.bank_charges
                report.append(
                    {
                        'id':data.id,
                        'company':data.company_type,
                        'customer':"BANK CHARGES",
                        'no':data.instrument_no,
                        'date':data.voucher_date,
                        'type':'Credit',
                        'from':"R",
                        'amount':round(data.bank_charges,2),
                        'clearing_date':data.bank_clearing_date
                    }
                )

            report.append(obj)
               
        if opening_balance_type == "WP":
            for data in opening_reciepts:
                totalRecievedAmount = data.received_amount 
                opening_balance += totalRecievedAmount

                if data.bank_charges > 0:
                    opening_balance -= data.bank_charges
            
        for data in payments:
            obj = {
                'id':data.id,
                'company':data.company_type,
                'customer':'',
                'no':data.instrument_no,
                'date':data.voucher_date,
                'type':'Credit',
                'amount':round(data.paid_amount,2),
                'clearing_date':data.bank_clearing_date,
                'data':data,
                'details':[]
            }
            party_name = ''
            closing_balance -= data.paid_amount
            for i in data.pay_voucher_detail.all():
                if i.party:
                    party_name += f'{i.party} /'
                elif i.vendor:
                    party_name += f'{i.vendor} /'

                elif i.ledger:
                    party_name += f'{i.ledger} /'

                obj['details'].append({
                    'party':i.party or i.ledger or i.vendor,
                    'payment_type':i.payment_type,
                    'amount':round(i.paid_amount,2),
                })

            party_name = party_name[:-1]
            obj['customer'] = party_name

            

            report.append(obj)
           
            if data.bank_charges > 0:
                net_balance -= data.bank_charges
                closing_balance -= data.bank_charges
                report.append(
                    {
                        'id':data.id,
                        'company':data.company_type,
                        'customer':"BANK CHARGES",
                        'no':data.instrument_no,
                        'date':data.voucher_date,
                        'type':'Credit',
                        'from':"R",
                        'amount':round(data.bank_charges,2),
                        'clearing_date':data.bank_clearing_date
                    }
                )
         
         
        if opening_balance_type == "WP":
            for data in opening_payments:  
                totalPaidAmount = (data.paid_amount)
                opening_balance -= totalPaidAmount

                if data.bank_charges > 0:
                    opening_balance -= data.bank_charges

            
        for data in contra:

            if data.bank_charges > 0:
                net_balance -= data.bank_charges
                closing_balance -= data.bank_charges
                
                report.append(
                    {
                        'id':data.id,
                        'company':data.company_type,
                        'customer':"BANK CHARGES",
                        'no':data.instrument_no,
                        'date':data.voucher_date,
                        'type':'Credit',
                        'from':"R",
                        'amount':round(data.bank_charges,2),
                        'clearing_date':data.bank_clearing_date
                    }
                )

            if data.contra_choice == "B2B":
                if data.account_from == bank:
                    if data.amount > 0:
                        net_balance -= data.amount
                        closing_balance -= data.amount
                        report.append(
                            {
                                'id':data.id,
                                'company':data.company_type,
                                'no':data.instrument_no,
                                'customer':f'{data.account_to}',
                                'date':data.voucher_date,
                                'type':'Credit',
                                'from':"C",
                                'amount':round(data.amount,2),
                                'clearing_date':data.bank_clearing_date
                            }
                        )

                
                        
                if data.account_to == bank:
                    if data.amount > 0:
                        net_balance += data.amount
                        closing_balance += data.amount
                        report.append(
                            {
                                'id':data.id,
                                'company':data.company_type,
                                'no':data.instrument_no,
                                'customer':f'{data.account_from}',
                                'date':data.voucher_date,
                                'type':'Debit',
                                'from':"C",
                                'amount':round(data.amount,2),
                                'clearing_date':data.bank_clearing_date
                            }
                        )
                        
            if data.contra_choice == "C2B":
                if data.account_to == bank:
                    if data.amount > 0:
                        net_balance += data.amount
                        closing_balance += data.amount
                        report.append(
                            {
                                'id':data.id,
                                'company':data.company_type,
                                'no':data.instrument_no,
                                'particular':f'{data.cash.company_name}',
                                'date':data.voucher_date,
                                'type':'Debit',
                                'from':"C",
                                'amount':round(data.amount,2),
                                'clearing_date':data.bank_clearing_date
                            }
                        )
                        
            if data.contra_choice == "B2C":
                if data.account_from == bank:
                    if data.amount > 0:
                        net_balance -= data.amount
                        closing_balance -= data.amount
                        report.append(
                            {
                                'id':data.id,
                                'company':data.company_type,
                                'no':data.instrument_no,
                                'particular':f'{data.cash.company_name}',
                                'date':data.voucher_date,
                                'type':'Credit',
                                'from':"C",
                                'amount':round(data.amount,2),
                                'clearing_date':data.bank_clearing_date
                            }
                        )
            
        if opening_balance_type == "WP":
            for data in opening_contra:
                if data.bank_charges > 0:
                    opening_balance -= data.bank_charges
                    
                if data.contra_choice == "B2B":
                    if data.account_from == bank:
                        if data.amount > 0:
                            net_balance -= data.amount
                            opening_balance -= data.amount
                            
                            
                    if data.account_to == bank:
                        if data.amount > 0:
                            net_balance += data.amount
                            opening_balance += data.amount
                            
                            
                if data.contra_choice == "C2B":
                    if data.account_to == bank:
                        if data.amount > 0:
                            net_balance += data.amount
                            opening_balance += data.amount
                            
                            
                if data.contra_choice == "B2C":
                    if data.account_from == bank:
                        if data.amount > 0:
                            net_balance -= data.amount
                            opening_balance -= data.amount
                    
                
        opening_report = {} 
        report.sort(key=lambda item:item['date'])
        
        if opening_balance_type == "WP":
            
           
            if bank.opening_in == "Debit":
                opening_balance += bank.opening_balance
            if bank.opening_in == "Credit":
                opening_balance -= bank.opening_balance

            closing_balance += opening_balance
            if opening_balance >= 0:
                debit_credit = "Debit"
            else:
                debit_credit = "Credit"
                opening_balance *= -1 
       
            opening_report = {
                    'id':0,
                    'company':None,
                    'customer':f"Opening Balance",
                    'no':"Opening Balance",
                    'date':None,
                    'type':debit_credit,
            
                    'amount':opening_balance,
                    'clearing_date':None
                }
            
        report.sort(key=lambda item:item['date'])
        running_balance = 0
        if opening_balance_type == "WP":
            if opening_report['type'] == 'Debit':
                running_balance = opening_balance
            else:
                running_balance = opening_balance * -1
            
            opening_report['balance'] = running_balance

        for i in report:
            if i['type'] == "Debit":
                running_balance += i['amount'] 
            else:
                running_balance -= i['amount'] 

            i['balance'] = running_balance
            

                
        context['report'] = report
        context['selected_bank'] = bank
        context['opening_balance'] = opening_balance
        context['closing_balance'] = closing_balance
        context['opening_report'] = opening_report
        context['opening_balance_type'] = opening_balance_type
        context['status'] = status
        context['net_balance'] = net_balance
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

            
    
    context['banks'] = banks
    context['module'] = module
    return render(request,'report/bank/bank_report.html',context)


@login_required(login_url='home:handle_login')
def cash_report(request,module):
    context = {}
    opening_balance_type = "WOP"
    if request.method == 'POST':
        report = []
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        opening_balance_type = request.POST['opening_balance_type']
        closing_balance = 0

        opening_reciepts = RecieptVoucher.objects.select_related('company_type','party_name','party_address','cash').filter(voucher_date__lt=from_date).filter(recieve_in="CASH").filter(old_voucher=False).filter(is_reversed=False).all()

        reciepts = RecieptVoucher.objects.select_related('company_type','party_name','party_address','cash').filter(voucher_date__range=[from_date,to_date]).filter(recieve_in="CASH").filter(old_voucher=False).filter(is_reversed=False).filter(voucher=None).prefetch_related('rec_voucher_detail','rec_voucher_detail__vendor','rec_voucher_detail__party','rec_voucher_detail__ledger').all()

        opening_payments = PaymentVoucher.objects.select_related('company_type').filter(old_voucher=False).filter(pay_from='Cash').filter(voucher_date__lt=from_date).all()
        
        payments = PaymentVoucher.objects.select_related('company_type','party_name','party_address','bank','vendor').prefetch_related('payment_voucer_advance','pay_voucher_detail','pay_voucher_detail__vendor','pay_voucher_detail__party','pay_voucher_detail__ledger').filter(old_voucher=False).filter(pay_from='Cash').filter(voucher_date__range=[from_date,to_date]).filter(voucher=None).all()

        
        opening_contra = ContraVoucher.objects.filter(voucher_date__lt=from_date).all()

        contra = ContraVoucher.objects.select_related('account_from','account_to','company_type').filter(voucher_date__range=[from_date,to_date]).all()

                
        net_balance = 0
        opening_balance = 0
        for data in reciepts:
            party_name = ""
            totalRecievedAmount = data.received_amount
            closing_balance += totalRecievedAmount
            for rec in data.rec_voucher_detail.all():
                if rec.party:
                    party_name += rec.party.party_name + " /"
                if rec.vendor:
                    party_name += rec.vendor.vendor_name + " /"
                if rec.ledger:
                    party_name += rec.ledger.ledger_name + " /"
        

            if totalRecievedAmount > 0 and not data.is_reversed:
                net_balance += totalRecievedAmount
                report.append(
                    {
                        'id':data.id,
                        'company':data.company_type,
                        'customer':party_name,
                        'no':data.instrument_no,
                        'date':data.voucher_date,
                        'type':'Debit',
                        'from':"R",
                        'amount':round(totalRecievedAmount,2),
                        'clearing_date':data.bank_clearing_date,
                        'data':data
                    }
                )

               
               
        for data in opening_reciepts:
            totalRecievedAmount = data.total_recieved_amount 
            opening_balance += totalRecievedAmount
         
        for data in payments:
            party_name = ""
            for payment in data.pay_voucher_detail.all():
                if payment.party:
                    party_name += payment.party.party_name + " /"
                if payment.vendor:
                    party_name += payment.vendor.vendor_name + " /"
                if payment.ledger:
                    party_name += payment.ledger.ledger_name + " /"
           
            totalPaidAmount = (data.paid_amount)
            closing_balance -= totalPaidAmount
            if totalPaidAmount > 0:
                net_balance -= totalPaidAmount
                report.append(
                    {
                        'id':data.id,
                        'company':data.company_type,
                        'customer':f"{party_name}",
                        'no':data.instrument_no,
                        'date':data.voucher_date,
                        'type':'Credit',
                        'from':"P",
                        'amount':round(totalPaidAmount,2),
                        'clearing_date':data.bank_clearing_date,
                        'data':data
                    }
                )

           
            
        for data in opening_payments:  
            totalPaidAmount = (data.paid_amount)
            opening_balance -= totalPaidAmount

            if data.bank_charges > 0:
                opening_balance -= data.bank_charges

           
        for data in contra:

            if data.bank_charges > 0:
                net_balance -= data.bank_charges
                closing_balance -= data.bank_charges
                
                report.append(
                    {
                        'id':data.id,
                        'company':data.company_type,
                        'customer':"BANK CHARGES",
                        'no':data.instrument_no,
                        'date':data.voucher_date,
                        'type':'Credit',
                        'from':"R",
                        'amount':round(data.bank_charges,2),
                        'clearing_date':data.bank_clearing_date
                    }
                )

                        
            if data.contra_choice == "C2B":
                if data.amount > 0:
                    net_balance += data.amount
                    closing_balance += data.amount
                    report.append(
                        {
                            'id':data.id,
                            'company':data.company_type,
                            'no':data.instrument_no,
                            'particular':f'{data.cash.company_name}',
                            'date':data.voucher_date,
                            'type':'Credit',
                            'from':"C",
                            'amount':round(data.amount,2),
                            'clearing_date':data.bank_clearing_date
                        }
                    )
                    
            if data.contra_choice == "B2C":
                if data.amount > 0:
                    net_balance -= data.amount
                    closing_balance -= data.amount
                    report.append(
                        {
                            'id':data.id,
                            'company':data.company_type,
                            'no':data.instrument_no,
                            'particular':f'{data.cash.company_name}',
                            'date':data.voucher_date,
                            'type':'Debit',
                            'from':"C",
                            'amount':round(data.amount,2),
                            'clearing_date':data.bank_clearing_date
                        }
                    )
            
        for data in opening_contra:
            if data.bank_charges > 0:
                opening_balance -= data.bank_charges
                    
            if data.contra_choice == "C2B":
                if data.amount > 0:
                    net_balance -= data.amount
                    opening_balance -= data.amount
                        
                        
            if data.contra_choice == "B2C":
                if data.amount > 0:
                    net_balance += data.amount
                    opening_balance += data.amount
                
            
        opening_report = {} 
        report.sort(key=lambda item:item['date'])
        
        if opening_balance_type == "WP":
            bank_ledger = LedgerMaster.objects.filter(ledger_name__icontains='cash').all()
            for i in bank_ledger:
                if i.balance_in == "Debit":
                    opening_balance += i.opening_balance
                if i.balance_in == "Credit":
                    opening_balance -= i.opening_balance

            closing_balance += opening_balance
            if opening_balance >= 0:
                debit_credit = "Debit"
            else:
                debit_credit = "Credit"
                opening_balance *= -1 
       
            opening_report = {
                    'id':0,
                    'company':None,
                    'customer':f"Opening Balance",
                    'no':"Opening Balance",
                    'date':None,
                    'type':debit_credit,
            
                    'amount':opening_balance,
                    'clearing_date':None
                }
            
        report.sort(key=lambda item:item['date'])
        running_balance = 0
        if opening_balance_type == "WP":
            if opening_report['type'] == 'Debit':
                running_balance = opening_balance
            else:
                running_balance = opening_balance * -1
            
            opening_report['balance'] = running_balance

        for i in report:
            if i['type'] == "Debit":
                running_balance += i['amount'] 
            else:
                running_balance -= i['amount'] 

            i['balance'] = running_balance
            

                
        context['report'] = report
        context['opening_balance'] = opening_balance
        context['closing_balance'] = closing_balance
        context['opening_report'] = opening_report
        context['opening_balance_type'] = opening_balance_type
        context['net_balance'] = net_balance
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

            
    
    context['module'] = module
    return render(request,'report/cash/cash_report.html',context)

@login_required(login_url='home:handle_login')
def addBankClearingDate(request,module,index):
    if request.method == 'POST':
        id = request.POST[f'id_{index}']
        clearing_date = request.POST[f'bank_clearing_date_{index}']
        voucher_type = request.POST[f'type_{index}']
        if voucher_type == "R":
            voucher = RecieptVoucher.objects.filter(id=int(id)).first()
            voucher.bank_clearing_date = clearing_date
            voucher.save()
            
        if voucher_type == "P":
            voucher = PaymentVoucher.objects.filter(id=int(id)).first()
            voucher.bank_clearing_date = clearing_date
            voucher.save()

        if voucher_type == "C":
            voucher = ContraVoucher.objects.filter(id=int(id)).first()
            voucher.bank_clearing_date = clearing_date
            voucher.save()

        messages.success(request,'Success')

    return redirect('dashboard:bank_report',module=module)

@login_required(login_url='home:handle_login')
def petty_cashbook(request,module):
    context = {}
    
    if request.method == 'POST':
        report = []
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        
        petty_cash = PettyCash.objects.filter(date__range=[from_date,to_date]).all()
               
        
        context['petty_cash'] = petty_cash
      
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")
        

    context['module'] = module
    return render(request,'report/cash/petty_cash.html',context)

@login_required(login_url='home:handle_login')
def transfer_to_petty_cash(request,module,id,index):
    if request.method == "POST":
        voucher = ContraVoucher.objects.filter(id=int(id)).first()
        check_cash = PettyCash.objects.filter(voucher=voucher).first()
        if check_cash or not voucher:
            messages.error(request,"Already exists in petty cash.")
            return redirect('dashboard:master_cashbook',module=module)
        transaction_date = request.POST[f'transaction_date_{index}']
        transaction_description = request.POST[f'transaction_description_{index}']
        type = request.POST[f'type_{index}']
        
        petty_cash = PettyCash.objects.create(voucher=voucher)
        petty_cash.amount = voucher.amount
        petty_cash.date = transaction_date
        petty_cash.description = transaction_description
        petty_cash.type = type
        petty_cash.save()
        messages.success(request,'Transferred To Petty Cash')

    return redirect('dashboard:master_cashbook',module=module)

@login_required(login_url='home:handle_login')
def sales_outstanding(request,module):
    context = {}
    selected_company = "A"
    if request.method == "POST":
        party = request.POST['party']
        company = request.POST['company']
        selected_region = request.POST['region']

        party = Party.objects.filter(id=int(party)).first()

        credit_notes = CreditNote.objects.select_related('job_no','bill_to','bill_to_address','invoice_currency','company_type').filter(company_type__region=selected_region).filter(is_cancel=False).filter(is_einvoiced=True).filter(is_deleted=False).filter(bill_to__id=party.id).all()
        advance_amount = RecieptVoucherDetails.objects.select_related('party','voucher','voucher__company_type','party_address').filter(party__id=party.id).filter(payment_type = 'OAC').filter(company_type__region=selected_region).all()
        journals= JournalEntry.objects.filter(party=party).all()
        invoices = InvoiceReceivable.objects.select_related('job_no','bill_to','bill_to_address','invoice_currency','company_type').filter(company_type__region=selected_region).prefetch_related('reciept_rec_inv','reciept_rec_inv__voucher','job_no__job_invoice').filter(is_einvoiced=True).filter(is_deleted=False).filter(bill_to__id=party.id).all()
        if not company == "A":
            company = Logistic.objects.filter(id=int(company)).first()
            invoices = invoices.filter(company_type__id = company.id).all()
            credit_notes = credit_notes.filter(company_type__id = company.id).all()
            advance_amount = advance_amount.filter(company_type__id=company.id).all()
            journals = journals.filter(journal_entry__company_type__id=company.id).all()
            company = company.id
        
        invoices_list = []
        for i in invoices:
            head = {
                'invoice':i,
                'recieved_amount':0,
                'balance_amount':0,
                'net_amount':0,
                # 'job_invoices':JobInvoice.objects.filter(job__job_no=i.job_no).values('invoice_no').all(),
                
            }
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == 'INR':
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass

            recieved_amount = 0
            for j in i.reciept_rec_inv.all():
                recieved_amount +=  (j.received_amount + j.tds_amount + j.adjustment_amount)
                

      
            head['recieved_amount'] = recieved_amount
            head['net_amount'] = (i.net_amount * currency_ex_rate)
            head['balance_amount'] = (i.net_amount * currency_ex_rate) - recieved_amount
            invoices_list.append(head)

        selected_company = company
        selected_party = party
        
        context['advance_amount'] = advance_amount
        context['invoices_list'] = invoices_list
        context['selected_party'] = selected_party
        context['selected_region'] = selected_region
        context['credit_notes'] = credit_notes
        context['journals'] = journals

    context['module'] = module
    context['selected_company'] = selected_company
    return render(request,'report/sales_outstanding/sales_outstanding.html',context)

@login_required(login_url='home:handle_login')
def direct_creditors_outstanding(request,module):
    context = {}
    selected_company = "A"
    if request.method == "POST":
        party = request.POST['party']
        company = request.POST['company']
        selected_region = request.POST['region']

        party = Party.objects.filter(id=int(party)).first()

        debit_notes = DebitNote.objects.filter(company_type__region=selected_region).filter(is_deleted=False).filter(bill_from__id=party.id).all()
        advance_amount = PaymentVoucher.objects.filter(party_name__id=party.id).filter(advance_amount__gt = 0).filter(company_type__region=selected_region).filter(payment_type="Direct").all()
        journals= JournalEntry.objects.filter(account__party=party).filter(journal_entry__auto_generated=False).all()
        invoices = InvoicePayable.objects.filter(company_type__region=selected_region).filter(is_deleted=False).filter(bill_from__id=party.id).all()
        if not company == "A":
            company = Logistic.objects.filter(id=int(company)).first()
            invoices = invoices.filter(company_type__id = company.id).all()
            debit_notes = debit_notes.filter(company_type__id = company.id).all()
            advance_amount = advance_amount.filter(company_type__id=company.id).all()
            journals = journals.filter(journal_entry__company_type__id=company.id).all()
            company = company.id
        
        invoices_list = []
        for i in invoices:
            head = {
                'invoice':i,
                'paid_amount':0,
                'balance_amount':0,
                'net_amount':0
            }
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == 'INR':
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass

            paid_amount = 0
            for j in i.pay_payment_inv.all():
                paid_amount +=  (j.paid_amount + j.tds_amount + j.adjustment_amount)
                
            if i.tds_payable:
                paid_amount += i.tds_payable

            head['paid_amount'] = paid_amount
            head['net_amount'] = (i.net_amount * currency_ex_rate)
            head['balance_amount'] = (i.net_amount * currency_ex_rate) - paid_amount
            invoices_list.append(head)

        selected_company = company
        selected_party = party
        
        context['advance_amount'] = advance_amount
        context['invoices_list'] = invoices_list
        context['selected_party'] = selected_party
        context['selected_region'] = selected_region
        context['debit_notes'] = debit_notes
        context['journals'] = journals

    context['module'] = module
    context['selected_company'] = selected_company
    return render(request,'report/creditors_outstanding/direct_creditors.html',context)

@login_required(login_url='home:handle_login')
def indirect_creditors_outstanding(request,module):
    context = {}
    selected_company = "A"
    if request.method == "POST":
        vendor = request.POST['vendor']
        company = request.POST['company']
        selected_region = request.POST['region']

        vendor = Vendor.objects.filter(id=int(vendor)).first()

       
        advance_amount = PaymentVoucher.objects.filter(vendor__id=vendor.id).filter(advance_amount__gt = 0).filter(company_type__region=selected_region).filter(payment_type="Indirect").all()
        rec_advance_amount = RecieptVoucher.objects.select_related("vendor",'company_type').filter(vendor__id=vendor.id).filter(advance_amount__gt = 0).filter(company_type__region=selected_region).filter(payment_type="Indirect").all()
        journals= JournalEntry.objects.filter(account__vendor=vendor).filter(journal_entry__auto_generated=False).all()
        invoices = IndirectExpense.objects.select_related('vendor','company_type').filter(company_type__region=selected_region).filter(is_deleted=False).filter(vendor__id=vendor.id).all()
        debit_note = DebitNote.objects.select_related('bill_from_vendor','company_type').filter(company_type__region=selected_region).filter(is_deleted=False).filter(bill_from_vendor__id=vendor.id).all()
        trailor_expenses = TrailorExpenseDetail.objects.filter(expense__company_type__region=selected_region).filter(expense__is_deleted=False).filter(vendor__id=vendor.id).all()

        if not company == "A":
            company = Logistic.objects.filter(id=int(company)).first()
            invoices = invoices.filter(company_type__id = company.id).all()
            debit_note = debit_note.filter(company_type__id = company.id).all()
            trailor_expenses = trailor_expenses.filter(expense__company_type__id = company.id).all()
            advance_amount = advance_amount.filter(company_type__id=company.id).all()
            rec_advance_amount = rec_advance_amount.filter(company_type__id=company.id).all()
            journals = journals.filter(journal_entry__company_type__id=company.id).all()
            company = company.id
        
        invoices_list = []
        trailor_expense_list = []
        for i in invoices:
            head = {
                'invoice':i,
                'paid_amount':0,
                'balance_amount':0,
                'net_amount':0
            }
            currency_ex_rate = 1
           

            paid_amount = 0
            for j in i.exp_payment_inv.all():
                paid_amount +=  (j.paid_amount + j.tds_amount + j.adjustment_amount)
                
            if i.tds_amount:
                paid_amount += i.tds_amount

            head['paid_amount'] = paid_amount
            head['net_amount'] = (i.net_amount * currency_ex_rate)
            head['balance_amount'] = (i.net_amount * currency_ex_rate) - paid_amount
            invoices_list.append(head)

        for i in trailor_expenses:
            head = {
                'invoice':i,
                'paid_amount':0,
                'balance_amount':0,
                'net_amount':0
            }
            currency_ex_rate = 1
           

            paid_amount = 0
          
            head['paid_amount'] = paid_amount
            head['net_amount'] = (i.charges)
            head['balance_amount'] = (i.charges) - paid_amount
            trailor_expense_list.append(head)

        selected_company = company
        selected_party = vendor
        
        context['rec_advance_amount'] = rec_advance_amount
        context['advance_amount'] = advance_amount
        context['debit_notes'] = debit_note
        context['invoices_list'] = invoices_list
        context['trailor_expense_list'] = trailor_expense_list
        context['selected_party'] = selected_party
        context['selected_region'] = selected_region
        context['journals'] = journals
       
    context['module'] = module
    context['selected_company'] = selected_company
    return render(request,'report/creditors_outstanding/indirect_creditors.html',context)



def getSalesInvoices(party=None,old_invoice=None,from_date=None,to_date=None,company_type=None,region="India",manager=None):
    invoices = InvoiceReceivable.objects.filter(is_einvoiced=True).filter(is_cancel=False).filter(is_deleted=False).filter(net_amount__gt=0).select_related('bill_to','company_type','bill_to_address','invoice_currency','job_no').prefetch_related('reciept_rec_inv','reciept_rec_inv__voucher','trailor_expense_party_invoice').filter(company_type__region=region).filter(is_single=True)
    if not old_invoice == None :
        invoices = invoices.filter(old_invoice=old_invoice)
    
    if party :
        invoices = invoices.filter(bill_to=party)
    
  
    if manager:
        invoices = invoices.filter(bill_to__account_manager=manager)
    
    if from_date :
        invoices = invoices.filter(einvoice_date__date__gte=from_date)

    if  to_date:
        invoices = invoices.filter(einvoice_date__date__lte=to_date)

    if company_type:
        invoices = invoices.filter(company_type=company_type)


    return invoices

def getCreditNotes(party=None,from_date=None,to_date=None,company_type=None,region="India",manager=None):
    invoices = CreditNote.objects.filter(is_einvoiced=True).filter(is_cancel=False).filter(is_deleted=False).filter(net_amount__gt=0).select_related('bill_to','company_type','bill_to_address','invoice_currency','job_no').filter(company_type__region=region)

    if party :
        invoices = invoices.filter(bill_to=party)

    if manager:
        invoices = invoices.filter(bill_to__account_manager=manager)
    
    if from_date :
        invoices = invoices.filter(einvoice_date__date__gte=from_date)

    if  to_date:
        invoices = invoices.filter(einvoice_date__date__lte=to_date)

    if company_type:
        invoices = invoices.filter(company_type=company_type)

    return invoices

def getBillWiseReceipts(party=None,from_date=None,to_date=None,company_type=None,region="India",manager=None):
    vouchers = RecieptVoucherDetails.objects.filter(is_deleted=False).exclude(payment_type='BW').select_related('party','voucher__company_type','party_address','voucher').filter(voucher__company_type__region=region)

    if party :
        vouchers = vouchers.filter(party=party)

    if manager:
        vouchers = vouchers.filter(party__account_manager=manager)
    
    
    if from_date :
        vouchers = vouchers.filter(voucher__voucher_date__date__gte=from_date)

    if  to_date:
        vouchers = vouchers.filter(voucher__voucher_date__date__lte=to_date)

    if company_type:
        vouchers = vouchers.filter(voucher__company_type=company_type)

    return vouchers

def getAdvanceReceipts(party=None,from_date=None,to_date=None,old_voucher=None,company_type=None,region="India",manager=None):
    vouchers = RecieptVoucherDetails.objects.filter(is_deleted=False).filter(payment_type='OAC').select_related('party','voucher__company_type','party_address','voucher').filter(voucher__company_type__region=region)

    if party :
        vouchers = vouchers.filter(party=party)

    if manager:
        vouchers = vouchers.filter(party__account_manager=manager)
    
    
    if from_date :
        vouchers = vouchers.filter(voucher__voucher_date__gte=from_date)

    if  to_date:
        vouchers = vouchers.filter(voucher__voucher_date__lte=to_date)

    if company_type:
        vouchers = vouchers.filter(voucher__company_type=company_type)

    return vouchers

def getJournalAjustments(party=None,from_date=None,to_date=None,company_type=None,region="India",manager=None,indirect=False,vendor=None):
    journals = JournalEntry.objects.filter(voucher__company_type__region=region).all()
    if party:
        journals = journals.filter(party=party)
        
    if vendor:
        journals = journals.filter(vendor=vendor)
        
    if manager:
        journals = journals.filter(party__account_manager=manager)
    
    if from_date :
        journals = journals.filter(voucher__date__gte=from_date)

    if  to_date:
        journals = journals.filter(voucher__date__lte=to_date)

    if company_type:
        journals = journals.filter(voucher__company_type=company_type)

    return journals

def getTrailorExpenseAjustments(party=None,from_date=None,to_date=None,company_type=None,region="India",manager=None):
    trailor_expense_details = TrailorExpenseDetail.objects.filter(expense__company_type__region=region).filter(payment_type="DIRECT CUSTOMER").select_related('expense').all()

    if party :
        trailor_expense_details = trailor_expense_details.filter(party = party)

    if manager:
        trailor_expense_details = trailor_expense_details.filter(party__account_manager=manager)
    
   
    if from_date :
        trailor_expense_details = trailor_expense_details.filter(date__gte=from_date)

    if  to_date:
        trailor_expense_details = trailor_expense_details.filter(date__lte=to_date)

    if company_type:
        trailor_expense_details = trailor_expense_details.filter(expense__company_type=company_type)

    return trailor_expense_details

def getPurchaseInvoices(party=None,old_invoice=None,from_date=None,to_date=None,company_type=None,region="India",manager=None,indirect=False,vendor=None):
    invoices = InvoicePayable.objects.filter(is_deleted=False).filter(net_amount__gt=0).select_related('bill_from','vendor','company_type','bill_from_address','invoice_currency','job_no').prefetch_related('pay_payment_inv').filter(company_type__region=region)


    if indirect:
        invoices = invoices.filter(party_type="Indirect")
    if vendor:
        invoices = invoices.filter(vendor=vendor)

    if not old_invoice == None :
        invoices = invoices.filter(old_invoice=old_invoice)

    if party :
        invoices = invoices.filter(bill_from=party)

    if manager:
        invoices = invoices.filter(bill_from__account_manager=manager)
    
    if from_date :
        invoices = invoices.filter(date_of_invoice__gte=from_date)

    if  to_date:
        invoices = invoices.filter(date_of_invoice__lte=to_date)

    if company_type:
        invoices = invoices.filter(company_type=company_type)

    return invoices

def getBillWisePayments(party=None,from_date=None,to_date=None,company_type=None,region="India",payment_type="Direct",manager=None):
    vouchers = PaymentVoucherDetails.objects.filter(voucher__is_deleted=False).filter(payment_type="BW").select_related('party_name','company_type','party_address','voucher').filter(company_type__region=region).filter(party_type=payment_type)
    
    if party:
        vouchers = vouchers.filter(party_name=party)

    if manager and payment_type == "Direct" :
        vouchers = vouchers.filter(party_name__account_manager=manager)
    
    if party and payment_type == "Indirect":
        vouchers = vouchers.filter(vendor=party)

    if from_date :
        vouchers = vouchers.filter(voucher_date__gte=from_date)

    if  to_date:
        vouchers = vouchers.filter(voucher_date__lte=to_date)

    if company_type:
        vouchers = vouchers.filter(company_type=company_type)

    return vouchers

def getAdvancePayments(party=None,vendor=None,from_date=None,to_date=None,old_voucher=None,company_type=None,region="India",manager=None,indirect=None):
    vouchers = PaymentVoucherDetails.objects.filter(voucher__is_deleted=False).filter(payment_type="OAC").select_related('voucher','voucher__company_type','party','vendor','party_address').filter(voucher__company_type__region=region)

    if party:
        vouchers = vouchers.filter(party=party)

    if party and manager:
        vouchers = vouchers.filter(party__account_manager=manager)
    
    if indirect:
        vouchers = vouchers.filter(party_type='Indirect')
    else:
        vouchers = vouchers.filter(party_type='Direct')

    
    if vendor:
        vouchers = vouchers.filter(vendor=vendor)
    
    if not old_voucher == None :
        vouchers = vouchers.filter(voucher__old_voucher=old_voucher)
    
    if from_date :
        vouchers = vouchers.filter(voucher__voucher_date__gte=from_date)

    if  to_date:
        vouchers = vouchers.filter(voucher__voucher_date__lte=to_date)

    if company_type:
        vouchers = vouchers.filter(voucher__company_type=company_type)

    return vouchers

def getDebitNote(party=None,from_date=None,to_date=None,company_type=None,region="India",party_type='Direct',manager=None):
    invoices = DebitNote.objects.filter(is_deleted=False).filter(net_amount__gt=0).select_related('bill_from','company_type','bill_from_address').filter(company_type__region=region).filter(party_type=party_type)

    if party and party_type == "Direct":
        invoices = invoices.filter(bill_from=party)

    if manager and party_type == "Direct" :
        invoices = invoices.filter(bill_from__account_manager=manager)
    
    if party and party_type == "Indirect":
        invoices = invoices.filter(bill_from_vendor=party)
  
    if from_date :
        invoices = invoices.filter(date_of_note__gte=from_date)

    if  to_date:
        invoices = invoices.filter(date_of_note__lte=to_date)

    if company_type:
        invoices = invoices.filter(company_type=company_type)

    return invoices


def getIndirectExpenses(party=None,old_invoice=None,from_date=None,to_date=None,company_type=None,region="India"):
    invoices = IndirectExpense.objects.filter(is_deleted=False).filter(net_amount__gt=0).select_related('vendor','company_type','invoice_currency','job_no').prefetch_related('exp_payment_inv').filter(company_type__region=region)

    if not old_invoice == None :
        invoices = invoices.filter(old_invoice=old_invoice)
    
    if party :
        invoices = invoices.filter(vendor=party)
    
    if from_date :
        invoices = invoices.filter(bill_date__gte=from_date)

    if  to_date:
        invoices = invoices.filter(bill_date__lte=to_date)

    if company_type:
        invoices = invoices.filter(company_type=company_type)

    return invoices

def getTrailorExpense(party=None,from_date=None,to_date=None,company_type=None,region="India"):
    invoices = TrailorExpenseDetail.objects.select_related('vendor','expense__company_type').filter(expense__company_type__region=region).filter(expense__is_deleted=False).all()

   
    if party :
        invoices = invoices.filter(vendor=party)
    
    if from_date :
        invoices = invoices.filter(date__gte=from_date)

    if  to_date:
        invoices = invoices.filter(date__lte=to_date)

    if company_type:
        invoices = invoices.filter(expense__company_type=company_type)


    return invoices




@login_required(login_url='home:handle_login')
def sales_outstanding_2(request,module):
    context = {}
    selected_company = "A"
    pending_bills = "Y"
    if request.method == "POST":
        party = request.POST['party']
        company = request.POST['company']
        selected_region = request.POST['region']
        pending_bills = request.POST['pending_bills']

        party = Party.objects.filter(id=int(party)).first()
        if not company == "A":
            selected_company = Logistic.objects.filter(id=int(company)).first()
        else:
            selected_company = None

        credit_notes = getCreditNotes(party=party,company_type=selected_company,region=selected_region)
        advance_amount = getAdvanceReceipts(party=party,company_type=selected_company,region=selected_region)
        
       
        journals= getJournalAjustments(party=party,company_type=selected_company,region=selected_region)

        invoices = getSalesInvoices(party=party,company_type=selected_company,region=selected_region)
        
        trailor_expense_details = getTrailorExpenseAjustments(party=party,company_type=selected_company,region=selected_region)
        
        
        if not company == "A":
            company = selected_company
        
        balance = 0
        invoices_list = []
        for i in invoices:
            head = {
                'invoice':i,
                'recieved_amount':0,
                'balance_amount':0,
                'net_amount':0,
                'adjustments':[]
                # 'job_invoices':JobInvoice.objects.filter(job__job_no=i.job_no).values('invoice_no').all(),
            }
            
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == 'INR':
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass

            recieved_amount = 0
            for j in i.reciept_rec_inv.filter(voucher__is_deleted=False).all():
                recieved_amount +=  ((j.received_amount + j.tds_amount + j.adjustment_amount) * currency_ex_rate)
                head['adjustments'].append({
                    'type':'Reciept',
                    'data':j
                })
                
                balance -= ((j.received_amount + j.tds_amount + j.adjustment_amount) * currency_ex_rate)
                 
            for j in i.crn_ref_invoice.filter(company_type__region=selected_region).filter(is_einvoiced=True).filter(is_deleted=False).filter(is_cancel=False).filter(bill_to__id=party.id).all():
                credit_notes = credit_notes.exclude(id=j.id)
                crn_currency_ex_rate = 1
                try:
                    if not j.invoice_currency.short_name == "INR":
                        crn_currency_ex_rate = j.currency_ex_rate
                except:
                    crn_currency_ex_rate = 1        
                    
                recieved_amount +=  (j.net_amount * crn_currency_ex_rate)
                balance -= (j.net_amount * crn_currency_ex_rate)
                head['adjustments'].append({
                    'type':'CRN',
                    'data':j
                })
                
            for j in i.trailor_expense_party_invoice.filter(is_deleted=False).filter(party__id = party.id).all():
                trailor_expense_details = trailor_expense_details.exclude(id=j.id)
                recieved_amount +=  j.charges
                balance -= j.charges
                head['adjustments'].append({
                    'type':'Trailor',
                    'data':j
                })
            
            
            
            balance += (i.net_amount * currency_ex_rate)
            head['recieved_amount'] = recieved_amount
            head['net_amount'] = (i.net_amount * currency_ex_rate)
            head['balance_amount'] = (i.net_amount * currency_ex_rate) - recieved_amount
            
            if pending_bills == "Y":
                if round(head['balance_amount'],2) != 0:
                    invoices_list.append(head)
            else:
                invoices_list.append(head)
                    
        selected_company = company
        selected_party = party
        
        context['pending_bills'] = pending_bills
        context['balance'] = balance
        context['advance_amount'] = advance_amount
        context['invoices_list'] = invoices_list
        context['trailor_expense_details'] = trailor_expense_details
        context['selected_party'] = selected_party
        context['selected_region'] = selected_region
        context['credit_notes'] = credit_notes
        context['journals'] = journals

    context['module'] = module
    context['selected_company'] = selected_company
    return render(request,'report/sales_outstanding/sales_outstanding2.html',context)

@login_required(login_url='home:handle_login')
def direct_creditors_outstanding_2(request,module):
    context = {}
    selected_company = "A"
    pending_bills = "Y"
    if request.method == "POST":
        party = request.POST['party']
        company = request.POST['company']
        selected_region = request.POST['region']
        pending_bills = request.POST['pending_bills']

        party = Party.objects.filter(id=int(party)).first()
        if not company == "A":
            selected_company = Logistic.objects.filter(id=int(company)).first()
        else:
            selected_company = None

        debit_notes = getDebitNote(party=party,company_type=selected_company,region=selected_region)
        advance_amount = getAdvancePayments(party=party,company_type=selected_company,region=selected_region)
        
       
        journals= getJournalAjustments(party=party,company_type=selected_company,region=selected_region)

        invoices = getPurchaseInvoices(party=party,company_type=selected_company,region=selected_region)
        
        
        
        if not company == "A":
            company = selected_company
        
        balance = 0
        invoices_list = []
        for i in invoices:
            

            head = {
                'invoice':i,
                'paid_amount':0,
                'balance_amount':0,
                'net_amount':0,
                'adjustments':[]
                # 'job_invoices':JobInvoice.objects.filter(job__job_no=i.job_no).values('invoice_no').all(),
            }
            
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == 'INR':
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass

            paid_amount = 0
            for j in i.pay_payment_inv.filter(voucher__is_deleted=False).all():
                paid_amount +=  ((j.paid_amount + j.tds_amount + j.adjustment_amount) * currency_ex_rate)
                head['adjustments'].append({
                    'type':'Payment',
                    'data':j
                })
                
                balance -= ((j.paid_amount + j.tds_amount + j.adjustment_amount) * currency_ex_rate)

          

            if i.tds_payable:
                paid_amount += (i.tds_payable * currency_ex_rate)


            debit_note = DebitNote.objects.filter(invoice_no=i.purchase_invoice_no).filter(is_deleted=False)
            debit_note_sum = 0
            for j in debit_note:
                debit_note_sum += (j.net_amount * j.currency_ex_rate)

                head['adjustments'].append({
                        'type':'DRN',
                        'data':j
                })
                
            paid_amount += debit_note_sum
            balance -= debit_note_sum

            debit_notes = debit_notes.exclude(invoice_no=i.purchase_invoice_no)
        
                 
            balance += (i.net_amount * currency_ex_rate)
            head['paid_amount'] = paid_amount
            head['net_amount'] = (i.net_amount * currency_ex_rate)
            head['balance_amount'] = (i.net_amount * currency_ex_rate) - paid_amount
            
            if pending_bills == "Y":
                if round(head['balance_amount'],2) != 0:
                    invoices_list.append(head)
            else:
                invoices_list.append(head)
                    
        selected_company = company
        selected_party = party
        
        context['pending_bills'] = pending_bills
        context['balance'] = balance
        context['advance_amount'] = advance_amount
        context['invoices_list'] = invoices_list
        context['selected_party'] = selected_party
        context['selected_region'] = selected_region
        context['debit_notes'] = debit_notes
        context['journals'] = journals

    context['module'] = module
    context['selected_company'] = selected_company
    return render(request,'report/creditors_outstanding/direct_creditors2.html',context)

@login_required(login_url='home:handle_login')
def indirect_creditors_outstanding_2(request,module):
    context = {}
    selected_company = "A"
    pending_bills = "Y"
    if request.method == "POST":
        party = request.POST['party']
        company = request.POST['company']
        selected_region = request.POST['region']
        pending_bills = request.POST['pending_bills']

        party = Vendor.objects.filter(id=int(party)).first()
        if not company == "A":
            selected_company = Logistic.objects.fillter(id=int(company)).first()
        else:
            selected_company = None

        debit_notes = getDebitNote(party=party,company_type=selected_company,region=selected_region,party_type="Indirect")
        advance_amount = getAdvancePayments(vendor=party,company_type=selected_company,region=selected_region,indirect=True)
        
       
        journals= getJournalAjustments(vendor=party,company_type=selected_company,region=selected_region)

        invoices = getPurchaseInvoices(vendor=party,company_type=selected_company,region=selected_region,indirect=True)
        
        
        
        if not company == "A":
            company = selected_company
        
        balance = 0
        invoices_list = []
        for i in invoices:
            

            head = {
                'invoice':i,
                'paid_amount':0,
                'balance_amount':0,
                'net_amount':0,
                'adjustments':[]
                # 'job_invoices':JobInvoice.objects.filter(job__job_no=i.job_no).values('invoice_no').all(),
            }
            
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == 'INR':
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass

            paid_amount = 0
            for j in i.pay_payment_inv.all():
                paid_amount +=  ((j.paid_amount + j.tds_amount + j.adjustment_amount) * currency_ex_rate)
                head['adjustments'].append({
                    'type':'Payment',
                    'data':j
                })
                
                balance -= ((j.paid_amount + j.tds_amount + j.adjustment_amount) * currency_ex_rate)

          

            if i.tds_payable:
                paid_amount += (i.tds_payable * currency_ex_rate)


            debit_note = DebitNote.objects.filter(invoice_no=i.purchase_invoice_no).filter(is_deleted=False)
            debit_note_sum = 0
            for j in debit_note:
                debit_note_sum += (j.net_amount * j.currency_ex_rate)

                head['adjustments'].append({
                        'type':'DRN',
                        'data':j
                })
                
            paid_amount += debit_note_sum
            balance -= debit_note_sum

            debit_notes = debit_notes.exclude(invoice_no=i.purchase_invoice_no)
        
                 
            balance += (i.net_amount * currency_ex_rate)
            head['paid_amount'] = paid_amount
            head['net_amount'] = (i.net_amount * currency_ex_rate)
            head['balance_amount'] = (i.net_amount * currency_ex_rate) - paid_amount
            
            if pending_bills == "Y":
                if round(head['balance_amount'],2) != 0:
                    invoices_list.append(head)
            else:
                invoices_list.append(head)
                    
        selected_company = company
        selected_party = party
        
        context['pending_bills'] = pending_bills
        context['balance'] = balance
        context['advance_amount'] = advance_amount
        context['invoices_list'] = invoices_list
        context['selected_party'] = selected_party
        context['selected_region'] = selected_region
        context['debit_notes'] = debit_notes
        context['journals'] = journals

    context['module'] = module
    context['selected_company'] = selected_company
    return render(request,'report/creditors_outstanding/indirect_creditors2.html',context)


def get_party_outstanding(party,selected_region):
    choose_party = party
    invoices_rec = []
    credit_notes = []
    invoices_pay = []
    rec_voucher = []
    pay_voucher = []

    invoices_rec = InvoiceReceivable.objects.filter(company_type__region=selected_region).filter(bill_to__id = choose_party.id).filter(is_einvoiced=True).filter(old_invoice=False).all()
    old_invoices_rec = InvoiceReceivable.objects.filter(company_type__region=selected_region).filter(bill_to__id = choose_party.id).filter(old_invoice=True).all()
    invoices_pay = InvoicePayable.objects.filter(company_type__region=selected_region).filter(bill_from__id = choose_party.id).all()
    rec_voucher = RecieptVoucher.objects.filter(company_type__region=selected_region).filter(party_name__id = choose_party.id).filter(advance_amount__gt=0).all()
    credit_notes = CreditNote.objects.filter(company_type__region=selected_region).filter(bill_to__id = choose_party.id).filter(is_einvoiced=True).filter(is_cancel=False).all()
    pay_voucher = PaymentVoucher.objects.filter(company_type__region=selected_region).filter(party_name__id = choose_party.id).filter(payment_type="Direct").all()

   

    credit_balance = 0
    debit_balance = 0
    party_ledgers = LedgerMaster.objects.filter(party=choose_party).all()
    for i in party_ledgers:
        if i.balance_in == "Debit":
            debit_balance += i.opening_balance
           
        if i.balance_in == "Credit":
            credit_balance += i.opening_balance
         
        if i.balance_in == "":
            debit_balance += i.opening_balance
         

    for i in credit_notes:
        currency_ex_rate = 1
        if i.currency_ex_rate:
            currency_ex_rate = i.currency_ex_rate
      
        credit_balance += (i.net_amount * i.currency_ex_rate)  
      
    for i in old_invoices_rec:
        for j in i.reciept_rec_inv.all():
            credit_balance += (j.received_amount + j.tds_amount + j.adjustment_amount)
   
    for i in invoices_rec:
        for j in i.reciept_rec_inv.all():
            credit_balance += (j.received_amount + j.tds_amount + j.adjustment_amount)
            
        currency_ex_rate = 1
        if i.currency_ex_rate:
            currency_ex_rate = i.currency_ex_rate
            
        if i.invoice_currency.short_name == "INR":
            currency_ex_rate = 1

        debit_balance += (i.net_amount * currency_ex_rate)
       
        
    for i in rec_voucher:
        credit_balance += i.advance_amount
        
    for i in invoices_pay:
        currency_ex_rate = 1
        if i.currency_ex_rate:
            currency_ex_rate = i.currency_ex_rate
            
        if i.invoice_currency.short_name == "INR" :
            currency_ex_rate = 1

        credit_balance += (i.net_amount * currency_ex_rate)
        

    for i in pay_voucher:
        for j in i.pay_voucher_detail.all():
         
            debit_balance += (j.paid_amount + j.tds_amount + j.adjustment_amount)
            
        if i.advance_amount:
            debit_balance += i.advance_amount
          
    return round((debit_balance - credit_balance),2)
  
@login_required(login_url='home:handle_login')
def party_wise_outstanding(request,module):
    context = {}
    parties = Party.objects.filter(is_active=True).all()
    report = []
    selected_region = None
    if request.method == "POST":
        selected_region = request.POST['region']
        
        for i in parties:
            
            balance = get_party_outstanding(i,selected_region)
            if abs(balance) > 0:
                report.append({
                    'party':i,
                    'outstanding':balance
                })

    context['selected_region'] = selected_region
    context['module'] = module
    context['report'] = report
    return render(request,'report/party_wise_outstanding/party_wise_outstanding.html',context)
  
@login_required(login_url='home:handle_login')
def party_outstanding_summary(request,module):
    context = {}
    parties = Party.objects.filter(is_active=True).all()
    report = []
    selected_region = None
    choose_type = None
    from_date = None
    to_date = None
    if request.method == "POST":
        selected_region = request.POST['region']
        choose_type = request.POST['choose_type']
        if not choose_type == "All":
            choose_type = int(choose_type)
            parties = parties.filter(party_type__id=int(choose_type)).all()

        for i in parties:
            balance = get_party_outstanding(i,selected_region)
            report.append({
                'party':i,
                'outstanding':balance
            })

    context['selected_region'] = selected_region
    context['from_date'] = from_date
    context['to_date'] = to_date
    context['choose_type'] = choose_type
    context['module'] = module
    context['report'] = report
    return render(request,'report/party_outstanding_summary/party_outstanding_summary.html',context)

def get_sundry_debtors_outstanding(party,selected_region,from_date=None,to_date=None):
    choose_party = party
    invoices_rec = []
    credit_notes = []
    rec_voucher = []
   

    invoices_rec = InvoiceReceivable.objects.filter(company_type__region=selected_region).filter(bill_to__id = choose_party.id).filter(is_einvoiced=True).filter(old_invoice=False).all()
    old_invoices_rec = InvoiceReceivable.objects.filter(bill_to__id = choose_party.id).filter(old_invoice=True).filter(company_type__region=selected_region).all()
    rec_voucher = RecieptVoucher.objects.filter(company_type__region=selected_region).filter(party_name__id = choose_party.id).filter(advance_amount__gt=0).all()
    credit_notes = CreditNote.objects.filter(company_type__region=selected_region).filter(bill_to__id = choose_party.id).filter(is_einvoiced=True).filter(is_cancel=False).all()

    party_ledgers = LedgerMaster.objects.filter(party=choose_party).all()

    if from_date and to_date:
        party_ledgers = party_ledgers.filter(opening_date__gte=from_date).filter(opening_date__lte=to_date).all()
        invoices_rec = invoices_rec.filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).all()
        old_invoices_rec = old_invoices_rec.filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).all()
        credit_notes = credit_notes.filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).all()
        rec_voucher = rec_voucher.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).all()
        
    
    credit_balance = 0
    debit_balance = 0
    for i in party_ledgers:
        if i.balance_in == "Debit":
            debit_balance += i.opening_balance
           
        if i.balance_in == "Credit":
            credit_balance += i.opening_balance
         
        if i.balance_in == "":
            debit_balance += i.opening_balance
         

    for i in credit_notes:
        currency_ex_rate = 1
        try:
            if not i.invoice_currency.short_name == "INR":
                currency_ex_rate = i.currency_ex_rate
        except:
            pass
      
        credit_balance += (i.net_amount * i.currency_ex_rate)  
      
    for i in old_invoices_rec:
        for j in i.reciept_rec_inv.all():
            credit_balance += (j.received_amount + j.tds_amount + j.adjustment_amount)
   
    for i in invoices_rec:
        for j in i.reciept_rec_inv.all():
            credit_balance += (j.received_amount + j.tds_amount + j.adjustment_amount)
            
        currency_ex_rate = 1
        try:
            if not i.invoice_currency.short_name == "INR":
                currency_ex_rate = i.currency_ex_rate
        except:
            pass
            
       
        debit_balance += (i.net_amount * currency_ex_rate)
       
        
    for i in rec_voucher:
        credit_balance += i.advance_amount
        
   
    return round((debit_balance - credit_balance),2)

def get_sundry_creditors_outstanding(party,party_type,selected_region,from_date=None,to_date=None):
    choose_party = party
    invoices_pay = []
    indirect_expense = []
    pay_voucher = []
   
    if party_type == "D":
        invoices_pay = InvoicePayable.objects.filter(company_type__region=selected_region).filter(bill_from__id = choose_party.id).all()
        pay_voucher = PaymentVoucher.objects.filter(company_type__region=selected_region).filter(party_name__id = choose_party.id).filter(payment_type="Direct").all()
        if from_date and to_date:
            invoices_pay = invoices_pay.filter(date_of_invoice__gte=from_date).filter(date_of_invoice__lte=to_date).all()
            pay_voucher = pay_voucher.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).all()
    else:
        pay_voucher = PaymentVoucher.objects.filter(company_type__region=selected_region).filter(vendor__id = choose_party.id).filter(payment_type="Indirect").all()
        indirect_expense = IndirectExpense.objects.filter(company_type__region=selected_region).filter(vendor=choose_party).all()
        if from_date and to_date:
            indirect_expense = indirect_expense.filter(bill_date__gte=from_date).filter(bill_date__lte=to_date).all()
            pay_voucher = pay_voucher.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).all()
    
    credit_balance = 0
    debit_balance = 0
    if party_type == "D":
        party_ledgers = LedgerMaster.objects.filter(party=choose_party).all()
    else:
        party_ledgers = LedgerMaster.objects.filter(vendor=choose_party).all()

    if from_date and to_date:
        party_ledgers = party_ledgers.filter(opening_date__gte=from_date).filter(opening_date__lte=to_date).all()

    for i in party_ledgers:
        if i.balance_in == "Debit":
            debit_balance += i.opening_balance
           
        if i.balance_in == "Credit":
            credit_balance += i.opening_balance
         
        if i.balance_in == "":
            debit_balance += i.opening_balance
         

    
    for i in indirect_expense:
        credit_balance += (i.net_amount)
        
    for i in invoices_pay:
        currency_ex_rate = 1
        if i.currency_ex_rate:
            currency_ex_rate = i.currency_ex_rate
            
        if i.invoice_currency.short_name == "INR" :
            currency_ex_rate = 1

        credit_balance += (i.net_amount * currency_ex_rate)
        

    for i in pay_voucher:
        for j in i.pay_voucher_detail.all():
         
            debit_balance += (j.paid_amount + j.tds_amount + j.adjustment_amount)
            
        if i.advance_amount:
            debit_balance += i.advance_amount
          
    return round((debit_balance - credit_balance),2)
  
@login_required(login_url='home:handle_login')
def sundry_creditors(request,module):
    context = {}
    parties = Party.objects.filter(is_active=True).exclude(Q(payable_invoice_bill_to=None) | Q(payment_party_name=None)).all()
    report = []
    selected_region = None
    from_date = None
    to_date = None
    if request.method == "POST":
        selected_region = request.POST['region']
        from_date = request.POST.get('from_date',None)
        to_date = request.POST.get('to_date',None)
        vendor = Vendor.objects.all()
       
        for i in parties:
            if from_date and to_date:
                balance = get_sundry_creditors_outstanding(i,'D',selected_region,from_date, to_date)
            else:
                balance = get_sundry_creditors_outstanding(i,'D',selected_region)

            report.append({
                'party':i,
                'outstanding':balance
            })
        for i in vendor:
            if from_date and to_date:
                balance = get_sundry_creditors_outstanding(i,'I',selected_region,from_date, to_date)
            else:
                balance = get_sundry_creditors_outstanding(i,'I',selected_region)
            report.append({
                'party':i,
                'outstanding':balance
            })

    context['from_date'] = from_date
    context['to_date'] = to_date

    context['selected_region'] = selected_region
  
    context['module'] = module
    context['report'] = report
    return render(request,'report/sundry_creditors/sundry_creditors.html',context)

@login_required(login_url='home:handle_login')
def sundry_debtors(request,module):
    context = {}
    parties = Party.objects.filter(is_active=True).exclude(Q(recievable_invoice_bill_to=None) | Q(received_party_name=None)).all()
    report = []
    selected_region = None
    from_date = None
    to_date = None
    if request.method == "POST":
        selected_region = request.POST['region']
        from_date = request.POST.get('from_date',None)
        to_date = request.POST.get('to_date',None)
        
        for i in parties:
            if from_date and to_date:
                balance = get_sundry_debtors_outstanding(i,selected_region,from_date,to_date)
            else:
                balance = get_sundry_debtors_outstanding(i,selected_region)
                
            report.append({
                'party':i,
                'outstanding':balance
            })
        
    context['from_date'] = from_date
    context['to_date'] = to_date
   
    context['selected_region'] = selected_region
  
    context['module'] = module
    context['report'] = report
    return render(request,'report/sundry_debtors/sundry_debtors.html',context)

@login_required(login_url='home:handle_login')
def sales_register(request,module):
    context = {}
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        finalize_bill = request.POST['finalize_bill']
        job_type = request.POST['job_type']
        location = request.POST['location']
        client = request.POST['client']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)
        if finalize_bill == "F":
            invoices = InvoiceReceivable.objects.filter(is_deleted=False).filter(is_einvoiced=True).filter(is_cancel=False).filter(old_invoice=False).filter(einvoice_date__range=[from_date,to_date]).select_related('bill_to','job_no','company_type','invoice_currency').all()
            
            credit_note = CreditNote.objects.filter(is_deleted=False).filter(is_cancel=False).filter(is_einvoiced=True).filter(einvoice_date__range=[from_date,to_date]).select_related('bill_to','job_no','company_type','invoice_currency').all()
        
        if finalize_bill == "U":
            invoices = InvoiceReceivable.objects.filter(is_deleted=False).filter(is_cancel=False).filter(old_invoice=False).filter(is_einvoiced=False).filter(is_deleted=False).filter(date_of_invoice__range=[from_date,to_date]).select_related('bill_to','job_no','company_type','invoice_currency').all()
            credit_note = CreditNote.objects.filter(is_deleted=False).filter(is_einvoiced=False).filter(is_deleted=False).filter(date_of_invoice__range=[from_date,to_date]).select_related('bill_to','job_no','company_type','invoice_currency').all()

        if not job_type == "A":
            invoices = invoices.filter(job_no__module = job_type).all()
            credit_note = credit_note.filter(job_no__module = job_type).all()

        if not location == "A":
            location = int(location)
            credit_note = credit_note.filter(company_type__id = int(location)).all()
            invoices = invoices.filter(company_type__id = int(location)).all()

        if not client == "A":
            client = int(client)
            credit_note = credit_note.filter(bill_to__id = int(client)).all()
            invoices = invoices.filter(bill_to__id = int(client)).all()
        
        context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
        context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()
        context['finalize_bill'] = finalize_bill
        context['job_type'] = job_type
        context['location'] = location
        context['client'] = client
        context['invoices'] = invoices
        context['credit_note'] = credit_note

    context['module'] = module

    return render(request,'report/register/sales_register.html',context)

@login_required(login_url='home:handle_login')
def purchase_register(request,module):
    context = {}
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        finalize_bill = request.POST['finalize_bill']
        job_type = request.POST['job_type']
        location = request.POST['location']
        client = request.POST['client']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)
        if finalize_bill == "F":
            invoices = InvoicePayable.objects.filter(is_deleted=False).filter(is_approved=True).filter(date_of_invoice__range=[from_date,to_date]).select_related('bill_from','job_no','company_type','invoice_currency').all()
        
        if finalize_bill == "U":
            invoices = InvoicePayable.objects.filter(is_deleted=False).filter(is_approved=False).filter(is_deleted=False).filter(date_of_invoice__range=[from_date,to_date]).select_related('bill_from','job_no','company_type','invoice_currency').all()

        if not job_type == "A":
            invoices = invoices.filter(job_no__module = job_type).all()

        if not location == "A":
            location = int(location)
            invoices = invoices.filter(company_type__id = int(location)).all()

        if not client == "A":
            client = int(client)
            invoices = invoices.filter(bill_from__id = int(client)).all()
        
        context['from_date'] = datetime.strptime(str(from_date),'%Y-%m-%d').date()
        context['to_date'] = datetime.strptime(str(to_date),'%Y-%m-%d').date()
        context['finalize_bill'] = finalize_bill
        context['job_type'] = job_type
        context['location'] = location
        context['client'] = client
        context['invoices'] = invoices

    context['module'] = module

    return render(request,'report/register/purchase_register.html',context)

def add_party_to_ledgers(request,module):
    parties = PartyAddress.objects.all()
    alter_count = 0
    for party in parties:
        ledger_name = f'{party.party.party_name} ({party.branch})'
        
        ledger = LedgerMaster.objects.filter(ledger_name=ledger_name).all()
        if ledger:
            for i in ledger:
                i.party = party.party
                i.party_address = party
                
                i.save()
                alter_count += 1
                
    messages.success(request,f'{alter_count} Repaired')
            
    return redirect('dashboard:accounting_dashboard',module=module)

def alter_final_invoice_for_e_invoices(request,module):
    invoices = InvoiceReceivable.objects.filter(is_einvoiced=True).filter(einvoice_date=None).all()
    alter_count = 0
    for invoice in invoices:
        if not invoice.einvoice_date:
            invoice.einvoice_date = invoice.date_of_invoice
            invoice.save()
            alter_count += 1
                
    messages.success(request,f'{alter_count} Invoice No. Repaired')
            
    return redirect('dashboard:accounting_dashboard',module=module)

def setb2bData(workbook,worksheet,from_date,to_date,company_type):
    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(category="B2B").filter(company_type__tax_policy="GST").all().order_by('final_invoice_no')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    no_of_customers = invoices.values('bill_to').annotate(count=Count('bill_to'))
    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']



    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.freeze_panes(4, 0)

    worksheet.write("A1","Summary For B2B(4)",cell_format_center)
    worksheet.write("A2","No. of Recipients",cell_format_center)
    worksheet.write("A3",f"{len(no_of_customers)}",cell_format_center_wc)
    worksheet.write("B1","",cell_format)
    worksheet.write("B2","",cell_format)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F3","",cell_format_wc)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("J3","",cell_format_wc)
    worksheet.write("K3","",cell_format_wc)
    worksheet.write("L3","",cell_format_wc)
    worksheet.write("M3","",cell_format_wc)
    
    worksheet.write("C2","No. of Invoices",cell_format_center)
    worksheet.write("C3",f"{len(invoices)}",cell_format_center_wc)
    worksheet.write("D2","",cell_format)

    worksheet.write("E2","Total Invoice Value",cell_format)
    worksheet.write("E3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("F2","",cell_format)
    worksheet.write("G2","",cell_format)
    worksheet.write("H2","",cell_format)
    worksheet.write("I2","",cell_format)
    worksheet.write("J2","",cell_format)
    worksheet.write("K2","",cell_format)
    
    worksheet.write("L2","Total Taxable Value",cell_format)
    worksheet.write("L3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    
    worksheet.write_url('M1', "internal:Help!A1")
    worksheet.write("M1","HELP",cell_format_center_wc)
    worksheet.write("M2","Total Cess",cell_format)
    worksheet.write("M3","0",cell_format_wc)


    worksheet.write("A4","GSTIN/UIN of Recipient",cell_format2)
    worksheet.write("B4","Receiver Name",cell_format2)
    worksheet.write("C4","Invoice Number",cell_format2)
    worksheet.write("D4","Invoice date",cell_format2)
    worksheet.write("E4","Invoice Value",cell_format2)
    worksheet.write("F4","Place Of Supply",cell_format2)
    worksheet.write("G4","Reverse Charge",cell_format2)
    worksheet.write("H4","Applicable % of Tax Rate",cell_format2)
    worksheet.write("I4","Invoice Type",cell_format2)
    worksheet.write("J4","E-Commerce GSTIN",cell_format2)
    worksheet.write("K4","Rate",cell_format2)
    worksheet.write("L4","Taxable Value",cell_format2)
    worksheet.write("M4","Cess Amount",cell_format2)

    start_index = 5
    for invoice in invoices:
        invoice_details  = invoice.recievable_invoice_reference.all()
        for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
            worksheet.write(f"A{start_index}",f"{invoice.bill_to_address.corp_gstin}",cell_format2_wc)
            worksheet.write(f"B{start_index}",f"{invoice.bill_to.party_name}",cell_format2_wc)
            worksheet.write(f"C{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
            worksheet.write(f"D{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
            worksheet.write(f"E{start_index}",f"{invoice.net_amount}",cell_format3_wc)
            worksheet.write(f"F{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)

            if invoice.type_of_invoice == "RCM":
                worksheet.write(f"G{start_index}","Y",cell_format2_wc)
            else:
                worksheet.write(f"G{start_index}","N",cell_format2_wc)

            worksheet.write(f"H{start_index}","",cell_format3_wc)

            if invoice.category == "B2B":
                worksheet.write(f"I{start_index}","Regular",cell_format2_wc)
            elif invoice.category == "SEWP":
                worksheet.write(f"I{start_index}","SEZ supplies with payment",cell_format2_wc)
            elif invoice.category == "SEWOP":
                worksheet.write(f"I{start_index}","SEZ supplies without payment",cell_format2_wc)

            worksheet.write(f"J{start_index}",f"{invoice.company_type.gstin_no}",cell_format2_wc)
            worksheet.write(f"K{start_index}",f"{detail['gst']}",cell_format3_wc)
            worksheet.write(f"L{start_index}",f"{detail['sum']}",cell_format3_wc)
            worksheet.write(f"M{start_index}","0",cell_format3_wc)

            start_index += 1

def setb2baData(workbook,worksheet,from_date,to_date,company_type):

    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference','ammendment_sales_invoice').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(category="B2B").filter(company_type__tax_policy="GST").exclude(ammendment_sales_invoice=None).all().order_by('ammendment_sales_invoice__id')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    no_of_customers = invoices.values('bill_to').annotate(count=Count('bill_to'))
    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']

    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.freeze_panes(4, 0)

    worksheet.write_url('O1',  'internal:"Help Instruction"!A1')

    worksheet.merge_range("E1:N1", "Revised Details", cell_format_center2)
    worksheet.write("A1","Summary For B2BA",cell_format_center)
    worksheet.write("A2","No. of Recipients",cell_format_center)
    worksheet.write("A3",f"{len(no_of_customers)}",cell_format_center_wc)
    worksheet.write("B1","Original details",cell_format2)
    worksheet.write("C1","",cell_format2)
    worksheet.write("D1","",cell_format2)
    worksheet.write("B2","",cell_format)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F3","",cell_format_wc)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("J3","",cell_format_wc)
    worksheet.write("K3","",cell_format_wc)
    worksheet.write("L3","",cell_format_wc)
    worksheet.write("M3","",cell_format_wc)
    
    worksheet.write("C2","No. of Invoices",cell_format_center)
    worksheet.write("C3",f"{len(invoices)}",cell_format_center_wc)
    worksheet.write("D2","",cell_format)

    worksheet.write("G2","Total Invoice Value",cell_format)
    worksheet.write("G3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("F2","",cell_format)
    worksheet.write("E2","",cell_format)
    worksheet.write("H2","",cell_format)
    worksheet.write("I2","",cell_format)
    worksheet.write("J2","",cell_format)
    worksheet.write("K2","",cell_format)
    
    worksheet.write("L2","",cell_format)
    worksheet.write("L3","",cell_format_wc)
    
    worksheet.write("N2","Total Taxable Value",cell_format)
    worksheet.write("N3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    
    worksheet.write("M2","",cell_format)
    worksheet.write("M3","",cell_format_wc)

    worksheet.write("O2","Total Cess",cell_format)
    worksheet.write("O3","0",cell_format_wc)
    worksheet.write_url('O1', "internal:Help!A1")
    worksheet.write("O1","HELP",cell_format_center)


    worksheet.write("A4","GSTIN/UIN of Recipient",cell_format2)
    worksheet.write("B4","Receiver Name",cell_format2)
    worksheet.write("C4","Original Invoice Number",cell_format2)
    worksheet.write("D4","Original Invoice date",cell_format2)
    worksheet.write("E4","Revised Invoice Number",cell_format_center2)
    worksheet.write("F4","Revised Invoice date",cell_format_center2)
    worksheet.write("G4","Invoice Value",cell_format_center2)
    worksheet.write("H4","Place of Supply",cell_format_center2)
    worksheet.write("I4","Reverse Charge",cell_format_center2)
    worksheet.write("J4","Applicable % of Tax Rate",cell_format_center2)
    worksheet.write("K4","Invoice Type",cell_format_center2)
    worksheet.write("L4","E-Commerce GSTIN",cell_format_center2)
    worksheet.write("M4","Rate",cell_format_center2)
    worksheet.write("N4","Taxable Value",cell_format_center2)
    worksheet.write("O4","Cess Amount",cell_format_center2)

    start_index = 5
    for invoice in invoices:
        for amm in invoice.ammendment_sales_invoice.all():
            invoice_details  = invoice.recievable_invoice_reference.all()
            for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
                worksheet.write(f"A{start_index}",f"{invoice.bill_to_address.corp_gstin}",cell_format2_wc)
                worksheet.write(f"B{start_index}",f"{invoice.bill_to.party_name}",cell_format2_wc)
                worksheet.write(f"C{start_index}",f"{amm.invoice_no}",cell_format2_wc)
                worksheet.write(f"D{start_index}",f"{datetime.strftime(amm.invoice_date,'%d-%b-%Y')}",cell_format2_wc)
                worksheet.write(f"E{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
                worksheet.write(f"F{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
                worksheet.write(f"G{start_index}",f"{invoice.net_amount}",cell_format3_wc)
                worksheet.write(f"H{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)

                if invoice.type_of_invoice == "RCM":
                    worksheet.write(f"I{start_index}","Y",cell_format2_wc)
                else:
                    worksheet.write(f"I{start_index}","N",cell_format2_wc)

                worksheet.write(f"J{start_index}","",cell_format3_wc)

                if invoice.category == "B2B":
                    worksheet.write(f"K{start_index}","Regular",cell_format2_wc)
                elif invoice.category == "SEWP":
                    worksheet.write(f"K{start_index}","SEZ supplies with payment",cell_format2_wc)
                elif invoice.category == "SEWOP":
                    worksheet.write(f"K{start_index}","SEZ supplies without payment",cell_format2_wc)

                worksheet.write(f"L{start_index}",f"{invoice.company_type.gstin_no}",cell_format2_wc)
                worksheet.write(f"M{start_index}",f"{round(detail['gst'],2)}",cell_format3_wc)
                worksheet.write(f"N{start_index}",f"{round(detail['sum'],2)}",cell_format3_wc)
                worksheet.write(f"O{start_index}","0",cell_format3_wc)

                start_index += 1

def setb2clData(workbook,worksheet,from_date,to_date,company_type):
    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(category="B2CL").filter(company_type__tax_policy="GST").all().order_by('final_invoice_no')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']


    worksheet.freeze_panes(4, 0)
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})

    worksheet.set_column(0, 20, 20)    

    worksheet.write_url('I1', "internal:Help!A1")
    worksheet.write('I1',"Help",cell_format_center_wc)


    worksheet.write("A1","Summary For B2CL(5)",cell_format_center)
    worksheet.write("A2","No. of Invoices",cell_format_center)
    worksheet.write("A3","0",cell_format_center_wc)
    worksheet.write("B2","",cell_format)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C2","Total Invoice Value",cell_format)
    worksheet.write("C3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("D2","",cell_format)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("E2","",cell_format)
    worksheet.write("E3","0",cell_format_wc)
    worksheet.write("F2","",cell_format)
    worksheet.write("F3","",cell_format_wc)
    worksheet.write("G2","Total Taxable Value",cell_format)
    worksheet.write("G3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    worksheet.write("H2","",cell_format)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I2","",cell_format)
    worksheet.write("I3","",cell_format_wc)
   
    

   


    worksheet.write("A4","Invoice Number",cell_format2)
    worksheet.write("B4","Invoice Date",cell_format2)
    worksheet.write("C4","Invoice Value",cell_format2)
    worksheet.write("D4","Place Of Supply",cell_format2)
    worksheet.write("E4","Applicable % of Tax Rate",cell_format2)
    worksheet.write("F4","Rate",cell_format2)
    worksheet.write("G4","Taxable Value",cell_format2)
    worksheet.write("H4","Cess Amount",cell_format2)
    worksheet.write("I4","E-Commerce GSTIN",cell_format2)

    start_index = 5
    for invoice in invoices:
        invoice_details  = invoice.recievable_invoice_reference.all()
        for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
            worksheet.write(f"A{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
            worksheet.write(f"B{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
            worksheet.write(f"C{start_index}",invoice.net_amount,cell_format3_wc)
            worksheet.write(f"D{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)
            worksheet.write(f"E{start_index}","",cell_format2_wc)
            worksheet.write(f"F{start_index}",f"{detail['gst']}",cell_format3_wc)
            worksheet.write(f"G{start_index}",f"{detail['sum']}",cell_format3_wc)
            worksheet.write(f"H{start_index}","0",cell_format3_wc)
            worksheet.write(f"I{start_index}",f"{invoice.company_type.gstin_no}",cell_format2_wc)
            start_index  += 1

def setb2claData(workbook,worksheet,from_date,to_date,company_type):

    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference','ammendment_sales_invoice').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(category="B2CL").filter(company_type__tax_policy="GST").exclude(ammendment_sales_invoice=None).all().order_by('ammendment_sales_invoice__id')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']

    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.freeze_panes(4, 0)


    worksheet.write("A1","Summary For B2CLA",cell_format_center)
    worksheet.write("B1","Original details",cell_format2)
    worksheet.write("C1","",cell_format2)
    worksheet.merge_range("D1:J1", "Revised Details", cell_format_center2)
    worksheet.write_url('K1', "internal:Help!A1")
    worksheet.write('K1',"Help",cell_format_center_wc)

    worksheet.write("A2","No. of Invoices",cell_format_center)
    worksheet.write("A3",f"{len(invoices)}",cell_format_center_wc)
    worksheet.write("B2","",cell_format_center)
    worksheet.write("B3:E3","",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("D2","",cell_format_center)
    worksheet.write("E2","",cell_format_center)
    
    worksheet.write("F2","Total Invoice Value",cell_format)
    worksheet.write("F3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("G2","",cell_format)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H2","",cell_format)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I2","Total Taxable Value",cell_format)
    worksheet.write("I3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    worksheet.write("J2","Total Cess",cell_format)
    worksheet.write("J3","0",cell_format_wc)
   
    worksheet.write("K2","",cell_format)
    worksheet.write("K3","",cell_format_wc)
    

   


    worksheet.write("A4","Original Invoice Number",cell_format2)
    worksheet.write("B4","Original Invoice date",cell_format2)
    worksheet.write("C4","Original Place Of Supply",cell_format2)
    worksheet.write("D4","Revised Invoice Number",cell_format_center2)
    worksheet.write("E4","Revised Invoice date",cell_format_center2)
    worksheet.write("F4","Invoice Value",cell_format_center2)
    worksheet.write("G4","Applicable % of Tax Rate",cell_format_center2)
   
    
    worksheet.write("H4","Rate",cell_format_center2)
    worksheet.write("I4","Taxable Value",cell_format_center2)
    worksheet.write("J4","Cess Amount",cell_format_center2)
    worksheet.write("K4","E-Commerce GSTIN",cell_format_center2)

    start_index = 5
    for invoice in invoices:
        for amm in invoice.ammendment_sales_invoice.all():
            invoice_details  = invoice.recievable_invoice_reference.all()
            for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
                worksheet.write(f"A{start_index}",f"{amm.invoice_no}",cell_format2_wc)
                worksheet.write(f"B{start_index}",f"{datetime.strftime(amm.invoice_date,'%d-%b-%Y')}",cell_format2_wc)
                worksheet.write(f"C{start_index}",f"{amm.party_address.corp_state.gst_code}-{amm.party_address.corp_state.name}",cell_format2_wc)
                worksheet.write(f"D{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
                worksheet.write(f"E{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
                worksheet.write(f"F{start_index}",f"{round(invoice.net_amount,2)}",cell_format2_wc)
                worksheet.write(f"G{start_index}",f"",cell_format2_wc)
                worksheet.write(f"H{start_index}",f"{detail['gst']}",cell_format2_wc)
                worksheet.write(f"I{start_index}",f"{round(detail['sum'],2)}",cell_format2_wc)
                worksheet.write(f"J{start_index}",f"0",cell_format2_wc)
                worksheet.write(f"K{start_index}",f"{invoice.company_type.gstin_no}",cell_format2_wc)
                start_index += 1

def setb2csData(workbook,worksheet,from_date,to_date,company_type):
    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(category="B2CS").filter(company_type__tax_policy="GST").all().order_by('final_invoice_no')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    worksheet.freeze_panes(4, 0)
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})

    worksheet.set_column(0, 20, 20)    

    worksheet.write_url('G1', "internal:Help!A1")
    worksheet.write('G1',"Help",cell_format_center_wc)


    worksheet.write("A1","Summary For B2CS(7)",cell_format_center)
    worksheet.write("A2","",cell_format_center)
    worksheet.write("A3","",cell_format_center_wc)
    worksheet.write("B2","",cell_format)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C2","",cell_format)
    worksheet.write("C3","",cell_format_wc)
    worksheet.write("D2","",cell_format)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("E2","Total Invoice Value",cell_format)
    worksheet.write("E3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("F2","Total Cess",cell_format)
    worksheet.write("F3","0",cell_format_wc)
    worksheet.write("G2","",cell_format)
  
    worksheet.write("A4","Type",cell_format2)
    worksheet.write("B4","Place of Supply",cell_format2)
    worksheet.write("C4","Applicable % of Tax Rate",cell_format2)
    worksheet.write("D4","Rate",cell_format2)
    worksheet.write("E4","Taxable Value",cell_format2)
    worksheet.write("F4","Cess Amount",cell_format2)
    worksheet.write("G4","E-Commerce GSTIN",cell_format2)

    start_index = 5
    for invoice in invoices:
        invoice_details  = invoice.recievable_invoice_reference.all()
        for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
            worksheet.write(f"A{start_index}","OE",cell_format2_wc)
            worksheet.write(f"B{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)
            worksheet.write(f"C{start_index}","",cell_format3_wc)
            worksheet.write(f"D{start_index}",f"{detail['gst']}",cell_format3_wc)
            worksheet.write(f"E{start_index}",f"{detail['sum']}",cell_format3_wc)
            worksheet.write(f"F{start_index}","0",cell_format3_wc)
            worksheet.write(f"G{start_index}",f"{invoice.company_type.gstin_no}",cell_format2_wc)
            start_index += 1
    
def setb2csaData(workbook,worksheet,from_date,to_date,company_type):
    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference','ammendment_sales_invoice').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(category="B2CS").filter(company_type__tax_policy="GST").exclude(ammendment_sales_invoice=None).all().order_by('ammendment_sales_invoice__id')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))
    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']
    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.freeze_panes(4, 0)



    worksheet.write("A1","Summary For B2CSA",cell_format_center)
    worksheet.write("B1","Original details",cell_format2)
    worksheet.merge_range("C1:H1", "Revised Details", cell_format_center2)
    worksheet.write_url('I1', "internal:Help!A1")
    worksheet.write('I1',"Help",cell_format_center2)

    worksheet.write("A2","",cell_format_center)
    worksheet.write("B2","",cell_format_center)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("D2","",cell_format_center)
    worksheet.write("E2","",cell_format_center)
    worksheet.write("F2","",cell_format_center)
    worksheet.write("A3","",cell_format_center_wc)
   
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C3","",cell_format_wc)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("E3","",cell_format_wc)
    worksheet.write("F3","",cell_format_wc)
   
    worksheet.write("G2","Total Taxable Value",cell_format)
    worksheet.write("G3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    worksheet.write("H2","Total Cess",cell_format)
    worksheet.write("H3","0",cell_format_wc)
    worksheet.write("I2","",cell_format)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("A4","Financial Year",cell_format2)
    worksheet.write("B4","Original Month",cell_format2)
    worksheet.write("C4","Place Of Supply",cell_format_center2)
    worksheet.write("D4","Type",cell_format_center2)
    worksheet.write("E4","Applicable % of Tax Rate",cell_format_center2)
    worksheet.write("F4","Rate",cell_format_center2)
    worksheet.write("G4","Taxable Value",cell_format_center2)
    worksheet.write("H4","Cess Amount",cell_format_center2)
    worksheet.write("I4","E-Commerce GSTIN",cell_format_center2)

    start_index = 5
    for invoice in invoices:
        for amm in invoice.ammendment_sales_invoice.all():
            invoice_details  = invoice.recievable_invoice_reference.all()
            for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
                worksheet.write(f"A{start_index}",f"",cell_format2_wc)
                worksheet.write(f"B{start_index}",f"",cell_format2_wc)
                worksheet.write(f"C{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)
                worksheet.write(f"D{start_index}",f"OE",cell_format2_wc)
                worksheet.write(f"E{start_index}",f"",cell_format2_wc)
                worksheet.write(f"F{start_index}",f"{round(detail['gst'],2)}",cell_format3_wc)
                worksheet.write(f"G{start_index}",f"{round(detail['sum'],2)}",cell_format3_wc)
                worksheet.write(f"H{start_index}",f"0",cell_format2_wc)
                worksheet.write(f"I{start_index}",f"{invoice.company_type.gstin_no}",cell_format2_wc)
                start_index += 1

def setcdnrData(workbook,worksheet,from_date,to_date,company_type):


    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = CreditNote.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('credit_note_reference').exclude(Q(category="B2CL")|Q(category="EXWP")|Q(category="EXWOP")).filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(company_type__tax_policy="GST").all().order_by('final_invoice_no')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    no_of_customers = invoices.values('bill_to').annotate(count=Count('bill_to'))
    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']



    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.freeze_panes(4, 0)

    worksheet.write("A1","Summary For CDNR(9B)",cell_format_center)
    worksheet.write("A2","No. of Recipients",cell_format_center)
    worksheet.write("A3",f"{len(no_of_customers)}",cell_format_center_wc)
    worksheet.write("B1","",cell_format)
    worksheet.write("B2","",cell_format_wc)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F3","",cell_format_wc)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("J3","",cell_format_wc)
    worksheet.write("K3","",cell_format_wc)
    worksheet.write("L3","",cell_format_wc)
    worksheet.write("M3","",cell_format_wc)
    
    worksheet.write("C2","No. of Notes",cell_format_center)
    worksheet.write("C3",f"{len(invoices)}",cell_format_center_wc)
    worksheet.write("D2","",cell_format)

    worksheet.write("I2","Total Note Value",cell_format)
    worksheet.write("I3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("F2","",cell_format)
    worksheet.write("G2","",cell_format)
    worksheet.write("H2","",cell_format)
    worksheet.write("E2","",cell_format)
    worksheet.write("J2","",cell_format)
    worksheet.write("K2","",cell_format)
    
    worksheet.write("L2","Total Taxable Value",cell_format)
    worksheet.write("L3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    
    worksheet.write("M2","Total Cess",cell_format)
    worksheet.write("M3","0",cell_format_wc)


    worksheet.write("A4","GSTIN/UIN of Recipient",cell_format2)
    worksheet.write("B4","Receiver Name",cell_format2)
    worksheet.write("C4","Note Number",cell_format2)
    worksheet.write("D4","Note date",cell_format2)
    worksheet.write("E4","Note Type",cell_format2)
    worksheet.write("F4","Place Of Supply",cell_format2)
    worksheet.write("G4","Reverse Charge",cell_format2)
    worksheet.write("H4","Note Supply Type",cell_format2)
    worksheet.write("I4","Note Value",cell_format2)
    worksheet.write("J4","Applicable % of Tax Rate",cell_format2)
    worksheet.write("K4","Rate",cell_format2)
    worksheet.write("L4","Taxable Value",cell_format2)
    worksheet.write("M4","Cess Amount",cell_format2)

    start_index = 5
    for invoice in invoices:
        invoice_details  = invoice.credit_note_reference.all()
        for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
            worksheet.write(f"A{start_index}",f"{invoice.bill_to_address.corp_gstin}",cell_format2_wc)
            worksheet.write(f"B{start_index}",f"{invoice.bill_to.party_name}",cell_format2_wc)
            worksheet.write(f"C{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
            worksheet.write(f"D{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
            worksheet.write(f"E{start_index}","C",cell_format2_wc)
            worksheet.write(f"F{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)
            if invoice.is_rcm:
                worksheet.write(f"G{start_index}","Y",cell_format2_wc)
            else:
                worksheet.write(f"G{start_index}","N",cell_format2_wc)

            if invoice.category == "B2B":
                worksheet.write(f"H{start_index}","Regular",cell_format2_wc)
            elif invoice.category == "SEWP":
                worksheet.write(f"H{start_index}","SEZ supplies with payment",cell_format2_wc)
            elif invoice.category == "SEWOP":
                worksheet.write(f"H{start_index}","SEZ supplies without payment",cell_format2_wc)

            worksheet.write(f"I{start_index}",f"{round(invoice.net_amount,2)}",cell_format3_wc)
            worksheet.write(f"J{start_index}","",cell_format3_wc)
            worksheet.write(f"K{start_index}",f"{round(detail['gst'],2)}",cell_format3_wc)
            worksheet.write(f"L{start_index}",f"{detail['sum']}",cell_format3_wc)
            worksheet.write(f"M{start_index}","0",cell_format3_wc)


            start_index += 1

def setcdnraData(workbook,worksheet,from_date,to_date,company_type):
    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = CreditNote.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('credit_note_reference','ammendment_crn').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(category="B2B").filter(company_type__tax_policy="GST").exclude(ammendment_crn=None).all().order_by('ammendment_crn__id')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    no_of_customers = invoices.values('bill_to').annotate(count=Count('bill_to'))
    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']

    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.freeze_panes(4, 0)

    worksheet.write_url('O1',  "internal:'Help'!A1")

    worksheet.merge_range("E1:N1", "Revised Details", cell_format_center2)
    worksheet.write("A1","Summary For CDNRA",cell_format_center)
    worksheet.write("A2","No. of Recipients",cell_format_center)
    worksheet.write("A3",f"{len(no_of_customers)}",cell_format_center_wc)
    worksheet.merge_range("B1:D1","Original details",cell_format2)
   
    worksheet.write("B2","",cell_format)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F3","",cell_format_wc)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("J3","",cell_format_wc)
    worksheet.write("K3","",cell_format_wc)
    worksheet.write("L3","",cell_format_wc)
    worksheet.write("M3","",cell_format_wc)
    
    worksheet.write("C2","No. of Notes",cell_format_center)
    worksheet.write("C3",f"{len(invoices)}",cell_format_center_wc)
    worksheet.write("D2","",cell_format)

    worksheet.write("K2","Total Note Value",cell_format)
    worksheet.write("K3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("F2","",cell_format)
    worksheet.write("E2","",cell_format)
    worksheet.write("H2","",cell_format)
    worksheet.write("I2","",cell_format)
    worksheet.write("J2","",cell_format)
    worksheet.write("G2","",cell_format)
    
    worksheet.write("L2","",cell_format)
    worksheet.write("L3","",cell_format_wc)
    
    worksheet.write("N2","Total Taxable Value",cell_format)
    worksheet.write("N3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    
    worksheet.write("M2","",cell_format)
    worksheet.write("M3","",cell_format_wc)

    worksheet.write("O2","Total Cess",cell_format)
    worksheet.write("O3","0",cell_format_wc)
    worksheet.write("O1","HELP",cell_format_center)


    worksheet.write("A4","GSTIN/UIN of Recipient",cell_format2)
    worksheet.write("B4","Receiver Name",cell_format2)
    worksheet.write("C4","Original Note Number",cell_format2)
    worksheet.write("D4","Original Note date",cell_format2)
    worksheet.write("E4","Revised Note Number",cell_format_center2)
    worksheet.write("F4","Revised Note date",cell_format_center2)
    worksheet.write("G4","Note Type",cell_format_center2)
    worksheet.write("H4","Place of Supply",cell_format_center2)
    worksheet.write("I4","Reverse Charge",cell_format_center2)
    worksheet.write("J4","Note Supply Type",cell_format_center2)
    worksheet.write("K4","Note Value",cell_format_center2)
    worksheet.write("L4","Applicable % of Tax Rate",cell_format_center2)
    worksheet.write("M4","Rate",cell_format_center2)
    worksheet.write("N4","Taxable Value",cell_format_center2)
    worksheet.write("O4","Cess Amount",cell_format_center2)

    start_index = 5
    for invoice in invoices:
        for amm in invoice.ammendment_crn.all():
            invoice_details  = invoice.credit_note_reference.all()
            for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
                worksheet.write(f"A{start_index}",f"{invoice.bill_to_address.corp_gstin}",cell_format2_wc)
                worksheet.write(f"B{start_index}",f"{invoice.bill_to.party_name}",cell_format2_wc)
                worksheet.write(f"C{start_index}",f"{amm.invoice_no}",cell_format2_wc)
                worksheet.write(f"D{start_index}",f"{datetime.strftime(amm.invoice_date,'%d-%b-%Y')}",cell_format2_wc)
                worksheet.write(f"E{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
                worksheet.write(f"F{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
                worksheet.write(f"G{start_index}",f"C",cell_format2_wc)
                worksheet.write(f"H{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)
                if invoice.is_rcm:
                    worksheet.write(f"I{start_index}","Y",cell_format2_wc)
                else:
                    worksheet.write(f"I{start_index}","N",cell_format2_wc)

                if invoice.category == "B2B":
                    worksheet.write(f"J{start_index}","Regular",cell_format2_wc)
                elif invoice.category == "SEWP":
                    worksheet.write(f"J{start_index}","SEZ supplies with payment",cell_format2_wc)
                elif invoice.category == "SEWOP":
                    worksheet.write(f"J{start_index}","SEZ supplies without payment",cell_format2_wc)

                worksheet.write(f"K{start_index}",f"{invoice.net_amount}",cell_format3_wc)
                worksheet.write(f"L{start_index}","",cell_format3_wc)
                worksheet.write(f"M{start_index}",f"{round(detail['gst'],2)}",cell_format3_wc)
                worksheet.write(f"N{start_index}",f"{round(detail['sum'],2)}",cell_format3_wc)
                worksheet.write(f"O{start_index}","0",cell_format3_wc)


               

                start_index += 1

def setcdnurData(workbook,worksheet,from_date,to_date,company_type):

    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = CreditNote.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('credit_note_reference').filter(Q(category="B2CL")|Q(category="EXWP")|Q(category="EXWOP")).filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(company_type__tax_policy="GST").all().order_by('final_invoice_no')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()


    no_of_customers = invoices.values('bill_to').annotate(count=Count('bill_to'))
    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']


    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center","text_wrap":True})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center","text_wrap":True})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.freeze_panes(4, 0)

    worksheet.set_column(0, 1, 28)   
    worksheet.write("A1","Summary For CDNUR(9B)",cell_format_center)

    worksheet.set_column(1, 10, 20)   
    
    worksheet.write_url('J1', "internal:Help!A1")
    worksheet.write("J1","Help",cell_format_center)
     
    worksheet.write("A2","",cell_format_center)
    worksheet.write("B2","No. of Notes/Vouchers",cell_format_center)
    worksheet.write("B3",f"{len(invoices)}",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_wc)
    worksheet.write("D2","",cell_format_center)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("E2","",cell_format_center)
    worksheet.write("E3","",cell_format_wc)
    worksheet.write("F2","Total Note Value",cell_format_center)
    worksheet.write("F3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("G2","",cell_format_center)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H2","",cell_format_center)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I2","Total Taxable Value",cell_format_center)
    worksheet.write("I3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
    worksheet.write("J2","Total Cess",cell_format_center)
    worksheet.write("J3","0",cell_format_wc)
    worksheet.write("A4","UR Type",cell_format2)
    worksheet.write("B4","Note Number",cell_format2)
    worksheet.write("C4","Note Date",cell_format2)
    worksheet.write("D4","Note Type",cell_format2)
    worksheet.write("E4","Place of Supply",cell_format2)
    worksheet.write("F4","Note Value",cell_format2)
    worksheet.write("G4","Applicable % of Tax Rate",cell_format2)
    worksheet.write("H4","Rate",cell_format2)
    worksheet.write("I4","Taxable Value",cell_format2)
    worksheet.write("J4","Cess Amount",cell_format2)

    start_index = 5
    for invoice in invoices:
        invoice_details  = invoice.credit_note_reference.all()
        for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
            worksheet.write(f"A{start_index}",f"{invoice.category}",cell_format2_wc)
            worksheet.write(f"B{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
            worksheet.write(f"C{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
            worksheet.write(f"D{start_index}",f"C",cell_format2_wc)
            worksheet.write(f"E{start_index}",f"{invoice.bill_to_address.corp_state.gst_code}-{invoice.bill_to_address.corp_state.name}",cell_format2_wc)
            worksheet.write(f"F{start_index}",f"{round(invoice.net_amount,2)}",cell_format3_wc)
            worksheet.write(f"G{start_index}","",cell_format3_wc)
            worksheet.write(f"H{start_index}",f"{detail['gst']}",cell_format3_wc)
            worksheet.write(f"I{start_index}",f"{detail['sum']}",cell_format3_wc)
            worksheet.write(f"J{start_index}","0",cell_format3_wc)

            start_index += 1

def setcdnuraData(workbook,worksheet):
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.write_url('L1',  "internal:'Help'!A1")

    worksheet.merge_range("D1:K1", "Revised Details", cell_format_center2)
    worksheet.write("A1","Summary For CDNRA",cell_format_center)
    worksheet.write("A2","",cell_format_center)
    worksheet.write("A3","",cell_format_center_wc)
    worksheet.merge_range("B1:C1","Original details",cell_format2)
   
    worksheet.write("B2","No. of Notes/Vouchers",cell_format)
    worksheet.write("B3","0",cell_format_wc)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F3","",cell_format_wc)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("J3","",cell_format_wc)
    worksheet.write("K3","",cell_format_wc)
    worksheet.write("L3","",cell_format_wc)
    
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_center_wc)
    worksheet.write("D2","",cell_format)
    worksheet.write("E2","",cell_format)
    worksheet.write("F2","",cell_format)
    worksheet.write("G2","",cell_format)
    worksheet.write("H2","Total Note Value",cell_format)
    worksheet.write("H3","0",cell_format_wc)
    worksheet.write("I2","",cell_format)
    worksheet.write("J2","",cell_format)

    worksheet.write("K2","Total Taxable Value",cell_format)
    worksheet.write("K3","0",cell_format_wc)
    
    worksheet.write("L1","HELP",cell_format_center)
    worksheet.write("L2","Total Cess",cell_format)
    worksheet.write("L3","0",cell_format_wc)
    


    worksheet.write("A4","UR Type",cell_format2)
    worksheet.write("B4","Original Note Number",cell_format2)
    worksheet.write("C4","Original Note Date",cell_format2)
    worksheet.write("D4","Revised Note Number",cell_format2)
    worksheet.write("E4","Revised Note Date",cell_format_center2)
    worksheet.write("F4","Note Type",cell_format_center2)
    worksheet.write("G4","Place Of Supply",cell_format_center2)
    worksheet.write("H4","Note Value",cell_format_center2)
    worksheet.write("I4","Applicable % of Tax Rate",cell_format_center2)
    worksheet.write("J4","Rate",cell_format_center2)
    worksheet.write("K4","Taxable Value",cell_format_center2)
    worksheet.write("L4","Cess Amount",cell_format_center2)
    
def setexpData(workbook,worksheet,from_date,to_date,company_type):

    from_date = datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date = datetime.strptime(str(to_date),'%Y-%m-%d')
    invoices = InvoiceReceivable.objects.select_related('company_type','bill_to','bill_to_address','bill_to_address__corp_state').prefetch_related('recievable_invoice_reference').filter(is_einvoiced=True).exclude(is_cancel=True).exclude(is_deleted=True).filter(einvoice_date__range=[from_date,to_date]).filter(Q(category='EXPWP')|Q(category='EXWOP')).filter(company_type__tax_policy="GST").all().order_by('final_invoice_no')
    if not company_type == "A":
        invoices = invoices.filter(company_type__company_gst_code=company_type).all()

    no_of_customers = invoices.values('bill_to').annotate(count=Count('bill_to'))
    total_invoice_value = invoices.aggregate(sum=Sum('net_amount'))
    total_gst_invoice_value = invoices.aggregate(sum=Sum('gst_amount'))

    if not total_invoice_value['sum']:
        total_invoice_value = 0
    else:
        total_invoice_value = total_invoice_value['sum']

    if not total_gst_invoice_value['sum']:
        total_gst_invoice_value = 0
    else:
        total_gst_invoice_value = total_gst_invoice_value['sum']


    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center","text_wrap":True})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center","text_wrap":True})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.freeze_panes(4, 0)

    worksheet.set_column(0, 1, 28)   
    worksheet.write("A1","Summary For EXP(6)",cell_format_center)

    worksheet.set_column(1, 10, 20)   
    
    worksheet.write_url('J1', "internal:Help!A1")
    worksheet.write("J1","Help",cell_format_center)
     
    worksheet.write("A2","",cell_format_center)
    worksheet.write("B2","No. of Invoices",cell_format_center)
    worksheet.write("B3",f"{len(invoices)}",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_wc)
    worksheet.write("D2","Total Invoice Value",cell_format_center)
    worksheet.write("D3",f"{round(total_invoice_value,2)}",cell_format_wc)
    worksheet.write("E2","",cell_format_center)
    worksheet.write("E3","",cell_format_wc)
    worksheet.write("F2","No. of Shipping Bill",cell_format_center)
    worksheet.write("F3","0",cell_format_wc)
    worksheet.write("G2","",cell_format_center)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H2","",cell_format_center)
    worksheet.write("H3","",cell_format_wc)
    worksheet.write("I2","",cell_format_center)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("J2","Total Taxable Value",cell_format_center)
    worksheet.write("J3",f"{round(total_gst_invoice_value,2)}",cell_format_wc)
   

    worksheet.write("A4","Export Type",cell_format2)
    worksheet.write("B4","Invoice Number",cell_format2)
    worksheet.write("C4","Invoice date",cell_format2)
    worksheet.write("D4","Invoice Value",cell_format2)
    worksheet.write("E4","Port Code",cell_format2)
    worksheet.write("F4","Shipping Bill Number",cell_format2)
    worksheet.write("G4","Shipping Bill Date",cell_format2)
    worksheet.write("H4","Rate",cell_format2)
    worksheet.write("I4","Taxable Value",cell_format2)
    worksheet.write("J4","Cess Amount",cell_format2)


    start_index = 5
    for invoice in invoices:
        invoice_details  = invoice.recievable_invoice_reference.all()
        for detail in invoice_details.values('gst').annotate(sum=Sum('gst_amount')).all():
            worksheet.write(f"A{start_index}",f"{invoice.category}",cell_format2_wc)
            worksheet.write(f"B{start_index}",f"{invoice.final_invoice_no}",cell_format2_wc)
            worksheet.write(f"C{start_index}",f"{datetime.strftime(invoice.einvoice_date,'%d-%b-%Y')}",cell_format2_wc)
            worksheet.write(f"D{start_index}",f"{invoice.net_amount}",cell_format3_wc)
            worksheet.write(f"E{start_index}",f"",cell_format2_wc)
            worksheet.write(f"F{start_index}",f"",cell_format2_wc)
            worksheet.write(f"G{start_index}",f"",cell_format2_wc)
            worksheet.write(f"H{start_index}",f"{detail['gst']}",cell_format3_wc)
            worksheet.write(f"I{start_index}",f"{round(detail['sum'],2)}",cell_format3_wc)
            worksheet.write(f"J{start_index}","0",cell_format3_wc)
            start_index += 1

def setexpaData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.write_url('L1',  "internal:'Help'!A1")

    worksheet.merge_range("D1:K1", "Revised Details", cell_format_center2)
    worksheet.write("A1","Summary For EXPA",cell_format_center)
    worksheet.write("A2","",cell_format_center)
    worksheet.write("A3","",cell_format_center_wc)
    worksheet.merge_range("B1:C1","Original details",cell_format2)
    worksheet.write("B2","No. of Invoices",cell_format)
    worksheet.write("B3","0",cell_format_wc)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F2","Total Invoice Value",cell_format)
    worksheet.write("F3","",cell_format_wc)
    worksheet.write("G3","",cell_format_wc)
    worksheet.write("H2","No. of Shipping Bill",cell_format)
    worksheet.write("H3","0",cell_format_wc)
    worksheet.write("I3","",cell_format_wc)
    worksheet.write("J3","",cell_format_wc)
    worksheet.write("K3","",cell_format_wc)
    worksheet.write("L3","Total Taxable Value",cell_format)
    worksheet.write("L3","0",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_center_wc)
    worksheet.write("D2","",cell_format)
    worksheet.write("E2","",cell_format)
    worksheet.write("F2","",cell_format)
    worksheet.write("G2","",cell_format)
    worksheet.write("H2","Total Note Value",cell_format)
    worksheet.write("H3","0",cell_format_wc)
    worksheet.write("I2","",cell_format)
    worksheet.write("J2","",cell_format)
    worksheet.write("K2","Total Taxable Value",cell_format)
    worksheet.write("K3","0",cell_format_wc)
    worksheet.write("L1","HELP",cell_format_center)
    worksheet.write("L2","Total Cess",cell_format)
    worksheet.write("L3","0",cell_format_wc)
    worksheet.write("A4","Export Type",cell_format2)
    worksheet.write("B4","Original Invoice Number",cell_format2)
    worksheet.write("C4","Original Invoice Date",cell_format2)
    worksheet.write("D4","Revised Invoice Number",cell_format2)
    worksheet.write("E4","Revised Invoice Date",cell_format_center2)
    worksheet.write("F4","Invoice Value",cell_format_center2)
    worksheet.write("G4","Port Code",cell_format_center2)
    worksheet.write("H4","Shipping Bill Number",cell_format_center2)
    worksheet.write("I4","Shipping Bill Date",cell_format_center2)
    worksheet.write("J4","Rate",cell_format_center2)
    worksheet.write("K4","Taxable Value",cell_format_center2)
    worksheet.write("L4","Cess Amount",cell_format_center2)

def setatData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center","text_wrap":True})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center","text_wrap":True})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.freeze_panes(4, 0)

    worksheet.set_column(0, 1, 28)   
    worksheet.write("A1","Summary For Advance Received (11B)",cell_format_center)
    worksheet.set_column(1, 10, 20)   
    worksheet.write_url('E1', "internal:Help!A1")
    worksheet.write("E1","Help",cell_format_center)
    worksheet.write("A2","",cell_format_center)
    worksheet.write("B2","",cell_format_center)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_wc)
    worksheet.write("D2","Total Advance Received",cell_format_center)
    worksheet.write("D3","0",cell_format_wc)
    worksheet.write("E2","Total Cess",cell_format_center)
    worksheet.write("E3","0",cell_format_wc)
   

    worksheet.write("A4","Place Of Supply",cell_format2)
    worksheet.write("B4","Applicable % of Tax Rate",cell_format2)
    worksheet.write("C4","Rate",cell_format2)
    worksheet.write("D4","Gross Advance Received",cell_format2)
    worksheet.write("E4","Cess Amount",cell_format2)
  
def setataData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center",'text_wrap': True})
    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.write_url('G1',  "internal:'Help'!A1")

    worksheet.merge_range("D1:F1", "Revised Details", cell_format_center2)
    worksheet.write("A1","Summary For Amended Tax Liability(Advance Received) ",cell_format_center)
    worksheet.write("A2","",cell_format_center)
    worksheet.write("A3","",cell_format_center_wc)
    worksheet.merge_range("B1:C1","Original details",cell_format2)
   
    worksheet.write("B2","",cell_format)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_center_wc)
    worksheet.write("D2","",cell_format)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F2","Total Advance Received",cell_format)
    worksheet.write("F3","0",cell_format_wc)
  
    worksheet.write("G2","Total Cess",cell_format)
    worksheet.write("G3","0",cell_format_wc)
    
    worksheet.write("E2","",cell_format)
    worksheet.write("F2","",cell_format)
   

    worksheet.write("G1","HELP",cell_format_center)
    
    


    worksheet.write("A4","Financial Year",cell_format2)
    worksheet.write("B4","Original Month",cell_format2)
    worksheet.write("C4","Original Place Of Supply",cell_format2)
    worksheet.write("D4","Applicable % of Tax Rate",cell_format_center2)
    worksheet.write("E4","Rate",cell_format_center2)
    worksheet.write("F4","Gross Advance Received",cell_format_center2)
    worksheet.write("G4","Cess Amount",cell_format_center2)
   
def setatdjData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center","text_wrap":True})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center","text_wrap":True})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.freeze_panes(4, 0)

    worksheet.set_column(0, 1, 50)   
    worksheet.write("A1","Summary For Advance Adjusted (11B)",cell_format_center)

    
    worksheet.write_url('E1', "internal:Help!A1")
    worksheet.write("E1","Help",cell_format_center)
    worksheet.set_column(1, 5, 25)   
    worksheet.write("A2","",cell_format_center)
    worksheet.write("B2","",cell_format_center)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_wc)
    worksheet.write("D2","Total Advance Adjusted",cell_format_center)
    worksheet.write("D3","0",cell_format_wc)
    worksheet.write("E2","Total Cess",cell_format_center)
    worksheet.write("E3","0",cell_format_wc)
   
   

    worksheet.write("A4","Place Of Supply",cell_format2)
    worksheet.write("B4","Applicable % of Tax Rate",cell_format2)
    worksheet.write("C4","Rate",cell_format2)
    worksheet.write("D4","Gross Advance Adjusted",cell_format2)
    worksheet.write("E4","Cess Amount",cell_format2)

def setatdjaData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center",'text_wrap': True})
    cell_format_center2 = workbook.add_format({'font_color': 'black','bg_color':"#B4C6E7","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    worksheet.set_column(0, 20, 20)   
    worksheet.write_url('G1',  "internal:'Help'!A1")

    worksheet.merge_range("D1:F1", "Revised Details", cell_format_center2)
    worksheet.write("A1","Summary For Amendement Of Adjustment Advances",cell_format_center)
    worksheet.write("A2","",cell_format_center)
    worksheet.write("A3","",cell_format_center_wc)
    worksheet.merge_range("B1:C1","Original details",cell_format2)
   
    worksheet.write("B2","",cell_format)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_center_wc)
    worksheet.write("D2","",cell_format)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("F2","Total Advance Adjusted",cell_format)
    worksheet.write("F3","0",cell_format_wc)
  
    worksheet.write("G2","Total Cess",cell_format)
    worksheet.write("G3","0",cell_format_wc)
    
    worksheet.write("E2","",cell_format)
    worksheet.write("F2","",cell_format)
   

    worksheet.write("G1","HELP",cell_format_center)
    
    


    worksheet.write("A4","Financial Year",cell_format2)
    worksheet.write("B4","Original Month",cell_format2)
    worksheet.write("C4","Original Place Of Supply",cell_format2)
    worksheet.write("D4","Applicable % of Tax Rate",cell_format_center2)
    worksheet.write("E4","Rate",cell_format_center2)
    worksheet.write("F4","Gross Advance Adjusted",cell_format_center2)
    worksheet.write("G4","Cess Amount",cell_format_center2)
   
def setexempData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center","text_wrap":True})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center","text_wrap":True})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.freeze_panes(4, 0)

    worksheet.set_column(0, 1, 50)   
    worksheet.write("A1","Summary For Nil rated, exempted and non GST outward supplies (8)",cell_format_center)

    
    worksheet.write_url('D1', "internal:Help!A1")
    worksheet.write("D1","Help",cell_format_center)
    worksheet.set_column(1, 5, 25)   
    worksheet.write("A2","",cell_format_center)
    worksheet.write("B2","Total Nil Rated Supplies",cell_format_center)
    worksheet.write("B3","0",cell_format_wc)
    worksheet.write("C2","Total Exempted Supplies",cell_format_center)
    worksheet.write("C3","0",cell_format_wc)
    worksheet.write("D2","Total Non-GST Supplies",cell_format_center)
    worksheet.write("D3","0",cell_format_wc)
   

    worksheet.write("A4","Description",cell_format2)
    worksheet.write("B4","Nil Rated Supplies",cell_format2)
    worksheet.write("C4","Exempted(other than nil rated/non GST supply)",cell_format2)
    worksheet.write("D4","Non-GST Supplies",cell_format2)

def setdocData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.freeze_panes(4, 0)

    worksheet.set_column(0, 1, 50)   
    worksheet.write("A1","Summary of documents issued during the tax period (13)",cell_format_center)

    
    worksheet.write_url('E1', "internal:Help!A1")
    worksheet.write("E1","Help",cell_format_center)
    worksheet.set_column(1, 5, 20)   
    worksheet.write("A2","",cell_format_center)
    worksheet.write("B2","",cell_format_center)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("D2","Total Number",cell_format_center)
    worksheet.write("D3","0",cell_format_wc)
    worksheet.write("E2","Total Cancelled",cell_format_center)
    worksheet.write("E3","0",cell_format_wc)

    worksheet.write("A4","Nature of Document",cell_format2)
    worksheet.write("B4","Sr. No. From",cell_format2)
    worksheet.write("C4","Sr. No. To",cell_format2)
    worksheet.write("D4","Total Number",cell_format2)
    worksheet.write("E4","Cancelled",cell_format2)

def sethsnData(workbook,worksheet):

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"right"})
    cell_format3_wc = workbook.add_format({"align":"right"})
    cell_format_center_wc = workbook.add_format({'bold': True, 'border':1,'border_color':"black","align":"center"})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    cell_format2_wc = workbook.add_format({"align":"center"})
    worksheet.freeze_panes(4, 0)

    worksheet.set_column(0, 10, 20)   
    worksheet.write("A1","Summary For HSN(12)",cell_format_center)

    
    worksheet.write_url('J1', "internal:Help!A1")
    worksheet.write("J1","Help",cell_format_center)
    
    worksheet.write("A2","No. of HSN",cell_format_center)
    worksheet.write("A3","0",cell_format_wc)
    worksheet.write("B2","",cell_format_center)
    worksheet.write("B3","",cell_format_wc)
    worksheet.write("C2","",cell_format_center)
    worksheet.write("C3","",cell_format_wc)
    worksheet.write("D2","",cell_format_center)
    worksheet.write("D3","",cell_format_wc)
    worksheet.write("E2","Total Value",cell_format_center)
    worksheet.write("E3","0",cell_format_wc)
    worksheet.write("F2","Total Taxable Value",cell_format_center)
    worksheet.write("F3","0",cell_format_wc)
    worksheet.write("G2","Total Integrated Tax",cell_format_center)
    worksheet.write("G3","0",cell_format_wc)
    worksheet.write("H2","Total Central Tax",cell_format_center)
    worksheet.write("H3","0",cell_format_wc)
    worksheet.write("I2","Total State/UT Tax",cell_format_center)
    worksheet.write("I3","0",cell_format_wc)
    worksheet.write("J2","Total Cess",cell_format_center)
    worksheet.write("J3","0",cell_format_wc)

    worksheet.write("A4","HSN",cell_format2)
    worksheet.write("B4","Description",cell_format2)
    worksheet.write("C4","UQC",cell_format2)
    worksheet.write("D4","Total Quantity",cell_format2)
    worksheet.write("E4","Total Value",cell_format2)
    worksheet.write("F4","Taxable Value",cell_format2)
    worksheet.write("G4","Integrated Tax Amount",cell_format2)
    worksheet.write("H4","Central Tax Amount",cell_format2)
    worksheet.write("I4","State/UT Tax Amount",cell_format2)
    worksheet.write("J4","Cess Amount",cell_format2)

def setmasterData(workbook,worksheet):
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black','bg_color':"#B4C6E7","align":"center",'text_wrap': True})
    cell_format_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"left",'text_wrap': True})
    cell_format_center_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"center",'text_wrap': True})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    worksheet.set_column(0, 20, 20)
    worksheet.freeze_panes(1, 0)
    
    worksheet.write("A1","UQC",cell_format_center2)
    worksheet.write("B1","Export Type",cell_format_center2)
    worksheet.write("C1","Reverse Charge/Provisional Assessment",cell_format_center2)
    worksheet.write("D1","Note Type",cell_format_center2)
    worksheet.write("E1","Type",cell_format_center2)
    worksheet.write("F1","Tax Rate",cell_format_center2)
    worksheet.write("G1","POS",cell_format_center2)
    worksheet.write("H1","Invoice Type",cell_format_center2)
    worksheet.write("I1","Nature  of Document",cell_format_center2)
    worksheet.write("J1","UR Type",cell_format_center2)
    worksheet.write("K1","Supply Type",cell_format_center2)
    worksheet.write("L1","Month",cell_format_center2)
    worksheet.write("M1","Financial Year",cell_format_center2)
    worksheet.write("N1","Differential Percentage",cell_format_center2)
    worksheet.write("O1","POS96",cell_format_center2)
    

    all_uqcs = ["BAG-BAGS","BAL-BALE","BDL-BUNDLES","BKL-BUCKLES","BOU-BILLION OF UNITS","BOX-BOX","BTL-BOTTLES","BUN-BUNCHES","CAN-CANS","CBM-CUBIC METERS","CCM-CUBIC CENTIMETERS","CMS-CENTIMETERS","CTN-CARTONS","DOZ-DOZENS","DRM-DRUMS","GGK-GREAT GROSS","GMS-GRAMMES","GRS-GROSS","GYD-GROSS YARDS","KGS-KILOGRAMS","KLR-KILOLITRE","KME-KILOMETRE","MLT-MILILITRE","MTR-METERS","MTS-METRIC TON","NOS-NUMBERS","PAC-PACKS","PCS-PIECES","PRS-PAIRS","QTL-QUINTAL","ROL-ROLLS","SET-SETS","SQF-SQUARE FEET","SQM-SQUARE METERS","SQY-SQUARE YARDS","TBS-TABLETS","TGM-TEN GROSS","THD-THOUSANDS","TON-TONNES","TUB-TUBES","UGS-US GALLONS","UNT-UNITS","YDS-YARDS","OTH-OTHERS",
    ]

    column = 2

    for i in all_uqcs:
        worksheet.write(f"A{column}",i,cell_format_wc)
        column += 1

    worksheet.write(f"B2",'WOPAY',cell_format_center_wc)
    worksheet.write(f"B3",'WPAY',cell_format_center_wc)
   
    worksheet.write(f"C2",'N',cell_format_center_wc)
    worksheet.write(f"C3",'Y',cell_format_center_wc)
    
    worksheet.write(f"D2",'C',cell_format_center_wc)
    worksheet.write(f"D3",'D',cell_format_center_wc)
    
    worksheet.write(f"E2",'OE',cell_format_center_wc)
    worksheet.write(f"E3",'E',cell_format_center_wc)

    tax_rates = ["0.00","0.10","0.25","1.00","1.50","3.00","5.00","7.50","12.00","18.00","28.00"]
    column = 2

    for i in tax_rates:
        worksheet.write(f"F{column}",i,cell_format_center_wc)
        column += 1

    states = ["01-Jammu & Kashmir","02-Himachal Pradesh","03-Punjab","04-Chandigarh","05-Uttarakhand","06-Haryana","07-Delhi","08-Rajasthan","09-Uttar Pradesh","10-Bihar","11-Sikkim","12-Arunachal Pradesh","13-Nagaland","14-Manipur","15-Mizoram","16-Tripura","17-Meghalaya","18-Assam","19-West Bengal","20-Jharkhand","21-Odisha","22-Chhattisgarh","23-Madhya Pradesh","24-Gujarat","25-Daman & Diu","26-Dadra & Nagar Haveli & Daman & Diu","27-Maharashtra","29-Karnataka","30-Goa","31-Lakshdweep","32-Kerala","33-Tamil Nadu","34-Puducherry","35-Andaman & Nicobar Islands","36-Telangana","37-Andhra Pradesh","38-Ladakh","97-Other Territory"]

    column = 2

    for i in states:
        worksheet.write(f"G{column}",i,cell_format_wc)
        column += 1

    invoice_type = ["Regular","SEZ supplies with payment","SEZ supplies without payment","Deemed Exp","Intra-State supplies attracting IGST"]

    column = 2

    for i in invoice_type:
        worksheet.write(f"H{column}",i,cell_format_wc)
        column += 1
    
    natures = ["Invoices for outward supply","Invoices for inward supply from unregistered person","Revised Invoice","Debit Note","Credit Note","Receipt Voucher","Payment Voucher","Refund Voucher","Delivery Challan for job work","Delivery Challan for supply on approval","Delivery Challan in case of liquid gas","Delivery Challan in case other than by way of supply (excluding at S no. 9 to 11)"]

    column = 2

    for i in natures:
        worksheet.write(f"I{column}",i,cell_format_wc)
        column += 1
    
    worksheet.write(f"J2","B2CL",cell_format_wc)
    worksheet.write(f"J3","EXPWP",cell_format_wc)
    worksheet.write(f"J4","EXPWOP",cell_format_wc)
    
    worksheet.write(f"K2","Inter State",cell_format_wc)
    worksheet.write(f"K3","Intra State",cell_format_wc)
    
    worksheet.write(f"L2","JANUARY",cell_format_wc)
    worksheet.write(f"L3","FEBRUARY",cell_format_wc)
    worksheet.write(f"L4","MARCH",cell_format_wc)
    worksheet.write(f"L5","APRIL",cell_format_wc)
    worksheet.write(f"L6","MAY",cell_format_wc)
    worksheet.write(f"L7","JUNE",cell_format_wc)
    worksheet.write(f"L8","JULY",cell_format_wc)
    worksheet.write(f"L9","AUGUST",cell_format_wc)
    worksheet.write(f"L10","SEPTEMBER",cell_format_wc)
    worksheet.write(f"L11","OCTOBER",cell_format_wc)
    worksheet.write(f"L12","NOVEMBER",cell_format_wc)
    worksheet.write(f"L13","DECEMBER",cell_format_wc)
    
    worksheet.write(f"M2","2017-18",cell_format_wc)
    worksheet.write(f"M3","2018-19",cell_format_wc)
    worksheet.write(f"M4","2019-20",cell_format_wc)
    worksheet.write(f"M5","2020-21",cell_format_wc)
    
    worksheet.write(f"N3","65.0",cell_format_wc)
    
    pos96 = ["01-Jammu & Kashmir","02-Himachal Pradesh","03-Punjab","04-Chandigarh","05-Uttarakhand","06-Haryana","07-Delhi","08-Rajasthan","09-Uttar Pradesh","10-Bihar","11-Sikkim","12-Arunachal Pradesh","13-Nagaland","14-Manipur","15-Mizoram","16-Tripura","17-Meghalaya","18-Assam","19-West Bengal","20-Jharkhand","21-Odisha","22-Chhattisgarh","23-Madhya Pradesh","24-Gujarat","25-Daman & Diu","26-Dadra & Nagar Haveli & Daman & Diu ","27-Maharashtra","29-Karnataka","30-Goa","31-Lakshdweep","32-Kerala","33-Tamil Nadu","34-Puducherry","35-Andaman & Nicobar Islands","36-Telangana","37-Andhra Pradesh","38-Ladakh","96-Foreign Country","97-Other Territory"]

    column = 2

    for i in pos96:
        worksheet.write(f"O{column}",i,cell_format_wc)
        column += 1

@login_required(login_url='login')
def exportGSTR1DetailsExcel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_help = workbook.add_worksheet(name='Help')
    worksheet_b2b = workbook.add_worksheet(name='b2b')
    worksheet_b2ba = workbook.add_worksheet(name='b2ba')
    worksheet_b2cl = workbook.add_worksheet(name='b2cl')
    worksheet_b2cla = workbook.add_worksheet(name='b2cla')
    worksheet_b2cs = workbook.add_worksheet(name='b2cs')
    worksheet_b2csa = workbook.add_worksheet(name='b2csa')
    worksheet_cdnr = workbook.add_worksheet(name='cdnr')
    worksheet_cdnra = workbook.add_worksheet(name='cdnra')
    worksheet_cdnur = workbook.add_worksheet(name='cdnur')
    worksheet_cdnura = workbook.add_worksheet(name='cdnura')
    worksheet_exp = workbook.add_worksheet(name='exp')
    worksheet_expa = workbook.add_worksheet(name='expa')
    worksheet_at = workbook.add_worksheet(name='at')
    worksheet_ata = workbook.add_worksheet(name='ata')
    worksheet_atadj = workbook.add_worksheet(name='atadj')
    worksheet_atadja = workbook.add_worksheet(name='atadja')
    worksheet_exemp = workbook.add_worksheet(name='exemp')
    worksheet_hsn = workbook.add_worksheet(name='hsn')
    worksheet_docs = workbook.add_worksheet(name='docs')
    worksheet_master = workbook.add_worksheet(name='master')
    if request.method == "POST":
        from_date = request.POST['from_date2']
        to_date = request.POST['to_date2']
        company_type = request.POST['company_gst_code2']
        setb2bData(workbook,worksheet_b2b,from_date,to_date,company_type)
        setb2baData(workbook,worksheet_b2ba,from_date,to_date,company_type)
        setb2clData(workbook,worksheet_b2cl,from_date,to_date,company_type)
        setb2claData(workbook,worksheet_b2cla,from_date,to_date,company_type)
        setb2csData(workbook,worksheet_b2cs,from_date,to_date,company_type)
        setb2csaData(workbook,worksheet_b2csa,from_date,to_date,company_type)
        setcdnrData(workbook,worksheet_cdnr,from_date,to_date,company_type)
        setcdnraData(workbook,worksheet_cdnra,from_date,to_date,company_type)
        setcdnurData(workbook,worksheet_cdnur,from_date,to_date,company_type)
        setcdnuraData(workbook,worksheet_cdnura)
        setexpData(workbook,worksheet_exp,from_date,to_date,company_type)
        setexpaData(workbook,worksheet_expa)
        setatData(workbook,worksheet_at)
        setataData(workbook,worksheet_ata)
        setatdjData(workbook,worksheet_atadj)
        setatdjaData(workbook,worksheet_atadja)
        setexempData(workbook,worksheet_exemp)
        setdocData(workbook,worksheet_docs)
        sethsnData(workbook,worksheet_hsn)
        setmasterData(workbook,worksheet_master)
        
        workbook.close()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = 'attachment;filename="gstr1.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response

@login_required(login_url='home:handle_login')
def outstading_report(request,module):
    context={}
    selected_company = "A"
    if request.method == "POST":
        # party = request.POST['party']
        company = request.POST['company']
        selected_region = request.POST['region']
        from_date=request.POST['from_date']
        to_date=request.POST['to_date']

        # party = Party.objects.filter(id=int(party)).first()

        credit_notes = CreditNote.objects.select_related('job_no','bill_to','bill_to_address','invoice_currency','company_type').filter(company_type__region=selected_region).filter(is_cancel=False).filter(is_einvoiced=True).filter(is_deleted=False).filter(date_of_note__range=[from_date,to_date]).all()



        advance_amount = RecieptVoucher.objects.select_related('party_name','company_type','party_address').filter(advance_amount__gt = 0).filter(company_type__region=selected_region).filter(voucher_date__range=[from_date,to_date]).all()

     
        
        invoices = InvoiceReceivable.objects.select_related('job_no','bill_to','bill_to_address','invoice_currency','company_type').filter(company_type__region=selected_region).prefetch_related('reciept_rec_inv','reciept_rec_inv__voucher','job_no__job_invoice').filter(is_einvoiced=True).filter(is_deleted=False).filter(date_of_invoice__range=[from_date,to_date]).all()
   

        if not company == "A":
            company = Logistic.objects.filter(id=int(company)).first()
            invoices = invoices.filter(company_type__id = company.id).all()
            credit_notes = credit_notes.filter(company_type__id = company.id).all()
            advance_amount = advance_amount.filter(company_type__id=company.id).all()
            company = company.id
        
        invoices_list = []
        for i in invoices:
            head = {
                'invoice':i,
                'recieved_amount':0,
                'balance_amount':0,
                'net_amount':0,
                # 'job_invoices':JobInvoice.objects.filter(job__job_no=i.job_no).values('invoice_no').all(),
                
            }
            currency_ex_rate = 1
            try:
                if not i.invoice_currency.short_name == 'INR':
                    currency_ex_rate = i.currency_ex_rate
            except:
                pass

            recieved_amount = 0
            recieved_date=''
            for j in i.reciept_rec_inv.all():
                recieved_amount +=  (j.received_amount + j.tds_amount + j.adjustment_amount)

                recieved_date=j.date
                

            head['recieved_amount'] = recieved_amount
            head['recieved_date'] = recieved_date
            head['net_amount'] = (i.net_amount * currency_ex_rate)
            head['balance_amount'] = (i.net_amount * currency_ex_rate) - recieved_amount
            invoices_list.append(head)

        

        # selected_company = company
        # selected_party = party
        
        context['advance_amount'] = advance_amount
        context['invoices_list'] = invoices_list
        # context['selected_party'] = selected_party
        context['selected_region'] = selected_region
        context['credit_notes'] = credit_notes

    context['module'] = module
    # context['selected_company'] = selected_company

    
    return render(request,'report/sales_outstanding/outstanding_report.html',context)

