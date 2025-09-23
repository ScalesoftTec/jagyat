from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from accounting.forms import  *
from accounting.models import  *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from masters.models import Bank, BillingHead, JobMaster, Party,currency,LedgerMaster,PartyAddress,TrailorBillingHead,Vendor,JobContainer
from dashboard.models import Logistic
from masters.views import check_permissions
from json import dumps,loads
from datetime import date, datetime, timedelta
from django.db.models import Count,Sum
import calendar
import num2words
from django.core.mail import EmailMultiAlternatives
import threading
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from accounting.api import login_and_get_token,add_invoice_recievable_irn,add_credit_note_irn,cancel_invoice_irn
from accounting.utils import generate_pdf,send_generate_pdf
import os
import xlsxwriter
import math
import pandas as pd
from django.core.files.storage import FileSystemStorage
from dashboard.views import EmailThread


@login_required(login_url='home:handle_login')
def index(request,module):

   
    context = {}
    check_permissions(request,module)
    
    proforma_invoice_count = InvoiceReceivable.objects.filter(is_deleted=False).filter(is_cancel=False).filter(is_einvoiced=False).filter(old_invoice=False).count()
    final_rec_invoice_count = InvoiceReceivable.objects.filter(is_deleted=False).filter(is_cancel=False).filter(is_einvoiced=True).filter(old_invoice=False).count()
    unfinal_invoice_payable_count = InvoicePayable.objects.filter(is_deleted=False).filter(is_final=False).filter(old_invoice=False).count()
    final_invoice_payable_count = InvoicePayable.objects.filter(is_deleted=False).filter(is_final=True).filter(old_invoice=False).count()
    proforma_crn_count = CreditNote.objects.filter(is_deleted=False).filter(is_einvoiced=False).filter(is_cancel=False).count()
    final_crn_count = CreditNote.objects.filter(is_deleted=False).filter(is_einvoiced=True).filter(is_cancel=False).count()
    drn_count = DebitNote.objects.filter(is_deleted=False).count()

    selected_company = 'all'
    if request.method == 'POST':
        company = (request.POST['company'])
        if not company == 'all':
            company = int(company)
            company = Logistic.objects.filter(id=company).first()
            selected_company = company
     
    if not request.user.user_account.see_global_data:
        selected_company = Logistic.objects.filter(id=request.user.user_account.office.id).first()

    if not selected_company == 'all':
        proforma_invoice_count = InvoiceReceivable.objects.filter(company_type=selected_company).filter(is_cancel=False).filter(is_deleted=False).filter(is_einvoiced=False).filter(old_invoice=False).count()
        final_rec_invoice_count = InvoiceReceivable.objects.filter(company_type=selected_company).filter(is_deleted=False).filter(is_cancel=False).filter(is_einvoiced=True).filter(old_invoice=False).count()
        unfinal_invoice_payable_count = InvoicePayable.objects.filter(company_type=selected_company).filter(is_final=False).filter(is_deleted=False).filter(old_invoice=False).count()
        final_invoice_payable_count = InvoicePayable.objects.filter(company_type=selected_company).filter(is_final=True).filter(is_deleted=False).filter(old_invoice=False).count()
        proforma_crn_count = CreditNote.objects.filter(company_type=selected_company).filter(is_deleted=False).filter(is_cancel=False).filter(is_einvoiced=False).count()
        final_crn_count = CreditNote.objects.filter(company_type=selected_company).filter(is_cancel=False).filter(is_deleted=False).filter(is_einvoiced=True).count()
        drn_count = DebitNote.objects.filter(company_type=selected_company).filter(is_deleted=False).count()
       
    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    context = {
        'selected_company':selected_company,
        'greeting':greeting,
        'module':module,
        'proforma_invoice_count':proforma_invoice_count,
        'final_rec_invoice_count':final_rec_invoice_count,
        'unfinal_invoice_payable_count':unfinal_invoice_payable_count,
        'final_invoice_payable_count':final_invoice_payable_count,
        'proforma_crn_count':proforma_crn_count,
        'final_crn_count':final_crn_count,
        'drn_count':drn_count
    }
   
    return render(request,'accounting_index.html',context)

# ------------------Salary Master----------------
@login_required(login_url='home:handle_login')
def create_salary(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = SalaryForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Salary Paid Created.")
        return redirect('accounting:create_salary',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'salary/create_salary.html',context)


@login_required(login_url='home:handle_login')
def salary_details(request,module):
    context ={}
    check_permissions(request,module)
  
    salaries = Salary.objects.select_related("employee",'bank','company_type').all()
    choose_company = "All"
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']

    salaries = salaries.filter(date__gte=from_date).filter(date__lte=to_date).all()

    context['choose_company'] = choose_company
    if not choose_company == "All":
        salaries = salaries.filter(company_type=int(choose_company)).all()
        context['choose_company'] = int(choose_company)

    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")
    context['salaries']= salaries
    context['module']= module
    return render(request,'salary/salary_details.html',context)


@login_required(login_url='home:handle_login')
def salary_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Salary, id = id)
    
    form = SalaryForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:salary_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'salary/create_salary.html',context)

@login_required(login_url='home:handle_login')
def salary_delete(request,module,id):
    check_permissions(request,module)
    salary = Salary.objects.filter(id=int(id)).first()
    salary.delete()
    return redirect('accounting:salary_details',module=module)

# Trailor Expense
        
def handle_trailor_expense_bh(request,id):
    trailor_expenses = TrailorExpenseDetail.objects.filter(expense__id = id).all()
    trailor_exp = TrailorExpense.objects.filter(id = id).first()
    trailor_expenses.delete()
    total_heads = int(request.POST['expense-heads-total'])
    
    for i in range(1,total_heads+1):
        isActive = request.POST[f'isActive_{i}']
        if isActive == '1':
            billing_head = TrailorBillingHead.objects.filter(id=int(request.POST[f'billing_head_{i}'])).first() 
            vendor = request.POST.get(f'vendor_{i}',None)
            
            
            date = request.POST[f'date_{i}']
            charges = request.POST[f'charges_{i}']
            payment_type = request.POST[f'payment_type_{i}']
            remarks = request.POST[f'remarks_{i}']
            
            new_expense_head = TrailorExpenseDetail(
                expense = trailor_exp,
                billing_head = billing_head,
                remarks = remarks,
               
                
                charges = charges,
                
                payment_type = payment_type,
                
            )
            if vendor:
                vendor = Vendor.objects.filter(id=int(request.POST[f'vendor_{i}'])).first()
                new_expense_head.vendor = vendor
            
            if date:
                new_expense_head.date = date
            new_expense_head.save()
                
@login_required(login_url='home:handle_login')
def create_trailor_expense(request,module):
    context ={}
    check_permissions(request,module)

    form = TrailorExpenseForm()
    if request.method == 'POST':
        form = TrailorExpenseForm(request.POST,request.FILES)

    if form.is_valid():
        form.instance.created_by = request.user
       
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        
        form.save()
        
        handle_trailor_expense_bh(request,form.instance.id)
        
        messages.add_message(request, messages.SUCCESS, f"Success, New Trailor Expense Created.") 
        form.save()
      
            
        return redirect('accounting:create_trailor_expense',module=module)
    billing_heads = BillingHead.objects.all()
    context['form']= form
    context['module']= module
   
    context['billing_heads'] = billing_heads
    context['invoice_length'] = len(InvoiceReceivable.objects.all())
    return render(request,'trailor_expense/create_trailor_expense.html',context)

@login_required(login_url='home:handle_login')
def trailor_expense_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(TrailorExpense, id = id)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:trailor_expense_details',module=module)
    
    invoice_heads = TrailorExpenseDetail.objects.filter(expense=obj).all()
    created_by = obj.created_by
    company_type = obj.company_type
    

    form = TrailorExpenseForm(instance = obj)
    if request.method == 'POST':
        form = TrailorExpenseForm(request.POST, request.FILES, instance=obj)

    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        form.instance.pending_amount = form.instance.net_amount
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        
        handle_trailor_expense_bh(request,form.instance.id)
        
     
    
        
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:trailor_expense_details',module=module)
          
    billing_heads = BillingHead.objects.all()
    
    
    context['form']= form
    
    context['module']= module
    context['update']= True
    context['billing_heads'] = billing_heads
    
    context['invoice_heads']= invoice_heads
    context['total_invoice_heads']= len(invoice_heads)
    return render(request,'trailor_expense/create_trailor_expense.html',context)
          
@login_required(login_url='home:handle_login')
def trailor_expense_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    invoices = TrailorExpense.objects.select_related('company_type','job_no','trailor_no','created_by').all()

    if not request.user.user_account.see_global_data:
        invoices = invoices.filter(company_type=company).all()
        
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    
    if request.method == 'POST':

        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)

  

    invoices = invoices.filter(job_no__job_date__range=[from_date,to_date]).all()
            
    if not request.user.user_account.also_handle_other_work:
        invoices = invoices.filter(created_by=request.user).all()
    
    invoices = invoices.filter(is_deleted = False).all()
          
    context['invoices']= invoices
    context['current_month']= current_month
    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")
    
    context['module']= module
    return render(request,'trailor_expense/trailor_expense_details.html',context)

@login_required(login_url='home:handle_login')
def trailor_expense_delete(request,module,id):
    check_permissions(request,module)
    invoice = TrailorExpense.objects.filter(id=int(id)).first()
    invoice.is_deleted = True
    invoice.deleted_by = request.user
    invoice.save()
    return redirect('accounting:trailor_expense_details',module=module)

# Sales Invoice
def handle_rec_inv_bh(request,id):
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    details = InvoiceReceivableDetail.objects.filter(invoice_receivable__id=id).all()
    details.delete()
    total_heads = int(request.POST['invoice-heads-total'])
    for i in range(1,total_heads+1):
        isActive = request.POST[f'isActive_{i}']
        if isActive == '1':
            billing_head = BillingHead.objects.filter(id=int(request.POST[f'billing_head_{i}'])).first() 
            currency_obj = currency.objects.filter(id=int(request.POST[f'currency_{i}'])).first() 
            ex_rate = request.POST[f'ex_rate_{i}']
            tax_applicable = request.POST[f'tax_applicable_{i}']
            rate = request.POST[f'rate_{i}']
            qty = request.POST[f'qty_{i}']
            gst = request.POST[f'gst_{i}']
            amount = request.POST[f'amount_{i}']
            total = request.POST[f'total_{i}']
            gst_amount = request.POST[f'inv_gst_amount_{i}'] 
            new_invoice_heads = InvoiceReceivableDetail(
                invoice_receivable = invoice,
                billing_head = billing_head,
                currency = currency_obj,
                ex_rate = ex_rate,
                rate = rate,
                qty_unit = qty,
                amount = amount,
                gst = gst,
                total = total,
                gst_amount=gst_amount,
                tax_applicable=tax_applicable
            )
            new_invoice_heads.save()
    
    

def handle_invoice_container_details(request,instance):
    invoice = InvoiceReceivable.objects.filter(id=instance.id).first()
    invoice_hbls = invoice.hbl_options.all()
    print(invoice_hbls)
    for i in invoice_hbls:
        
        containers = JobContainer.objects.filter(hbl=i).all()
        for j in containers:
            try:
                detention_from = request.POST[f'detention_from_{j.id}']
                detention_to = request.POST[f'detention_to_{j.id}']
                j.detention_from = detention_from
                j.detention_to = detention_to
                j.save()   
            except:
                pass         
             
@login_required(login_url='home:handle_login')
def create_recievable_invoice(request,module):
    context ={}
    check_permissions(request,module)
    job_id = request.GET.get('job_id') or None
    form = InvoiceReceivableForm(request.POST or None ,initial={'job_no':job_id})
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.instance.pending_amount = (form.instance.net_amount) - (form.instance.tds_payable)
        form.instance.is_single = True
        
        form.save()
        
        handle_rec_inv_bh(request,form.instance.id)
        handle_invoice_container_details(request,form.instance)
        
       
        form.instance.is_approved = True
        
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Invoice Created.")
        return redirect('accounting:create_recievable_invoice',module=module)
    else:
        print(form.errors.as_json())
 
    
    context['form']= form
    context['module']= module


   
    return render(request,'receivable_invoice/create_recievable_invoice.html',context)

@login_required(login_url='home:handle_login')
def recievable_invoice_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(InvoiceReceivable, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:recievable_invoice_details',module=module)
    
    invoice_heads = InvoiceReceivableDetail.objects.filter(invoice_receivable=obj).all()
    created_by = obj.created_by
    company_type = obj.company_type
    is_approved = obj.is_approved
    job_no = obj.job_no

    form = InvoiceReceivableForm(request.POST or None, instance = obj)
  
    
    context['form']= form
    context['module']= module
    context['update']= True
    context['invoice_heads']= invoice_heads
    context['data']= obj
    context['total_invoice_heads']= len(invoice_heads)
    
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.pending_amount = (form.instance.net_amount) - (form.instance.tds_payable)
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
            form.instance.is_approved = is_approved
            
        form.instance.is_single = True
        if not form.instance.job_no:
            form.instance.job_no = job_no
    
        form.save()

        if not form.instance.company_type.is_rec_inv_approve_required:
            form.instance.is_approved = True
        
        handle_rec_inv_bh(request,form.instance.id)
        handle_invoice_container_details(request,form.instance)
                
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:recievable_invoice_details',module=module)
          
    
    return render(request,'receivable_invoice/create_recievable_invoice.html',context)
           
@login_required(login_url='home:handle_login')
def recievable_invoice_details(request,module):
    context ={}

    check_permissions(request,module)
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    invoices = InvoiceReceivable.objects.filter(old_invoice=False).filter(is_einvoiced=False).filter(is_deleted=False).select_related('bill_to','company_type','job_no','invoice_currency','bill_to_address','bill_to_address__corp_state','created_by','application_handler').prefetch_related('hbl_options').all().order_by('-id')

    if not request.user.user_account.see_global_data:
        invoices = invoices.filter(company_type=company).all()

    if not request.user.user_account.also_handle_other_work:
        invoices = invoices.filter(created_by=request.user).all()

    context['invoices']= invoices
    context['module']= module

    return render(request,'receivable_invoice/recievable_invoice_details.html',context)

@login_required(login_url='home:handle_login')
def e_invoice_recievable_details(request,module):
    context ={}
    check_permissions(request,module)
    cancelled_bill = "N"
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    invoices = InvoiceReceivable.objects.select_related('bill_to','company_type','job_no','invoice_currency','bill_to_address','created_by').prefetch_related('hbl_options').filter(old_invoice=False).filter(is_einvoiced=True).filter(company_type__tax_policy = "GST").all().order_by('-id')


    # for invoice in invoices:
    #     invoice.save()
    
    
    if not request.user.user_account.see_global_data:
        invoices = invoices.filter(company_type=company).all()

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"
    if request.method == 'POST':

        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']
        cancelled_bill = request.POST['cancelled_bill']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)

    invoices = invoices.filter(einvoice_date__range=[from_date,to_date]).all()

    context['choose_company'] = choose_company
    if not choose_company == "All":
        invoices = invoices.filter(company_type__id=int(choose_company))
        context['choose_company'] = int(choose_company)

    if cancelled_bill == "N":
        invoices = invoices.filter(is_cancel=False).all()

    if cancelled_bill == "Y":
        invoices = invoices.filter(is_cancel=True).all()
    
    if not request.user.user_account.also_handle_other_work:
        invoices = invoices.filter(created_by=request.user).all()

    context['invoices']= invoices
    context['cancelled_bill']= cancelled_bill
    context['current_date'] = datetime.now()
    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")
    context['module']= module
    return render(request,'receivable_invoice/einvoice_list.html',context)
       
@login_required(login_url='home:handle_login')
def final_invoice_recievable_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    invoices = InvoiceReceivable.objects.select_related('company_type','job_no','bill_to','bill_to_address','created_by').all()

    if not request.user.user_account.see_global_data:
        invoices = invoices.filter(company_type=company).all()

    
    current_month = datetime.now().month
    
    
        
    if not request.user.user_account.also_handle_other_work:
        invoices = invoices.filter(created_by=request.user).all()
    
    invoices = invoices.filter(is_deleted=False).filter(old_invoice=False).exclude(company_type__tax_policy = "GST").all().order_by('-id')
    
    for i in invoices:
        if not i.is_einvoiced:
            i.is_einvoiced = True
            i.final_invoice_no = i.invoice_no
            i.einvoice_date = i.date_of_invoice
            i.save()

    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"
    if request.method == 'POST':
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)

    context['choose_company'] = choose_company
    if not choose_company == "All":
        invoices = invoices.filter(company_type__id=int(choose_company))
        context['choose_company'] = int(choose_company)

    invoices = invoices.filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).all()
            
    
    context['invoices']= invoices
    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")
    context['current_date'] = datetime.now()
    context['module']= module
    return render(request,'receivable_invoice/final_invoice_recievable_details.html',context)



@login_required(login_url='home:handle_login')
def make_eninvoice_recievable(request, module, id):
    check_permissions(request, module)
    
    invoice = InvoiceReceivable.objects.get(id=int(id))
    invoice.final_invoice_no = invoice.invoice_no

    date_of_invoice = invoice.date_of_invoice
    invoice.einvoice_date = timezone.make_aware(
        datetime.combine(date_of_invoice, datetime.min.time())
    )

    invoice.is_einvoiced = True
    invoice.save()
    messages.add_message(request, messages.SUCCESS, "E-invoiced marked final")
    return redirect('accounting:recievable_invoice_details', module=module)


@login_required(login_url='home:handle_login')
def recievable_invoice_delete(request,module,id):
    check_permissions(request,module)
    invoice = InvoiceReceivable.objects.filter(id=int(id)).first()
    invoice.is_deleted = True
    invoice.deleted_by = request.user
    invoice.save()
    return redirect('accounting:recievable_invoice_details',module=module)


# def recievable_invoice_pdf(request,id):
#     template_path = 'receivable_invoice/tax_invoice_pdf.html'
#     invoice = InvoiceReceivable.objects.filter(id=int(id)).first()
#     # print('-----',invoice.hbl_options.all())
#     commoditys=[]
#     vessels=[]
#     hbl_no=[]
#     mbl_no=[]
#     total_pkg=[]
#     total_gross_weight=[]
#     total_cbm=[]
    
#     selected_hbls = []
    
#     container_count = JobContainer.objects.exclude(job_container_no="").filter(job=invoice.job_no).filter(job__is_deleted=False).values("container_type").annotate(type_count=Count('container_type'))
    
#     for i in invoice.hbl_options.all():
#         selected_hbls.append(i.job_hbl_no)
#         hbl_no.append(i.job_hbl_no)
#         mbl_no.append(i.mbl_no)
#         commoditys.append(i.commodity)
#         vessels.append(i.vessel_name)
#         if i.no_of_packages:
#           total_pkg.append(float(i.no_of_packages))
#         else:
#             total_pkg.append(int(0))
#         total_gross_weight.append(float(i.gross_weight))
#         total_cbm.append(float(i.volume))
        
#     container_count = JobContainer.objects.exclude(job_container_no="").filter(hbl__job_hbl_no__in=selected_hbls).filter(job=invoice.job_no).filter(job__is_deleted=False).values("container_type").annotate(type_count=Count('container_type'))

#     hbl_data =" / ".join(hbl_no)
#     try:
#        mbl_no =" / ".join(mbl_no)
#     except:
#         mbl_no='None'

#     try:
#        vessel =" / ".join(vessels)
#     except:
#         vessel='None'

#     try:
#        commodity =" / ".join(commoditys)
#     except:
#         commodity='None'

#     t_pkg=sum(total_pkg)
   
#     t_gross_weight=sum(total_gross_weight)
#     t_cbm=sum(total_cbm)
    


#     amount_in_words = num2words.num2words(round(invoice.net_amount,2), to="currency" ,lang='en_IN')
#     amount_in_words = amount_in_words.replace(',','')
#     amount_in_words = amount_in_words.replace('-',' ')
#     domain = Site.objects.get_current().domain
#     per_5 = 0
#     per_i5 = 0
#     per_12 = 0
#     per_i12 = 0
#     per_18 = 0
#     per_i18 = 0
#     total_taxable_amount = 0
#     per_5_taxable = 0
#     per_12_taxable = 0
#     per_18_taxable = 0
#     is_local = False
#     try:
#         if  invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
#             is_local = True
#     except:
#         pass
        
#     for i in invoice.recievable_invoice_reference.all():
        
#         if i.gst == 5:
#             if is_local and not i.billing_head.always_igst:
#                 per_5 += i.gst_amount
#                 per_5_taxable += i.amount
#             else:
#                 per_i5 += i.gst_amount
#                 per_5_taxable += i.amount
        
#         if i.gst == 12:
#             if is_local and not i.billing_head.always_igst:
#                 per_12 += i.gst_amount
#                 per_12_taxable += i.amount
#             else:
#                 per_i12 += i.gst_amount
#                 per_12_taxable += i.amount
        
        
#         if i.gst == 18:
#             if is_local and not i.billing_head.always_igst:
#                 per_18 += i.gst_amount
#                 per_18_taxable += i.amount
#             else:
#                 per_i18 += i.gst_amount
#                 per_18_taxable += i.amount
        
#         if i.gst > 0:
#             total_taxable_amount += i.amount
    
#     pending_col = []
    
#     col_in_invoice = 15
#     if invoice.is_einvoiced and invoice.signed_qr_code:
#         col_in_invoice = 15
    
#     for i in range(col_in_invoice - len(invoice.recievable_invoice_reference.all())):
#         pending_col.append(i)
        
   
#     head = invoice.company_type



#     try:    
#         data_container=[i.job_container_no for i in invoice.job_no.job_container.all()]
#         container_details=", ".join(data_container)
#     except:
#         container_details = ""
            

    
#     if invoice.type_of_invoice == "RCM":
#         template_path = 'receivable_invoice/rcm_pdf.html'
        
            
#     if invoice.company_type.tax_policy == "NO TAX":
#         template_path = 'receivable_invoice/non_tax_pdf.html'
    
#     if invoice.company_type.tax_policy == "VAT":
#         invoice = InvoiceReceivable.objects.filter(id=int(id)).first()
#         amount_in_words = num2words.num2words(round(int(invoice.net_amount),2))
        
#         template_path = 'receivable_invoice/vat_invoice_pdf.html'
    
#     invoice_detail = invoice.recievable_invoice_reference.values('billing_head__hsn_code','gst','amount').annotate(gst_sum=Sum('gst_amount'))

#     for head in invoice_detail:
#         for i in invoice.recievable_invoice_reference.all():
#             if head['gst'] == i.gst and head['billing_head__hsn_code'] == i.billing_head.hsn_code and i.gst_amount > 0:
#                 try:
#                     head['taxable_amount'] += i.gst_amount
#                 except:
#                     head['taxable_amount'] = i.gst_amount


    
#     # container_count = invoice.container_options.count() or invoice.job_no.container_no or invoice.job_no.job_container.filter(hbl=None).count()
#     # container_count =  invoice.job_no.container_no or invoice.job_no.job_container.filter(hbl=None).count()

#     # t_gross_weight = 0
#     # t_net_weight = 0
#     # t_cbm = 0
#     # t_pkg = 0
#     # packages_type = ""
#     # ship_bill_no_date = ""
#     # shipper_invoice_no_date = ""
    
#     # for weight in invoice.hbl_options.all():
#     #     try:
#     #         t_gross_weight += (float(weight.gross_weight) or 0)
#     #     except:
#     #         pass
       
#     #     try:
#     #         t_pkg += (int(weight.t_pkg) or 0)
#     #     except:
#     #         pass

#     #     try:
#     #         t_net_weight += (float(weight.net_weight) or 0)
#     #     except:
#     #         pass
       
#     #     try:
#     #         t_cbm += (int(weight.volume) or 0)
#     #     except:
#     #         pass
        
#     #     try:
#     #         packages_type = weight.packages_type
#     #     except:
#     #         pass
        
#     #     try:
#     #         ship_bill_no_date += f"{weight.ship_bill_no or ''} / {weight.ship_bill_date or ''},"
#     #     except:
#     #         pass
        
#     #     try:
#     #         shipper_invoice_no_date += f"{weight.shipper_invoice_no or ''} / {weight.shipper_invoice_date or ''} ,"
#     #     except:
#     #         pass
        
    

#     # if not t_gross_weight > 0:
#     #     t_gross_weight = invoice.job_no.gross_weight
   
#     # if not t_net_weight > 0:
#     #     t_net_weight = invoice.job_no.net_weight
   
#     # if not t_cbm > 0:
#     #     t_cbm = invoice.job_no.cbm

#     # print(t_pkg)
#     # if not t_pkg:
#     #     t_pkg = invoice.job_no.no_of_packages

    
#     # if not packages_type:
#     #     packages_type = invoice.job_no.packages_type

    
#     # if not ship_bill_no_date:
#     #     try:
#     #         ship_bill_no_date = f"{invoice.job_no.job_invoice.first().ship_bill_no} {invoice.job_no.job_invoice.first().ship_bill_date}"
#     #     except:
#     #         pass

#     # if not shipper_invoice_no_date:
#     #     try:
#     #         shipper_invoice_no_date = f"{invoice.job_no.job_invoice.first().invoice_no} {invoice.job_no.job_invoice.first().invoice_date}"
#     #     except:
#     #         pass


   

#     context = {
#         'container_details':container_details,
#         'commodity':commodity,
#         'vessel_name':vessel,
#         'hbl_data':hbl_data,
#         'mbl_no':mbl_no,
#         't_pkg':t_pkg,
#         't_gross_weight':t_gross_weight,
#         't_cbm':t_cbm,
#         'data':invoice,
#         'invoice_detail':invoice_detail,
#         'head':head,
#         'blank':pending_col,
#         'container_count':container_count,
#         'amount_in_words':amount_in_words.upper(),
#         'per_5':per_5,
#         'per_12':per_12,
#         'per_18':per_18,
#         'total_cgst':(per_5 + per_12 + per_18)/2,
#         'total_sgst':(per_5 + per_12 + per_18)/2,
#         'total_igst':(per_i5 + per_i12 + per_i18),
#         'total_5':per_5 + per_i5,
#         'total_12':per_12 + per_i12,
#         'total_18':per_18 + per_i18,
#         'per_i5':round(per_i5,2),
#         'per_i12':round(per_i12,2),
#         'per_i18':round(per_i18,2),
#         'per_5_taxable':per_5_taxable,
#         'per_12_taxable':per_12_taxable,
#         'per_18_taxable':per_18_taxable,
#         'total_taxable_amount':total_taxable_amount,
#         'domain':domain
#     }
    
#     return generate_pdf(request,template_path,context)



def recievable_invoice_pdf(request,id):
    template_path = 'receivable_invoice/tax_invoice_pdf.html'
    invoice = InvoiceReceivable.objects.filter(id=int(id)).first()
    invoice.save()
    amount_in_words = num2words.num2words(round(invoice.net_amount,2), to="currency" ,lang='en_IN')
    amount_in_words = amount_in_words.replace(',','')
    amount_in_words = amount_in_words.replace('-',' ')
    domain = Site.objects.get_current().domain
    per_5 = 0
    per_i5 = 0
    per_12 = 0
    per_i12 = 0
    per_18 = 0
    per_i18 = 0
    total_taxable_amount = 0
    per_5_taxable = 0
    per_12_taxable = 0
    per_18_taxable = 0
    is_local = False
    try:
        if  invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
            is_local = True
    except:
        pass
        
    for i in invoice.recievable_invoice_reference.all():
        
        if i.gst == 5:
            if is_local and not i.billing_head.always_igst:
                per_5 += i.gst_amount
                per_5_taxable += i.amount
            else:
                per_i5 += i.gst_amount
                per_5_taxable += i.amount
        
        if i.gst == 12:
            if is_local and not i.billing_head.always_igst:
                per_12 += i.gst_amount
                per_12_taxable += i.amount
            else:
                per_i12 += i.gst_amount
                per_12_taxable += i.amount
        
        
        if i.gst == 18:
            if is_local and not i.billing_head.always_igst:
                per_18 += i.gst_amount
                per_18_taxable += i.amount
            else:
                per_i18 += i.gst_amount
                per_18_taxable += i.amount
        
        if i.gst > 0:
            total_taxable_amount += i.amount
    
    pending_col = []
    
    col_in_invoice = 25
    if invoice.is_einvoiced and invoice.signed_qr_code:
        col_in_invoice = 22
    
    for i in range(col_in_invoice - len(invoice.recievable_invoice_reference.all())):
        pending_col.append(i)
        
    rcm_head = Logistic.objects.filter(company_name = "Pinkcity Kanpur").first()
    export_head = Logistic.objects.filter(company_gst_code = "27").first()
    head = invoice.company_type
    if invoice.type_of_invoice == "RCM":
        template_path = 'receivable_invoice/rcm_pdf.html'
        if rcm_head:
            head = rcm_head

    
    if invoice.type_of_invoice == "EXPORT":
        if export_head:
            head = export_head

    
            
    if invoice.company_type.tax_policy == "NO TAX":
        template_path = 'receivable_invoice/non_tax_pdf.html'
    
            
    context = {
        'data':invoice,
        'head':head,
        'blank':pending_col,
        'amount_in_words':amount_in_words.upper(),
        'per_5':per_5,
        'per_12':per_12,
        'per_18':per_18,
        'total_cgst':(per_5 + per_12 + per_18)/2,
        'total_sgst':(per_5 + per_12 + per_18)/2,
        'total_igst':(per_i5 + per_i12 + per_i18),
        'total_5':per_5 + per_i5,
        'total_12':per_12 + per_i12,
        'total_18':per_18 + per_i18,
        'per_i5':round(per_i5,2),
        'per_i12':round(per_i12,2),
        'per_i18':round(per_i18,2),
        'per_5_taxable':per_5_taxable,
        'per_12_taxable':per_12_taxable,
        'per_18_taxable':per_18_taxable,
        'total_taxable_amount':total_taxable_amount,
        'domain':domain
    }
    
    return generate_pdf(request,template_path,context)
    

def recievable_invoice_print_pdf(request,id):
    template_path = 'receivable_invoice/print_tax_invoice_pdf.html'
    invoice = InvoiceReceivable.objects.filter(id=int(id)).first()
    amount_in_words = num2words.num2words(round(invoice.net_amount,2), to="currency" ,lang='en_IN')
    amount_in_words = amount_in_words.replace(',','')
    amount_in_words = amount_in_words.replace('-',' ')
    domain = Site.objects.get_current().domain
    per_5 = 0
    per_i5 = 0
    per_12 = 0
    per_i12 = 0
    per_18 = 0
    per_i18 = 0
    total_taxable_amount = 0
    per_5_taxable = 0
    per_12_taxable = 0
    per_18_taxable = 0
    is_local = False
    try:
        if  invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
            is_local = True
    except:
        pass
        
    for i in invoice.recievable_invoice_reference.all():
        
        if i.gst == 5:
            if is_local and not i.billing_head.always_igst:
                per_5 += i.gst_amount
                per_5_taxable += i.amount
            else:
                per_i5 += i.gst_amount
                per_5_taxable += i.amount
        
        if i.gst == 12:
            if is_local and not i.billing_head.always_igst:
                per_12 += i.gst_amount
                per_12_taxable += i.amount
            else:
                per_i12 += i.gst_amount
                per_12_taxable += i.amount
        
        
        if i.gst == 18:
            if is_local and not i.billing_head.always_igst:
                per_18 += i.gst_amount
                per_18_taxable += i.amount
            else:
                per_i18 += i.gst_amount
                per_18_taxable += i.amount
        
        if i.gst > 0:
            total_taxable_amount += i.amount
    
    pending_col = []
    
    col_in_invoice = 16
    if invoice.is_einvoiced and invoice.signed_qr_code:
        col_in_invoice = 20
    
    for i in range(col_in_invoice - len(invoice.recievable_invoice_reference.all())):
        pending_col.append(i)
    



    data_container=[i.job_container_no for i in invoice.job_no.job_container.all()]
    container_details=", ".join(data_container)
        
        
    
    head = invoice.company_type
    if invoice.type_of_invoice == "RCM":
        template_path = 'receivable_invoice/rcm_pdf.html'
        
            
    if invoice.company_type.tax_policy == "NO TAX":
        template_path = 'receivable_invoice/non_tax_pdf.html'
    
    if invoice.company_type.tax_policy == "VAT": 
        template_path = 'receivable_invoice/print_vat_invoice_pdf.html'
    
    context = {
        'container_details':container_details,
        'data':invoice,
        'head':head,
        'blank':pending_col,
        'amount_in_words':amount_in_words.upper(),
        'per_5':per_5,
        'per_12':per_12,
        'per_18':per_18,
        'total_cgst':(per_5 + per_12 + per_18)/2,
        'total_sgst':(per_5 + per_12 + per_18)/2,
        'total_igst':(per_i5 + per_i12 + per_i18),
        'total_5':per_5 + per_i5,
        'total_12':per_12 + per_i12,
        'total_18':per_18 + per_i18,
        'per_i5':round(per_i5,2),
        'per_i12':round(per_i12,2),
        'per_i18':round(per_i18,2),
        'per_5_taxable':per_5_taxable,
        'per_12_taxable':per_12_taxable,
        'per_18_taxable':per_18_taxable,
        'total_taxable_amount':total_taxable_amount,
        'domain':domain
    }
    
    return generate_pdf(request,template_path,context)




def send_rec_invoice(request,module,id,from_url):
    template_path = 'receivable_invoice/tax_invoice_pdf.html'
    invoice = InvoiceReceivable.objects.filter(id=int(id)).first()
    amount_in_words = num2words.num2words(round(invoice.net_amount,2), to="currency" ,lang='en_IN')
    amount_in_words = amount_in_words.replace(',','')
    amount_in_words = amount_in_words.replace('-',' ')
    domain = Site.objects.get_current().domain
    per_5 = 0
    per_i5 = 0
    per_12 = 0
    per_i12 = 0
    per_18 = 0
    per_i18 = 0
    total_taxable_amount = 0
    per_5_taxable = 0
    per_12_taxable = 0
    per_18_taxable = 0
    is_local = False
    try:
        if  invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
            is_local = True
    except:
        pass
        
    for i in invoice.recievable_invoice_reference.all():
        
        if i.gst == 5:
            if is_local and not i.billing_head.always_igst:
                per_5 += i.gst_amount
                per_5_taxable += i.amount
            else:
                per_i5 += i.gst_amount
                per_5_taxable += i.amount
        
        if i.gst == 12:
            if is_local and not i.billing_head.always_igst:
                per_12 += i.gst_amount
                per_12_taxable += i.amount
            else:
                per_i12 += i.gst_amount
                per_12_taxable += i.amount
        
        
        if i.gst == 18:
            if is_local and not i.billing_head.always_igst:
                per_18 += i.gst_amount
                per_18_taxable += i.amount
            else:
                per_i18 += i.gst_amount
                per_18_taxable += i.amount
        
        if i.gst > 0:
            total_taxable_amount += i.amount
    
    pending_col = []
    
    col_in_invoice = 25
    if invoice.is_einvoiced and invoice.signed_qr_code:
        col_in_invoice = 22
    
    for i in range(col_in_invoice - len(invoice.recievable_invoice_reference.all())):
        pending_col.append(i)
        
    
    rcm_head = Logistic.objects.filter(company_name = "Pinkcity Kanpur").first()
    head = invoice.company_type
    if invoice.type_of_invoice == "RCM":
        template_path = 'receivable_invoice/rcm_pdf.html'
        if rcm_head:
            head = rcm_head
            
    if invoice.company_type.tax_policy == "NO TAX":
        template_path = 'receivable_invoice/non_tax_pdf.html'
            
    context = {
        'data':invoice,
        'head':head,
        'blank':pending_col,
        'amount_in_words':amount_in_words.upper(),
        'per_5':per_5,
        'per_12':per_12,
        'per_18':per_18,
        'total_cgst':(per_5 + per_12 + per_18)/2,
        'total_sgst':(per_5 + per_12 + per_18)/2,
        'total_igst':(per_i5 + per_i12 + per_i18),
        'total_5':per_5 + per_i5,
        'total_12':per_12 + per_i12,
        'total_18':per_18 + per_i18,
        'per_i5':round(per_i5,2),
        'per_i12':round(per_i12,2),
        'per_i18':round(per_i18,2),
        'per_5_taxable':per_5_taxable,
        'per_12_taxable':per_12_taxable,
        'per_18_taxable':per_18_taxable,
        'total_taxable_amount':total_taxable_amount,
        'domain':domain
    }
    
    
    
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    
    to_email = [invoice.bill_to_address.corp_email,]
    subject = "Invoice from " + invoice.company_type.company_name
    domain = Site.objects.get_current().domain
    invoice_url = f'/dashboard/recievable-invoice/pdf/{invoice.id}/'
    html_content = render_to_string("email/invoice.html",{
        'data':invoice,
        'invoice_url':invoice_url
    })
    
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(
        subject=subject,
        body = text_content,
        from_email = from_email,
        to=to_email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.attach(f'invoice_{invoice.id}.pdf',send_generate_pdf(request,template_path,context),'application/pdf')
    EmailThread(msg).start()
    return redirect(f'accounting:{from_url}',module=module)

# Credit Note
def handle_crn_bh(request,id):
    crn = CreditNote.objects.filter(id=id).first()
    details = CreditNoteDetail.objects.filter(credit_note__id=id).all()
    details.delete()
    total_heads = int(request.POST['invoice-heads-total'])
    for i in range(1,total_heads+1):
        isActive = request.POST[f'isActive_{i}']
        if isActive == '1':
            billing_head = BillingHead.objects.filter(id=int(request.POST[f'billing_head_{i}'])).first() 
            currency_obj = currency.objects.filter(id=int(request.POST[f'currency_{i}'])).first() 
            ex_rate = request.POST[f'ex_rate_{i}']
            tax_applicable = request.POST[f'tax_applicable_{i}']
            rate = request.POST[f'rate_{i}']
            qty = request.POST[f'qty_{i}']
            gst = request.POST[f'gst_{i}']
            amount = request.POST[f'amount_{i}']
            total = request.POST[f'total_{i}']
            gst_amount = request.POST[f'inv_gst_amount_{i}'] 
            new_crn_heads = CreditNoteDetail(
                credit_note = crn,
                billing_head = billing_head,
                currency = currency_obj,
                ex_rate = ex_rate,
                rate = rate,
                qty_unit = qty,
                amount = amount,
                gst = gst,
                total = total,
                gst_amount=gst_amount,
                tax_applicable=tax_applicable
            )
            new_crn_heads.save()
    
    

@login_required(login_url='home:handle_login')
def create_credit_note(request,module):
    context ={}
    check_permissions(request,module)
    form = CreditNoteForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        try:
            if form.instance.reference_invoice:
                form.instance.invoice_no = form.instance.reference_invoice.final_invoice_no
        except:
            pass
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
            
        form.save()
        handle_crn_bh(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, New Credit Note Created.")
        return redirect('accounting:create_credit_note',module=module)
    billing_heads = BillingHead.objects.all()
    currencies = currency.objects.all()
    context['form']= form
    context['module']= module
    context['billing_heads'] = billing_heads
    context['currencies'] = currencies
    return render(request,'credit_note/create_credit_note.html',context)

@login_required(login_url='home:handle_login')
def credit_note_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(CreditNote, id = id)
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
   
    current_financial_date = date(current_year, 4, 1)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:credit_note_details',module=module)
    
    invoice_heads = CreditNoteDetail.objects.filter(credit_note=obj).all()
    
    created_by = obj.created_by
    company_type = obj.company_type
    job_no = obj.job_no
    is_rcm = obj.is_rcm
    form = CreditNoteForm(request.POST or None, instance = obj)
    if form.is_valid():
        try:
            if form.instance.reference_invoice:
                form.instance.invoice_no = form.instance.reference_invoice.final_invoice_no
        except:
            pass
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
            
        if not form.instance.job_no:
            form.instance.job_no = job_no
       
        form.save()
        
        handle_crn_bh(request,form.instance.id)
        
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:credit_note_details',module=module)
          
    billing_heads = BillingHead.objects.all()
    currencies = currency.objects.all()
    
    context['form']= form
    context['module']= module
    context['update']= True
    context['billing_heads'] = billing_heads
    context['currencies'] = currencies
    context['invoice_heads']= invoice_heads
    context['total_invoice_heads']= len(invoice_heads)
    return render(request,'credit_note/create_credit_note.html',context)

@login_required(login_url='home:handle_login')
def credit_note_details(request,module):
    

    context ={}
    check_permissions(request,module)
  
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    notes = CreditNote.objects.filter(is_einvoiced=False).filter(is_deleted = False).select_related('job_no','bill_to','company_type','bill_to_address','created_by').all()

    if not request.user.user_account.see_global_data:
        notes = notes.filter(company_type=company).all()
    
    if not request.user.user_account.also_handle_other_work:
        notes = notes.filter(created_by=request.user).all()
    
    context['notes']= notes
    context['current_date']= date.today()
    
 
    context['module']= module
    return render(request,'credit_note/credit_note_details.html',context)

@login_required(login_url='home:handle_login')
def e_credit_note_details(request,module):
    context ={}
    check_permissions(request,module)
  
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    notes = CreditNote.objects.filter(is_deleted = False).filter(is_einvoiced=True).select_related('bill_to','bill_to_address','company_type','created_by','job_no').all()

   

    if not request.user.user_account.see_global_data:
        notes = notes.filter(company_type=company).all()
   
    if not request.user.user_account.also_handle_other_work:
        notes = notes.filter(created_by=request.user).all()

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"
    if request.method == 'POST':

        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)

    notes = notes.filter(einvoice_date__range=[from_date,to_date]).all()
            
    context['choose_company'] = choose_company
    if not choose_company == "All":
        notes = notes.filter(company_type__id=int(choose_company))
        context['choose_company'] = int(choose_company)
    
    notes = notes.filter(company_type__tax_policy = "GST").all()      
    
    context['notes']= notes
    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")

    context['module']= module
    return render(request,'credit_note/e_credit_note.html',context)

@login_required(login_url='home:handle_login')
def final_credit_note_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    note = CreditNote.objects.select_related('bill_to','bill_to_address','company_type','created_by','job_no').all()
    
    if not request.user.user_account.see_global_data:
        note = note.filter(company_type=company).all()
   
    
    if not request.user.user_account.also_handle_other_work:
        note = note.filter(created_by=request.user).all()

    note = note.filter(is_deleted=False).filter(is_final=True).exclude(company_type__tax_policy = "GST").all().order_by('-id')
    for i in note:
        if not i.is_einvoiced:
            i.is_einvoiced = True
            i.final_invoice_no = i.credit_note_no
            i.einvoice_date = i.date_of_note
            i.save()

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"
    if request.method == 'POST':

        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)

    note = note.filter(date_of_note__range=[from_date,to_date]).all()
    
    context['choose_company'] = choose_company
    if not choose_company == "All":
        note = note.filter(company_type__id=int(choose_company))
        context['choose_company'] = int(choose_company)
                

    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")
    context['note']= note
    context['module']= module
    return render(request,'credit_note/final_credit_note.html',context)

@login_required(login_url='home:handle_login')
def make_eninvoice_credit_note(request,module,id):
    check_permissions(request,module)
    login_and_get_token(request)
    status = add_credit_note_irn(request,id)
    messages.success(request,status)
    return redirect('accounting:credit_note_details',module=module)

@login_required(login_url='home:handle_login')
def credit_note_delete(request,module,id):
    check_permissions(request,module)
    note = CreditNote.objects.filter(id=int(id)).first()
    note.is_deleted = True
    note.deleted_by = request.user
    note.save()
    return redirect('accounting:credit_note_details',module=module)

def crn_pdf(request,id):
    template_path = 'credit_note/tax_invoice_pdf.html'
   
    invoice = CreditNote.objects.filter(id=int(id)).first()
    invoice.save()


    commoditys=[]
    vessels=[]
    hbl_no=[]
    mbl_no=[]
    total_pkg=[]
    total_gross_weight=[]
    total_cbm=[]
    for i in invoice.hbl_options.all():
        hbl_no.append(i.job_hbl_no)
        mbl_no.append(i.mbl_no)
        commoditys.append(i.commodity)
        vessels.append(i.vessel_name)
        if i.no_of_packages:
          total_pkg.append(int(i.no_of_packages))
        else:
            total_pkg.append(int(0))
        total_gross_weight.append(float(i.gross_weight))
        total_cbm.append(float(i.volume))

    hbl_data =" / ".join(hbl_no)
    try:
       mbl_no =" / ".join(mbl_no)
    except:
        mbl_no='None'

    try:
       vessel =" / ".join(vessels)
    except:
        vessel='None'

    try:
       commodity =" / ".join(commoditys)
    except:
        commodity='None'

    t_pkg=sum(total_pkg)
   
    t_gross_weight=sum(total_gross_weight)
    t_cbm=sum(total_cbm)

   
    
    domain = Site.objects.get_current().domain
    per_5 = 0
    per_i5 = 0
    per_12 = 0
    per_i12 = 0
    per_18 = 0
    per_i18 = 0
    total_taxable_amount = 0
    per_5_taxable = 0
    per_12_taxable = 0
    per_18_taxable = 0
    is_local = False
    try:
        if  invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
            is_local = True
    except:
        pass
        
    for i in invoice.credit_note_reference.all():
        
        if i.gst == 5:
            if is_local and not i.billing_head.always_igst:
                per_5 += i.gst_amount
                per_5_taxable += i.amount
            else:
                per_i5 += i.gst_amount
                per_5_taxable += i.amount
        
        if i.gst == 12:
            if is_local and not i.billing_head.always_igst:
                per_12 += i.gst_amount
                per_12_taxable += i.amount
            else:
                per_i12 += i.gst_amount
                per_12_taxable += i.amount
        
        
        if i.gst == 18:
            if is_local and not i.billing_head.always_igst:
                per_18 += i.gst_amount
                per_18_taxable += i.amount
            else:
                per_i18 += i.gst_amount
                per_18_taxable += i.amount
        
        if i.gst > 0:
            total_taxable_amount += i.amount
    
    pending_col = []

    try:    
        data_container=[i.job_container_no for i in invoice.job_no.job_container.all()]
        container_details=", ".join(data_container)
    except:
        container_details = ""
    
    col_in_invoice = 17
    if invoice.is_einvoiced and invoice.signed_qr_code:
        col_in_invoice = 18
    
    for i in range(col_in_invoice - len(invoice.credit_note_reference.all())):
        pending_col.append(i)
        
    rcm_head = Logistic.objects.filter(company_name = "Pinkcity Kanpur").first()
    head = invoice.company_type
    if invoice.is_rcm:
        template_path = 'credit_note/rcm_pdf.html'
        if rcm_head:
            head = rcm_head
            
    if invoice.company_type.tax_policy == "VAT":
        invoice = CreditNote.objects.filter(id=int(id)).first()
        template_path = 'credit_note/vat_invoice_pdf.html'


            
    context = {
        'container_details':container_details,
        'commodity':commodity,
        'vessel_name':vessel,
        'hbl_data':hbl_data,
        'mbl_no':mbl_no,
        't_pkg':t_pkg,
        't_gross_weight':t_gross_weight,
        't_cbm':t_cbm,
        'data':invoice,
        'head':head,
        'blank':pending_col,
        'per_5':per_5,
        'per_12':per_12,
        'per_18':per_18,
        'total_cgst':(per_5 + per_12 + per_18)/2,
        'total_sgst':(per_5 + per_12 + per_18)/2,
        'total_igst':(per_i5 + per_i12 + per_i18),
        'total_5':per_5 + per_i5,
        'total_12':per_12 + per_i12,
        'total_18':per_18 + per_i18,
        'per_i5':round(per_i5,2),
        'per_i12':round(per_i12,2),
        'per_i18':round(per_i18,2),
        'per_5_taxable':per_5_taxable,
        'per_12_taxable':per_12_taxable,
        'per_18_taxable':per_18_taxable,
        'total_taxable_amount':total_taxable_amount,
        'domain':domain,
        'container_details':container_details,
        
    }
    
    return generate_pdf(request,template_path,context)

def crn_print_pdf(request,id):
    template_path = 'credit_note/tax_invoice_pdf.html'
    invoice = CreditNote.objects.filter(id=int(id)).first()

   
    
    domain = Site.objects.get_current().domain
    per_5 = 0
    per_i5 = 0
    per_12 = 0
    per_i12 = 0
    per_18 = 0
    per_i18 = 0
    total_taxable_amount = 0
    per_5_taxable = 0
    per_12_taxable = 0
    per_18_taxable = 0
    is_local = False
    try:
        if  invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
            is_local = True
    except:
        pass

    try:    
        data_container=[i.job_container_no for i in invoice.job_no.job_container.all()]
        container_details=",".join(data_container)
    except:
        container_details = ""
        
    for i in invoice.credit_note_reference.all():
        
        if i.gst == 5:
            if is_local and not i.billing_head.always_igst:
                per_5 += i.gst_amount
                per_5_taxable += i.amount
            else:
                per_i5 += i.gst_amount
                per_5_taxable += i.amount
        
        if i.gst == 12:
            if is_local and not i.billing_head.always_igst:
                per_12 += i.gst_amount
                per_12_taxable += i.amount
            else:
                per_i12 += i.gst_amount
                per_12_taxable += i.amount
        
        
        if i.gst == 18:
            if is_local and not i.billing_head.always_igst:
                per_18 += i.gst_amount
                per_18_taxable += i.amount
            else:
                per_i18 += i.gst_amount
                per_18_taxable += i.amount
        
        if i.gst > 0:
            total_taxable_amount += i.amount
    
    pending_col = []
    
    col_in_invoice = 16
    if invoice.is_einvoiced and invoice.signed_qr_code:
        col_in_invoice = 22
    
    for i in range(col_in_invoice - len(invoice.credit_note_reference.all())):
        pending_col.append(i)
        
    rcm_head = Logistic.objects.filter(company_name = "Pinkcity Kanpur").first()
    head = invoice.company_type
    if invoice.is_rcm:
        template_path = 'credit_note/rcm_pdf.html'
        if rcm_head:
            head = rcm_head
            
    if invoice.company_type.tax_policy == "VAT":
        invoice = CreditNote.objects.filter(id=int(id)).first()
        
        template_path = 'credit_note/credit_note_print_pdf.html'
    

    
            
    context = {
        'data':invoice,
        'head':head,
        'blank':pending_col,
        'per_5':per_5,
        'per_12':per_12,
        'per_18':per_18,
        'total_cgst':(per_5 + per_12 + per_18)/2,
        'total_sgst':(per_5 + per_12 + per_18)/2,
        'total_igst':(per_i5 + per_i12 + per_i18),
        'total_5':per_5 + per_i5,
        'total_12':per_12 + per_i12,
        'total_18':per_18 + per_i18,
        'per_i5':round(per_i5,2),
        'per_i12':round(per_i12,2),
        'per_i18':round(per_i18,2),
        'per_5_taxable':per_5_taxable,
        'per_12_taxable':per_12_taxable,
        'per_18_taxable':per_18_taxable,
        'total_taxable_amount':total_taxable_amount,
        'domain':domain,
        'container_details':container_details,
    }
    
    return generate_pdf(request,template_path,context)

@login_required(login_url='home:handle_login')
def ammend_credit_note(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(CreditNote, id = id)

    if not obj.is_einvoiced:
        messages.add_message(request, messages.SUCCESS, f"Credit Note is not e-invoiced.")
        return redirect('accounting:e_credit_note_details',module=module)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user and request.user.user_account.can_update :
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:e_credit_note_details',module=module)
    
   
    invoice_no = obj.final_invoice_no
    einvoice_date = obj.einvoice_date
    bill_to = obj.bill_to
    bill_to_address = obj.bill_to_address

    form = AmmendCreditNoteForm(request.POST or None, instance = obj)
  
    context['form']= form
    context['module']= module
    context['update']= True
    context['data']= obj
    
    if form.is_valid():
        form.instance.pending_amount = form.instance.net_amount
        form.instance.bill_to = bill_to
        form.instance.bill_to_address = bill_to_address
        form.save()

        new_ammend = Ammendment.objects.create(
            amm_type = "C",
            invoice_no = invoice_no,
            invoice_date = einvoice_date.date(),
            credit_note=form.instance
        )   
        new_ammend.save()
    
        handle_crn_bh(request,form.instance.id)

        
                
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:e_credit_note_details',module=module)

    return render(request,'credit_note/ammend_credit_note.html',context)
    
# Debit Note
def handleDebitNoteHeads(request,id):
    total_heads = int(request.POST['invoice-heads-total'])
    debit_note_instance = DebitNote.objects.filter(id = int(id)).first()
    debit_note_heads = DebitNoteDetail.objects.filter(debit_note=debit_note_instance).all()
    debit_note_heads.delete()

    for i in range(1,total_heads+1):
        isActive = request.POST[f'isActive_{i}']
        if isActive == '1':
            billing_head = BillingHead.objects.filter(id=int(request.POST[f'billing_head_{i}'])).first() 
            currency_obj = currency.objects.filter(id=int(request.POST[f'currency_{i}'])).first() 
            ex_rate = request.POST[f'ex_rate_{i}']
            rate = request.POST[f'rate_{i}']
            qty = request.POST[f'qty_{i}']
            gst = request.POST[f'gst_{i}']
            amount = request.POST[f'amount_{i}']
            total = request.POST[f'total_{i}']
            gst_amount = request.POST[f'inv_gst_amount_{i}']
            new_debit_note_detail = DebitNoteDetail(
                debit_note = debit_note_instance,
                billing_head = billing_head,
                currency = currency_obj,
                ex_rate = ex_rate,
                rate = rate,
                qty_unit = qty,
                amount = amount,
                gst = gst,
                total = total,
                gst_amount=gst_amount
            )
            new_debit_note_detail.save()
    
    debit_note_instance.save()

@login_required(login_url='home:handle_login')
def create_debit_note(request,module):
    context ={}
    check_permissions(request,module)
    form = DebitNoteForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office

        if form.instance.party_type == "Direct":
            form.instance.bill_from_vendor = None
        else:
            form.instance.bill_from = None
            form.instance.bill_from_address = None


        form.save()
        handleDebitNoteHeads(request,id=form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, New Debit Note Created.")
        return redirect('accounting:create_debit_note',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,f'debit_note/create_debit_note.html',context)
   
@login_required(login_url='home:handle_login')
def debit_note_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(DebitNote, id = id)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:debit_note_details',module=module)
    
    form = DebitNoteForm(request.POST or None, instance = obj)
   
    created_by = obj.created_by
    company_type = obj.company_type
    job_no = obj.job_no
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type

        if not form.instance.job_no:
            form.instance.job_no = job_no

        if form.instance.party_type == "Direct":
            form.instance.bill_from_vendor = None
        else:
            form.instance.bill_from = None
            form.instance.bill_from_address = None

        form.save()
        handleDebitNoteHeads(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:debit_note_details',module=module)
    
    else:
        print(form.errors.as_json())
          
    context['form']= form
    context['module']= module
    context['update']= True
    template_name = 'debit_note'
    return render(request,f'debit_note/create_debit_note.html',context)

@login_required(login_url='home:handle_login')
def debit_note_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    notes = DebitNote.objects.select_related('company_type','bill_from','bill_from_address','created_by','job_no').filter(is_deleted=False).all()

    if not request.user.user_account.see_global_data:
        notes = notes.filter(company_type=company).all()
   
    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    
    if request.method == 'POST':

        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)

    notes = notes.filter(date_of_note__range=[from_date,to_date]).all()
            
    if not request.user.user_account.also_handle_other_work:
        notes = notes.filter(created_by=request.user).all()  
          
    context['notes']= notes
    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")
    
    context['module']= module
    return render(request,'debit_note/debit_note_details.html',context)

@login_required(login_url='home:handle_login')
def debit_note_delete(request,module,id):
    check_permissions(request,module)
    note = DebitNote.objects.filter(id=int(id)).first()
    note.is_deleted = True
    note.deleted_by = request.user
    note.save()
    return redirect('accounting:debit_note_details',module=module)

@login_required(login_url='home:handle_login')
def drn_pdf(request,id):
    invoice = DebitNote.objects.filter(id=int(id)).first()
    amount_in_words = num2words.num2words(invoice.net_amount, lang='en_IN')
    context = {
        'data':invoice,
        'amount_in_words':amount_in_words
    }
    return render(request,'debit_note/pdf.html',context)

# Invoice Payable
def handleInvoicePayableHead(request,id):
    payable_invoice = InvoicePayable.objects.filter(id = int(id)).first()
    invoice_heads = InvoicePayableDetail.objects.filter(invoice_payable = payable_invoice).all()
    invoice_heads.delete()

    total_heads = int(request.POST['invoice-heads-total'])
    for i in range(1,total_heads+1):
        isActive = request.POST[f'isActive_{i}']
        if isActive == '1':
            billing_head = BillingHead.objects.filter(id=int(request.POST[f'billing_head_{i}'])).first() 
            currency_obj = currency.objects.filter(id=int(request.POST[f'currency_{i}'])).first() 
            ex_rate = request.POST[f'ex_rate_{i}']
            rate = request.POST[f'rate_{i}']
            qty = request.POST[f'qty_{i}']
            gst = request.POST[f'gst_{i}']
            amount = request.POST[f'amount_{i}']
            total = request.POST[f'total_{i}']
            gst_amount = request.POST[f'inv_gst_amount_{i}']
            
            new_invoice_payable_detail = InvoicePayableDetail(
                invoice_payable = payable_invoice,
                billing_head = billing_head,
                currency = currency_obj,
                ex_rate = ex_rate,
                rate = rate,
                qty_unit = qty,
                amount = amount,
                gst = gst,
                total = total,
                gst_amount=gst_amount
            )
            new_invoice_payable_detail.save()

    payable_invoice.save()

@login_required(login_url='home:handle_login')
def create_invoice_payable(request,module):
    context ={}

    check_permissions(request,module)
  
    form = InvoicePayableForm()
    if request.method == 'POST':
        form = InvoicePayableForm(request.POST,request.FILES)
   
    if form.is_valid():
        form.instance.invoice_no = form.instance.purchase_invoice_no
        form.instance.created_by = request.user
        form.instance.pending_amount = form.instance.net_amount - form.instance.tds_payable
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office

        if form.instance.party_type == "Direct":
            form.instance.vendor = None
        else:
            form.instance.bill_from = None
            form.instance.bill_from_address = None

        form.save()
        
        handleInvoicePayableHead(request,form.instance.id)
            
        messages.add_message(request, messages.SUCCESS, f"Success, New Payable Invoice Created.")
        return redirect('accounting:create_invoice_payable',module=module)
    
    billing_heads = BillingHead.objects.all()
    currencies = currency.objects.all()

    context['form']= form
    context['module']= module
    context['billing_heads'] = billing_heads
    context['currencies'] = currencies
   
    return render(request,'invoice_payable/create_invoice_payable.html',context)

@login_required(login_url='home:handle_login')
def invoice_payable_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(InvoicePayable, id = id)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:invoice_payable_details',module=module)
    
    invoice_heads = InvoicePayableDetail.objects.filter(invoice_payable=obj).all()
    
    form = InvoicePayableForm(instance = obj)
    if request.method == 'POST':
        form = InvoicePayableForm(request.POST, request.FILES, instance=obj)
    invoice = InvoicePayable.objects.filter(id=id).first()
    created_by = obj.created_by
    company_type = obj.company_type
    is_final = obj.is_final
    job_no = obj.job_no     
    if form.is_valid():
        form.instance.invoice_no = form.instance.purchase_invoice_no
        form.instance.pending_amount = form.instance.net_amount - form.instance.tds_payable
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        form.instance.is_final = is_final
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        
        if not form.instance.job_no:
            form.instance.job_no = job_no

        if form.instance.party_type == "Direct":
            form.instance.vendor = None
        else:
            form.instance.bill_from = None
            form.instance.bill_from_address = None

        form.save()
        
        handleInvoicePayableHead(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:invoice_payable_details',module=module)
          
    billing_heads = BillingHead.objects.all()
    currencies = currency.objects.all()
    
    context['form']= form
    context['module']= module
    context['update']= True
    context['billing_heads'] = billing_heads
    context['currencies'] = currencies
    context['invoice'] = invoice
    context['invoice_heads']= invoice_heads
    context['total_invoice_heads']= len(invoice_heads)
    return render(request,'invoice_payable/create_invoice_payable.html',context)

@login_required(login_url='home:handle_login')
def invoice_payable_details(request,module):
    context ={}
    check_permissions(request,module)

    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    invoices = InvoicePayable.objects.filter(is_deleted=False).filter(old_invoice=False).select_related('company_type','bill_from','invoice_currency','job_no','created_by','bill_from_address').prefetch_related('pay_payment_inv','pay_payment_inv__voucher').all()


    if not request.user.user_account.see_global_data:
        invoices = invoices.filter(company_type=company).all()

    
    jobs = JobMaster.objects.filter(company_type=1).all()
    # for job in jobs:
       
    #     for invoice in invoices.filter(job_no=None).all():
    #         if job.job_no in invoice.remark_on_invoice:
    #             invoice.job_no = job
    #             invoice.save()
    #             print(job.job_no,invoice.remark_on_invoice,str(invoice.remark_on_invoice).find(job.job_no))

    current_year = datetime.now().year
    new_current_year = datetime.now().year
    
    current_month = datetime.now().month
    new_month=current_month-3
    if new_month < 0:
        new_month = 13 + new_month
        new_current_year -= 1
        
    if new_month == 0:
        new_month = 12 + new_month
        new_current_year -= 1
        

    _,end_day = calendar.monthrange(current_year, current_month)

    from_date = date(new_current_year,new_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']
        to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date()
        from_to_date = to_date + timedelta(days=1)
        

    invoices = invoices.filter(date_of_invoice__range=[from_date,to_date]).all()
        
    context['choose_company'] = choose_company
    if not choose_company == "All":
        invoices = invoices.filter(company_type__id=int(choose_company))
        context['choose_company'] = int(choose_company)

        
    if not request.user.user_account.also_handle_other_work:
        invoices = invoices.filter(created_by=request.user).all()   
        
    # for i in invoices:
    #     if i.pay_payment_inv.count() == 0:
    #         i.pending_amount = round(i.net_amount - i.tds_payable,2)
    #         i.save()
    
    context['notes']= invoices
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()
    return render(request,'invoice_payable/invoice_payable_details.html',context)

@login_required(login_url='home:handle_login')
def invoice_payable_adjustment(request,module,id):
    check_permissions(request,module)
    if request.method == "POST":
        invoice = InvoicePayable.objects.filter(id=int(id)).first()
        confirm = request.POST.get('confirm',False)
        adjusted_amount = request.POST.get('adjusted_amount',0)
        if confirm:
            invoice.pending_amount = round(invoice.pending_amount - float(adjusted_amount),2)
        invoice.save()
    return redirect('accounting:invoice_payable_details',module=module)

@login_required(login_url='home:handle_login')
def invoice_payable_delete(request,module,id):
    check_permissions(request,module)
    invoice = InvoicePayable.objects.filter(id=int(id)).first()
    invoice.is_deleted = True
    invoice.deleted_by = request.user
    invoice.save()
    return redirect('accounting:invoice_payable_details',module=module)

@login_required(login_url='home:handle_login')
def approve_invoice_payable(request,module,id):
    check_permissions(request,module)
   
    if request.method == "POST":
        invoice_no = request.POST['verify_invoice_no']
        invoice = InvoicePayable.objects.filter(id=int(id)).first()
        if invoice.invoice_no == invoice_no:
            invoice.is_approved = True
            invoice.save()
            messages.add_message(request, messages.SUCCESS, f"Success, {invoice.invoice_no} is approved.")
        else:
            messages.add_message(request, messages.SUCCESS, f"Fail, {invoice.invoice_no} is not approved.")
        return redirect('accounting:invoice_payable_details',module=module)
    return redirect('accounting:invoice_payable_details',module=module)

def invoice_payable_pdf(request,id):
    template_path = 'invoice_payable/pdf2.html'
    invoice = InvoicePayable.objects.filter(id=int(id)).first()
    amount_in_words = num2words.num2words(round(invoice.net_amount), lang='en_IN')
    amount_in_words = amount_in_words.replace(',','')
    domain = Site.objects.get_current().domain
    per_5 = 0
    per_i5 = 0
    per_12 = 0
    per_i12 = 0
    per_18 = 0
    per_i18 = 0
    total_taxable_amount = 0
    per_5_taxable = 0
    per_12_taxable = 0
    per_18_taxable = 0
    is_local = False
    try:
        if  invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
            is_local = True
    except:
        pass
        
    for i in invoice.payable_invoice_reference.all():
        
        if i.gst == 5:
            if is_local and not i.billing_head.always_igst:
                per_5 += i.gst_amount
                per_5_taxable += i.amount
            else:
                per_i5 += i.gst_amount
                per_5_taxable += i.amount
        
        if i.gst == 12:
            if is_local and not i.billing_head.always_igst:
                per_12 += i.gst_amount
                per_12_taxable += i.amount
            else:
                per_i12 += i.gst_amount
                per_12_taxable += i.amount
        
        
        if i.gst == 18:
            if is_local and not i.billing_head.always_igst:
                per_18 += i.gst_amount
                per_18_taxable += i.amount
            else:
                per_i18 += i.gst_amount
                per_18_taxable += i.amount
        
        if i.gst > 0:
            total_taxable_amount += i.amount
    
    pending_col = []
    
    col_in_invoice = 25

    
    for i in range(col_in_invoice - len(invoice.payable_invoice_reference.all())):
        pending_col.append(i)
        
   
    head = invoice.company_type
 
    
            
    context = {
        'data':invoice,
        'head':head,
        'blank':pending_col,
        'amount_in_words':amount_in_words.upper(),
        'per_5':per_5,
        'per_12':per_12,
        'per_18':per_18,
        'per_i5':round(per_i5),
        'per_i12':round(per_i12),
        'per_i18':round(per_i18),
        'per_5_taxable':per_5_taxable,
        'per_12_taxable':per_12_taxable,
        'per_18_taxable':per_18_taxable,
        'total_taxable_amount':total_taxable_amount,
        'domain':domain
    }
    
    return generate_pdf(request,template_path,context)

# ------------- Receipt Voucher -------------
def handleRecieptVoucherHeads(request,id):
    parent_voucher = RecieptVoucher.objects.filter(id=int(id)).first()
    total_rows = int(request.POST['total_rows'])
    net_tds_amount = 0
    net_recieved_amount = 0
    for i in range(1,total_rows+1):
        recieved_amount = float(request.POST[f'amount-{i}'])
        adjustment_amount = float(request.POST[f'adjustment_amount-{i}'])
        tds_amount = float(request.POST[f'tds_amount-{i}'])
        is_active = request.POST[f'is_active-{i}']
        is_update = request.POST[f'is_update-{i}']
        
        if is_active == "no" and is_update == "yes":
            voucher_id = request.POST[f'voucher_id-{i}']
            rv = RecieptVoucherDetails.objects.filter(id=int(voucher_id)).first()
            rv.delete()


        if recieved_amount > 0 or tds_amount > 0 or adjustment_amount > 0 and is_active == "yes":
            payment_type = request.POST[f'payment_type-{i}']
            net_tds_amount += tds_amount
            net_recieved_amount += recieved_amount

            if is_update == "yes":
                voucher_id = request.POST[f'voucher_id-{i}']
                new_rv_details = RecieptVoucherDetails.objects.filter(id=int(voucher_id)).first()
                new_rv_details.voucher = parent_voucher
                new_rv_details.payment_type = payment_type
            else:
                new_rv_details = RecieptVoucherDetails.objects.create(
                    voucher=parent_voucher,
                    payment_type = payment_type
                )

            party = request.POST[f'party-{i}'].split('_')

            if party[0] == "P":
                
                party_address = request.POST[f'party_address-{i}']
                new_rv_details.party_type = 'Direct'
                new_rv_details.party = Party.objects.filter(id=int(party[1])).first()
                new_rv_details.party_address = PartyAddress.objects.filter(id=int(party_address)).first()
                new_rv_details.vendor = None
                new_rv_details.ledger = None
            
            if party[0] == "V":
                new_rv_details.party_type = "Indirect"
                new_rv_details.vendor = Vendor.objects.filter(id=int(party[1])).first()
                new_rv_details.ledger = None
                new_rv_details.party = None
                new_rv_details.party_address = None
            
            if party[0] == "L":
                new_rv_details.party_type = 'Other'
                new_rv_details.ledger = LedgerMaster.objects.filter(id=int(party[1])).first()
                new_rv_details.vendor = None
                new_rv_details.party = None
                new_rv_details.party_address = None

            if payment_type == "BW":
                try:
                    bill = request.POST[f'bill-{i}']
                    if bill:
                        new_rv_details.invoice = InvoiceReceivable.objects.filter(id=int(bill)).first()
                except:
                    pass
            else:
                new_rv_details.invoice = None
                
            new_rv_details.received_amount = recieved_amount
            new_rv_details.adjustment_amount = adjustment_amount
            new_rv_details.tds_amount = tds_amount

            new_rv_details.save()

    parent_voucher.net_amount = net_recieved_amount + net_tds_amount + adjustment_amount
    parent_voucher.received_amount = net_recieved_amount
    parent_voucher.adjustment_amount = adjustment_amount
    parent_voucher.reciept_tds_amount = net_tds_amount
    parent_voucher.save()

@login_required(login_url='home:handle_login')
def create_reciept_voucher(request,module):
    context ={}
    check_permissions(request,module)
    form = RecieptVoucherForm(request.POST or None,initial={'company_type':request.user.user_account.office})
    if form.is_valid():
        form.save()
        handleRecieptVoucherHeads(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, New Reciept Voucher Created.")
        return redirect('accounting:create_reciept_voucher',module=module)    
    context['form']= form
    context['module']= module
    return render(request,'reciept_voucher/create_reciept_voucher.html',context)

@login_required(login_url='home:handle_login')
def reciept_voucher_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(RecieptVoucher, id = id)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:reciept_voucher_details',module=module)
    form = RecieptVoucherForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        handleRecieptVoucherHeads(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:reciept_voucher_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'reciept_voucher/create_reciept_voucher.html',context)

@login_required(login_url='home:handle_login')
def reciept_voucher_details(request,module):
    context ={}
    check_permissions(request,module)
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    vouchers = RecieptVoucher.objects.select_related('company_type','party_name','created_by').prefetch_related('rec_voucher_detail','rec_voucher_detail__party','rec_voucher_detail__vendor','rec_voucher_detail__ledger').filter(is_deleted=False).all()

    
    # RecieptVoucher.objects.filter(is_deleted=True).all().update(is_deleted=False)

    # for voucher in vouchers:
    #     if voucher.party_name or voucher.vendor:
    #         new_format_rv = RecieptVoucher.objects.create(
    #             voucher_no = voucher.voucher_no,
    #             voucher_date = voucher.voucher_date,
    #             company_type = voucher.company_type,
    #             recieve_in = voucher.recieve_in,
    #             instrument_no = voucher.instrument_no,
    #             bank = voucher.to_bank,
    #             bank_charges = voucher.bank_charges,
    #             bank_charges_cgst = voucher.bank_charges_cgst,
    #             bank_charges_sgst = voucher.bank_charges_sgst,
    #             bank_charges_igst = voucher.bank_charges_igst,
    #             bank_charges_tax = voucher.bank_charges_tax,
    #             narration = voucher.narration,
    #             created_by = voucher.created_by,
    #             created_at = voucher.created_at,
    #             updated_by = voucher.updated_by,
    #             updated_at = voucher.updated_at,
    #         )
    #         tds_amount = 0
    #         received_amount = 0
    #         new_format_rv.save()

    #         for detail in voucher.rec_voucher_detail.all():
    #             # if detail.party or detail.vendor:
    #             #     detail.delete()
    #             #     continue

    #             received_amount += detail.received_amount
    #             tds_amount += detail.tds_amount
    #             new_format_detail = RecieptVoucherDetails.objects.create(
    #                 voucher=new_format_rv,
    #                 party = voucher.party_name or None,
    #                 party_address = voucher.party_address or None,
    #                 vendor = voucher.vendor or None,
    #                 invoice = detail.invoice or None,
    #                 party_type = voucher.payment_type,
    #                 payment_type = "BW",
    #                 received_amount = detail.received_amount,
    #                 tds_amount = detail.tds_amount,
    #                 tds_claimed = detail.tds_claimed,
    #                 tds_claim_date = detail.tds_claim_date,
                    

    #             )
    #             new_format_detail.save()

    #         if voucher.advance_amount > 0:
    #             received_amount += voucher.advance_amount
    #             new_format_detail = RecieptVoucherDetails.objects.create(
    #                 voucher=new_format_rv,
    #                 party = voucher.party_name or None,
    #                 party_address = voucher.party_address or None,
    #                 vendor = voucher.vendor or None,
    #                 party_type = voucher.payment_type,
    #                 payment_type = "OAC",
    #                 received_amount = voucher.advance_amount,
    #             )
    #             new_format_detail.save()

           
    #         if voucher.voucher and  voucher.voucher.advance_amount > 0:
    #             received_amount += voucher.voucher.advance_amount
    #             new_format_detail = RecieptVoucherDetails.objects.create(
    #                 voucher=new_format_rv,
    #                 party = voucher.party_name or None,
    #                 party_address = voucher.party_address or None,
    #                 vendor = voucher.vendor or None,
    #                 party_type = voucher.payment_type,
    #                 payment_type = "OAC",
    #                 received_amount = voucher.voucher.advance_amount,
    #             )
    #             new_format_detail.save()

           
    #         new_format_rv.received_amount = received_amount
    #         new_format_rv.reciept_tds_amount = tds_amount
    #         new_format_rv.net_amount = received_amount + tds_amount
    #         new_format_rv.save()

    #         voucher.is_deleted = True
    #         voucher.save()

    
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']        
        
    vouchers = vouchers.filter(voucher_date__range=[from_date,to_date])
    
    if not request.user.user_account.see_global_data:
        vouchers = vouchers.filter(company_type=company).all()
   
    if not request.user.user_account.also_handle_other_work:
        vouchers = vouchers.filter(created_by=request.user).all()
    
    
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()
    context['vouchers']= vouchers
    context['module']= module
    return render(request,'reciept_voucher/reciept_voucher_detail.html',context)

@login_required(login_url='home:handle_login')
def reciept_voucher_delete(request,module,id):
    check_permissions(request,module)
    voucher = RecieptVoucher.objects.filter(id=int(id)).first()
    voucher.delete()
    return redirect('accounting:reciept_voucher_details',module=module)




# ------------- Payment Voucher -------------

def handlePaymentVoucherHeads(request,id):
    parent_voucher = PaymentVoucher.objects.filter(id=int(id)).first()
    total_rows = int(request.POST['total_rows'])
    net_tds_amount = 0
    net_paid_amount = 0
    for i in range(1,total_rows+1):
        paid_amount = float(request.POST[f'amount-{i}'])
        tds_amount = float(request.POST[f'tds_amount-{i}'])
        adjustment_amount = float(request.POST[f'adjustment_amount-{i}'])
        is_active = request.POST[f'is_active-{i}']
        is_update = request.POST[f'is_update-{i}']
        
        if is_active == "no" and is_update == "yes":
            voucher_id = request.POST[f'voucher_id-{i}']
            pv = PaymentVoucherDetails.objects.filter(id=int(voucher_id)).first()
            pv.delete()


        if (paid_amount > 0 or tds_amount > 0  or adjustment_amount > 0  ) and is_active == "yes":
            payment_type = request.POST[f'payment_type-{i}']
            net_tds_amount += tds_amount
            net_paid_amount += paid_amount

            if is_update == "yes":
                voucher_id = request.POST[f'voucher_id-{i}']
                new_pv_details = PaymentVoucherDetails.objects.filter(id=int(voucher_id)).first()
                new_pv_details.voucher = parent_voucher
                new_pv_details.payment_type = payment_type
            else:
                new_pv_details = PaymentVoucherDetails.objects.create(
                    voucher=parent_voucher,
                    payment_type = payment_type
                )

            party = request.POST[f'party-{i}'].split('_')
            if party[0] == "P":
                party_address = request.POST[f'party_address-{i}']
                new_pv_details.party_type = 'Direct'
                new_pv_details.party = Party.objects.filter(id=int(party[1])).first()
                new_pv_details.party_address = PartyAddress.objects.filter(id=int(party_address)).first()
                new_pv_details.vendor = None
                new_pv_details.ledger = None
            
            if party[0] == "V":
                new_pv_details.party_type = "Indirect"
                new_pv_details.vendor = Vendor.objects.filter(id=int(party[1])).first()
                new_pv_details.ledger = None
                new_pv_details.party = None
                new_pv_details.party_address = None
            
            if party[0] == "L":
                new_pv_details.party_type = 'Other'
                new_pv_details.ledger = LedgerMaster.objects.filter(id=int(party[1])).first()
                new_pv_details.vendor = None
                new_pv_details.party = None
                new_pv_details.party_address = None


            if payment_type == "BW":
                try:
                    bill = request.POST[f'bill-{i}']
                    if bill:
                        new_pv_details.invoice = InvoicePayable.objects.filter(id=int(bill)).first()
                except:
                    pass
                
        
            else:
                new_pv_details.invoice = None
                
            new_pv_details.adjustment_amount = adjustment_amount
            new_pv_details.paid_amount = paid_amount
            new_pv_details.tds_amount = tds_amount

            new_pv_details.save()

    parent_voucher.net_amount = net_paid_amount + net_tds_amount
    parent_voucher.adjustment_amount = adjustment_amount
    parent_voucher.paid_amount = net_paid_amount
    parent_voucher.payment_tds_amount = net_tds_amount
    parent_voucher.save()

@login_required(login_url='home:handle_login')
def create_payment_voucher(request,module):
    context ={}
    check_permissions(request,module)
    form = PaymentVoucherForm(request.POST or None)
    if form.is_valid():
        form.save()
        handlePaymentVoucherHeads(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, New Payment Voucher Created.")
        return redirect('accounting:create_payment_voucher',module=module)    
    context['form']= form
    context['module']= module
    return render(request,'payment_voucher/create_payment_voucher.html',context)

@login_required(login_url='home:handle_login')
def payment_voucher_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(PaymentVoucher, id = id)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:payment_voucher_details',module=module)
    form = PaymentVoucherForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        handlePaymentVoucherHeads(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:payment_voucher_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'payment_voucher/create_payment_voucher.html',context)

@login_required(login_url='home:handle_login')
def payment_voucher_details(request,module):
    context ={}
    check_permissions(request,module)
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    vouchers = PaymentVoucher.objects.select_related('company_type','party_name','party_address','from_bank','updated_by','voucher','created_by','vendor').prefetch_related('pay_voucher_detail','pay_voucher_detail__invoice','pay_voucher_detail__party','pay_voucher_detail__vendor','pay_voucher_detail__ledger').filter(is_deleted=False).all()

    
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']        
        
    vouchers = vouchers.filter(voucher_date__range=[from_date,to_date])
    # payment_voucher_detail_to_be_create = []
    # for voucher in vouchers:
    #     if voucher.party_name or voucher.vendor:
    #         new_format_pv = PaymentVoucher.objects.create(
    #             voucher_no = voucher.voucher_no,
    #             voucher_date = voucher.voucher_date,
    #             company_type = voucher.company_type,
    #             pay_from = voucher.pay_from,
    #             instrument_no = voucher.instrument_no,
    #             bank = voucher.from_bank,
    #             bank_charges = voucher.bank_charges,
    #             bank_charges_cgst = voucher.bank_charges_cgst,
    #             bank_charges_sgst = voucher.bank_charges_sgst,
    #             bank_charges_igst = voucher.bank_charges_igst,
    #             bank_charges_tax = voucher.bank_charges_tax,
    #             narration = voucher.narration,
    #             created_by = voucher.created_by,
    #             created_at = voucher.created_at,
    #             updated_by = voucher.updated_by,
    #             updated_at = voucher.updated_at,
    #         )
    #         tds_amount = 0
    #         paid_amount = 0
    #         new_format_pv.save()

    #         for detail in voucher.pay_voucher_detail.all():
    #             paid_amount += detail.paid_amount
    #             tds_amount += detail.tds_amount
    #             new_format_detail = PaymentVoucherDetails(
    #                 voucher=new_format_pv,
    #                 party = voucher.party_name or None,
    #                 party_address = voucher.party_address or None,
    #                 vendor = voucher.vendor or None,
    #                 invoice = detail.invoice or None,
    #                 party_type = voucher.payment_type,
    #                 payment_type = "BW",
    #                 paid_amount = detail.paid_amount,
    #                 tds_amount = detail.tds_amount,
    #             )
    #             if detail.expense:
    #                 new_format_detail.invoice = detail.expense.payable_expense.first()
    #             # new_format_detail.save()

    #             payment_voucher_detail_to_be_create.append(new_format_detail)

    #         if voucher.advance_amount > 0:
    #             paid_amount += voucher.advance_amount
    #             new_format_detail = PaymentVoucherDetails(
    #                 voucher=new_format_pv,
    #                 party = voucher.party_name or None,
    #                 party_address = voucher.party_address or None,
    #                 vendor = voucher.vendor or None,
    #                 party_type = voucher.payment_type,
    #                 payment_type = "OAC",
    #                 paid_amount = voucher.advance_amount,
    #             )
    #             # new_format_detail.save()
    #             payment_voucher_detail_to_be_create.append(new_format_detail)

           
    #         if voucher.voucher and  voucher.voucher.advance_amount > 0:
    #             paid_amount += voucher.voucher.advance_amount
    #             new_format_detail = PaymentVoucherDetails(
    #                 voucher=new_format_pv,
    #                 party = voucher.party_name or None,
    #                 party_address = voucher.party_address or None,
    #                 vendor = voucher.vendor or None,
    #                 party_type = voucher.payment_type,
    #                 payment_type = "OAC",
    #                 paid_amount = voucher.voucher.advance_amount,
    #             )
    #             # new_format_detail.save()
    #             payment_voucher_detail_to_be_create.append(new_format_detail)

           
    #         new_format_pv.paid_amount = paid_amount
    #         new_format_pv.payment_tds_amount = tds_amount
    #         new_format_pv.net_amount = paid_amount + tds_amount
    #         new_format_pv.save()

    #         voucher.is_deleted = True
    
    # PaymentVoucher.objects.bulk_update(vouchers,['is_deleted'])
    # PaymentVoucherDetails.objects.bulk_create(payment_voucher_detail_to_be_create)
    
    
    if not request.user.user_account.see_global_data:
        vouchers = vouchers.filter(company_type=company).all()
   
    if not request.user.user_account.also_handle_other_work:
        vouchers = vouchers.filter(created_by=request.user).all()

    duplicate_list = []
    duplicate_narration = []

    for voucher in vouchers:
        narration = f'{voucher.instrument_no}'
        if duplicate_narration.count(narration) > 1:
            duplicate_list.append(voucher)
            duplicate_narration.append(narration)
        else:
            duplicate_narration.append(narration)
    
    
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()
    context['vouchers']= vouchers
    context['module']= module
    context['duplicate_list']= duplicate_list
    return render(request,'payment_voucher/payment_voucher_detail.html',context)

@login_required(login_url='home:handle_login')
def payment_voucher_delete(request,module,id):
    check_permissions(request,module)
    voucher = PaymentVoucher.objects.filter(id=int(id)).first()
    voucher.delete()
    return redirect('accounting:payment_voucher_details',module=module)



# --------------- DEPRECATED PART ENDED ----------------
def receipt_voucher_pdf(request,id):
    template_path = 'reciept_voucher/on_account/pdf.html'
    dta=RecieptVoucher.objects.filter(id=int(id)).first()
    head = dta.company_type
    domain = Site.objects.get_current().domain     
    context = {
        'data':dta,
        'head':head,
        'domain':domain,
    }
    
    return generate_pdf(request,template_path,context)

def bill_wise_receipt_voucher_pdf(request,id):
    template_path = 'reciept_voucher/bill_wise/pdf.html'
    dta=RecieptVoucher.objects.filter(id=int(id)).first()
    rvd=RecieptVoucherDetails.objects.filter(voucher=dta).all()
    head = dta.company_type
    domain = Site.objects.get_current().domain
    currency = "INR"
    if dta.company_type.branch_name == "THAILAND":
        currency = "THB"
    
    if dta.company_type.branch_name == "Indonesia":
        currency = "IDR"
    
    context = {
        'data':dta,
        'head':head,
        'data2':rvd,
        'domain':domain,
        'currency':currency,
    }
    
    return generate_pdf(request,template_path,context)

# ------------- Contra Voucher -------------
@login_required(login_url='home:handle_login')
def create_contra_voucher(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = ContraVoucherForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        length = str(int(form.instance.id)).zfill(5)
        form.instance.voucher_no = f"CV/{length}"
        form.save()
        
       
      
        messages.add_message(request, messages.SUCCESS, f"Success, New Contra Voucher Created.")
        return redirect('accounting:create_contra_voucher',module=module)
    
    
    context['form']= form
    context['module']= module
    return render(request,'contra_voucher/create_contra_voucher.html',context)

@login_required(login_url='home:handle_login')
def contra_voucher_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    vouchers = ContraVoucher.objects.select_related('company_type','created_by','account_from','account_to','cash').all()
    
  
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = 'All'
    if request.method == 'POST':
        choose_company = request.POST['choose_company']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date()
        from_to_date = to_date + timedelta(days=1)
        
    vouchers = vouchers.filter(voucher_date__range=[from_date,to_date])

    context['choose_company'] = choose_company
    if not choose_company == "All":
        vouchers = vouchers.filter(company_type__id=int(choose_company))
        context['choose_company'] = int(choose_company)
    
    if not request.user.user_account.see_global_data:
        vouchers =vouchers.filter(company_type=company).all()
    
    
    if not request.user.user_account.also_handle_other_work:
        vouchers = vouchers.filter(created_by=request.user).all()

    
    
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d').date()
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d').date()
    context['vouchers']= vouchers
    context['module']= module
    return render(request,'contra_voucher/contra_voucher_detail.html',context)

@login_required(login_url='home:handle_login')
def contra_voucher_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(ContraVoucher, id = id)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:contra_voucher_details',module=module)
    
    form = ContraVoucherForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    voucher_no = obj.voucher_no
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        form.instance.voucher_no = voucher_no
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:contra_voucher_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'contra_voucher/create_contra_voucher.html',context)

@login_required(login_url='home:handle_login')
def contra_voucher_delete(request,module,id):
    check_permissions(request,module)
    voucher = ContraVoucher.objects.filter(id=int(id)).first()
    voucher.delete()
    
    return redirect('accounting:contra_voucher_details',module=module)


# ------------- Journal Voucher -------------

def handleJournalVoucherHeads(request,id):
    parent_voucher = Journal.objects.filter(id=int(id)).first()
    total_rows = int(request.POST['total_rows'])
   
    for i in range(1,total_rows+1):
        account = request.POST[f'account-{i}']
        desc = request.POST[f'desc-{i}']
        action = request.POST[f'action-{i}']
        amount = float(request.POST[f'amount-{i}'])
        is_active = request.POST[f'is_active-{i}']
        is_update = request.POST[f'is_update-{i}']
        
        if is_active == "no" and is_update == "yes":
            voucher_id = request.POST[f'voucher_id-{i}']
            jv = JournalEntry.objects.filter(id=int(voucher_id)).first()
            jv.delete()

        if is_active == "yes":
            if is_update == "yes":
                voucher_id = request.POST[f'voucher_id-{i}']
                new_jv_details = JournalEntry.objects.filter(id=int(voucher_id)).first()
                new_jv_details.voucher = parent_voucher
               
            else:
                new_jv_details = JournalEntry.objects.create(
                    voucher=parent_voucher
                    
                )

            new_jv_details.particular = desc
            new_jv_details.dr_cr = action
            new_jv_details.amount = amount

            account = account.split('_')
            if account[0] == "L":
                new_jv_details.ledger = LedgerMaster.objects.filter(id=int(account[1])).first()

            if account[0] == "P":
                new_jv_details.party = Party.objects.filter(id=int(account[1])).first()
            
            if account[0] == "V":
                new_jv_details.vendor = Vendor.objects.filter(id=int(account[1])).first()

            new_jv_details.save()
     
@login_required(login_url='home:handle_login')
def create_journal(request,module):
    context ={}
    check_permissions(request,module)
    form = JournalVoucherForm(request.POST or None)
    if form.is_valid():
        form.save()
        handleJournalVoucherHeads(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, New Journal Voucher Created.")
        return redirect('accounting:create_journal',module=module)    
    context['form']= form
    context['module']= module
    return render(request,'journal/create_journal.html',context)

@login_required(login_url='home:handle_login')
def journal_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(Journal, id = id)
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('accounting:journal_details',module=module)
    form = JournalVoucherForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        handleJournalVoucherHeads(request,form.instance.id)
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('accounting:journal_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'journal/create_journal.html',context)



@login_required(login_url='home:handle_login')
def journal_details(request,module):
    context = {}
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    Journal.objects.filter(auto_generated=True).all().delete()
    journals = Journal.objects.select_related('company_type','created_by').prefetch_related('journal_entry','journal_entry__party','journal_entry__ledger','journal_entry__vendor').all().order_by('-id')
    
    if not request.user.user_account.see_global_data:
        journals = journals.filter(company_type=company).all()

    current_month = datetime.now().month
   
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    choose_company = "All"
    if request.method == 'POST':

        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        choose_company = request.POST['choose_company']
        

    journals = journals.filter(date__range=[from_date,to_date]).filter(is_deleted=False).all()

    context['choose_company'] = choose_company
    if not choose_company == "All":
        journals = journals.filter(company_type__id=int(choose_company))
        context['choose_company'] = int(choose_company)


    context["module"]= module
    context["choose_company"]= choose_company
    context["journals"]= journals
    context["from_date"]= datetime.strptime(str(from_date),"%Y-%m-%d").date()
    context["to_date"]= datetime.strptime(str(to_date),"%Y-%m-%d").date()
       
    return render(request,'journal/journal_list.html',context)

def journal_delete(request,module,id):
    journal = Journal.objects.filter(id=id).first()
    journal.is_deleted = True
    journal.deleted_by = request.user
    journal.save()
    messages.success(request,"Journal deleted successfully.")
    return redirect("accounting:journal_details",module=module)



# Tally Work
def set_party_tally_group(request):
    if request.GET.get('tally_group') and request.GET.get('party_id'):
        party = Party.objects.filter(id=int(request.GET.get('party_id'))).first()
        party.tally_group = LedgerCategory.objects.filter(id=int(request.GET.get('tally_group'))).first()
        party.save()
        print("Party Tally Group Updated")


@login_required(login_url='login')
def party_details_tally(request,module):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Ledger')
    
    
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black','bg_color':"#B4C6E7","align":"center",'text_wrap': True})
    cell_format_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"left",'text_wrap': True})
    cell_format_center_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"center",'text_wrap': True})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    
    
    worksheet.set_column(0, 20, 20)
    worksheet.freeze_panes(1, 0)
    
    
    
    row = 2
    party_data = Party.objects.select_related('tally_group').prefetch_related('party_address','party_address__corp_state').all()    
    if request.method == "POST" and request.POST['export_type'] == "EXPORT XML":
        selected_id = request.POST['selected_fields']
        selected_id = selected_id.split(',')
        party_list = []
        # existing_parties = []
        for i in selected_id:
            party = party_data.filter(id=int(i)).first()
            
            
            tally_under = request.POST[f'party_under-{i}']
            print(tally_under)
            tally_group = LedgerCategory.objects.filter(id=int(tally_under)).first()
            party.tally_group = tally_group
            party.save()
            
            party_list.append(party)
            
        t = loader.get_template('tally/party/party_tally.xml')
        c = {'parties': party_list}
        response = HttpResponse(t.render(c), content_type="application/xml")
        response['Content-Disposition'] = 'attachment; filename=party_import.xml'
        return response
    
    if request.method == 'POST' and request.POST['export_type'] == "EXPORT EXCEL":
        worksheet.write("A1","Name",cell_format_center2)
        worksheet.write("B1","Group Name",cell_format_center2)
        worksheet.write("C1","Default credit period",cell_format_center2)
        worksheet.write("D1","Ledger - Opening Balance",cell_format_center2)
        worksheet.write("E1","Ledger Opening Balance - Dr/Cr",cell_format_center2)
        worksheet.write("F1","Address Type",cell_format_center2)
        worksheet.write("G1","Address",cell_format_center2)
        worksheet.write("H1","State",cell_format_center2)
        worksheet.write("I1","Country",cell_format_center2)
        worksheet.write("J1","Pincode",cell_format_center2)
        worksheet.write("K1","GST Registration Type",cell_format_center2)
        worksheet.write("L1","GST Registration - GSTIN/UIN",cell_format_center2)
        worksheet.write("M1","PAN/IT No.",cell_format_center2)
        # Multiple Address Entries
        worksheet.write("N1","Multiple Mailing Details - Address Type",cell_format_center2)
        worksheet.write("O1","Multiple Mailing Details - Address",cell_format_center2)
        worksheet.write("P1","Multiple Mailing Details - Country",cell_format_center2)
        worksheet.write("Q1","Multiple Mailing Details - State",cell_format_center2)
        worksheet.write("R1","Multiple Mailing Details - Place of Supply",cell_format_center2)
        worksheet.write("S1","Multiple Mailing Details - City",cell_format_center2)
        worksheet.write("T1","Multiple Mailing Details - Pincode",cell_format_center2)
        worksheet.write("U1","Multiple Mailing Details - Email",cell_format_center2)
        worksheet.write("V1","Multiple Mailing Details - PAN/Income tax no.",cell_format_center2)
        worksheet.write("W1","Multiple Mailing Details - GST Registration Type",cell_format_center2)
        worksheet.write("X1","Multiple Mailing Details - GSTIN/UIN",cell_format_center2)
        worksheet.write("Y1","Set Multiple Mailing Details",cell_format_center2)
        selected_id = request.POST['selected_fields']
        # company = request.POST['company']
        company = Logistic.objects.first()
        selected_id = selected_id.split(',')
        party_list = []
        existing_parties = []
        for i in selected_id:
            party = party_data.filter(id=int(i)).first()
            tally_under = request.POST[f'party_under-{i}']
            print(tally_under)
            tally_group = LedgerCategory.objects.filter(id=int(tally_under)).first()
            party.tally_group = tally_group
            party.save()
            
            name = f'{party.party_name}'
            if not name in existing_parties:
                existing_parties.append(name)
                worksheet.write(f"Y{row}","Y",cell_format_center2)
                worksheet.write(f"A{row}",f"{name}",cell_format_center2)
                worksheet.write(f"B{row}",party.tally_group.name,cell_format_center2)
                if party.credit_days:
                    worksheet.write(f"C{row}",f"{int(party.credit_days)} Days",cell_format_center2)
                else:
                    worksheet.write(f"C{row}",f"0",cell_format_center2)
                worksheet.write(f"D{row}","0",cell_format_center2)
                worksheet.write(f"E{row}","Dr",cell_format_center2)
                worksheet.write(f"F{row}","Primary",cell_format_center2)
               
                if party.party_address.first().corp_state:
                    worksheet.write(f"H{row}",f"{party.party_address.first().corp_state.name}",cell_format_center2)
                worksheet.write(f"I{row}",f"{party.party_address.first().corp_country}",cell_format_center2)
                worksheet.write(f"J{row}",f"{party.party_address.first().corp_zip}",cell_format_center2)
                if party.party_address.first().corp_gstin:
                    worksheet.write(f"K{row}",f"Regular",cell_format_center2)
                    worksheet.write(f"L{row}",f"{party.party_address.first().corp_gstin}",cell_format_center2)
                else:
                    worksheet.write(f"K{row}",f"Unregistered/Consumer",cell_format_center2)
                    worksheet.write(f"L{row}",f"URP",cell_format_center2)
                    
                if party.party_address.first().corp_pan:
                    worksheet.write(f"M{row}",f"{party.party_address.first().corp_pan}",cell_format_center2)
                else:
                    worksheet.write(f"L{row}",f"",cell_format_center2)
                    
                if party.party_address.first().corp_address_line1:
                    worksheet.write(f"G{row}",f"{party.party_address.first().corp_address_line1}",cell_format_center2)
                    
                if party.party_address.first().corp_address_line2:
                    row += 1
                    worksheet.write(f"G{row}",f"{party.party_address.first().corp_address_line2}",cell_format_center2)
                
                if party.party_address.first().corp_address_line3:
                    row += 1
                    worksheet.write(f"G{row}",f"{party.party_address.first().corp_address_line3}",cell_format_center2)
                    
                for address in party.party_address.all():
                    if not party.party_address.first() == address:
                        worksheet.write(f"N{row}",f"{address.branch}",cell_format_center2)
                        worksheet.write(f"P{row}",f"{address.corp_country}",cell_format_center2)
                        if party.party_address.first().corp_state:
                            worksheet.write(f"Q{row}",f"{address.corp_state.name}",cell_format_center2)
                            worksheet.write(f"R{row}",f"{address.corp_state.gst_code}",cell_format_center2)
                            
                        worksheet.write(f"S{row}",f"{address.corp_city}",cell_format_center2)
                        worksheet.write(f"T{row}",f"{address.corp_zip}",cell_format_center2)
                        worksheet.write(f"U{row}",f"{address.corp_email}",cell_format_center2)
                        
                        if address.corp_pan:
                            worksheet.write(f"V{row}",f"{address.corp_pan}",cell_format_center2)
                        else:
                            worksheet.write(f"V{row}",f"",cell_format_center2)
                            
                        if address.corp_gstin:
                            worksheet.write(f"W{row}",f"Regular",cell_format_center2)
                            worksheet.write(f"X{row}",f"{address.corp_gstin}",cell_format_center2)
                        else:
                            worksheet.write(f"W{row}",f"Unregistered/Consumer",cell_format_center2)
                            worksheet.write(f"X{row}",f"URP",cell_format_center2)
                            
                        if address.corp_address_line1:
                            worksheet.write(f"O{row}",f"{address.corp_address_line1}",cell_format_center2)
                            
                        if address.corp_address_line2:
                            row += 1
                            worksheet.write(f"O{row}",f"{address.corp_address_line2}",cell_format_center2)
                        
                        if address.corp_address_line3:
                            row += 1
                            worksheet.write(f"O{row}",f"{address.corp_address_line3}",cell_format_center2)
                            
                        row += 1
                            
                        
                row += 1
                 
        workbook.close()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = 'attachment;filename="ledger.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response

    context = {
            'parties':party_data,
            'module':module
        }
    return render(request,'tally/party/tally_parties.html',context)

def export_bh_ledger(request,bh_list):
    suffix = request.POST['suffix']
    category = request.POST['category']
    
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Ledger')
    
    
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black','bg_color':"#B4C6E7","align":"center",'text_wrap': True})
    cell_format_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"left",'text_wrap': True})
    cell_format_center_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"center",'text_wrap': True})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    
    
    worksheet.set_column(0, 20, 20)
    worksheet.freeze_panes(1, 0)
    
    worksheet.write("A1","Name",cell_format_center2)
    worksheet.write("B1","Group Name",cell_format_center2)
    worksheet.write("C1","GST Applicability",cell_format_center2)
    worksheet.write("D1","HSN/SAC Details",cell_format_center2)
    worksheet.write("E1","HSN/SAC",cell_format_center2)
    worksheet.write("F1","HSN Description",cell_format_center2)
    worksheet.write("G1","GST Rate Details",cell_format_center2)
    worksheet.write("H1","GST - Taxability Type",cell_format_center2)
    worksheet.write("I1","IGST Rate",cell_format_center2)
    worksheet.write("J1","CGST Rate",cell_format_center2)
    worksheet.write("K1","SGST/UTGST Rate",cell_format_center2)
    worksheet.write("L1","Type of Supply",cell_format_center2)
    row = 2
    
    for data in bh_list:
        name = data.billing_head
        if suffix:
            name = name + f" {suffix}"
            
        worksheet.write(f"A{row}",f"{name}",cell_format_center2)
        worksheet.write(f"B{row}",f"{category}",cell_format_center2)
        worksheet.write(f"C{row}","Applicable",cell_format_center2)
        worksheet.write(f"D{row}","Specify Details Here",cell_format_center2)
        worksheet.write(f"E{row}",f"{data.hsn_code}",cell_format_center2)
        worksheet.write(f"F{row}",f"{data.billing_head}",cell_format_center2)
        worksheet.write(f"G{row}",f"Specify Details Here",cell_format_center2)
        worksheet.write(f"H{row}",f"Taxable",cell_format_center2)
        worksheet.write(f"I{row}",f"{data.gst}",cell_format_center2)
        worksheet.write(f"J{row}",f"{data.gst//2}",cell_format_center2)
        worksheet.write(f"K{row}",f"{data.gst//2}",cell_format_center2)
        worksheet.write(f"L{row}","Services",cell_format_center2)
        
        row += 1
    
    
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="bh_ledgers.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response
    
@login_required(login_url='home:handle_login')
def bh_details_tally(request,module):
    data = BillingHead.objects.all()
    
    
    
    
    if request.method == 'POST' and request.POST['export_type'] == "EXPORT STOCK":
        selected_id = request.POST['selected_fields']
        company = request.POST['company']
        uom = request.POST['uom']
        selected_id = selected_id.split(',')
        bh_list = []
        existing_list = []
        for i in selected_id:
            entry = data.filter(id=int(i)).first()
            if not entry.billing_head in existing_list:
                existing_list.append(entry.billing_head)
                bh_list.append(entry)
        
        
        
    if request.method == 'POST' and request.POST['export_type'] == "EXPORT LEDGER WISE":
        selected_id = request.POST['selected_fields']
        selected_id = selected_id.split(',')
        bh_list = []
        existing_list = []
        for i in selected_id:
            entry = data.filter(id=int(i)).first()
            if not entry.billing_head in existing_list:
                existing_list.append(entry.billing_head)
                bh_list.append(entry)
                
        return export_bh_ledger(request,bh_list)
       
    context = {
        'data':data,
        'module':module
    }
    return render(request,'tally/billing_head/tally_bh.html',context)

@login_required(login_url='home:handle_login')
def sales_invoice_details_tally(request,module):
    context = {}
    if request.method == 'POST':
        data = InvoiceReceivable.objects.filter(old_invoice=False).filter(is_einvoiced=True).filter(company_type__tax_policy="GST").select_related('bill_to','company_type','bill_to_address','job_no').all()
        from_date = request.POST['from_date']
        company_id = request.POST['company_id']
        to_date = request.POST['to_date']
        invoices = data.filter(einvoice_date__gte=from_date).filter(einvoice_date__lte=to_date).filter(company_type__id=int(company_id)).all()
        invoice_details = InvoiceReceivableDetail.objects.filter(invoice_receivable__old_invoice=False).filter(invoice_receivable__is_einvoiced=True).filter(invoice_receivable__company_type__tax_policy="GST").filter(invoice_receivable__einvoice_date__gte=from_date).filter(invoice_receivable__einvoice_date__lte=to_date).filter(invoice_receivable__company_type__id=int(company_id)).values('billing_head','billing_head__billing_head','billing_head__sales_head').annotate(count=Count('billing_head__id'))
        
        
        context['invoices'] = invoices
        context['invoice_details'] = invoice_details
        context['company_id'] = int(company_id)
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

    context['module'] = module

    return render(request,'tally/sales_invoice/sales_invoice.html',context)

@login_required(login_url='home:handle_login')
def sales_invoice_export_tally(request,module):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Ledger')

    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black','bg_color':"#B4C6E7","align":"center",'text_wrap': True})
    cell_format_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"left",'text_wrap': True})
    cell_format_center_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"center",'text_wrap': True})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    
    worksheet.set_column(0, 20, 20)
    worksheet.freeze_panes(1, 0)
    
    worksheet.write("A1","Change Mode",cell_format_center2)
    worksheet.write("B1","Voucher Type Name",cell_format_center2)
    worksheet.write("C1","Voucher Date",cell_format_center2)
    worksheet.write("D1","Ledger Name",cell_format_center2)
    worksheet.write("E1","Ledger Amount",cell_format_center2)
    worksheet.write("F1","Ledger Amount Dr/Cr",cell_format_center2)
    worksheet.write("G1","Voucher Number",cell_format_center2)
    worksheet.write("H1","Buyer/Supplier - Bill to/from",cell_format_center2)
    worksheet.write("I1","Buyer/Supplier - Mailing Name",cell_format_center2)
    worksheet.write("J1","Buyer/Supplier - Address Type",cell_format_center2)
    worksheet.write("K1","Buyer/Supplier - Address",cell_format_center2)
    worksheet.write("L1","Buyer/Supplier - Country",cell_format_center2)
    worksheet.write("M1","Buyer/Supplier - State",cell_format_center2)
    worksheet.write("N1","Buyer/Supplier - Pincode",cell_format_center2)
    worksheet.write("O1","Buyer/Supplier - GST Registration Type",cell_format_center2)
    worksheet.write("P1","Buyer/Supplier - GSTIN/UIN",cell_format_center2)
    worksheet.write("Q1","Reference No.",cell_format_center2)
    worksheet.write("R1","Reference Date",cell_format_center2)
    worksheet.write("S1","Voucher Narration",cell_format_center2)
    worksheet.write("T1","e-Invoice - Ack No.",cell_format_center2)
    worksheet.write("U1","e-Invoice - IRN",cell_format_center2)
    worksheet.write("V1","e-Invoice - Ack Date",cell_format_center2)
    worksheet.write("W1","Cancelled",cell_format_center2)
    # Item Details
    worksheet.write("X1","Item Name",cell_format_center2)
    worksheet.write("Y1","Actual Quantity",cell_format_center2)
    worksheet.write("Z1","Billed Quantity",cell_format_center2)
    worksheet.write("AA1","Ledger Rate",cell_format_center2)
    worksheet.write("AB1","Bill Amount - Dr/Cr",cell_format_center2)
    worksheet.write("AC1","Ledger - GST Rate Details",cell_format_center2)
    worksheet.write("AD1","Ledger - GST Taxability Type",cell_format_center2)
    worksheet.write("AE1","Ledger - IGST Rate",cell_format_center2)
    worksheet.write("AF1","Ledger - CGST Rate",cell_format_center2)
    worksheet.write("AG1","Ledger - SGST/UTGST Rate",cell_format_center2)
    worksheet.write("AH1","Bill Amount",cell_format_center2)
    worksheet.write("AI1","Bill Due Dt or Credit Days",cell_format_center2)
    worksheet.write("AJ1","Cost Allocation for - Cost Centre",cell_format_center2)
    worksheet.write("AK1","Cost Allocation for - Amount",cell_format_center2)
    worksheet.write("AL1","HSN/SAC",cell_format_center2)
    
    worksheet.write("AM1","Consignee - (Ship To)",cell_format_center2)
    worksheet.write("AN1","Consignee - Mailing Name",cell_format_center2)
    worksheet.write("AO1","Consignee - Address Type",cell_format_center2)
    worksheet.write("AP1","Consignee - Address",cell_format_center2)
    worksheet.write("AQ1","Consignee - Country",cell_format_center2)
    worksheet.write("AR1","Consignee - State",cell_format_center2)
    worksheet.write("AS1","Consignee - Pincode",cell_format_center2)
    worksheet.write("AT1","Consignee - GST Registration Type",cell_format_center2)
    worksheet.write("AU1","Consignee - GSTIN/UIN",cell_format_center2)
    
    row = 2
    if request.method == 'POST':
        selected_id = request.POST['selected_fields']
        change_mode = request.POST['change_mode']
        voucher_name = request.POST['voucher_name']

        company = Logistic.objects.filter(company_gst_code="09").first()
        selected_id = selected_id.split(',')
        
        invoices = InvoiceReceivable.objects.select_related('bill_to','bill_to_address','job_no').prefetch_related('recievable_invoice_reference','bill_to__party_address').all()
        
        
        
        for i in selected_id:
            invoice = invoices.filter(id=int(i)).first()
            
            flag = 0
            for detail in invoice.recievable_invoice_reference.all():
                if detail.billing_head == None or detail.amount <= 0 or detail.total <= 0 or detail.rate <= 0:
                    flag = 1
            
            if not invoice.bill_to or not invoice.bill_to_address or not invoice.net_amount > 0 or flag == 1:
                continue
            
            worksheet.write(f"A{row}",f"{change_mode}",cell_format_center2)
            worksheet.write(f"B{row}",f"{voucher_name}",cell_format_center2)
            worksheet.write(f"C{row}",f"{invoice.einvoice_date.date().strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"D{row}",f"{invoice.bill_to.party_name}",cell_format_center2)
            worksheet.write(f"E{row}",f"{invoice.net_amount}",cell_format_center2)
            worksheet.write(f"AB{row}",f"Dr",cell_format_center2)
            worksheet.write(f"AH{row}",f"{invoice.net_amount}",cell_format_center2)
            if invoice.due_date:
                worksheet.write(f"AI{row}",f"{invoice.due_date.strftime('%d-%b-%Y')}",cell_format_center2)
            else:
                worksheet.write(f"AI{row}",f"{invoice.einvoice_date.date().strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"F{row}",f"Dr",cell_format_center2)
            worksheet.write(f"G{row}",f"{invoice.final_invoice_no}",cell_format_center2)
            worksheet.write(f"H{row}",f"{invoice.bill_to.party_name}",cell_format_center2)
            worksheet.write(f"I{row}",f"{invoice.bill_to.party_name}",cell_format_center2)
            if invoice.bill_to.party_address.first() == invoice.bill_to_address:
                worksheet.write(f"J{row}","Primary",cell_format_center2)
            else:
                worksheet.write(f"J{row}",f"{invoice.bill_to_address.branch}",cell_format_center2)
                
            # Bill To Address Details
            address_row = row
            worksheet.write(f"K{address_row}",f"{invoice.bill_to_address.corp_address_line1}",cell_format_center2)
            address_row += 1
            worksheet.write(f"K{address_row}",f"{invoice.bill_to_address.corp_address_line2}",cell_format_center2)
            address_row += 1
            worksheet.write(f"K{address_row}",f"{invoice.bill_to_address.corp_address_line3}",cell_format_center2)
            
            worksheet.write(f"L{row}",f"{invoice.bill_to_address.corp_country}",cell_format_center2)
            worksheet.write(f"M{row}",f"{invoice.bill_to_address.corp_state.name}",cell_format_center2)
            worksheet.write(f"N{row}",f"{invoice.bill_to_address.corp_zip}",cell_format_center2)
            worksheet.write(f"O{row}",f"{invoice.category}",cell_format_center2)
            worksheet.write(f"P{row}",f"{invoice.bill_to_address.corp_gstin}",cell_format_center2)
            
            # Consignee Details
            worksheet.write(f"AM{row}",f"{invoice.bill_to.party_name}",cell_format_center2)
            worksheet.write(f"AN{row}",f"{invoice.bill_to.party_name}",cell_format_center2)
            if invoice.bill_to.party_address.first() == invoice.bill_to_address:
                worksheet.write(f"AO{row}","Primary",cell_format_center2)
            else:
                worksheet.write(f"AO{row}",f"{invoice.bill_to_address.branch}",cell_format_center2)
                
            # Consignee Address Details
            address_row = row
            worksheet.write(f"AP{address_row}",f"{invoice.bill_to_address.corp_address_line1}",cell_format_center2)
            address_row += 1
            worksheet.write(f"AP{address_row}",f"{invoice.bill_to_address.corp_address_line2}",cell_format_center2)
            address_row += 1
            worksheet.write(f"AP{address_row}",f"{invoice.bill_to_address.corp_address_line3}",cell_format_center2)
            
            worksheet.write(f"AQ{row}",f"{invoice.bill_to_address.corp_country}",cell_format_center2)
            worksheet.write(f"AR{row}",f"{invoice.bill_to_address.corp_state.name}",cell_format_center2)
            worksheet.write(f"AS{row}",f"{invoice.bill_to_address.corp_zip}",cell_format_center2)
            worksheet.write(f"AT{row}",f"{invoice.category}",cell_format_center2)
            worksheet.write(f"AU{row}",f"{invoice.bill_to_address.corp_gstin}",cell_format_center2)
            # Consignee Deatils End
            
            worksheet.write(f"Q{row}",f"{invoice.final_invoice_no}",cell_format_center2)
            worksheet.write(f"R{row}",f"{invoice.einvoice_date.date().strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"S{row}",f"JOB NO. = {invoice.job_no.job_no} ,BILL No = {invoice.final_invoice_no} ,BILL DATE = {invoice.einvoice_date.date().strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"T{row}",f"{invoice.ack_no}",cell_format_center2)
            worksheet.write(f"U{row}",f"{invoice.irn_no}",cell_format_center2)
            worksheet.write(f"V{row}",f"{invoice.einvoice_date.date().strftime('%d-%b-%Y')}",cell_format_center2)
            if invoice.is_cancel:
                worksheet.write(f"W{row}","Yes",cell_format_center2)
            else:
                worksheet.write(f"W{row}","No",cell_format_center2)
            
            # worksheet.write(f"AJ{row}",f"{invoice.job_no.job_no}",cell_format_center2)
            
                
            # Item Details
            item_row =  address_row + 1
            igst = 0
            cgst = 0
            sgst = 0
            for detail in invoice.recievable_invoice_reference.all():
                
                sales_head_name = request.POST[f'billing_head_name_{detail.billing_head.id}']
                detail.billing_head.sales_head = sales_head_name
                detail.billing_head.save()
               
                worksheet.write(f"D{item_row}",f"{detail.billing_head.sales_head}",cell_format_center2)
                # worksheet.write(f"Y{item_row}",f"{detail.qty_unit}",cell_format_center2)
                # worksheet.write(f"Z{item_row}",f"{detail.qty_unit}",cell_format_center2)
                # worksheet.write(f"AA{item_row}",f"{detail.rate * detail.ex_rate}",cell_format_center2)
                worksheet.write(f"E{item_row}",f"{detail.amount}",cell_format_center2)
                worksheet.write(f"F{item_row}",f"Cr",cell_format_center2)
                worksheet.write(f"AC{item_row}","Specify Details Here",cell_format_center2)
                worksheet.write(f"AD{item_row}",f"{detail.tax_applicable}",cell_format_center2)
                if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                    worksheet.write(f"AE{item_row}",f"{detail.gst}",cell_format_center2)
                else:
                    worksheet.write(f"AF{item_row}",f"{detail.gst / 2}",cell_format_center2)
                    worksheet.write(f"AG{item_row}",f"{detail.gst / 2}",cell_format_center2)
                # worksheet.write(f"AJ{item_row}",f"{invoice.job_no}",cell_format_center2)
                # worksheet.write(f"AK{item_row}",f"{round(detail.amount,2)}",cell_format_center2)
                worksheet.write(f"AL{item_row}",f"{detail.billing_head.hsn_code}",cell_format_center2)
                    
                    
                item_row += 1
            
            gst_grouping = invoice.recievable_invoice_reference.values('gst').annotate(sum=Sum('gst_amount')) 

            if invoice.gst_amount > 0:   
                for gst in gst_grouping: 
                    igst_head_name = ""
                    cgst_head_name = ""
                    sgst_head_name = ""
                    if gst['gst'] == 5:
                        if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_5
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_5
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_5
                        
                    if gst['gst'] == 12:
                        if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_12
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_12
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_12
                        
                    if gst['gst'] == 18:
                        if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_18
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_18
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_18
                        
                    if gst['gst'] == 28:
                        if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_28
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_28
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_28
                        
                    if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                        cgst += round((gst['sum'] / 2),2)
                        sgst += round((gst['sum'] / 2),2)
                        worksheet.write(f"D{item_row}",f"{cgst_head_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{round((gst['sum'] / 2),2)}",cell_format_center2)
                        worksheet.write(f"F{item_row}",f"Cr",cell_format_center2)
                        item_row += 1
                        worksheet.write(f"D{item_row}",f"{sgst_head_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{round((gst['sum'] / 2),2)}",cell_format_center2)
                        worksheet.write(f"F{item_row}",f"Cr",cell_format_center2)
                    else:
                        igst += round((gst['sum']),2)
                        worksheet.write(f"D{item_row}",f"{igst_head_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{gst['sum']}",cell_format_center2)
                        worksheet.write(f"F{item_row}",f"Cr",cell_format_center2)
                    
                    item_row += 1
                
                if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                    rounded_calc_net_amount = cgst + sgst + invoice.gross_amount
                    if not rounded_calc_net_amount == invoice.net_amount:
                        round_off_value = round((invoice.net_amount - rounded_calc_net_amount ),2)
                        worksheet.write(f"D{item_row}",f"{invoice.company_type.round_off_ledger_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{abs(round_off_value)}",cell_format_center2)
                        if round_off_value < 0:
                            worksheet.write(f"F{item_row}",f"Dr",cell_format_center2)
                        else:
                            worksheet.write(f"F{item_row}",f"Cr",cell_format_center2)
                            
                        
                        item_row += 1
                        
                else:
                    rounded_calc_net_amount = igst + invoice.gross_amount
                    if not rounded_calc_net_amount == invoice.net_amount:
                        round_off_value = round((invoice.net_amount - rounded_calc_net_amount ),2)
                        worksheet.write(f"D{item_row}",f"{invoice.company_type.round_off_ledger_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{abs(round_off_value)}",cell_format_center2)
                        if round_off_value < 0:
                            worksheet.write(f"F{item_row}",f"Dr",cell_format_center2)
                        else:
                            worksheet.write(f"F{item_row}",f"Cr",cell_format_center2)
                            
                        
                        item_row += 1
                        
                    
                        
                
                if len(gst_grouping) > 1:
                    item_row -= 1
              
            
            
            row = item_row + 1
            
        workbook.close()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = 'attachment;filename="sales_vouchers.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response
    
    return redirect('accounting:sales_invoice_details_tally',module=module)

@login_required(login_url='home:handle_login')
def reciept_details_tally(request,module):
    context = {}
    if request.method == 'POST':
        data = RecieptVoucher.objects.select_related('party_name','party_address','company_type','to_bank').filter(voucher=None).filter(total_recieved_amount__gt=0).filter(old_voucher=False).all()
        from_date = request.POST['from_date']
        company_id = request.POST['company_id']
        to_date = request.POST['to_date']
        data = data.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).filter(company_type__id=int(company_id)).all()
        context['data'] = data
        context['company_id'] = int(company_id)
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

    context['module'] = module

    return render(request,'tally/reciept/tally_reciept.html',context)

@login_required(login_url='home:handle_login')
def reciept_export_tally(request,module):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Ledger')
    
    
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black','bg_color':"#B4C6E7","align":"center",'text_wrap': True})
    cell_format_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"left",'text_wrap': True})
    cell_format_center_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"center",'text_wrap': True})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    
    worksheet.set_column(0, 20, 20)
    worksheet.freeze_panes(1, 0)
    
    worksheet.write("A1","Voucher Number",cell_format_center2)
    worksheet.write("B1","Voucher Type Name",cell_format_center2)
    worksheet.write("C1","Voucher Date",cell_format_center2)
    worksheet.write("D1","Reference No.",cell_format_center2)
    worksheet.write("E1","Ledger Name",cell_format_center2)
    worksheet.write("F1","Ledger Amount",cell_format_center2)
    worksheet.write("G1","Ledger Amount Dr/Cr",cell_format_center2)
    worksheet.write("H1","Reference Date",cell_format_center2)
    worksheet.write("I1","Voucher Narration",cell_format_center2)
    
    worksheet.write("J1","Bill Type of Ref",cell_format_center2)
    worksheet.write("K1","Bill Name",cell_format_center2)
    worksheet.write("L1","Bill Amount - Dr/Cr",cell_format_center2)
    worksheet.write("M1","Bill Amount",cell_format_center2)
    
    worksheet.write("N1","Bank Allocations - Transaction Type",cell_format_center2)
    worksheet.write("O1","Bank Allocations - Amount",cell_format_center2)
    worksheet.write("P1","Bank Allocations - A/c No.",cell_format_center2)
    worksheet.write("Q1","Bank Allocations - Bank Name",cell_format_center2)
    worksheet.write("R1","Bank Allocations - Inst No.",cell_format_center2)
    worksheet.write("S1","Bank Allocations - Inst Date",cell_format_center2)
    
    row = 2
    if request.method == 'POST':
        selected_id = request.POST['selected_fields']
        voucher_name = request.POST['voucher_name']

        
        selected_id = selected_id.split(',')
        
        vouchers = RecieptVoucher.objects.select_related('party_name','party_address','company_type','to_bank').filter(voucher=None).filter(total_recieved_amount__gt=0).filter(old_voucher=False).all()
        
        
        
        for i in selected_id:
            invoice = vouchers.filter(id=int(i)).first()
            
            if not invoice.party_name or not invoice.party_address or not invoice.total_recieved_amount > 0 or not invoice.to_bank:
                continue
            
            voucher_narration = ""
            
            worksheet.write(f"A{row}",f"{invoice.voucher_no}",cell_format_center2)
            worksheet.write(f"B{row}",f"{voucher_name}",cell_format_center2)
            worksheet.write(f"C{row}",f"{invoice.voucher_date.strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"D{row}",f"{invoice.instrument_no}",cell_format_center2)
            
            
            worksheet.write(f"H{row}",f"{invoice.voucher_date.strftime('%d-%b-%Y')}",cell_format_center2)
            voucher_narration = ""
            for detail in invoice.rec_voucher_detail.all():
                narration = f"{detail.invoice.final_invoice_no} - {detail.received_amount}, "
                voucher_narration += narration
                
                
            if voucher_narration == "":
                voucher_narration = f"On A/C Recieved on {invoice.voucher_date.strftime('%d-%d-%Y')}"
                
            worksheet.write(f"I{row}",f"{voucher_narration}",cell_format_center2)
            
            # Cr Line
            worksheet.write(f"E{row}",f"{invoice.party_name.party_name}",cell_format_center2)
            worksheet.write(f"F{row}",f"{invoice.total_recieved_amount}",cell_format_center2)
            worksheet.write(f"G{row}","Cr",cell_format_center2)
            
            
            if invoice.rec_voucher_detail.count() == 0:
                row += 1
                worksheet.write(f"J{row}","On Account",cell_format_center2)
                worksheet.write(f"L{row}","Cr",cell_format_center2)
                worksheet.write(f"M{row}",f"{invoice.total_recieved_amount}",cell_format_center2)
            else:
                for detail in invoice.rec_voucher_detail.all():
                    narration = f"{detail.invoice.final_invoice_no} - {detail.received_amount}, "
                    voucher_narration += narration
                    
                    row += 1
                    worksheet.write(f"J{row}","Agst Ref",cell_format_center2)
                    worksheet.write(f"K{row}",f"{detail.invoice.final_invoice_no}",cell_format_center2)
                    worksheet.write(f"L{row}",f"Cr",cell_format_center2)
                    worksheet.write(f"M{row}",f"{detail.received_amount}",cell_format_center2)
                
            
            
            # Dr Line
            row += 1
            worksheet.write(f"E{row}",f"{invoice.to_bank.bank_name} ({invoice.to_bank.account_no})",cell_format_center2)
            worksheet.write(f"F{row}",f"{invoice.total_recieved_amount}",cell_format_center2)
            worksheet.write(f"G{row}","Dr",cell_format_center2)
            row += 1
            worksheet.write(f"N{row}","Others",cell_format_center2)
            worksheet.write(f"O{row}",f"{invoice.total_recieved_amount}",cell_format_center2)
            worksheet.write(f"P{row}",f"{invoice.to_bank.account_no}",cell_format_center2)
            worksheet.write(f"Q{row}",f"{invoice.to_bank.bank_name}",cell_format_center2)
            worksheet.write(f"R{row}",f"{invoice.instrument_no}",cell_format_center2)
            worksheet.write(f"S{row}",f"{invoice.received_amount_date.strftime('%d-%b-%Y')}",cell_format_center2)
            
            
            
            
    
            
            row += 1
            
        workbook.close()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = 'attachment;filename="reciept_vouchers.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response
    
    return redirect('accounting:reciept_details_tally',module=module)

@login_required(login_url='home:handle_login')
def purchase_invoice_details_tally(request,module):
    context = {}
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        company_id = request.POST['company_id']
        data = InvoicePayable.objects.filter(is_single=True).filter(old_invoice=False).filter(company_type__id=int(company_id)).filter(company_type__tax_policy="GST").filter(is_deleted=False).select_related('bill_from','company_type','bill_from_address')
        invoices = data.filter(date_of_invoice__gte=from_date).filter(date_of_invoice__lte=to_date).all()
        
        invoice_details = InvoicePayableDetail.objects.filter(invoice_payable__is_single=True).filter(invoice_payable__old_invoice=False).filter(invoice_payable__company_type__tax_policy="GST").filter(invoice_payable__is_deleted=False).filter(invoice_payable__date_of_invoice__gte=from_date).filter(invoice_payable__date_of_invoice__lte=to_date).filter(invoice_payable__company_type__id=int(company_id)).values('billing_head','billing_head__billing_head','billing_head__purchase_head').annotate(count=Count('billing_head__id'))
        print(invoice_details)
        context['invoices'] = invoices
        context['invoice_details'] = invoice_details
        context['company_id']= int(company_id)
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

    context['module'] = module

    return render(request,'tally/purchase_invoice/purchase_invoice.html',context)

@login_required(login_url='home:handle_login')
def purchase_invoice_export_tally(request,module):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Ledger')
    
    
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black','bg_color':"#B4C6E7","align":"center",'text_wrap': True})
    cell_format_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"left",'text_wrap': True})
    cell_format_center_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"center",'text_wrap': True})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    
    worksheet.set_column(0, 20, 20)
    worksheet.freeze_panes(1, 0)
    
    worksheet.write("A1","Change Mode",cell_format_center2)
    worksheet.write("B1","Voucher Type Name",cell_format_center2)
    worksheet.write("C1","Voucher Date",cell_format_center2)
    worksheet.write("D1","Ledger Name",cell_format_center2)
    worksheet.write("E1","Ledger Amount",cell_format_center2)
    worksheet.write("F1","Ledger Amount Dr/Cr",cell_format_center2)
    worksheet.write("G1","Voucher Number",cell_format_center2)
    worksheet.write("H1","Buyer/Supplier - Bill to/from",cell_format_center2)
    worksheet.write("I1","Buyer/Supplier - Mailing Name",cell_format_center2)
    worksheet.write("J1","Buyer/Supplier - Address Type",cell_format_center2)
    worksheet.write("K1","Buyer/Supplier - Address",cell_format_center2)
    worksheet.write("L1","Buyer/Supplier - Country",cell_format_center2)
    worksheet.write("M1","Buyer/Supplier - State",cell_format_center2)
    worksheet.write("N1","Buyer/Supplier - Pincode",cell_format_center2)
    worksheet.write("O1","Buyer/Supplier - GST Registration Type",cell_format_center2)
    worksheet.write("P1","Buyer/Supplier - GSTIN/UIN",cell_format_center2)
    worksheet.write("Q1","Reference No.",cell_format_center2)
    worksheet.write("R1","Reference Date",cell_format_center2)
    worksheet.write("S1","Voucher Narration",cell_format_center2)
    worksheet.write("T1","e-Invoice - Ack No.",cell_format_center2)
    worksheet.write("U1","e-Invoice - IRN",cell_format_center2)
    worksheet.write("V1","e-Invoice - Ack Date",cell_format_center2)
    worksheet.write("W1","Cancelled",cell_format_center2)
    # Item Details
    worksheet.write("X1","Item Name",cell_format_center2)
    worksheet.write("Y1","Actual Quantity",cell_format_center2)
    worksheet.write("Z1","Billed Quantity",cell_format_center2)
    worksheet.write("AA1","Ledger Rate",cell_format_center2)
    # worksheet.write("AB1","Ledger Amount",cell_format_center2)
    worksheet.write("AC1","Ledger - GST Rate Details",cell_format_center2)
    worksheet.write("AD1","Ledger - GST Taxability Type",cell_format_center2)
    worksheet.write("AE1","Ledger - IGST Rate",cell_format_center2)
    worksheet.write("AF1","Ledger - CGST Rate",cell_format_center2)
    worksheet.write("AG1","Ledger - SGST/UTGST Rate",cell_format_center2)
    row = 2
    if request.method == 'POST':
        selected_id = request.POST['selected_fields']
        change_mode = request.POST['change_mode']
        voucher_name = request.POST['voucher_name']

        selected_id = selected_id.split(',')
        
        invoices = InvoicePayable.objects.filter(is_single=True).select_related('bill_from','bill_from_address','job_no').prefetch_related('payable_invoice_reference','bill_from__party_address').all()
        for i in selected_id:
            invoice = invoices.filter(id=int(i)).first()
            flag = 0
            for detail in invoice.payable_invoice_reference.all():
                if detail.billing_head == None or detail.amount <= 0 or detail.total <= 0 or detail.rate <= 0:
                    flag = 1
            
            if not invoice.bill_from or not invoice.bill_from_address or not invoice.net_amount > 0 or flag == 1:
                continue
            
            worksheet.write(f"A{row}",f"{change_mode}",cell_format_center2)
            worksheet.write(f"B{row}",f"{voucher_name}",cell_format_center2)
            worksheet.write(f"C{row}",f"{invoice.date_of_invoice.strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"D{row}",f"{invoice.bill_from.party_name}",cell_format_center2)
            worksheet.write(f"E{row}",f"{invoice.net_amount}",cell_format_center2)
            worksheet.write(f"F{row}",f"Cr",cell_format_center2)
            worksheet.write(f"G{row}",f"{invoice.purchase_invoice_no}",cell_format_center2)
            worksheet.write(f"H{row}",f"{invoice.bill_from.party_name}",cell_format_center2)
            worksheet.write(f"I{row}",f"{invoice.bill_from.party_name}",cell_format_center2)
            if invoice.bill_from.party_address.first() == invoice.bill_from_address:
                worksheet.write(f"J{row}","Primary",cell_format_center2)
            else:
                worksheet.write(f"J{row}",f"{invoice.bill_from_address.branch}",cell_format_center2)
                
            # Bill To Address Details
            address_row = row
            worksheet.write(f"K{address_row}",f"{invoice.bill_from_address.corp_address_line1}",cell_format_center2)
            address_row += 1
            worksheet.write(f"K{address_row}",f"{invoice.bill_from_address.corp_address_line2}",cell_format_center2)
            address_row += 1
            worksheet.write(f"K{address_row}",f"{invoice.bill_from_address.corp_address_line3}",cell_format_center2)
            
            worksheet.write(f"L{row}",f"{invoice.bill_from_address.corp_country}",cell_format_center2)
            worksheet.write(f"M{row}",f"{invoice.bill_from_address.corp_state.name}",cell_format_center2)
            worksheet.write(f"N{row}",f"{invoice.bill_from_address.corp_zip}",cell_format_center2)
            # worksheet.write(f"O{row}",f"{invoice.category}",cell_format_center2)
            worksheet.write(f"P{row}",f"{invoice.bill_from_address.corp_gstin}",cell_format_center2)
            worksheet.write(f"Q{row}",f"{invoice.purchase_invoice_no}",cell_format_center2)
            worksheet.write(f"R{row}",f"{invoice.date_of_invoice.strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"S{row}",f"JOB NO. = {invoice.job_no.job_no} ,BILL No = {invoice.purchase_invoice_no} ,BILL DATE = {invoice.date_of_invoice.strftime('%d-%b-%Y')}",cell_format_center2)
            
            if invoice.is_deleted:
                worksheet.write(f"W{row}","Yes",cell_format_center2)
            else:
                worksheet.write(f"W{row}","No",cell_format_center2)
                
            # Item Details
            item_row = address_row + 1
            igst = 0
            cgst = 0
            sgst = 0
            gross_amount = 0
          
            for detail in invoice.payable_invoice_reference.all():
                if not detail.billing_head:
                    print(invoice.purchase_invoice_no)
                    
                try:
                    purchase_head_name = request.POST[f'billing_head_name_{detail.billing_head.id}']
                    detail.billing_head.purchase_head = purchase_head_name
                    detail.billing_head.save()
                except:
                    pass
                
                worksheet.write(f"D{item_row}",f"{detail.billing_head.purchase_head}",cell_format_center2)
                gross_amount += (round((detail.ex_rate * detail.qty_unit * detail.rate),2))
                worksheet.write(f"E{item_row}",f"{round((detail.ex_rate * detail.qty_unit * detail.rate),2)}",cell_format_center2)
                worksheet.write(f"F{item_row}",f"Dr",cell_format_center2)
                worksheet.write(f"AC{item_row}","Specify Details Here",cell_format_center2)
                if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                    worksheet.write(f"AE{item_row}",f"{detail.gst}",cell_format_center2)
                    cgst +=  detail.gst_amount / 2 
                    sgst += detail.gst_amount / 2
               
                else:
                    worksheet.write(f"AF{item_row}",f"{detail.gst / 2}",cell_format_center2)
                    worksheet.write(f"AG{item_row}",f"{detail.gst / 2}",cell_format_center2)
                    igst += detail.gst_amount
                    
                item_row += 1
                
            
            
            gst_grouping = invoice.payable_invoice_reference.values('gst').annotate(sum=Sum('gst_amount')) 
               
               
            
            if invoice.gst_amount > 0:   
                for gst in gst_grouping:
                    if gst['gst'] == 0:
                        continue
                    
                    igst_head_name = ""
                    cgst_head_name = ""
                    sgst_head_name = ""
                    if gst['gst'] == 5:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_5
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_5
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_5
                        
                    if gst['gst'] == 12:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_12
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_12
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_12
                        
                    if gst['gst'] == 18:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_12
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_12
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_12
                        
                    if gst['gst'] == 28:
                        if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                            cgst_head_name = invoice.company_type.cgst_out_ledger_name_28
                            sgst_head_name = invoice.company_type.sgst_out_ledger_name_28
                        else:
                            igst_head_name = invoice.company_type.igst_out_ledger_name_28
                        
                    if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                        cgst += round((gst['sum'] / 2),2)
                        sgst += round((gst['sum'] / 2),2)
                        worksheet.write(f"D{item_row}",f"{cgst_head_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{round((gst['sum'] / 2),2)}",cell_format_center2)
                        worksheet.write(f"F{item_row}",f"Dr",cell_format_center2)
                        item_row += 1
                        worksheet.write(f"D{item_row}",f"{sgst_head_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{round((gst['sum'] / 2),2)}",cell_format_center2)
                        worksheet.write(f"F{item_row}",f"Dr",cell_format_center2)
                    else:
                        worksheet.write(f"D{item_row}",f"{igst_head_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{gst['sum']}",cell_format_center2)
                        worksheet.write(f"F{item_row}",f"Dr",cell_format_center2)
                    
                    item_row += 1
                
                if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code:
                    rounded_calc_net_amount = cgst + sgst + gross_amount
                    if not rounded_calc_net_amount == invoice.net_amount:
                        round_off_value = round((invoice.net_amount - rounded_calc_net_amount ),2)
                        worksheet.write(f"D{item_row}",f"{invoice.company_type.round_off_ledger_name}",cell_format_center2)
                        worksheet.write(f"E{item_row}",f"{abs(round_off_value)}",cell_format_center2)
                        if round_off_value < 0:
                            worksheet.write(f"F{item_row}",f"Cr",cell_format_center2)
                        else:
                            worksheet.write(f"F{item_row}",f"Dr",cell_format_center2)
                        item_row += 1
                        
                
                if len(gst_grouping) > 1:
                    item_row -= 1
              
            
          
            row = item_row + 1
            
        workbook.close()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = 'attachment;filename="purchase_vouchers.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response
    
    return redirect('accounting:purchase_invoice_details_tally',module=module)

@login_required(login_url='home:handle_login')
def payment_details_tally(request,module):
    context = {}
    if request.method == 'POST':
        data = PaymentVoucher.objects.select_related('party_name','party_address','company_type','from_bank','vendor').filter(voucher=None).filter(total_paid_amount__gt=0).filter(old_voucher=False).all()
        from_date = request.POST['from_date']
        company_id = request.POST['company_id']
        to_date = request.POST['to_date']
        data = data.filter(voucher_date__gte=from_date).filter(voucher_date__lte=to_date).filter(company_type__id=int(company_id)).all()
        context['data'] = data
        context['company_id'] = int(company_id)
        context['from_date']= datetime.strptime(from_date,"%Y-%m-%d")
        context['to_date']= datetime.strptime(to_date,"%Y-%m-%d")

    context['module'] = module

    return render(request,'tally/payment/tally_payment.html',context)

@login_required(login_url='home:handle_login')
def payment_export_tally(request,module):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='Ledger')
    
    
    cell_format = workbook.add_format({'bold': True, 'font_color': 'white','border':1,'bg_color':"#0069B4",'border_color':"black","align":"right"})
    cell_format_center = workbook.add_format({'bold': True, 'border':1,'font_color': 'white','bg_color':"#0069B4",'border_color':"black","align":"center"})
    cell_format_center2 = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black','bg_color':"#B4C6E7","align":"center",'text_wrap': True})
    cell_format_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"left",'text_wrap': True})
    cell_format_center_wc = workbook.add_format({'border':1,'border_color':"black",'font_color': 'black',"align":"center",'text_wrap': True})
    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#F8CBAD","align":"center"})
    
    worksheet.set_column(0, 20, 20)
    worksheet.freeze_panes(1, 0)
    
    worksheet.write("A1","Voucher Number",cell_format_center2)
    worksheet.write("B1","Voucher Type Name",cell_format_center2)
    worksheet.write("C1","Voucher Date",cell_format_center2)
    worksheet.write("D1","Reference No.",cell_format_center2)
    worksheet.write("E1","Ledger Name",cell_format_center2)
    worksheet.write("F1","Ledger Amount",cell_format_center2)
    worksheet.write("G1","Ledger Amount Dr/Cr",cell_format_center2)
    worksheet.write("H1","Reference Date",cell_format_center2)
    worksheet.write("I1","Voucher Narration",cell_format_center2)
    
    worksheet.write("J1","Bill Type of Ref",cell_format_center2)
    worksheet.write("K1","Bill Name",cell_format_center2)
    worksheet.write("L1","Bill Amount - Dr/Cr",cell_format_center2)
    worksheet.write("M1","Bill Amount",cell_format_center2)
    
    worksheet.write("N1","Bank Allocations - Transaction Type",cell_format_center2)
    worksheet.write("O1","Bank Allocations - Amount",cell_format_center2)
    worksheet.write("P1","Bank Allocations - A/c No.",cell_format_center2)
    worksheet.write("Q1","Bank Allocations - Bank Name",cell_format_center2)
    worksheet.write("R1","Bank Allocations - Inst No.",cell_format_center2)
    worksheet.write("S1","Bank Allocations - Inst Date",cell_format_center2)
    
    row = 2
    if request.method == 'POST':
        selected_id = request.POST['selected_fields']
        voucher_name = request.POST['voucher_name']

        
        selected_id = selected_id.split(',')
        
        vouchers = PaymentVoucher.objects.select_related('party_name','party_address','company_type','from_bank').filter(voucher=None).filter(total_paid_amount__gt=0).filter(old_voucher=False).prefetch_related('pay_voucher_detail','pay_voucher_detail__invoice','pay_voucher_detail__expense').all()
        
        
        
        for i in selected_id:
            invoice = vouchers.filter(id=int(i)).first()
            
            if not invoice.party_name or not invoice.party_address or not invoice.total_paid_amount > 0 or not invoice.from_bank:
                continue
            
            voucher_narration = ""
            
            worksheet.write(f"A{row}",f"{invoice.voucher_no}",cell_format_center2)
            worksheet.write(f"B{row}",f"{voucher_name}",cell_format_center2)
            worksheet.write(f"C{row}",f"{invoice.voucher_date.strftime('%d-%b-%Y')}",cell_format_center2)
            worksheet.write(f"D{row}",f"{invoice.instrument_no}",cell_format_center2)
            
            
            worksheet.write(f"H{row}",f"{invoice.voucher_date.strftime('%d-%b-%Y')}",cell_format_center2)
            voucher_narration = ""
            for detail in invoice.pay_voucher_detail.all():
                narration = f"{detail.invoice.purchase_invoice_no} - {detail.paid_amount}, "
                voucher_narration += narration
                
            if invoice.payment_voucer_advance:
                for advance in invoice.payment_voucer_advance.all():
                    for detail in advance.pay_voucher_detail.all():
                        narration = f"{detail.invoice.purchase_invoice_no} - {detail.paid_amount}, "
                        voucher_narration += narration
                        
                
            if voucher_narration == "":
                voucher_narration = f"On A/C Paid on {invoice.voucher_date.strftime('%d-%d-%Y')}"
                
            worksheet.write(f"I{row}",f"{voucher_narration}",cell_format_center2)
            
            # Dr Line
            worksheet.write(f"E{row}",f"{invoice.party_name.party_name}",cell_format_center2)
            worksheet.write(f"F{row}",f"{invoice.total_paid_amount}",cell_format_center2)
            worksheet.write(f"G{row}","Dr",cell_format_center2)
            
            
            if invoice.pay_voucher_detail.count() == 0 and not invoice.payment_voucer_advance:
                # row += 1
                worksheet.write(f"J{row}","On Account",cell_format_center2)
                worksheet.write(f"L{row}","Dr",cell_format_center2)
                worksheet.write(f"M{row}",f"{invoice.total_paid_amount}",cell_format_center2)
            else:
                for detail in invoice.pay_voucher_detail.all():
                    row += 1
                    worksheet.write(f"J{row}","Agst Ref",cell_format_center2)
                    worksheet.write(f"K{row}",f"{detail.invoice.purchase_invoice_no}",cell_format_center2)
                    worksheet.write(f"L{row}",f"Dr",cell_format_center2)
                    worksheet.write(f"M{row}",f"{detail.paid_amount}",cell_format_center2)
                
                if invoice.payment_voucer_advance:
                    for advance in invoice.payment_voucer_advance.all():
                        for detail in advance.pay_voucher_detail.all():
                            row += 1
                            worksheet.write(f"J{row}","Agst Ref",cell_format_center2)
                            worksheet.write(f"K{row}",f"{detail.invoice.purchase_invoice_no}",cell_format_center2)
                            worksheet.write(f"L{row}",f"Dr",cell_format_center2)
                            worksheet.write(f"M{row}",f"{detail.paid_amount}",cell_format_center2)
                
            
            
            # Cr Line
            row += 1
            worksheet.write(f"E{row}",f"{invoice.from_bank.bank_name} ({invoice.from_bank.account_no})",cell_format_center2)
            worksheet.write(f"F{row}",f"{invoice.total_paid_amount}",cell_format_center2)
            worksheet.write(f"G{row}","Cr",cell_format_center2)
            row += 1
            worksheet.write(f"N{row}","Others",cell_format_center2)
            worksheet.write(f"O{row}",f"{invoice.total_paid_amount}",cell_format_center2)
            worksheet.write(f"P{row}",f"{invoice.from_bank.account_no}",cell_format_center2)
            worksheet.write(f"Q{row}",f"{invoice.from_bank.bank_name}",cell_format_center2)
            worksheet.write(f"R{row}",f"{invoice.instrument_no}",cell_format_center2)
            worksheet.write(f"S{row}",f"{invoice.voucher_date.strftime('%d-%b-%Y')}",cell_format_center2)

            row += 1
            
        workbook.close()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = 'attachment;filename="payment_vouchers.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response
    
    return redirect('accounting:payment_details_tally',module=module)


