from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from masters.views import check_permissions,messages,get_object_or_404
from hr.forms import DepartmentForm, DesignationForm, LeaveForm, LeaveStatusForm, LeaveTypeForm, EventForm,EmployeeForm
from hr.models import Department,Designation,Leave,LeaveStatus,LeaveType,Event,Employee
# Create your views here.
# ------------------Event Master----------------
@login_required(login_url='home:handle_login')
def create_event(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Event Created.")
        return redirect('hr:create_event',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'event/event_create.html',context)


@login_required(login_url='home:handle_login')
def event_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Event.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'event/event_details.html',context)


@login_required(login_url='home:handle_login')
def event_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Event, id = id)
    
    form = EventForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('hr:event_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'event/event_create.html',context)

@login_required(login_url='home:handle_login')
def event_delete(request,module,id):
    check_permissions(request,module)
    event = Event.objects.filter(id=int(id)).first()
    event.delete()
    return redirect('hr:event_details',module=module)


# ------------------Leave Type Master----------------
@login_required(login_url='home:handle_login')
def create_leave_type(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = LeaveTypeForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Leaave Type Created.")
        return redirect('hr:create_leave_type',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'leave_type/leave_type_create.html',context)


@login_required(login_url='home:handle_login')
def leave_type_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = LeaveType.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'leave_type/leave_type_details.html',context)


@login_required(login_url='home:handle_login')
def leave_type_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(LeaveType, id = id)
    
    form = LeaveTypeForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('hr:leave_type_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'leave_type/leave_type_create.html',context)

@login_required(login_url='home:handle_login')
def leave_type_delete(request,module,id):
    check_permissions(request,module)
    leave_type = LeaveType.objects.filter(id=int(id)).first()
    leave_type.delete()
    return redirect('hr:leave_type_details',module=module)


# ------------------Leave Status Master----------------
@login_required(login_url='home:handle_login')
def create_leave_status(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = LeaveStatusForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Leave Status Created.")
        return redirect('hr:create_leave_status',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'leave_status/leave_status_create.html',context)


@login_required(login_url='home:handle_login')
def leave_status_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = LeaveStatus.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'leave_status/leave_status_details.html',context)


@login_required(login_url='home:handle_login')
def leave_status_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(LeaveStatus, id = id)
    
    form = LeaveStatusForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('hr:leave_status_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'leave_status/leave_status_create.html',context)

@login_required(login_url='home:handle_login')
def leave_status_delete(request,module,id):
    check_permissions(request,module)
    leave_status = LeaveStatus.objects.filter(id=int(id)).first()
    leave_status.delete()
    return redirect('hr:leave_status_details',module=module)


# ------------------Leave Master----------------
@login_required(login_url='home:handle_login')
def create_leave(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = LeaveForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Leave Created.")
        return redirect('hr:create_leave_status',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'leave/leave_create.html',context)


@login_required(login_url='home:handle_login')
def leave_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Leave.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'leave/leave_details.html',context)


@login_required(login_url='home:handle_login')
def leave_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Leave, id = id)
    
    form = LeaveForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('hr:leave_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'leave/leave_create.html',context)

@login_required(login_url='home:handle_login')
def leave_delete(request,module,id):
    check_permissions(request,module)
    leave = Leave.objects.filter(id=int(id)).first()
    leave.delete()
    return redirect('hr:leave_details',module=module)


@login_required(login_url='home:handle_login')
def my_profile(request,module):
    context ={}
    check_permissions(request,module)
    context['module']= module
    return render(request,'hr/my_profile.html',context)