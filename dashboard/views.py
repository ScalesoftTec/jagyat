from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from masters.models import JobMaster
from datetime import timedelta,datetime
from django.db.models import Q
from home.models import UserAccount
from django.contrib import messages
import threading

# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self,msg):
        self.msg = msg
        threading.Thread.__init__(self)
    
    def run(self):
        self.msg.send(fail_silently=True)




def check_permissions(request,module):
    user = request.user
    account = UserAccount.objects.filter(user=user).first()
    if module == 'sea_export' and not account.is_sea_export:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Sea Export")
        return redirect('home:choose_operations')
    elif module == 'sea_import' and not account.is_sea_import:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Sea Import")
        return redirect('home:choose_operations')
    elif module == 'air_export' and not account.is_air_export:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Air Export")
        return redirect('home:choose_operations')
    elif module == 'air_import' and not account.is_air_import:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Air Import")
        return redirect('home:choose_operations')
    elif module == 'accounting' and not account.is_finance:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Accounting")
        return redirect('home:home_index')
    elif module == 'crm' and not account.is_crm:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access CRM")
        return redirect('home:home_index')
    elif module == 'bi' and not account.is_bi:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Business Intelligence")
        return redirect('home_index')
    
    elif module == 'hr' and not account.is_hr:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access HR")
        return redirect('home_index')
    
    elif module == 'transportation' and not account.is_transportation:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Transportation")
        return redirect('home:home_index')
    
    elif module == 'advance_admin' and not user.is_superuser:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Admin Dashboard")
        return redirect('home:home_index')
    
@login_required(login_url='home:handle_login')
def index(request,module):
    user = request.user
    account = UserAccount.objects.filter(user=user).first()
    if module == 'sea_export' and not account.is_sea_export:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Sea Export")
        return redirect('home:choose_operations')
    elif module == 'sea_import' and not account.is_sea_import:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Sea Import")
        return redirect('home:choose_operations')
    elif module == 'air_export' and not account.is_air_export:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Air Export")
        return redirect('home:choose_operations')
    elif module == 'air_import' and not account.is_air_import:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Air Import")
        return redirect('home:choose_operations')
    elif module == 'accounting' and not account.is_finance:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Accounting")
        return redirect('home:home_index')
    elif module == 'crm' and not account.is_crm:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access CRM")
        return redirect('home:home_index')
    elif module == 'bi' and not account.is_bi:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Business Intelligence")
        return redirect('home:home_index')
    elif module == 'hr' and not account.is_hr:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Admin Dashboard")
        return redirect('home:home_index')
    
    elif module == 'advance_admin' and not user.is_superuser:
        messages.add_message(request, messages.SUCCESS, f"Sorry, You Haven't Permission To Access Admin Dashboard")
        return redirect('home:home_index')
    
        
    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    
    
    context = {
        'module':module,
        'greeting':greeting
    }
    return render(request,'dashboard/index.html',context)



@login_required(login_url='home:handle_login')
def sea_export_dashboard(request,module):
    context = {}
    check_permissions(request,module)
    
    jobs = JobMaster.objects.filter(module="Sea Export")    
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(company_type=request.user.user_account.office)
    
    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user)
        
        
    today = datetime.now().date()  # Get today's date
    today_plus_5days_date = today + timedelta(days=5)

    coming_eta_jobs = jobs.filter(
        is_deleted=False
    ).exclude(
        job_status__in=["Cancel", "Close"]
    ).filter(
        eta_date__range=(today,today_plus_5days_date)
    )
    
    active_jobs = jobs.filter(is_deleted=False).exclude(job_status="Cancel").exclude(job_status="Close").count()
    closed_jobs = jobs.filter(is_deleted=False).filter(job_status="Close").count()
    cancel_jobs = jobs.filter(Q(is_deleted=True)|Q(job_status="Cancel")).count()
       
    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    context = {
    
        'greeting':greeting,
        'module':module,
        'coming_eta_jobs':coming_eta_jobs,
        'active_jobs':active_jobs,
        'closed_jobs':closed_jobs,
        'cancel_jobs':cancel_jobs,
       
    }
   
    return render(request,'sea_export_dashboard_index.html',context)

@login_required(login_url='home:handle_login')
def sea_import_dashboard(request,module):
    context = {}
    check_permissions(request,module)
    
    
       
    jobs = JobMaster.objects.filter(module="Sea Import")
    
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(company_type=request.user.user_account.office)
    
    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user)
    
    active_jobs = jobs.filter(is_deleted=False).exclude(job_status="Cancel").exclude(job_status="Close").count()
    closed_jobs = jobs.filter(is_deleted=False).filter(job_status="Close").count()
    cancel_jobs = jobs.filter(Q(is_deleted=True)|Q(job_status="Cancel")).count()
    
    
    today = datetime.now().date()  # Get today's date
    today_plus_5days_date = today + timedelta(days=5)

    coming_eta_jobs = jobs.filter(
        is_deleted=False
    ).exclude(
        job_status__in=["Cancel", "Close"]
    ).filter(
        eta_date__range=(today,today_plus_5days_date)
    )
       
    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    context = {
    
        'greeting':greeting,
        'module':module,
        'active_jobs':active_jobs,
        'closed_jobs':closed_jobs,
        'cancel_jobs':cancel_jobs,
        'coming_eta_jobs':coming_eta_jobs,
       
    }
   
    return render(request,'sea_import_dashboard_index.html',context)

@login_required(login_url='home:handle_login')
def air_import_dashboard(request,module):
    context = {}
    check_permissions(request,module)
    
    
       
    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    context = {
    
        'greeting':greeting,
        'module':module,
       
    }
   
    return render(request,'air_import_dashboard_index.html',context)

@login_required(login_url='home:handle_login')
def air_export_dashboard(request,module):
    context = {}
    check_permissions(request,module)
    
    
       
    currentTime = datetime.now()
    greeting = ''
    if currentTime.hour < 12:
        greeting = 'Good Morning'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    context = {
    
        'greeting':greeting,
        'module':module,
       
    }
   
    return render(request,'air_export_dashboard_index.html',context)
