from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import UserAccount,DocumentHandler
from django.contrib.auth.models import User
from masters.models import JobMaster, Party,MBLMaster,JobContainer,PartyAddress,GRMaster,JobHBL,BookingMaster, Vendor
from masters.views import check_permissions
from dashboard.models import Logistic
from accounting.models import InvoicePayable,CreditNote,PaymentVoucherDetails,DebitNote,InvoiceReceivable,RecieptVoucherDetails
from datetime import datetime,date
from crm.models import Inquiry
from collections import defaultdict

def handle_login(request):
    user = request.user
    if user.username:
       return redirect('home:home_index')
    
    now = datetime.now()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        
        if user:
            if user.user_account.office.open_time and user.user_account.office.close_time:
                open_time = datetime.combine(date.today(),user.user_account.office.open_time)
                close_time = datetime.combine(date.today(),user.user_account.office.close_time)
                if open_time and close_time:
                    if open_time <= now and close_time >= now:
                        login(request,user)
                        
                        messages.add_message(request, messages.SUCCESS, f"Welcome, {request.user.first_name} {request.user.last_name}")
                        return redirect('home:home_index')
                    else:
                        messages.add_message(request, messages.SUCCESS, f"Sorry, Office Time is Over")
            else:
                login(request,user)
                messages.add_message(request, messages.SUCCESS, f"Welcome, {request.user.first_name} {request.user.last_name}")
                return redirect('home:home_index')
                    
        else:
            messages.add_message(request, messages.SUCCESS, f"Sorry, Check Your Username & Password Again")
    return render(request,'authentication/login.html')
   

def handle_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f"Success, Logout Successfull")
    return redirect('home:handle_login')

@login_required(login_url='home:handle_login')
def home_index(request):
    user = request.user
    account = UserAccount.objects.filter(user=user).first()
    context = {
        'account':account
    }
    return render(request,'root/home.html',context)

@login_required(login_url='home:handle_login')
def choose_operations(request):
    user = request.user
    account = UserAccount.objects.filter(user=user).first()
    context = {
        'account':account
    }
    return render(request,'root/choose_operations.html',context)


# ---------------------- Upload City, State, Ports, Locations, etc. -------------------

def job_details(request):
    job_no = request.GET.get('job_no')
    jobs = JobMaster.objects.filter(pk=job_no).values()
    return JsonResponse({"job": list(jobs)})

def job_hbl_container_details(request):
    job_no = request.GET.get('job_no')
    jobs = JobContainer.objects.filter(job__id=job_no).values()
    return JsonResponse({"job": list(jobs)})



def hbl_details(request):
    hbl_no = request.GET.get('hbl_no')
    mbl = MBLMaster.objects.filter(pk=hbl_no).values()
    return JsonResponse({"hbl": list(mbl)})


def inquiry_details(request):
    inquiry = request.GET.get('inquiry')
    inquiry = Inquiry.objects.filter(pk=inquiry).values()
    return JsonResponse({"inquiry": list(inquiry)})


def party_details(request):
    party = request.GET.get('party')
    party = Party.objects.filter(pk=party).values()
    return JsonResponse({"party": list(party)})

def party_address_details(request):
    party = request.GET.get('party')
    party = PartyAddress.objects.filter(pk=party).values()
    return JsonResponse({"party": list(party)})

def job_gr_details(request):
    job = request.GET.get('job')
    grs = GRMaster.objects.filter(job__id=job).values()
    return JsonResponse({"job_gr": list(grs)})

def job_hbl_details(request):
    job = request.GET.get('job')
    hbls = JobHBL.objects.filter(job__id=job).values()
    return JsonResponse({"job_hbl": list(hbls)})

def job_container_details(request):
    hbl_id = request.GET.get('hbl_id')
    hbls = JobContainer.objects.filter(hbl__id=hbl_id).values()
    return JsonResponse({"job_container": list(hbls)})


def job_booking_details(request):
    id = request.GET.get('booking')
    booking = BookingMaster.objects.filter(id=id).values()
    return JsonResponse({"booking": list(booking)})



def payment_bill_details(request):
    party_type = request.GET.get('party_type')
    party_id = request.GET.get('party_id')
    report_dict = defaultdict(lambda : {'id':'','invoice_no':'','date':'','paid_amount':0,'pending_amount':0,'net_amount':0,'tds_amount':0})
    if party_type == 'Direct':
        purchase_invoice = InvoicePayable.objects.filter(bill_from__id=int(party_id)).filter(is_deleted=False)
    else:
        purchase_invoice = InvoicePayable.objects.filter(vendor__id=int(party_id)).filter(is_deleted=False)
    
    for i in purchase_invoice:
        report = report_dict[i.id]
        
        report['invoice_no'] = i.purchase_invoice_no
        report['id'] = f'{i.id}'
        report['date'] = f'{i.date_of_invoice}'
        paid_amount = 0
        tds_amount = 0

        for j in PaymentVoucherDetails.objects.filter(invoice=i).filter(voucher__is_deleted=False).all():
            paid_amount += (j.paid_amount + j.adjustment_amount + j.tds_amount)
            tds_amount += (j.tds_amount)
        
        for j in DebitNote.objects.filter(invoice_no=i.purchase_invoice_no).all():
            paid_amount += (j.net_amount)

        paid_amount += i.tds_payable
        tds_amount += i.tds_payable

        report['paid_amount'] = round(paid_amount,2)
        report['pending_amount'] = round(i.net_amount - paid_amount,2)
        report['net_amount'] = round(i.net_amount,2)
        report['tds_amount'] = round(tds_amount,2)
    return JsonResponse({"report": list(report_dict.values())})




def get_vendor_emails(request):
    vendor = request.GET.get('party')
    vendors = Vendor.objects.filter(id=vendor)
    emails = []
    for party in vendors:
        try:
            emails += party.email.split(",")
        except:
            pass
        try:
            emails += party.email.split("/")
        except:
            pass
        try:
            emails += party.email.split(" ")
        except:
            pass
        
  
    emails = list(set(emails))
    for i in emails:
        if i == "" or len(i) > 40:
            emails.remove(i)
    
    return JsonResponse({"emails": emails})


def get_party_emails(request):
    party = request.GET.get('party')
    parties = PartyAddress.objects.filter(party__id=party)
    emails = []
    for party in parties:
        try:
            emails += party.corp_email.split(",")
        except:
            pass
        try:
            emails += party.corp_email.split("/")
        except:
            pass
        try:
            emails += party.corp_email.split(" ")
        except:
            pass
        
  
    emails = list(set(emails))
    for i in emails:
        if i == "" or len(i) > 40:
            emails.remove(i)
            
    return JsonResponse({"emails": emails})


def reciept_bill_details(request):
    party_id = request.GET.get('party_id')
    report_dict = defaultdict(lambda : {'id':'','invoice_no':'','date':'','recieved_amount':0,'pending_amount':0,'net_amount':0,'tds_amount':0})
    
    sale_invoices = InvoiceReceivable.objects.filter(bill_to__id=int(party_id)).filter(is_deleted=False).filter(is_einvoiced=True)
    
    for i in sale_invoices:
        report = report_dict[i.id]
        report['invoice_no'] = i.final_invoice_no
        report['id'] = f'{i.id}'
        report['date'] = f'{i.date_of_invoice}'
        recieved_amount = 0
        tds_amount = 0

        for j in RecieptVoucherDetails.objects.filter(invoice=i).filter(voucher__is_deleted=False).all():
            recieved_amount += (j.received_amount + j.adjustment_amount + j.tds_amount)
            tds_amount += (j.tds_amount)
        
        for j in CreditNote.objects.filter(reference_invoice=i).all():
            recieved_amount += (j.net_amount)
            

        recieved_amount += i.tds_payable
        tds_amount += i.tds_payable

        report['recieved_amount'] = round(recieved_amount,2)
        report['pending_amount'] = round(i.net_amount - recieved_amount,2)
        report['net_amount'] = round(i.net_amount,2)
        report['tds_amount'] = round(tds_amount,2)
    return JsonResponse({"report": list(report_dict.values())})



@login_required(login_url='home:handle_login')
def handle_document_approvers(request,module):
    check_permissions(request,module)  
    
    if request.method == 'POST':
        handler = DocumentHandler.objects.filter(user__id=int(request.POST['user'])).filter(company_type__id=int(request.POST['company_type'])).first()
        if not handler:
            handler = DocumentHandler.objects.create(
                user = User.objects.filter(id=int(request.POST['user'])).first()
            )
        company_type = Logistic.objects.filter(id=int(request.POST['company_type'])).first()
        handler.company_type = company_type
        
        is_sea_ex_job = request.POST.get('is_sea_ex_job',False)
        if is_sea_ex_job:
            handler.is_sea_ex_job = True
        else:
            handler.is_sea_ex_job = False
        is_sea_im_job = request.POST.get('is_sea_im_job',False)
        
        if is_sea_im_job:
            handler.is_sea_im_job = True
        else:
            handler.is_sea_im_job = False
        is_air_im_job = request.POST.get('is_air_im_job',False)
        
        if is_air_im_job:
            handler.is_air_im_job = True
        else:
            handler.is_air_im_job = False
        is_air_ex_job = request.POST.get('is_air_ex_job',False)
        
        if is_air_ex_job:
            handler.is_air_ex_job = True
        else:
            handler.is_air_ex_job = False
        
        is_transport_job = request.POST.get('is_transport_job',False)
        if is_transport_job:
            handler.is_transport_job = True
        else:
            handler.is_transport_job = False
            
        is_rec_invoice = request.POST.get('is_rec_invoice',False)
        
        if is_rec_invoice:
            handler.is_rec_invoice = True
        else:
            handler.is_rec_invoice = False
        

        handler.save()
        return redirect('dashboard:handle_document_approvers',module=module)
   
    users = User.objects.filter(is_active=True).all()
    handlers = DocumentHandler.objects.all()
    context = {
        "users":users,
        "module":module,
        "handlers":handlers,
    }
   
    
    return render(request,'advance_admin/handle_document_approvers/handle_document_approvers.html',context)


