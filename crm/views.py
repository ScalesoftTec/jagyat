from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from masters.models import BillingHead,currency
from dashboard.models import Logistic
from masters.views import check_permissions
from accounting.utils import generate_pdf
from json import dumps
from datetime import date, datetime
from django.db.models import Count
from crm.models import Inquiry,Lead,InquiryDetail,Leads_Details,Event,sales_person_party
from crm.forms import InquiryForm,LeadForm,EventForm,sales_person_party_Form
import calendar
from django.template.loader import get_template
import os

from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.contrib.sites.models import Site
import num2words
from django.http import HttpResponse

@login_required(login_url='home:handle_login')
def index(request,module):
    context = {}
    check_permissions(request,module)
    events = Event.objects.select_related('user','company_type','assigned_by','customer').filter(is_deleted=False).all()
    if not request.user.is_staff:
        events = events.filter(user=request.user).all()
        
    current_events = []
    for i in events:
        if i.start.date() == date.today():
            current_events.append(i)

    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    context = {
        'events':current_events,
        'greeting':greeting,
        'module':module,
        
    }
   
    return render(request,'crm_index.html',context)

# Event
    
@login_required(login_url='home:handle_login')
def create_event(request,module):
    user=request.user
    context ={}
    
    check_permissions(request,module)
  
    form = EventForm(user ,request.POST or None )
    if form.is_valid():
        form.instance.user = request.user
        form.instance.created_by = request.user
        form.instance.assigned_by = user
        
        if not form.instance.user:
            form.instance.user = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Event Created.")
        return redirect('crm:create_event',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'event/event_create.html',context)


@login_required(login_url='home:handle_login')
def event_details(request,module):
    context ={}
    check_permissions(request,module)
    if request.user.is_staff:
        events = Event.objects.select_related('user','company_type','assigned_by').filter(is_deleted=False).all()
    else:
        events = Event.objects.select_related('user','company_type','assigned_by').filter(user=request.user,is_deleted=False).all()
    context['events']= events
    context['module']= module
    return render(request,'event/event_details.html',context)


@login_required(login_url='home:handle_login')
def event_update(request,module,id):
    context ={}
    check_permissions(request,module)
    user=request.user
    
    obj = get_object_or_404(Event, id = id)
    
    
    if  obj.start.date() < date.today() and not request.user.is_staff:
        messages.add_message(request, messages.SUCCESS, f"Fail, Previous date meeting cannot be edited.")
        return redirect('crm:event_details',module=module)
    form = EventForm(user,request.POST or None, instance = obj)
    created_by = obj.created_by
    assigned_by = obj.assigned_by
   
    company_type=obj.company_type
   

    user = obj.user
    start = obj.start
    end = obj.end
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        form.instance.assigned_by = assigned_by
        form.instance.user = user
        form.instance.start = start
        form.instance.end = end
       
        form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('crm:event_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'event/event_create.html',context)


@login_required(login_url='home:handle_login')
def event_delete(request,module,id):
    check_permissions(request,module)
    event = Event.objects.filter(id=int(id)).first()
    event.is_deleted  = True
    event.save()
    return redirect('crm:event_details',module=module)



# sales Party
@login_required(login_url='home:handle_login')
def create_sales_party(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = sales_person_party_Form(request.POST or None)
    if form.is_valid():
        form.instance.user = request.user
        form.instance.created_by = request.user
        form.instance.sales_person = request.user
        
        if not form.instance.user:
            form.instance.user = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Event Created.")
        return redirect('crm:create_sales_party',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'sales_party/create_sales_party.html',context)



@login_required(login_url='home:handle_login')
def sales_party_details(request,module):
    context ={}
    check_permissions(request,module)
    user=request.user
    if request.user.is_staff:
        events=sales_person_party.objects.all()
    else:
        events = sales_person_party.objects.filter(sales_person=user).select_related('states').all()
    # print('e---------',events)
    context['events']= events
    context['module']= module
    return render(request,'sales_party/sales_party_details.html',context)


@login_required(login_url='home:handle_login')
def sales_party_update(request,module,id):
    context ={}
    check_permissions(request,module)
    
    obj = get_object_or_404(sales_person_party, id = id)
    form = sales_person_party_Form(request.POST or None, instance = obj)
    created_by = obj.created_by
    user = obj.sales_person
   
   
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        form.instance.sales_person = user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('crm:create_sales_party',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'sales_party/create_sales_party.html',context)


@login_required(login_url='home:handle_login')
def sales_party_delete(request,module,id):
    check_permissions(request,module)
    event = sales_person_party.objects.filter(id=int(id)).first()
    event.delete()
    return redirect('crm:sales_party_details',module=module)




# Inquiry
@login_required(login_url='handle_login')
def create_inquiry(request,module,extra_module):
    context ={}
    
    check_permissions(request,module)
  
    form = InquiryForm(request.user,request.POST or None)
   
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()
        
        total_heads = int(request.POST['invoice-heads-total'])
        for i in range(1,total_heads+1):
            isActive = request.POST[f'isActive_{i}']
            if isActive == '1':
                billing_head = BillingHead.objects.filter(id=int(request.POST[f'billing_head_{i}'])).first() 
                currency_obj = currency.objects.filter(id=int(request.POST[f'currency_{i}'])).first() 
                ex_rate = request.POST[f'ex_rate_{i}']
                rate = request.POST[f'rate_{i}']
                rate_rec = request.POST[f'rate_rec_{i}']
                profit = request.POST[f'profit_{i}']
                qty = request.POST[f'qty_{i}']
                gst = request.POST[f'gst_{i}']
                amount = request.POST[f'amount_{i}']
                total = request.POST[f'total_{i}']
                gst_amount = request.POST[f'inv_gst_amount_{i}']
                
                inquiry = Inquiry.objects.filter(id = int(form.instance.id)).first()
                
                new_inquiry_heads = InquiryDetail(
                    inquiry = inquiry,
                    billing_head = billing_head,
                    currency = currency_obj,
                    ex_rate = ex_rate,
                    rate = rate,
                    profit = profit,
                    rate_rec = rate_rec,
                    qty_unit = qty,
                    amount = amount,
                    gst = gst,
                    total = total,
                    gst_amount=gst_amount
                )
                new_inquiry_heads.save()
        
        
        messages.add_message(request, messages.SUCCESS, f"Success, New Inquiry Created.")
        return redirect('crm:create_inquiry',module=module,extra_module=extra_module)
    
    
   
    billing_heads = BillingHead.objects.all()
    currencies = currency.objects.all()
    
    current_year = datetime.now().year
    current_financial_date = date(current_year, 4, 1)

    jobs_current_len_of_companies = Inquiry.objects.filter(created_at__gte = current_financial_date).values('company_type').annotate(count=Count('company_type'))
    current_len_of_companies = []
    
    total_companies = Logistic.objects.all()
    

    if len(jobs_current_len_of_companies) == len(total_companies):
        for i in jobs_current_len_of_companies:
            cuurent_company = Logistic.objects.get(id=i['company_type'])
            current_len_of_companies.append({'company_type':i['company_type'],'count':i['count'],'cn_starting':cuurent_company.pre_inquiry})
            
    if len(jobs_current_len_of_companies) < len(total_companies):
        for i in jobs_current_len_of_companies:
            cuurent_company = Logistic.objects.get(id=i['company_type'])
            current_len_of_companies.append({'company_type':i['company_type'],'count':i['count'],'cn_starting':cuurent_company.pre_inquiry})
            
        
      
        for j in total_companies:
            check_already_exits = any(x['company_type'] == j.id for x in current_len_of_companies)
            if not check_already_exits:
                current_len_of_companies.append({'company_type':j.id,'count':0,'cn_starting':j.pre_inquiry})
        

    if not jobs_current_len_of_companies:
        for j in total_companies:
            current_len_of_companies.append({'company_type':j.id,'count':0,'cn_starting':j.pre_inquiry})
 
    context['form']= form
    context['module']= module
    context['extra_module'] = extra_module
    context['billing_heads'] = billing_heads
    context['currencies'] = currencies
    context['invoice_length'] = len(Inquiry.objects.all())
    context['jobs_current_len_of_companies']= dumps(current_len_of_companies)
   
    return render(request,'inquiry/create_inquiry.html',context)

@login_required(login_url='handle_login')
def inquiry_update(request,module,id,extra_module):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Inquiry, id = id)

    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('crm:inquiry_details',module=module,extra_module=extra_module)
    
    invoice_heads = InquiryDetail.objects.filter(inquiry=obj).all()
    
    form = InquiryForm(request.user,request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        
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
                rate_rec = request.POST[f'rate_rec_{i}']
                profit = request.POST[f'profit_{i}']
                inquiry = Inquiry.objects.filter(id = int(form.instance.id)).first()
                
                new_invoice_heads = InquiryDetail(
                    inquiry = inquiry,
                    billing_head = billing_head,
                    currency = currency_obj,
                    ex_rate = ex_rate,
                    rate = rate,
                    qty_unit = qty,
                    rate_rec = rate_rec,
                    profit = profit,
                    amount = amount,
                    gst = gst,
                    total = total,
                    gst_amount=gst_amount
                )
                new_invoice_heads.save()
        
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('crm:inquiry_details',module=module,extra_module=extra_module)
          
    billing_heads = BillingHead.objects.all()
    currencies = currency.objects.all()
    
    context['form']= form
    context['extra_module'] = extra_module
    context['module']= module
    context['update']= True
    context['billing_heads'] = billing_heads
    context['currencies'] = currencies
    context['invoice_heads']= invoice_heads
    context['total_invoice_heads']= len(invoice_heads)
    return render(request,'inquiry/create_inquiry.html',context)

@login_required(login_url='handle_login')
def inquiry_details(request,module,extra_module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        inquiries = Inquiry.objects.filter(company_type=company).all()
    else:
        inquiries = Inquiry.objects.all()
    
    if not request.user.user_account.also_handle_other_work:
        inquiries = inquiries.filter(created_by=request.user).all()
    
    
    current_month = datetime.now().month
    
    if request.method == 'POST':
        choose_option = request.POST['choose_option']
        if choose_option == 'date':
            start_date = request.POST['from_date']
            end_date = request.POST['to_date']

        else:
            current_month = int(request.POST['months'])
            current_year = datetime.now().year
            _,end_day = calendar.monthrange(current_year, current_month)
            start_date = date(current_year,current_month,1)
            end_date = date(current_year,current_month,end_day)
        
    
        if not request.user.user_account.see_global_data:
            inquiries = Inquiry.objects.filter(company_type=company).filter(date_of_inquiry__gte=start_date).filter(date_of_inquiry__lte=end_date).all()
        else:
            inquiries = Inquiry.objects.filter(date_of_inquiry__gte=start_date).filter(date_of_inquiry__lte=end_date).all()
            
        
          
    context['inquiries']= inquiries
    context['current_month']= current_month
    context['extra_module']= extra_module
    context['module']= module
    return render(request,'inquiry/inquiry_details.html',context)

@login_required(login_url='handle_login')
def inquiry_delete(request,module,id,extra_module):
    check_permissions(request,module)
    inquiry = Inquiry.objects.filter(id=int(id)).first()
    inquiry.delete()
    return redirect('crm:inquiry_details',module=module,extra_module=extra_module)

# Leads
@login_required(login_url='home:handle_login')
def create_lead(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = LeadForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()

        total_heads=int(request.POST['leads-heads-total'])
       
        for i in range(1,total_heads+1):
            isActive=request.POST[f"isActive_{i}"]
            if isActive =='1':
                c_name=request.POST[f"company_name-{i}"]
                person=request.POST[f"contact_person-{i}"]
                email=request.POST[f"contact_email-{i}"]
                phone=request.POST[f"phone_no-{i}"]
                location=request.POST[f"location-{i}"]
                remarks=request.POST[f"remarks-{i}"]
                lead_d=Lead.objects.filter(id=int(form.instance.id)).first()
                leads_head_dt=Leads_Details(
                    lead=lead_d,
                    company_name=c_name,
                    contact_person=person,
                    contact_email=email,
                    phone=phone,
                    location=location,
                    remarks=remarks


                )
                leads_head_dt.save()
          

        messages.add_message(request, messages.SUCCESS, f"Success, New Lead Created.")
        return redirect('crm:create_lead',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'lead/lead_create.html',context)

@login_required(login_url='home:handle_login')
def lead_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        leads = Lead.objects.filter(company_type=company).all()
    else:
        leads = Lead.objects.all()
    
    if not request.user.user_account.also_handle_other_work:
        leads = leads.filter(created_by=request.user).all()
    
    context['leads']= leads
    context['module']= module
    return render(request,'lead/lead_details.html',context)

@login_required(login_url='home:handle_login')
def lead_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Lead, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('crm:lead_details',module=module)
    
    leads_heads=Leads_Details.objects.filter(lead=obj).all()
    print('l-----',leads_heads)
    
    form = LeadForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        leads_heads.delete()

        total_heads=int(request.POST['leads-heads-total'])
        print('----',total_heads)
       
        for i in range(1,total_heads+1):
            isActive=request.POST[f"isActive_{i}"]
            if isActive =='1':
                c_name=request.POST[f"company_name-{i}"]
                person=request.POST[f"contact_person-{i}"]
                email=request.POST[f"contact_email-{i}"]
                phone=request.POST[f"phone_no-{i}"]
                location=request.POST[f"location-{i}"]
                remarks=request.POST[f"remarks-{i}"]
                lead_d=Lead.objects.filter(id=int(form.instance.id)).first()
                new_leads_head_dt=Leads_Details(
                    lead=lead_d,
                    company_name=c_name,
                    contact_person=person,
                    contact_email=email,
                    phone=phone,
                    location=location,
                    remarks=remarks


                )
                new_leads_head_dt.save()


        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('crm:lead_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    context['leads_heads']= leads_heads
    context['total_leads_heads']= len(leads_heads)
    
    return render(request,'lead/lead_create.html',context)

@login_required(login_url='home:handle_login')
def lead_delete(request,module,id):
    check_permissions(request,module)
    lead = Lead.objects.filter(id=int(id)).first()
    lead.delete()
    return redirect('crm:lead_details',module=module)


def inquiry_pdf(request,id):
    template_path = 'inquiry/pdf.html'
    invoice = Inquiry.objects.filter(id=int(id)).first()
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
        if  invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code:
            is_local = True
    except:
        pass
        
    for i in invoice.inquiry_reference.all():
        
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
    
    col_in_invoice = 29
 
    
    for i in range(col_in_invoice - len(invoice.inquiry_reference.all())):
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
    
    # Create a Django response object, and specify content_type as pdf
    return generate_pdf(request,template_path,context)