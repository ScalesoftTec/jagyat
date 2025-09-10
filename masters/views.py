from django.shortcuts import get_object_or_404, render,redirect, HttpResponse
from dashboard.models import Logistic
from masters.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from masters.models import *
import requests
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from hr.models import Employee
from accounting.models import InvoiceReceivable,InvoicePayable,IndirectExpense,RecieptVoucher,PaymentVoucher,DebitNote,DebitNoteDetail,CreditNote,CreditNoteDetail,InvoicePayableDetail,InvoiceReceivableDetail
from hr.models import *
from hr.forms import *
from django.template.loader import render_to_string
from dashboard.views import check_permissions
import traceback
from django.conf import settings
import os
import pandas as pd
from django.core.files.storage import FileSystemStorage
# Create your views here.

    
# ------------------Country Master----------------
@login_required(login_url='home:handle_login')
def create_country(request,module):
    context ={}
    check_permissions(request,module)
    form = CountryForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Country Created.")
        return redirect('masters:create_country',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'country/country_create.html',context)

@login_required(login_url='home:handle_login')
def country_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Country.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'country/country_details.html',context)

@login_required(login_url='home:handle_login')
def country_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(Country, id = id)
    form = CountryForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:country_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'country/country_create.html',context)

@login_required(login_url='home:handle_login')
def country_delete(request,module,id):
    check_permissions(request,module)
    country = Country.objects.filter(id=int(id)).first()
    country.delete()
    return redirect('masters:country_details',module=module)


    
# ------------------State Master----------------
@login_required(login_url='home:handle_login')
def create_state(request,module):
    context ={}
    check_permissions(request,module)
    form = StateForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New State Created.")
        return redirect('masters:create_state',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'state/state_create.html',context)

@login_required(login_url='home:handle_login')
def state_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = State.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'state/state_details.html',context)

@login_required(login_url='home:handle_login')
def state_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(State, id = id)
    form = StateForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:state_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'state/state_create.html',context)

@login_required(login_url='home:handle_login')
def state_delete(request,module,id):
    check_permissions(request,module)
    state = State.objects.filter(id=int(id)).first()
    state.delete()
    return redirect('masters:state_details',module=module)




# ------------------Port Master----------------
@login_required(login_url='home:handle_login')
def create_port(request,module):
    context ={}
    check_permissions(request,module)
    form = PortForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Port Created.")
        return redirect('masters:create_port',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'port/port_create.html',context)

@login_required(login_url='home:handle_login')
def port_details(request,module):
    context ={}
    check_permissions(request,module)
  
    ports = Ports.objects.all()
          
    context['ports']= ports
    context['module']= module
    return render(request,'port/port_details.html',context)

@login_required(login_url='home:handle_login')
def port_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(Ports, id = id)
    form = PortForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:port_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'port/port_create.html',context)

@login_required(login_url='home:handle_login')
def port_delete(request,module,id):
    check_permissions(request,module)
    port = Ports.objects.filter(id=int(id)).first()
    port.delete()
    return redirect('masters:port_details',module=module)

# ------------------Location Master----------------
@login_required(login_url='home:handle_login')
def create_location(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = LocationForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Location Created.")
        return redirect('masters:create_location',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'location/location_create.html',context)

@login_required(login_url='home:handle_login')
def location_details(request,module):
    context ={}
    check_permissions(request,module)
  
    locations = Location.objects.all()
          
    context['locations']= locations
    context['module']= module
    return render(request,'location/location_details.html',context)


@login_required(login_url='home:handle_login')
def location_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Location, id = id)
    
    form = LocationForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:location_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'location/location_create.html',context)

@login_required(login_url='home:handle_login')
def location_delete(request,module,id):
    check_permissions(request,module)
    location = Location.objects.filter(id=int(id)).first()
    location.delete()
    return redirect('masters:location_details',module=module)


# ------------------Ledger Categories Master----------------
@login_required(login_url='home:handle_login')
def create_ledger_categories(request,module):
    context ={}
    check_permissions(request,module)
    form = LedgerCategoriesForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Ledger Category Created.")
        return redirect('masters:create_ledger_categories',module=module)
    context['form']= form
    context['module']= module
    return render(request,'ledger_categories/ledger_categories_create.html',context)

@login_required(login_url='home:handle_login')
def ledger_categories_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = LedgerCategories.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'ledger_categories/ledger_categories_details.html',context)

@login_required(login_url='home:handle_login')
def ledger_categories_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(LedgerCategories, id = id)
    
    form = LedgerCategoriesForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:ledger_categories_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'ledger_categories/ledger_categories_create.html',context)

@login_required(login_url='home:handle_login')
def ledger_categories_delete(request,module,id):
    check_permissions(request,module)
    data = LedgerCategories.objects.filter(id=int(id)).first()
    data.delete()
    return redirect('masters:ledger_categories_details',module=module)

# ------------------Ledger Sub Categories Master----------------
@login_required(login_url='home:handle_login')
def create_ledger_sub_categories(request,module):
    context ={}
    check_permissions(request,module)
    form = LedgerSubCategoriesForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Ledger Sub Category Created.")
        return redirect('masters:create_ledger_sub_categories',module=module)
    context['form']= form
    context['module']= module
    return render(request,'ledger_sub_categories/ledger_sub_categories_create.html',context)

@login_required(login_url='home:handle_login')
def ledger_sub_categories_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = LedgerSubCategories.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'ledger_sub_categories/ledger_sub_categories_details.html',context)

@login_required(login_url='home:handle_login')
def ledger_sub_categories_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(LedgerSubCategories, id = id)
    
    form = LedgerSubCategoriesForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:ledger_sub_categories_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'ledger_sub_categories/ledger_sub_categories_create.html',context)

@login_required(login_url='home:handle_login')
def ledger_sub_categories_delete(request,module,id):
    check_permissions(request,module)
    data = LedgerSubCategories.objects.filter(id=int(id)).first()
    data.delete()
    return redirect('masters:ledger_sub_categories_details',module=module)


# ------------------Ledger Master----------------
def handleSalesInvoiceOpeningBalance(request,id,is_update):
    ledger = LedgerMaster.objects.filter(id=id).first()
    total_heads = int(request.POST['sales_total_head'])
    if total_heads == 0:
        return
    for i in range(1,total_heads+1):
        is_active = request.POST[f'sales_is_active-{i}']
        existing_id = int(request.POST[f'sales_existing_id_{i}'])
        if is_active == "yes" and existing_id == 0:
            invoice_no = request.POST[f'sales_invoice_no-{i}']
            date = request.POST[f'sales_date-{i}']
            amount = request.POST[f'sales_amount-{i}']
            is_final = request.POST.get(f'sales_is_final-{i}',False)
              
            invoice = InvoiceReceivable.objects.create(
                invoice_no = invoice_no,
                final_invoice_no = invoice_no,
                einvoice_date = date,
                date_of_invoice = date,
                old_invoice = True,
                is_einvoiced = True,
                company_type=ledger.company_type,
                net_amount = amount,
                currency_ex_rate = 1,
                pending_amount = amount,
                invoice_status = "Close"
            )
            invoice.save()
            
            if ledger.party:
                invoice.bill_to = ledger.party
        
            if ledger.party_address:
                invoice.bill_to_address = ledger.party_address
                
            invoice.save()
            new_ledger_opening = LedgerMasterOpeningBalanceDetails.objects.create(
                invoice_no = invoice_no,
                date = date,
                amount = amount,
                sales_invoice = True,
                ledger = ledger
            )
            new_ledger_opening.invoice = invoice
          
            if is_final:
                new_ledger_opening.is_final = True

            new_ledger_opening.save()

        else:
            try:
                is_deletable = int(request.POST[f'sales_is_deletable_{i}'])
                opening_details = LedgerMasterOpeningBalanceDetails.objects.filter(id=existing_id).first()
                invoice_no = request.POST[f'sales_invoice_no-{i}']
                date = request.POST[f'sales_date-{i}']
                amount = request.POST[f'sales_amount-{i}']
                is_final = request.POST.get(f'sales_is_final-{i}',False)
                if is_active == "yes":
                    opening_details.invoice.company_type = ledger.company_type
                    opening_details.invoice.save()

                if is_deletable == 1 and is_active == "yes":
                    opening_details.invoice_no = invoice_no
                    opening_details.amount = amount
                    opening_details.date = date
                    opening_details.invoice.invoice_no = invoice_no
                    opening_details.invoice.date_of_invoice = date
                    opening_details.invoice.einvoice_date = date
                    opening_details.invoice.final_invoice_no = invoice_no
                    opening_details.invoice.net_amount = amount
                    opening_details.invoice.pending_amount = amount
                    opening_details.invoice.save()
                    opening_details.save()


                if is_deletable == 1 and is_active == "no":
                    if not existing_id == 0:
                        opening_details.invoice.delete()
                        opening_details.delete()
                    
            except:
                pass    
              
def handlePurchaseInvoiceOpeningBalance(request,id,is_update):
    ledger = LedgerMaster.objects.filter(id=id).first()
    total_heads = int(request.POST['purchase_total_head'])
    if total_heads == 0:
        return
    for i in range(1,total_heads+1):
        is_active = request.POST[f'purchase_is_active-{i}']
        existing_id = int(request.POST[f'purchase_existing_id_{i}'])
        if is_active == "yes" and existing_id == 0:
            invoice_no = request.POST[f'purchase_invoice_no-{i}']
            date = request.POST[f'purchase_date-{i}']
            amount = request.POST[f'purchase_amount-{i}']
            is_final = request.POST.get(f'purchase_is_final-{i}',False)

            invoice = InvoicePayable.objects.create(
                invoice_no = invoice_no,
                purchase_invoice_no = invoice_no,
                date_of_invoice = date,
                old_invoice = True,
                company_type=ledger.company_type,
                net_amount = amount,
                currency_ex_rate = 1,
                pending_amount = amount,
            )
            invoice.save()
            
            if ledger.party:
                invoice.bill_from = ledger.party
        
            if ledger.party_address:
                invoice.bill_from_address = ledger.party_address
                
                
                
            invoice.save()
            new_ledger_opening = LedgerMasterOpeningBalanceDetails.objects.create(
                invoice_no = invoice_no,
                date = date,
                amount = amount,
                ledger = ledger,
                purchase_invoice = True,
            )
            new_ledger_opening.invoice_payable = invoice
          
            if is_final:
                new_ledger_opening.is_final = True

            new_ledger_opening.save()
        
        else:
            try:
                is_deletable = int(request.POST[f'purchase_is_deletable_{i}'])
                invoice_no = request.POST[f'purchase_invoice_no-{i}']
                date = request.POST[f'purchase_date-{i}']
                amount = request.POST[f'purchase_amount-{i}']
                opening_details = LedgerMasterOpeningBalanceDetails.objects.filter(id=existing_id).first()
                if is_active == "yes":
                    opening_details.invoice_payable.company_type = ledger.company_type
                    opening_details.invoice_payable.save()
                if is_deletable == 1 and is_active == "yes":
                    opening_details.invoice_no = invoice_no
                    opening_details.amount = amount
                    opening_details.date = date
                    opening_details.invoice_payable.purchase_invoice_no = invoice_no
                    opening_details.invoice_payable.invoice_no = invoice_no
                    opening_details.invoice_payable.net_amount = amount
                    opening_details.invoice_payable.pending_amount = amount
                    opening_details.invoice_payable.save()
                    opening_details.save()

                if is_deletable == 1 and is_active == "no":
                    if not existing_id == 0:
                        opening_details.invoice_payable.delete()
                        opening_details.delete()
            except:
                pass    
                 
def handleIndirectExpenseOpeningBalance(request,id,is_update):
    ledger = LedgerMaster.objects.filter(id=id).first()
    total_heads = int(request.POST['expense_total_head'])
    if total_heads == 0:
        return
    for i in range(1,total_heads+1):
        is_active = request.POST[f'expense_is_active-{i}']
        existing_id = int(request.POST[f'expense_existing_id_{i}'])
        if is_active == "yes" and existing_id == 0:
            invoice_no = request.POST[f'expense_invoice_no-{i}']
            date = request.POST[f'expense_date-{i}']
            amount = request.POST[f'expense_amount-{i}']
            is_final = request.POST.get(f'expense_is_final-{i}',False)

            invoice = IndirectExpense.objects.create(
                bill_no = invoice_no,
                bill_date = date,
                old_invoice = True,
                company_type=ledger.company_type,
                net_amount = amount,
                pending_amount = amount,
            )
            invoice.save()
            
            if ledger.vendor:
                invoice.vendor = ledger.vendor
            
            invoice.save()
            new_ledger_opening = LedgerMasterOpeningBalanceDetails.objects.create(
                invoice_no = invoice_no,
                date = date,
                amount = amount,
                ledger = ledger,
                ind_expense = True,
            )
            new_ledger_opening.indirect_expense = invoice
          
            if is_final:
                new_ledger_opening.is_final = True

            new_ledger_opening.save()
        
        else:
            try:
                is_deletable = int(request.POST[f'expense_is_deletable_{i}'])
                invoice_no = request.POST[f'expense_invoice_no-{i}']
                date = request.POST[f'expense_date-{i}']
                amount = request.POST[f'expense_amount-{i}']
                opening_details = LedgerMasterOpeningBalanceDetails.objects.filter(id=existing_id).first()
                if is_active == "yes":
                    opening_details.indirect_expense.company_type = ledger.company_type
                    opening_details.indirect_expense.save()
                if is_deletable == 1 and is_active == "yes":
                    opening_details.invoice_no = invoice_no
                    opening_details.amount = amount
                    opening_details.date = date
                    opening_details.indirect_expense.bill_no = invoice_no
                    opening_details.indirect_expense.net_amount = amount
                    opening_details.indirect_expense.pending_amount = amount
                    opening_details.indirect_expense.save()
                    opening_details.save()

                if is_deletable == 1 and is_active == "no":
                    if not existing_id == 0:
                        opening_details.indirect_expense.delete()
                        opening_details.delete()
            except:
                pass    
                
def handleRecieptVoucherOpeningBalance(request,id,is_update):
    ledger = LedgerMaster.objects.filter(id=id).first()
    total_heads = int(request.POST['rec_voucher_total_head'])
    if total_heads == 0:
        return
    for i in range(1,total_heads+1):
        is_active = request.POST[f'rec_voucher_is_active-{i}']
        existing_id = int(request.POST[f'rec_voucher_existing_id_{i}'])
  
        if is_active == "yes" and existing_id == 0:
            invoice_no = request.POST[f'rec_voucher_invoice_no-{i}']
            date = request.POST[f'rec_voucher_date-{i}']
            amount = request.POST[f'rec_voucher_amount-{i}']
            is_final = request.POST.get(f'rec_voucher_is_final-{i}',False)
            bank = request.POST[f'rec_voucher_bank-{i}']
            bank = Bank.objects.filter(id=int(bank)).first()
            invoice = RecieptVoucher.objects.create(
                voucher_no = invoice_no,
                voucher_date = date,
                old_voucher = True,
                company_type=ledger.company_type,
                received_amount = amount,
                advance_amount = amount,
                net_amount = amount,
                total_recieved_amount = amount,
                instrument_no = "Old Balance",
                narration = "Old Balance",
                party_name = ledger.party,
                party_address = ledger.party_address,
                to_bank = bank,
            )
            
            
          
            invoice.save()
            new_ledger_opening = LedgerMasterOpeningBalanceDetails.objects.create(
                invoice_no = invoice_no,
                date = date,
                amount = amount,
                ledger = ledger,
                rec_voucher = True,
            )
            new_ledger_opening.reciept_voucher = invoice
          
            if is_final:
                new_ledger_opening.is_final = True

            new_ledger_opening.save()
        
        else:
            try:
                is_deletable = int(request.POST[f'rec_voucher_is_deletable_{i}'])
                opening_details = LedgerMasterOpeningBalanceDetails.objects.filter(id=existing_id).first()
                invoice_no = request.POST[f'rec_voucher_invoice_no-{i}']
                date = request.POST[f'rec_voucher_date-{i}']
                amount = request.POST[f'rec_voucher_amount-{i}']
                bank = request.POST[f'rec_voucher_bank-{i}']
                bank = Bank.objects.filter(id=int(bank)).first()
                if is_active == "yes":
                    opening_details.reciept_voucher.to_bank = bank
                    opening_details.reciept_voucher.company_type = ledger.company_type
                    opening_details.reciept_voucher.save()
                if is_deletable == 1 and is_active == "yes":
                    opening_details.invoice_no = invoice_no
                    opening_details.amount = amount
                    opening_details.date = date
                    opening_details.reciept_voucher.voucher_no = invoice_no
                    opening_details.reciept_voucher.instrument_no = invoice_no
                    opening_details.reciept_voucher.received_amount = amount
                    opening_details.reciept_voucher.advance_amount = amount
                    opening_details.reciept_voucher.net_amount = amount
                    opening_details.reciept_voucher.total_recieved_amount = amount
                    opening_details.reciept_voucher.save()
                    opening_details.save()

                if is_deletable == 1 and is_active == "no":
                    if not existing_id == 0:
                        opening_details.reciept_voucher.delete()
                        opening_details.delete()
            except:
                pass    
                
def handlePaymentVoucherOpeningBalance(request,id,is_update):
    ledger = LedgerMaster.objects.filter(id=id).first()
    total_heads = int(request.POST['pay_voucher_total_head'])
    if total_heads == 0:
        return
    for i in range(1,total_heads+1):
        is_active = request.POST[f'pay_voucher_is_active-{i}']
        existing_id = int(request.POST[f'pay_voucher_existing_id_{i}'])
        if is_active == "yes" and existing_id == 0:
            invoice_no = request.POST[f'pay_voucher_invoice_no-{i}']
            date = request.POST[f'pay_voucher_date-{i}']
            amount = request.POST[f'pay_voucher_amount-{i}']
            is_final = request.POST.get(f'pay_voucher_is_final-{i}',False)
            bank = request.POST[f'pay_voucher_bank-{i}']
            bank = Bank.objects.filter(id=int(bank)).first()

            invoice = PaymentVoucher.objects.create(
                voucher_no = invoice_no,
                voucher_date = date,
                old_voucher = True,
                company_type=ledger.company_type,
                paid_amount = amount,
                advance_amount = amount,
                net_amount = amount,
                total_paid_amount = amount,
                instrument_no = "Old Balance",
                narration = "Old Balance",
            )
            invoice.from_bank = bank
            
            if ledger.party_type == "Direct":
                invoice.party_name = ledger.party
                invoice.party_address = ledger.party_address
                
            if ledger.party_type == "Indirect":
                invoice.vendor = ledger.vendor

           
            
           
            invoice.save()
            new_ledger_opening = LedgerMasterOpeningBalanceDetails.objects.create(
                invoice_no = invoice_no,
                date = date,
                amount = amount,
                ledger = ledger,
                pay_voucher = True,
            )
            new_ledger_opening.payment_voucher = invoice
          
            if is_final:
                new_ledger_opening.is_final = True

            new_ledger_opening.save()
        
        else:
            try:
                is_deletable = int(request.POST[f'pay_voucher_is_deletable_{i}'])
                opening_details = LedgerMasterOpeningBalanceDetails.objects.filter(id=existing_id).first()
                invoice_no = request.POST[f'pay_voucher_invoice_no-{i}']
                date = request.POST[f'pay_voucher_date-{i}']
                bank = request.POST[f'rec_voucher_bank-{i}']
                bank = Bank.objects.filter(id=int(bank)).first()
                amount = request.POST[f'pay_voucher_amount-{i}']
                if is_active == "yes":
                    opening_details.payment_voucher.company_type = ledger.company_type
                    invoice.from_bank = bank
                    opening_details.payment_voucher.save()
                if is_deletable == 1 and is_active == "yes":
                    opening_details.invoice_no = invoice_no
                    opening_details.amount = amount
                    opening_details.date = date
                    opening_details.payment_voucher.voucher_no = invoice_no
                    opening_details.payment_voucher.instrument_no = invoice_no
                    opening_details.payment_voucher.paid_amount = amount
                    opening_details.payment_voucher.advance_amount = amount
                    opening_details.payment_voucher.net_amount = amount
                    opening_details.payment_voucher.total_paid_amount = amount
                    opening_details.payment_voucher.save()
                    opening_details.save()

                if is_deletable == 1 and is_active == "no":
                    if not existing_id == 0:
                        opening_details.reciept_voucher.delete()
                        opening_details.delete()
            except:
                pass    
              
# ------------------Ledger Master----------------            
@login_required(login_url='home:handle_login')
def create_ledger(request,module):
    context ={}
    check_permissions(request,module)
    form = LedgerForm(request.POST or None,initial={'company_type':Logistic.objects.first()})
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Ledger  Created.")
        return redirect('masters:create_ledger',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'ledger/ledger_create.html',context)

@login_required(login_url='home:handle_login')
def ledger_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = LedgerMaster.objects.select_related('company_type').prefetch_related('ledger_opening_details').all()
   
    context['data']= data
    context['module']= module
    return render(request,'ledger/ledger_details.html',context)

@login_required(login_url='home:handle_login')
def ledger_update(request,module,id):
    
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(LedgerMaster, id = id)
    ledger = LedgerMaster.objects.filter(id=id).first()
    form = LedgerForm(request.POST or None, instance = obj)
    data = obj
    created_by = obj.created_by
    ledger_name = obj.ledger_name
    id = obj.id
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
      
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:ledger_details',module=module)
          
    context['form']= form
    context['module']= module
    context['ledger']= ledger
    context['update']= True
   
    return render(request,'ledger/ledger_create.html',context)

@login_required(login_url='home:handle_login')
def ledger_delete(request,module,id):
    check_permissions(request,module)
    data = LedgerMaster.objects.filter(id=int(id)).first()

    for i in data.ledger_opening_details.all():
        if i.invoice_payable:
            i.invoice_payable.delete()
        if i.invoice:
            i.invoice.delete()
        if i.indirect_expense:
             i.indirect_expense.delete()    
        i.delete()

    data.delete()
    return redirect('masters:ledger_details',module=module)

# ------------------Vendor Master----------------
@login_required(login_url='home:handle_login')
def create_vendor(request,module):
    context ={}
    check_permissions(request,module)
    form = VendorForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Vendor  Created.")
        return redirect('masters:create_vendor',module=module)
    context['form']= form
    context['module']= module
    return render(request,'vendor/vendor_create.html',context)


@login_required(login_url='home:handle_login')
def vendor_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Vendor.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'vendor/vendor_details.html',context)


@login_required(login_url='home:handle_login')
def vendor_update(request,module,id):
    
    context ={}
    check_permissions(request,module)
  
  
    obj = get_object_or_404(Vendor, id = id)
    
    form = VendorForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:vendor_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'vendor/vendor_create.html',context)

@login_required(login_url='home:handle_login')
def vendor_delete(request,module,id):
    check_permissions(request,module)
    data = Vendor.objects.filter(id=int(id)).first()
    data.delete()
    return redirect('masters:vendor_details',module=module)
# ------------------Currency Master----------------

    
@login_required(login_url='home:handle_login')
def create_currency(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = CurrencyForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Currency Created.")
        return redirect('masters:create_currency',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'currency/currency_create.html',context)


@login_required(login_url='home:handle_login')
def currency_details(request,module):
    context ={}
    check_permissions(request,module)
  
    currencies = currency.objects.all()
          
    context['currencies']= currencies
    context['module']= module
    return render(request,'currency/currency_details.html',context)


@login_required(login_url='home:handle_login')
def currency_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(currency, id = id)
    
    form = CurrencyForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:currency_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'currency/currency_create.html',context)

@login_required(login_url='home:handle_login')
def currency_delete(request,module,id):
    check_permissions(request,module)
    currency_obj = currency.objects.filter(id=int(id)).first()
    currency_obj.delete()
    return redirect('masters:currency_details',module=module)

    
# ------------------Shipping Line Master----------------

    
@login_required(login_url='home:handle_login')
def create_shippingline(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = ShippingLineForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Shipping Line Created.")
        return redirect('masters:create_shippingline',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'shippingline/shippingline_create.html',context)

@login_required(login_url='home:handle_login')
def shippingline_details(request,module):
    context ={}
    check_permissions(request,module)
  
    lines = ShippingLines.objects.all()
          
    context['lines']= lines
    context['module']= module
    return render(request,'shippingline/shippingline_details.html',context)

@login_required(login_url='home:handle_login')
def shippingline_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(ShippingLines, id = id)
    
    form = ShippingLineForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:shippingline_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'shippingline/shippingline_create.html',context)

@login_required(login_url='home:handle_login')
def shippingline_delete(request,module,id):
    check_permissions(request,module)
    shipping_line = ShippingLines.objects.filter(id=int(id)).first()
    shipping_line.delete()
    return redirect('masters:shippingline_details',module=module)

    

# ------------------Air Line Master----------------
@login_required(login_url='home:handle_login')
def create_airline(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = AirLineForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Air Line Created.")
        return redirect('masters:create_airline',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'airline/airline_create.html',context)

@login_required(login_url='home:handle_login')
def airline_details(request,module):
    context ={}
    check_permissions(request,module)
  
    lines = Airlines.objects.all()
          
    context['lines']= lines
    context['module']= module
    return render(request,'airline/airline_details.html',context)

@login_required(login_url='home:handle_login')
def airline_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Airlines, id = id)
    
    form = AirLineForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:airline_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'airline/airline_create.html',context)

@login_required(login_url='home:handle_login')
def airline_delete(request,module,id):
    check_permissions(request,module)
    air_line = Airlines.objects.filter(id=int(id)).first()
    air_line.delete()
    return redirect('masters:airline_details',module=module)

# ----------------Party------------------------
   
@login_required(login_url='home:handle_login')
def create_party(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = PartyForm(request.POST or None,initial={'company_type':request.user.user_account.office})
    if form.is_valid():
       
        form.save()
        form.instance.created_by = request.user
        try:
            kyc_form = request.FILES['kyc_form']
            form.instance.kyc_form = kyc_form
        except:
            pass
    
        
        try:
            gst_certificate = request.FILES['gst_certificate']
            form.instance.gst_certificate = gst_certificate
        except:
            pass
        
        try:
            other_document = request.FILES['other_document']
            form.instance.other_document = other_document
        except:
            pass
            
        
        
        total_rows = int(request.POST['total_rows'])
        for i in range(1,total_rows+1):
            is_active = request.POST[f'is_active-{i}']
            
            state = request.POST.get(f'state-{i}',None)
            branch = request.POST.get(f'branch-{i}',None)
            if is_active == "yes" and state and branch:
                address_line_1 = request.POST.get(f'address_line_1-{i}',None)
                address_line_2 = request.POST.get(f'address_line_2-{i}',None)
                address_line_3 = request.POST.get(f'address_line_3-{i}',None)
                country = request.POST.get(f'country-{i}',None)
                state = State.objects.filter(id=state).first()
                city = request.POST.get(f'city-{i}',None)
                zip = request.POST.get(f'zip-{i}',None)
                gstin = request.POST.get(f'gstin-{i}',None)
                contact = request.POST.get(f'contact-{i}',None)
                email = request.POST.get(f'email-{i}',None)
                pan = request.POST.get(f'pan-{i}',None)
                contact_person = request.POST.get(f'contact_person-{i}', '')
                
                new_party_address = PartyAddress.objects.create(
                    party = form.instance,
                    branch = branch,
                    corp_address_line1 = address_line_1,
                    corp_address_line2 = address_line_2,
                    corp_address_line3 = address_line_3,
                    corp_country = country,
                    corp_state = state,
                    corp_city = city,
                    corp_email = email,
                    corp_gstin = gstin,
                    corp_zip = zip,
                    corp_contact = contact,
                    corp_pan = pan,
                    corp_contact_person = contact_person
                )
                
                new_party_address.save()
        
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Party Created.")
        return redirect('masters:create_party',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'party/create_party.html',context)


@login_required(login_url='home:handle_login')
def party_details(request,module):
    context ={}
    check_permissions(request,module)
  
    parties = Party.objects.select_related('account_manager','created_by','tally_group').prefetch_related('party_address').all()
          
    context['parties']= parties
    context['module']= module
    return render(request,'party/party_details.html',context)


@login_required(login_url='home:handle_login')
def party_update(request,module,id):
    context ={}
    
    check_permissions(request,module)
  
    obj = get_object_or_404(Party, id = id)
    
    form = PartyForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        
        party_addresses = PartyAddress.objects.filter(party__id=id).all()
  
        total_rows = int(request.POST['total_rows'])
  
        for i in range(1,total_rows+1):
            is_active = request.POST[f'is_active-{i}']
            is_update = request.POST[f'is_update-{i}']
            branch = request.POST.get(f'branch-{i}',None)
            state = request.POST.get(f'state-{i}',None)
        
            address_line_1 = request.POST.get(f'address_line_1-{i}',None)
            address_line_2 = request.POST.get(f'address_line_2-{i}',None)
            address_line_3 = request.POST.get(f'address_line_3-{i}',None)
            country = request.POST.get(f'country-{i}',None)
            if state:
                state = State.objects.filter(id=state).first()
            city = request.POST.get(f'city-{i}', '')
            zip = request.POST.get(f'zip-{i}', '')
            gstin = request.POST.get(f'gstin-{i}','')
            contact = request.POST.get(f'contact-{i}', '')
            email = request.POST.get(f'email-{i}', '')
            pan = request.POST.get(f'pan-{i}', '')
            contact_person = request.POST.get(f'contact_person-{i}', '')
            
            if is_active == "yes":
                if is_update == "yes":
                    party_address = PartyAddress.objects.filter(id=request.POST[f'party_address_id-{i}']).first()
                    party_address.branch = branch
                    party_address.corp_address_line1 = address_line_1
                    party_address.corp_address_line2 = address_line_2
                    party_address.corp_address_line3 = address_line_3
                    party_address.corp_country = country
                    party_address.corp_state = state
                    party_address.corp_city = city
                    party_address.corp_email = email
                    party_address.corp_gstin = gstin
                    party_address.corp_zip = zip
                    party_address.corp_contact = contact
                    party_address.corp_pan = pan
                    party_address.corp_contact_person = contact_person
                    party_address.save()
                else:
                    new_party_address = PartyAddress.objects.create(
                        party = form.instance,
                        branch = branch,
                        corp_address_line1 = address_line_1,
                        corp_address_line2 = address_line_2,
                        corp_address_line3 = address_line_3,
                        corp_country = country,
                        
                        corp_city = city,
                        corp_email = email,
                        corp_gstin = gstin,
                        corp_zip = zip,
                        corp_contact = contact,
                        corp_pan = pan,
                        corp_contact_person = contact_person,
                        
                    )
                    if state:
                        new_party_address.corp_state = state
                    
                    
                    new_party_address.save()
           
            if is_active == "no":
                if is_update == "yes":
                    party_address = PartyAddress.objects.filter(id=request.POST[f'party_address_id-{i}']).first()
                    party_address.delete()
                    
        
        try:
            kyc_form = request.FILES['kyc_form']
            form.instance.kyc_form = kyc_form
        except:
            pass
        
        try:
            photo_id = request.FILES['photo_id']
            form.instance.photo_id = photo_id
        except:
            pass
        
        try:
            gst_certificate = request.FILES['gst_certificate']
            form.instance.gst_certificate = gst_certificate
        except Exception as e:
            pass
          
        try:
            other_document = request.FILES['other_document']
            form.instance.other_document = other_document
        except:
            pass

        
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:party_details',module=module)
          
    context['form']= form
    context['data']= obj
    context['module']= module
    context['update']= True
    return render(request,'party/create_party.html',context)

@login_required(login_url='home:handle_login')
def party_delete(request,module,id):
    check_permissions(request,module)
    party = Party.objects.filter(id=int(id)).first()
    party.delete()
    return redirect('masters:party_details',module=module)


def party_to_tally(request,module,id):
    if request.method == 'POST':
        company = Logistic.objects.filter(id=int(request.POST['company'])).first()
        party = Party.objects.filter(id=int(id)).first()
        url = request.POST['url']
        xml = render_to_string("party/party_tally.xml",{
            'company':company,
            'party':party,
        }).encode('utf-8')
        headers = {'Content-Type':'application/xml'}
        requests.post(url=url,data=xml,headers=headers)
        party.is_transfered_to_tally = True
        party.save()
        return redirect('masters:party_details',module=module)


    

# ----------------Party Address------------------------
    
@login_required(login_url='home:handle_login')
def create_party_address(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = PartyAddressForm(request.POST or None)
    if form.is_valid():
        form.save()
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Party Address Created.")
        return redirect('masters:create_party_address',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'party_address/create_party_address.html',context)


@login_required(login_url='home:handle_login')
def party_address_details(request,module):
    context ={}
    check_permissions(request,module)
  
    parties = PartyAddress.objects.all()
          
    context['parties']= parties
    context['module']= module
    return render(request,'party_address/party_address_details.html',context)


@login_required(login_url='home:handle_login')
def party_address_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(PartyAddress, id = id)
    
    form = PartyAddressForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        
       

        
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:party_address_details',module=module)
          
    context['form']= form
    context['data']= obj
    context['module']= module
    context['update']= True
    return render(request,'party_address/create_party_address.html',context)

@login_required(login_url='home:handle_login')
def party_address_delete(request,module,id):
    check_permissions(request,module)
    party_address = PartyAddress.objects.filter(id=int(id)).first()
    party_address.delete()
    return redirect('masters:party_address_details',module=module)

# Commodity
    
@login_required(login_url='home:handle_login')
def create_commodity(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = CommodityForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Commodity Created.")
        return redirect('masters:create_commodity',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'commodity/create_commodity.html',context)


@login_required(login_url='home:handle_login')
def commodity_details(request,module):
    context ={}
    check_permissions(request,module)
  
    commodities = Commodity.objects.all()
          
    context['commodities']= commodities
    context['module']= module
    return render(request,'commodity/commodity_details.html',context)


@login_required(login_url='home:handle_login')
def commodity_update(request,module,id):
    context ={}
    check_permissions(request,module)
    obj = get_object_or_404(Commodity, id = id)
    form = CommodityForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:commodity_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'commodity/create_commodity.html',context)


@login_required(login_url='home:handle_login')
def commodity_delete(request,module,id):
    check_permissions(request,module)
    commodity = Commodity.objects.filter(id=int(id)).first()
    commodity.delete()
    return redirect('masters:commodity_details',module=module)

# Billing Head
    
@login_required(login_url='home:handle_login')
def create_billing_head(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = BillingHeadForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Billing Head Created.")
        return redirect('masters:create_billing_head',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'billing_head/bh_create.html',context)


@login_required(login_url='home:handle_login')
def billing_head_details(request,module):
    context ={}
    check_permissions(request,module)
  
    billing_head = BillingHead.objects.all()
    # for i in billing_head:
    #     i.is_service = True
    #     i.save()
    uoms = UOM.objects.filter(is_transfered_to_tally=True).all()
    context['billing_head']= billing_head
    context['module']= module
    context['uoms']= uoms
    return render(request,'billing_head/bh_details.html',context)


@login_required(login_url='home:handle_login')
def billing_head_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(BillingHead, id = id)
    
    form = BillingHeadForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:billing_head_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'billing_head/bh_create.html',context)


@login_required(login_url='home:handle_login')
def billing_head_delete(request,module,id):
    check_permissions(request,module)
    billing_head = BillingHead.objects.filter(id=int(id)).first()
    billing_head.delete()
    return redirect('masters:billing_head_details',module=module)


def billing_head_to_tally(request,module,id):
    if request.method == 'POST':
        company = Logistic.objects.filter(id=int(request.POST['company'])).first()
        data = BillingHead.objects.filter(id=int(id)).first()
        uom = UOM.objects.filter(id=int(request.POST['uom'])).first()
        url = request.POST['url']
        xml = render_to_string("billing_head/billing_head_tally.xml",{
            'company':company,
            'data':data,
            'uom':uom,
        }).encode('utf-8')
        headers = {'Content-Type':'application/xml'}
        requests.post(url=url,data=xml,headers=headers)
        data.is_transfered_to_tally = True
        data.save()
        return redirect('masters:billing_head_details',module=module)

# Bank Details
    
@login_required(login_url='home:handle_login')
def create_bank(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = BankForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        
        messages.add_message(request, messages.SUCCESS, f"Success, New Bank Detail Created.")
        return redirect('masters:create_bank',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'bank/bank_create.html',context)


@login_required(login_url='home:handle_login')
def bank_details(request,module):
    context ={}
    check_permissions(request,module)
  
    bank = Bank.objects.all()
          
    context['bank']= bank
    context['module']= module
    return render(request,'bank/bank_details.html',context)


@login_required(login_url='home:handle_login')
def bank_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Bank, id = id)
    
    form = BankForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:bank_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'bank/bank_create.html',context)


@login_required(login_url='home:handle_login')
def bank_delete(request,module,id):
    check_permissions(request,module)
    bank = Bank.objects.filter(id=int(id)).first()
    bank.delete()
    return redirect('masters:bank_details',module=module)

# UOM
    
@login_required(login_url='home:handle_login')
def create_uom(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = UOMForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Unit of Measurement Created.")
        return redirect('masters:create_uom',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'uom/uom_create.html',context)


@login_required(login_url='home:handle_login')
def uom_details(request,module):
    context ={}
    check_permissions(request,module)
  
    uom = UOM.objects.all()
          
    context['uom']= uom
    context['module']= module
    return render(request,'uom/uom_details.html',context)


@login_required(login_url='home:handle_login')
def uom_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(UOM, id = id)
    
    form = UOMForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:uom_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'uom/uom_create.html',context)


@login_required(login_url='home:handle_login')
def uom_delete(request,module,id):
    check_permissions(request,module)
    uom = UOM.objects.filter(id=int(id)).first()
    uom.delete()
    return redirect('masters:uom_details',module=module)


def uom_to_tally(request,module,id):
    if request.method == 'POST':
        company = Logistic.objects.filter(id=int(request.POST['company'])).first()
        data = UOM.objects.filter(id=int(id)).first()
        url = request.POST['url']
        xml = render_to_string("uom/uom_tally.xml",{
            'company':company,
            'data':data,
        }).encode('utf-8')
        headers = {'Content-Type':'application/xml'}
        requests.post(url=url,data=xml,headers=headers)
        data.is_transfered_to_tally = True
        data.save()
        return redirect('masters:uom_details',module=module)

# Battery
    
@login_required(login_url='home:handle_login')
def create_battery(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = BatteryForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Battery Detail Created.")
        return redirect('masters:create_battery',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'battery/battery_create.html',context)


@login_required(login_url='home:handle_login')
def battery_details(request,module):
    context ={}
    check_permissions(request,module)
  
    batteries = Battery.objects.all()
          
    context['batteries']= batteries
    context['module']= module
    return render(request,'battery/battery_details.html',context)


@login_required(login_url='home:handle_login')
def battery_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Battery, id = id)
    
    form = BatteryForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:battery_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'battery/battery_create.html',context)


@login_required(login_url='home:handle_login')
def battery_delete(request,module,id):
    check_permissions(request,module)
    battery = Battery.objects.filter(id=int(id)).first()
    battery.delete()
    return redirect('masters:battery_details',module=module)



# Tyre
    
@login_required(login_url='home:handle_login')
def create_tyre(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = TyreForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Tyre Detail Created.")
        return redirect('masters:create_tyre',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'tyre/tyre_create.html',context)


@login_required(login_url='home:handle_login')
def tyre_details(request,module):
    context ={}
    check_permissions(request,module)
  
    tyres = Tyre.objects.all()
          
    context['tyres']= tyres
    context['module']= module
    return render(request,'tyre/tyre_details.html',context)


@login_required(login_url='home:handle_login')
def tyre_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Tyre, id = id)
    
    form = TyreForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:tyre_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'tyre/tyre_create.html',context)


@login_required(login_url='home:handle_login')
def tyre_delete(request,module,id):
    check_permissions(request,module)
    tyre = Tyre.objects.filter(id=int(id)).first()
    tyre.delete()
    return redirect('masters:tyre_details',module=module)


def PortCreatePopup(request,id):
	form = PortForm(request.POST or None)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_author". This is the element id in the form
		id = "#"+id
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance,id))
	
	return render(request, "additional_form/port_form.html", {"form" : form})

def LocationCreatePopup(request,id):
	form = LocationForm(request.POST or None)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_author". This is the element id in the form
		id = "#"+id
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance,id))
	
	return render(request, "additional_form/location_form.html", {"form" : form})


# Category   
@login_required(login_url='home:handle_login')
def create_category(request,module):
    context ={}

    check_permissions(request,module)
  
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Category Created.")
        return redirect('masters:create_category',module=module)
    
    context['form']= form
    context['module']= module
    
    return render(request,'category/category_create.html',context)


@login_required(login_url='home:handle_login')
def category_details(request,module):
    context ={}
    check_permissions(request,module)
  
    categories = CategoryMaster.objects.all()
          
    context['categories']= categories
    context['module']= module
    return render(request,'category/category_details.html',context)


@login_required(login_url='home:handle_login')
def category_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(CategoryMaster, id = id)
    
    form = CategoryForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        
        
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:category_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'category/category_create.html',context)


@login_required(login_url='home:handle_login')
def category_delete(request,module,id):
    check_permissions(request,module)
    category = CategoryMaster.objects.filter(id=int(id)).first()
    category.delete()
    return redirect('masters:category_details',module=module)


# Driver Form
    
@login_required(login_url='home:handle_login')
def create_driver(request,module):
    context ={}
    check_permissions(request,module)
  
    form = DriverForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Driver Created.")
        return redirect('masters:create_driver',module=module)
    
    context['form']= form
    context['module']= module
    
    return render(request,'driver/driver_create.html',context)


@login_required(login_url='home:handle_login')
def driver_details(request,module):
    context ={}
    check_permissions(request,module)
    drivers = DriverMaster.objects.all()
    context['drivers']= drivers
    context['module']= module
    
    return render(request,'driver/driver_details.html',context)


@login_required(login_url='home:handle_login')
def driver_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
  
    obj = get_object_or_404(DriverMaster, id = id)
    
    form = DriverForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
      
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:driver_details',module=module)
    
    
    
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'driver/driver_create.html',context)


@login_required(login_url='home:handle_login')
def driver_delete(request,module,id):
    check_permissions(request,module)
    driver = DriverMaster.objects.filter(id=int(id)).first()
    driver.delete()
    return redirect('masters:driver_details',module=module)

# Trailor Form
    
@login_required(login_url='home:handle_login')
def create_trailor(request,module):
    context ={}
    check_permissions(request,module)
  
    form = TrailorForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        
        
        driver_total_rows = int(request.POST['driver_total_rows'])
        for i in range(1,driver_total_rows+1):
            is_driver_active = request.POST[f'is_driver_active_{i}']
            if is_driver_active == 'yes':
                driver = request.POST.get(f'driver_{i}',None)
                from_date = request.POST.get(f'from_date_{i}',None)
                to_date = request.POST.get(f'to_date_{i}',None)
                remarks = request.POST.get(f'remarks_{i}',None)
                if driver:
                    driver = DriverMaster.objects.filter(id=int(driver)).first()
                    new_trailor_driver = TrailorDriver.objects.create(
                        trailor = form.instance,
                        driver = driver,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_driver.to_date = to_date
                    if from_date:
                        new_trailor_driver.from_date = from_date
                    new_trailor_driver.save()
                    
            
        horse_total_rows = int(request.POST['horse_total_rows'])
        for i in range(1,horse_total_rows+1):
            is_horse_active = request.POST[f'is_horse_active_{i}']
            if is_horse_active == 'yes':
                tyre = request.POST.get(f'tyre_{i}',None)
                from_date = request.POST.get(f'horse_from_date_{i}',None)
                to_date = request.POST.get(f'horse_to_date_{i}',None)
                remarks = request.POST.get(f'horse_remarks_{i}',None)
                if tyre:
                    tyre = Tyre.objects.filter(id=int(tyre)).first()
                    new_trailor_horse = TrailorTyreHorse.objects.create(
                        trailor = form.instance,
                        tyre = tyre,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_horse.to_date = to_date
                    if from_date:
                        new_trailor_horse.from_date = from_date
                    new_trailor_horse.save()
                    
        trolley_total_rows = int(request.POST['trolley_total_rows'])
        for i in range(1,trolley_total_rows+1):
            is_trolley_active = request.POST[f'is_trolley_active_{i}']
            if is_trolley_active == 'yes':
                tyre = request.POST.get(f'trolley_tyre_{i}',None)
                from_date = request.POST.get(f'trolley_from_date_{i}',None)
                to_date = request.POST.get(f'trolley_to_date_{i}',None)
                remarks = request.POST.get(f'trolley_remarks_{i}',None)
                if tyre:
                    tyre = Tyre.objects.filter(id=int(tyre)).first()
                    new_trailor_trolley = TrailorTyreTrolley.objects.create(
                        trailor = form.instance,
                        tyre = tyre,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_trolley.to_date = to_date
                    if from_date:
                        new_trailor_trolley.from_date = from_date
                    new_trailor_trolley.save()
        
        trailor_fit_total_rows = int(request.POST['trailor_fit_total_rows'])
        for i in range(1,trailor_fit_total_rows+1):
            is_fit_active = request.POST[f'is_fit_active_{i}']
            if is_fit_active == 'yes':
                fitness_no = request.POST.get(f'fitness_no_{i}',None)
                from_date = request.POST.get(f'fit_from_date_{i}',None)
                to_date = request.POST.get(f'fit_to_date_{i}',None)
                remarks = request.POST.get(f'fit_remarks_{i}',None)
                if fitness_no:
                  
                    new_trailor_fitness = TrailorFitness.objects.create(
                        trailor = form.instance,
                        fitness_no = fitness_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_fitness.to_date = to_date
                    if from_date:
                        new_trailor_fitness.from_date = from_date
                    try:
                        file = request.FILES[f'fitness_file_{i}']
                        new_trailor_fitness.file = file
                    except:
                        pass
                    new_trailor_fitness.save()
                    
        trailor_np_total_rows = int(request.POST['trailor_np_total_rows'])
        for i in range(1,trailor_np_total_rows+1):
            is_np_active = request.POST[f'is_np_active_{i}']
            if is_np_active == 'yes':
                permit_no = request.POST.get(f'np_no_{i}',None)
                from_date = request.POST.get(f'np_from_date_{i}',None)
                to_date = request.POST.get(f'np_to_date_{i}',None)
                remarks = request.POST.get(f'np_remarks_{i}',None)
                if permit_no:
                  
                    new_trailor_np = TrailorNationalPermit.objects.create(
                        trailor = form.instance,
                        permit_no = permit_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_np.to_date = to_date
                    if from_date:
                        new_trailor_np.from_date = from_date
                    try:
                        file = request.FILES[f'np_file_{i}']
                        new_trailor_np.file = file
                    except:
                        pass
                    new_trailor_np.save()
                    
            
        trailor_ng_total_rows = int(request.POST['trailor_ng_total_rows'])
        for i in range(1,trailor_ng_total_rows+1):
            is_ng_active = request.POST[f'is_ng_active_{i}']
            if is_ng_active == 'yes':
                permit_no = request.POST.get(f'ng_no_{i}',None)
                from_date = request.POST.get(f'ng_from_date_{i}',None)
                to_date = request.POST.get(f'ng_to_date_{i}',None)
                remarks = request.POST.get(f'ng_remarks_{i}',None)
                if permit_no:
                  
                    new_trailor_ng = TrailorNationalGoodPermit.objects.create(
                        trailor = form.instance,
                        permit_no = permit_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_ng.to_date = to_date
                    if from_date:
                        new_trailor_ng.from_date = from_date
                    try:
                        file = request.FILES[f'ng_file_{i}']
                        new_trailor_ng.file = file
                    except:
                        pass
                    new_trailor_ng.save()
                    
            
        trailor_ins_total_rows = int(request.POST['trailor_ins_total_rows'])
        for i in range(1,trailor_ins_total_rows+1):
            is_insurance_active = request.POST[f'is_insurance_active_{i}']
            if is_insurance_active == 'yes':
                insurance_no = request.POST.get(f'insurance_no_{i}',None)
                from_date = request.POST.get(f'insurance_from_date_{i}',None)
                to_date = request.POST.get(f'insurance_to_date_{i}',None)
                remarks = request.POST.get(f'insurance_remarks_{i}',None)
                if insurance_no:
                  
                    new_trailor_insurance = TrailorInsurance.objects.create(
                        trailor = form.instance,
                        insurance_no = insurance_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_insurance.to_date = to_date
                    if from_date:
                        new_trailor_insurance.from_date = from_date
                    try:
                        file = request.FILES[f'insurance_file_{i}']
                        new_trailor_insurance.file = file
                    except:
                        pass
                    new_trailor_insurance.save()
                    
            
        trailor_roadtax_total_rows = int(request.POST['trailor_roadtax_total_rows'])
        for i in range(1,trailor_roadtax_total_rows+1):
            is_road_tax_active = request.POST[f'is_road_tax_active_{i}']
            if is_road_tax_active == 'yes':
                permit_no = request.POST.get(f'road_tax_no_{i}',None)
                from_date = request.POST.get(f'road_tax_from_date_{i}',None)
                to_date = request.POST.get(f'road_tax_to_date_{i}',None)
                remarks = request.POST.get(f'road_tax_remarks_{i}',None)
                if permit_no:
                  
                    new_trailor_road_tax = TrailorRoadTax.objects.create(
                        trailor = form.instance,
                        permit_no = permit_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_road_tax.to_date = to_date
                    if from_date:
                        new_trailor_road_tax.from_date = from_date
                    try:
                        file = request.FILES[f'road_tax_file_{i}']
                        new_trailor_road_tax.file = file
                    except:
                        pass
                    new_trailor_road_tax.save()
                    
            
        trailor_puc_total_rows = int(request.POST['trailor_puc_total_rows'])
        for i in range(1,trailor_puc_total_rows+1):
            is_puc_active = request.POST[f'is_puc_active_{i}']
            if is_puc_active == 'yes':
                permit_no = request.POST.get(f'puc_no_{i}',None)
                from_date = request.POST.get(f'puc_from_date_{i}',None)
                to_date = request.POST.get(f'puc_to_date_{i}',None)
                remarks = request.POST.get(f'puc_remarks_{i}',None)
                if permit_no:
                  
                    new_trailor_puc = TrailorPUC.objects.create(
                        trailor = form.instance,
                        permit_no = permit_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_puc.to_date = to_date
                    if from_date:
                        new_trailor_puc.from_date = from_date
                    try:
                        file = request.FILES[f'puc_file_{i}']
                        new_trailor_puc.file = file
                    except:
                        pass
                    new_trailor_puc.save()
                    
        trailor_rc_total_rows = int(request.POST['trailor_rc_total_rows'])
        for i in range(1,trailor_rc_total_rows+1):
            is_rc_active = request.POST[f'is_rc_active_{i}']
            if is_rc_active == 'yes':
                permit_no = request.POST.get(f'rc_no_{i}',None)
                from_date = request.POST.get(f'rc_from_date_{i}',None)
                to_date = request.POST.get(f'rc_to_date_{i}',None)
                remarks = request.POST.get(f'rc_remarks_{i}',None)
                if permit_no:
                  
                    new_trailor_rc = TrailorRC.objects.create(
                        trailor = form.instance,
                        permit_no = permit_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_rc.to_date = to_date
                    if from_date:
                        new_trailor_rc.from_date = from_date
                    try:
                        file = request.FILES[f'rc_file_{i}']
                        new_trailor_rc.file = file
                    except:
                        pass
                    new_trailor_rc.save()
                    
        trailor_org_inv_total_rows = int(request.POST['trailor_org_inv_total_rows'])
        for i in range(1,trailor_org_inv_total_rows+1):
            is_orginv_active = request.POST[f'is_orginv_active_{i}']
            if is_orginv_active == 'yes':
                permit_no = request.POST.get(f'orginv_no_{i}',None)
                from_date = request.POST.get(f'orginv_from_date_{i}',None)
                to_date = request.POST.get(f'orginv_to_date_{i}',None)
                remarks = request.POST.get(f'orginv_remarks_{i}',None)
                if permit_no:
                  
                    new_trailor_orginv = TrailorOrgInv.objects.create(
                        trailor = form.instance,
                        permit_no = permit_no,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_orginv.to_date = to_date
                    if from_date:
                        new_trailor_orginv.from_date = from_date
                    try:
                        file = request.FILES[f'orginv_file_{i}']
                        new_trailor_orginv.file = file
                    except:
                        pass
                    new_trailor_orginv.save()
                    
        trailor_event_total_rows = int(request.POST['trailor_event_total_rows'])
        for i in range(1,trailor_event_total_rows+1):
            is_event_active = request.POST[f'is_event_active_{i}']
            if is_event_active == 'yes':
                event_remarks = request.POST.get(f'event_remarks_{i}',None)
                date = request.POST.get(f'event_date_{i}',None)
               
                if event_remarks:
                  
                    new_trailor_event = TrailorEventBook.objects.create(
                        trailor = form.instance,
                        event_remarks = event_remarks,
                        
                    ) 
                    if date:
                        new_trailor_event.date = date
                 
                    new_trailor_event.save()
                    
        trailor_service_total_rows = int(request.POST['trailor_service_total_rows'])
        for i in range(1,trailor_service_total_rows+1):
            is_service_active = request.POST[f'is_service_active_{i}']
            if is_service_active == 'yes':
                service_date = request.POST.get(f'service_date_{i}',None)
                next_due_date = request.POST.get(f'next_due_date_{i}',None)
                place = request.POST.get(f'place_{i}',None)
                expense_amount = request.POST.get(f'expense_amount_{i}',0)
                remarks = request.POST.get(f'service_remarks_{i}',None)
               
                if service_date:
                  
                    new_trailor_service = TrailorService.objects.create(
                        trailor = form.instance,
                        place = place,
                        
                        remarks = remarks,
                        
                    ) 
                    if service_date:
                        new_trailor_service.service_date = service_date
                    if next_due_date:
                        new_trailor_service.next_due_date = next_due_date
                    if expense_amount:
                        new_trailor_service.expense_amount = expense_amount
                 
                    new_trailor_service.save()
                    
        trailor_acessory_total_rows = int(request.POST['trailor_acessory_total_rows'])
        print(trailor_acessory_total_rows)
        for i in range(1,trailor_acessory_total_rows+1):
            is_acessory_active_ = request.POST[f'is_acessory_active_{i}']
            if is_acessory_active_ == 'yes':
                acessory = request.POST.get(f'acessory_{i}',None)
                from_date = request.POST.get(f'acessory_from_date_{i}',None)
                to_date = request.POST.get(f'acessory_to_date_{i}',None)
                price = request.POST.get(f'price_{i}',None)
                remarks = request.POST.get(f'acessory_remarks_{i}',None)
               
                if acessory and from_date:
                  
                    new_trailor_acessory = TrailorAcessory.objects.create(
                        trailor = form.instance,
                        acessory = acessory,
                        price=price,
                        remarks = remarks,
                        
                    ) 
                    if from_date:
                        new_trailor_acessory.from_date = from_date
                    if to_date:
                        new_trailor_acessory.to_date = to_date
                   
                 
                    new_trailor_acessory.save()
                    
        trailor_location_total_rows = int(request.POST['trailor_location_total_rows'])
       
        for i in range(1,trailor_location_total_rows+1):
            is_location_active = request.POST[f'is_location_active_{i}']
            if is_location_active == 'yes':
                location = request.POST.get(f'location_{i}',None)
                if location:
                    location = Location.objects.filter(id=int(location)).first()
                from_date = request.POST.get(f'location_date_{i}',None)
                employee = request.POST.get(f'employee_{i}',None)
                if employee:
                    employee = Employee.objects.filter(id=int(employee)).first()
                    
                remarks = request.POST.get(f'location_remarks_{i}',None)
               
                if location and employee:
                  
                    new_trailor_location = TrailorLocation.objects.create(
                        trailor = form.instance,
                        location = location,
                        employee = employee,
                        remarks = remarks,
                        
                    ) 
                    if from_date:
                        new_trailor_location.from_date = from_date
                 
                   
                 
                    new_trailor_location.save()
                    
            
        messages.add_message(request, messages.SUCCESS, f"Success, New Trailor Created.")
        return redirect('masters:create_trailor',module=module)
    drivers = DriverMaster.objects.all()
    horse_tyres = Tyre.objects.filter(type="HORSE").all()
    trolley_tyres = Tyre.objects.filter(type="TROLLEY").all()
    
    context['form']= form
    context['module']= module
    context['drivers']= drivers
    context['horse_tyres']= horse_tyres
    context['trolley_tyres']= trolley_tyres
    
    return render(request,'trailor/trailor_create.html',context)


@login_required(login_url='home:handle_login')
def trailor_details(request,module):
    context ={}
    check_permissions(request,module)
    trailors = TrailorMaster.objects.all()
    context['trailors']= trailors
    context['module']= module
    
    return render(request,'trailor/trailor_details.html',context)


@login_required(login_url='home:handle_login')
def trailor_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
  
    obj = get_object_or_404(TrailorMaster, id = id)
    
    form = TrailorForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
      
        form.save()
        
        trailor_drivers = TrailorDriver.objects.all()
        trailor_drivers.delete()
        driver_total_rows = int(request.POST['driver_total_rows'])
        for i in range(1,driver_total_rows+1):
            is_driver_active = request.POST[f'is_driver_active_{i}']
            if is_driver_active == 'yes':
                driver = request.POST.get(f'driver_{i}',None)
                from_date = request.POST.get(f'from_date_{i}',None)
                to_date = request.POST.get(f'to_date_{i}',None)
                remarks = request.POST.get(f'remarks_{i}',None)
                if driver:
                    driver = DriverMaster.objects.filter(id=int(driver)).first()
                    new_trailor_driver = TrailorDriver.objects.create(
                        trailor = form.instance,
                        driver = driver,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_driver.to_date = to_date
                    if from_date:
                        new_trailor_driver.from_date = from_date
                    new_trailor_driver.save()

        trailor_horse = TrailorTyreHorse.objects.all()
        trailor_horse.delete()
        horse_total_rows = int(request.POST['horse_total_rows'])
        for i in range(1,horse_total_rows+1):
            is_horse_active = request.POST[f'is_horse_active_{i}']
            if is_horse_active == 'yes':
                tyre = request.POST.get(f'tyre_{i}',None)
                from_date = request.POST.get(f'horse_from_date_{i}',None)
                to_date = request.POST.get(f'horse_to_date_{i}',None)
                remarks = request.POST.get(f'horse_remarks_{i}',None)
                if tyre:
                    tyre = Tyre.objects.filter(id=int(tyre)).first()
                    new_trailor_horse = TrailorTyreHorse.objects.create(
                        trailor = form.instance,
                        tyre = tyre,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_horse.to_date = to_date
                    if from_date:
                        new_trailor_horse.from_date = from_date
                    new_trailor_horse.save()
        
        trailor_trolley = TrailorTyreTrolley.objects.all()
        trailor_trolley.delete()
        trolley_total_rows = int(request.POST['trolley_total_rows'])
        for i in range(1,trolley_total_rows+1):
            is_trolley_active = request.POST[f'is_trolley_active_{i}']
            if is_trolley_active == 'yes':
                tyre = request.POST.get(f'trolley_tyre_{i}',None)
                from_date = request.POST.get(f'trolley_from_date_{i}',None)
                to_date = request.POST.get(f'trolley_to_date_{i}',None)
                remarks = request.POST.get(f'trolley_remarks_{i}',None)
                if tyre:
                    tyre = Tyre.objects.filter(id=int(tyre)).first()
                    new_trailor_trolley = TrailorTyreTrolley.objects.create(
                        trailor = form.instance,
                        tyre = tyre,
                        remarks = remarks,
                    ) 
                    if to_date:
                        new_trailor_trolley.to_date = to_date
                    if from_date:
                        new_trailor_trolley.from_date = from_date
                    new_trailor_trolley.save()
        
        
        trailor_fit_total_rows = int(request.POST['trailor_fit_total_rows'])
        for i in range(1,trailor_fit_total_rows+1):
            is_fit_active = request.POST[f'is_fit_active_{i}']
            is_fit_update = request.POST[f'is_fit_update_{i}']
            if is_fit_active == 'yes':
                fitness_no = request.POST.get(f'fitness_no_{i}',None)
                from_date = request.POST.get(f'fit_from_date_{i}',None)
                to_date = request.POST.get(f'fit_to_date_{i}',None)
                remarks = request.POST.get(f'fit_remarks_{i}',None)
                if is_fit_update == "yes":
                    fitness = TrailorFitness.objects.filter(id=int(request.POST[f'is_fit_id_{i}'])).first()
                    fitness.fitness_no = fitness_no
                    fitness.remarks = remarks
                    
                else:
                    if fitness_no:
                        fitness = TrailorFitness.objects.create(
                            trailor = form.instance,
                            fitness_no = fitness_no,
                            remarks = remarks,
                        )
                    else:
                        fitness = None
                     
                if to_date:
                    fitness.to_date = to_date
                   
                if from_date:
                    fitness.from_date = from_date
                
                try:
                    file = request.FILES[f'fitness_file_{i}']
                    fitness.file = file
                except:
                    pass
                
                if fitness is not None:
                    fitness.save()
                

            elif is_fit_active == 'no' and is_fit_update == "yes":
                fitness = TrailorFitness.objects.filter(id=int(request.POST[f'is_fit_id_{i}'])).first()
                fitness.delete()
                
        
        trailor_np_total_rows = int(request.POST['trailor_np_total_rows'])
        for i in range(1,trailor_np_total_rows+1):
            is_np_active = request.POST[f'is_np_active_{i}']
            is_np_update = request.POST[f'is_np_update_{i}']
            if is_np_active == 'yes':
                permit_no = request.POST.get(f'np_no_{i}',None)
                from_date = request.POST.get(f'np_from_date_{i}',None)
                to_date = request.POST.get(f'np_to_date_{i}',None)
                remarks = request.POST.get(f'np_remarks_{i}',None)
                if is_np_update == "yes":
                    np = TrailorNationalPermit.objects.filter(id=int(request.POST[f'is_np_id_{i}'])).first()
                    np.permit_no = permit_no
                    np.remarks = remarks
                else:
                    if permit_no:
                        np = TrailorNationalPermit.objects.create(
                            trailor = form.instance,
                            permit_no = permit_no,
                            remarks = remarks,
                        ) 
                    else:
                        np = None
                if to_date:
                    np.to_date = to_date
                if from_date:
                    np.from_date = from_date
                try:
                    file = request.FILES[f'np_file_{i}']
                    np.file = file
                except:
                    pass
                
                if np is not None:
                    np.save()

            elif is_np_active == 'no' and is_np_update == "yes":
                np = TrailorNationalPermit.objects.filter(id=int(request.POST[f'is_np_id_{i}'])).first()
                np.delete()
                
        
        trailor_ng_total_rows = int(request.POST['trailor_ng_total_rows'])
        for i in range(1,trailor_ng_total_rows+1):
            is_ng_active = request.POST[f'is_ng_active_{i}']
            is_ng_update = request.POST[f'is_ng_update_{i}']
            if is_ng_active == 'yes':
                permit_no = request.POST.get(f'ng_no_{i}',None)
                from_date = request.POST.get(f'ng_from_date_{i}',None)
                to_date = request.POST.get(f'ng_to_date_{i}',None)
                remarks = request.POST.get(f'ng_remarks_{i}',None)
                if is_ng_update == "yes":
                    ng = TrailorNationalGoodPermit.objects.filter(id=int(request.POST[f'is_ng_id_{i}'])).first()
                    ng.permit_no = permit_no
                    ng.remarks = remarks
                else:
                    if permit_no:
                        ng = TrailorNationalGoodPermit.objects.create(
                            trailor = form.instance,
                            permit_no = permit_no,
                            remarks = remarks,
                        ) 
                    else:
                        ng = None
                if to_date:
                    ng.to_date = to_date
                if from_date:
                    ng.from_date = from_date
                try:
                    file = request.FILES[f'ng_file_{i}']
                    ng.file = file
                except:
                    pass
                if ng is not None:
                    ng.save()

            elif is_ng_active == 'no' and is_ng_update == "yes":
                ng = TrailorNationalGoodPermit.objects.filter(id=int(request.POST[f'is_ng_id_{i}'])).first()
                ng.delete()
                
        
        trailor_ins_total_rows = int(request.POST['trailor_ins_total_rows'])
        for i in range(1,trailor_ins_total_rows+1):
            is_insurance_active = request.POST[f'is_insurance_active_{i}']
            is_insurance_update = request.POST[f'is_insurance_update_{i}']
            if is_insurance_active == 'yes':
                insurance_no = request.POST.get(f'insurance_no_{i}',None)
                from_date = request.POST.get(f'insurance_from_date_{i}',None)
                to_date = request.POST.get(f'insurance_to_date_{i}',None)
                remarks = request.POST.get(f'insurance_remarks_{i}',None)
                if is_insurance_update == "yes":
                    insurance = TrailorInsurance.objects.filter(id=int(request.POST[f'is_insurance_id_{i}'])).first()
                    insurance.insurance_no = insurance_no
                    insurance.remarks = remarks
                else:
                    if insurance_no:
                        insurance = TrailorInsurance.objects.create(
                            trailor = form.instance,
                            insurance_no = insurance_no,
                            remarks = remarks,
                        ) 
                    else:
                        insurance = None
                if to_date:
                    insurance.to_date = to_date
                if from_date:
                    insurance.from_date = from_date
                try:
                    file = request.FILES[f'insurance_file_{i}']
                    insurance.file = file
                except:
                    pass
                if insurance is not None:
                    insurance.save()

            elif is_insurance_active == 'no' and is_insurance_update == "yes":
                insurance = TrailorInsurance.objects.filter(id=int(request.POST[f'is_insurance_id_{i}'])).first()
                insurance.delete()
                
        trailor_roadtax_total_rows = int(request.POST['trailor_roadtax_total_rows'])
        for i in range(1,trailor_roadtax_total_rows+1):
            is_road_tax_active = request.POST[f'is_road_tax_active_{i}']
            is_road_tax_update = request.POST[f'is_road_tax_update_{i}']
            if is_road_tax_active == 'yes':
                permit_no = request.POST.get(f'road_tax_no_{i}',None)
                from_date = request.POST.get(f'road_tax_from_date_{i}',None)
                to_date = request.POST.get(f'road_tax_to_date_{i}',None)
                remarks = request.POST.get(f'road_tax_remarks_{i}',None)
                if is_road_tax_update == "yes":
                    road_tax = TrailorRoadTax.objects.filter(id=int(request.POST[f'is_road_tax_id_{i}'])).first()
                    road_tax.permit_no = permit_no
                    road_tax.remarks = remarks
                else:
                    if permit_no:
                        road_tax = TrailorRoadTax.objects.create(
                            trailor = form.instance,
                            permit_no = permit_no,
                            remarks = remarks,
                        ) 
                    else:
                        road_tax = None
                if to_date:
                    road_tax.to_date = to_date
                if from_date:
                    road_tax.from_date = from_date
                try:
                    file = request.FILES[f'road_tax_file_{i}']
                    road_tax.file = file
                except:
                    pass
                if road_tax is not None:
                    road_tax.save()

            elif is_road_tax_active == 'no' and is_road_tax_update == "yes":
                road_tax = TrailorRoadTax.objects.filter(id=int(request.POST[f'is_road_tax_id_{i}'])).first()
                road_tax.delete()
                
        trailor_puc_total_rows = int(request.POST['trailor_puc_total_rows'])
        for i in range(1,trailor_puc_total_rows+1):
            is_puc_active = request.POST[f'is_puc_active_{i}']
            is_puc_update = request.POST[f'is_puc_update_{i}']
            if is_puc_active == 'yes':
                permit_no = request.POST.get(f'puc_no_{i}',None)
                from_date = request.POST.get(f'puc_from_date_{i}',None)
                to_date = request.POST.get(f'puc_to_date_{i}',None)
                remarks = request.POST.get(f'puc_remarks_{i}',None)
                if is_puc_update == "yes":
                    puc = TrailorPUC.objects.filter(id=int(request.POST[f'is_puc_id_{i}'])).first()
                    puc.permit_no = permit_no
                    puc.remarks = remarks
                else:
                    if permit_no:
                        puc = TrailorPUC.objects.create(
                            trailor = form.instance,
                            permit_no = permit_no,
                            remarks = remarks,
                        ) 
                    else:
                        puc = None
                if to_date:
                    puc.to_date = to_date
                if from_date:
                    puc.from_date = from_date
                try:
                    file = request.FILES[f'puc_file_{i}']
                    puc.file = file
                except:
                    pass
                if puc is not None:
                    puc.save()

            elif is_puc_active == 'no' and is_puc_update == "yes":
                puc = TrailorPUC.objects.filter(id=int(request.POST[f'is_puc_id_{i}'])).first()
                puc.delete()
                
        trailor_rc_total_rows = int(request.POST['trailor_rc_total_rows'])
        for i in range(1,trailor_rc_total_rows+1):
            is_rc_active = request.POST[f'is_rc_active_{i}']
            is_rc_update = request.POST[f'is_rc_update_{i}']
            if is_rc_active == 'yes':
                permit_no = request.POST.get(f'rc_no_{i}',None)
                from_date = request.POST.get(f'rc_from_date_{i}',None)
                to_date = request.POST.get(f'rc_to_date_{i}',None)
                remarks = request.POST.get(f'rc_remarks_{i}',None)
                if is_rc_update == "yes":
                    rc = TrailorRC.objects.filter(id=int(request.POST[f'is_rc_id_{i}'])).first()
                    rc.permit_no = permit_no
                    rc.remarks = remarks
                else:
                    if permit_no:
                        rc = TrailorRC.objects.create(
                            trailor = form.instance,
                            permit_no = permit_no,
                            remarks = remarks,
                        ) 
                    else:
                        rc = None
                if to_date:
                    rc.to_date = to_date
                if from_date:
                    rc.from_date = from_date
                try:
                    file = request.FILES[f'rc_file_{i}']
                    rc.file = file
                except:
                    pass
                if rc is not None:
                    rc.save()

            elif is_rc_active == 'no' and is_rc_update == "yes":
                rc = TrailorRC.objects.filter(id=int(request.POST[f'is_rc_id_{i}'])).first()
                rc.delete()
                
        trailor_org_inv_total_rows = int(request.POST['trailor_org_inv_total_rows'])
        for i in range(1,trailor_org_inv_total_rows+1):
            is_orginv_active = request.POST[f'is_orginv_active_{i}']
            is_orginv_update = request.POST[f'is_orginv_update_{i}']
            if is_orginv_active == 'yes':
                permit_no = request.POST.get(f'orginv_no_{i}',None)
                from_date = request.POST.get(f'orginv_from_date_{i}',None)
                to_date = request.POST.get(f'orginv_to_date_{i}',None)
                remarks = request.POST.get(f'orginv_remarks_{i}',None)
                if is_orginv_update == "yes":
                    orginv = TrailorOrgInv.objects.filter(id=int(request.POST[f'is_orginv_id_{i}'])).first()
                    orginv.permit_no = permit_no
                    orginv.remarks = remarks
                else:
                    if permit_no:
                        orginv = TrailorOrgInv.objects.create(
                            trailor = form.instance,
                            permit_no = permit_no,
                            remarks = remarks,
                        ) 
                    else:
                        orginv = None
                if to_date:
                    orginv.to_date = to_date
                if from_date:
                    orginv.from_date = from_date
                try:
                    file = request.FILES[f'orginv_file_{i}']
                    orginv.file = file
                except:
                    pass
                if orginv is not None:
                    orginv.save()

            elif is_orginv_active == 'no' and is_orginv_update == "yes":
                orginv = TrailorOrgInv.objects.filter(id=int(request.POST[f'is_orginv_id_{i}'])).first()
                orginv.delete()
                
                
        trailor_event_total_rows = int(request.POST['trailor_event_total_rows'])
        for i in range(1,trailor_event_total_rows+1):
            is_event_active = request.POST[f'is_event_active_{i}']
            is_event_update = request.POST[f'is_event_update_{i}']
            if is_event_active == 'yes':
                event_remarks = request.POST.get(f'event_remarks_{i}',None)
                date = request.POST.get(f'event_date_{i}',None)
               
                if is_event_update == "yes":
                    event = TrailorEventBook.objects.filter(id=int(request.POST[f'is_event_id_{i}'])).first()
                    event.event_remarks = event_remarks
                   
                else:
                    if permit_no:
                        event = TrailorEventBook.objects.create(
                            trailor = form.instance,
                            event_remarks = event_remarks,
                            
                        ) 
                    else:
                        event = None
                if date:
                    event.date = date
               
                if event is not None:
                    event.save()

            elif is_event_active == 'no' and is_event_update == "yes":
                event = TrailorEventBook.objects.filter(id=int(request.POST[f'is_event_id_{i}'])).first()
                event.delete()
        
        trailor_service_total_rows = int(request.POST['trailor_service_total_rows'])
        for i in range(1,trailor_service_total_rows+1):
            is_service_active = request.POST[f'is_service_active_{i}']
            is_service_update = request.POST[f'is_service_update_{i}']
            if is_service_active == 'yes':
                service_date = request.POST.get(f'service_date_{i}',None)
                next_due_date = request.POST.get(f'next_due_date_{i}',None)
                place = request.POST.get(f'place_{i}',None)
                expense_amount = request.POST.get(f'expense_amount_{i}',0)
                remarks = request.POST.get(f'service_remarks_{i}',None)
               
                if is_service_update == "yes":
                    service = TrailorService.objects.filter(id=int(request.POST[f'is_service_id_{i}'])).first()
                    service.remarks = remarks
                    service.place = place
                   
                else:
                    if service_date:
                        service = TrailorService.objects.create(
                            trailor = form.instance,
                           
                            remarks = remarks,
                            place = place,
                        ) 
                    else:
                        service = None
               
               
                if service is not None:
                    if service_date:
                        service.service_date = service_date
                        
                    if expense_amount:
                        service.expense_amount = expense_amount
                
                
                    if next_due_date:
                        service.next_due_date = next_due_date
                    service.save()

            elif is_service_active == 'no' and is_service_update == "yes":
                service = TrailorService.objects.filter(id=int(request.POST[f'is_service_id_{i}'])).first()
                service.delete()
        
        trailor_acessory_total_rows = int(request.POST['trailor_acessory_total_rows'])
        for i in range(1,trailor_acessory_total_rows+1):
            is_acessory_active = request.POST[f'is_acessory_active_{i}']
            is_acessory_update = request.POST[f'is_acessory_update_{i}']
            if is_acessory_active == 'yes':
                acessory = request.POST.get(f'acessory_{i}',None)
                from_date = request.POST.get(f'acessory_from_date_{i}',None)
                to_date = request.POST.get(f'acessory_to_date_{i}',None)
                price = request.POST.get(f'price_{i}',0)
                remarks = request.POST.get(f'service_remarks_{i}',None)
               
                if is_acessory_update == "yes":
                    trailor_acessory = TrailorAcessory.objects.filter(id=int(request.POST[f'is_acessory_id_{i}'])).first()
                    trailor_acessory.remarks = remarks
                    trailor_acessory.price = price
                    trailor_acessory.acessory = acessory
                   
                else:
                    if acessory and from_date:
                        trailor_acessory = TrailorAcessory.objects.create(
                            trailor = form.instance,
                            remarks = remarks,
                            price = price,
                            acessory = acessory,
                        ) 
                 
                if from_date:
                    trailor_acessory.from_date = from_date
                 
                if to_date:
                    trailor_acessory.to_date = to_date
                
             
                if trailor_acessory is not None:
                    trailor_acessory.save()

            elif is_acessory_active == 'no' and is_acessory_update == "yes":
                trailor_acessory = TrailorAcessory.objects.filter(id=int(request.POST[f'is_acessory_id_{i}'])).first()
                trailor_acessory.delete()
                
        trailor_location_total_rows = int(request.POST['trailor_location_total_rows'])
        for i in range(1,trailor_location_total_rows+1):
            is_location_active = request.POST[f'is_location_active_{i}']
            is_location_update = request.POST[f'is_location_update_{i}']
            if is_location_active == 'yes':
                location = request.POST.get(f'location_{i}',None)
                if location:
                    location = Location.objects.filter(id=int(location)).first()
                from_date = request.POST.get(f'location_date_{i}',None)
                employee = request.POST.get(f'employee_{i}',None)
                if employee:
                    employee = Employee.objects.filter(id=int(employee)).first()
               
                remarks = request.POST.get(f'location_remarks_{i}',None)
               
                if is_location_update == "yes":
                    trailor_location = TrailorLocation.objects.filter(id=int(request.POST[f'is_location_id_{i}'])).first()
                    trailor_location.location = location
                    trailor_location.employee = employee
                    trailor_location.remarks = remarks
                   
                else:
                    if location and employee:
                        trailor_location = TrailorLocation.objects.create(
                            trailor = form.instance,
                            location = location,
                            employee = employee,
                            remarks = remarks,
                        ) 
                 
                if from_date:
                    trailor_location.from_date = from_date
                
                if trailor_location is not None:
                    trailor_location.save()

            elif is_location_active == 'no' and is_location_update == "yes":
                trailor_location = TrailorLocation.objects.filter(id=int(request.POST[f'is_location_id_{i}'])).first()
                trailor_location.delete()
                
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:trailor_details',module=module)
    
    
    drivers = DriverMaster.objects.all()
    horse_tyres = Tyre.objects.filter(type="HORSE").all()
    trolley_tyres = Tyre.objects.filter(type="TROLLEY").all()

    context['form']= form
    context['module']= module
    context['update']= True
    context['obj']= obj
    context['drivers']= drivers
    context['horse_tyres']= horse_tyres
    context['trolley_tyres']= trolley_tyres
    return render(request,'trailor/trailor_create.html',context)



@login_required(login_url='home:handle_login')
def trailor_delete(request,module,id):
    check_permissions(request,module)
    trailor = TrailorMaster.objects.filter(id=int(id)).first()
    trailor.delete()
    return redirect('masters:trailor_details',module=module)


    

# ------------------Department Master----------------
@login_required(login_url='home:handle_login')
def create_department(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Department Created.")
        return redirect('masters:create_department',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'department/department_create.html',context)


@login_required(login_url='home:handle_login')
def department_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Department.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'department/department_details.html',context)


@login_required(login_url='home:handle_login')
def department_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Department, id = id)
    
    form = DepartmentForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:department_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'department/department_create.html',context)

@login_required(login_url='home:handle_login')
def department_delete(request,module,id):
    check_permissions(request,module)
    department = Department.objects.filter(id=int(id)).first()
    department.delete()
    return redirect('masters:department_details',module=module)

# ------------------Designation Master----------------
@login_required(login_url='home:handle_login')
def create_designation(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = DesignationForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Designation Created.")
        return redirect('masters:create_designation',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'designation/designation_create.html',context)


@login_required(login_url='home:handle_login')
def designation_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Designation.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'designation/designation_details.html',context)


@login_required(login_url='home:handle_login')
def designation_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Designation, id = id)
    
    form = DesignationForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:designation_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'designation/designation_create.html',context)

@login_required(login_url='home:handle_login')
def designation_delete(request,module,id):
    check_permissions(request,module)
    designation = Designation.objects.filter(id=int(id)).first()
    designation.delete()
    return redirect('masters:designation_details',module=module)


# ------------------Employee Master----------------
@login_required(login_url='home:handle_login')
def create_employee(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Employee Created.")
        return redirect('masters:create_employee',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'employee/employee_create.html',context)


@login_required(login_url='home:handle_login')
def employee_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Employee.objects.all()
          
    context['data']= data
    context['module']= module
    return render(request,'employee/employee_details.html',context)


@login_required(login_url='home:handle_login')
def employee_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Employee, id = id)
    
    form = EmployeeForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('masters:employee_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'employee/employee_create.html',context)

@login_required(login_url='home:handle_login')
def employee_delete(request,module,id):
    check_permissions(request,module)
    employee = Employee.objects.filter(id=int(id)).first()
    employee.delete()
    return redirect('masters:employee_details',module=module)



#----------------------- User ----------------------------

@login_required(login_url='home:handle_login')
def create_user(request,module):
    check_permissions(request,module)
    offices = Logistic.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        username = request.POST['username']
        
        office = Logistic.objects.filter(id=int(request.POST['office'])).first()
        
        user = User.objects.filter(username=username).first()
        if not user:
            is_admin = request.POST.get('is_admin',False)
            if is_admin:
                is_admin = True
                
            is_sea_export = request.POST.get('is_sea_export',False)
            if is_sea_export:
                is_sea_export = True

            is_sea_import = request.POST.get('is_sea_import',False)
            if is_sea_import:
                is_sea_import = True

            is_air_export = request.POST.get('is_air_export',False)
            if is_air_export:
                is_air_export = True

            is_air_import = request.POST.get('is_air_import',False)
            if is_air_import:
                is_air_import = True

            is_finance = request.POST.get('is_finance',False)
            if is_finance:
                is_finance = True

            is_crm = request.POST.get('is_crm',False)
            if is_crm:
                is_crm = True

            is_bi = request.POST.get('is_bi',False)
            if is_bi:
                is_bi = True

            is_operations = request.POST.get('is_operations',False)
            if is_operations:
                is_operations = True
            
            can_report = request.POST.get('can_report',False)
            if can_report:
                can_report = True
            
            see_global_data = request.POST.get('see_global_data',False)
            if see_global_data:
                see_global_data = True
            
            can_delete = request.POST.get('can_delete',False)
            if can_delete:
                can_delete = True
            
            create_global_data = request.POST.get('create_global_data',False)
            if create_global_data:
                create_global_data = True
            
            also_handle_other_work = request.POST.get('also_handle_other_work',False)
            if also_handle_other_work:
                also_handle_other_work = True
            
            is_transportation = request.POST.get('is_transportation',False)
            if is_transportation:
                is_transportation = True
           
            handle_masters = request.POST.get('handle_masters',False)
            if handle_masters:
                handle_masters = True
                
            is_hr = request.POST.get('is_hr',False)
            if is_hr:
                is_hr = True
           
            is_special_access = request.POST.get('is_special_access',False)
            if is_special_access:
                is_special_access = True

            
            if password == confirm_password:
                new_user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username=username,
                    email = email,
                    password = password,
                    is_superuser = is_admin
                )
                new_user.save()
                
                new_user_account = UserAccount.objects.create(
                    user = new_user,
                    is_sea_export = is_sea_export,
                    is_sea_import = is_sea_import,
                    is_air_export = is_air_export,
                    is_air_import = is_air_import,
                    is_finance = is_finance,
                    is_transportation=is_transportation,
                    is_crm = is_crm,
                    is_bi = is_bi,
                    is_operations = is_operations,
                    can_report = can_report,
                    also_handle_other_work=also_handle_other_work,
                    see_global_data = see_global_data,
                    office = office,
                    can_delete = can_delete,
                    handle_masters = handle_masters,
                    is_hr = is_hr,
                    is_special_access = is_special_access,
                    create_global_data=create_global_data
                )
                new_user_account.save()
                
                messages.add_message(request, messages.SUCCESS, f"Success, New Employee in {office.company_name} registered Successfully.")
        
    context = {
        'module':module,
        'offices':offices,
    }
    
    return render(request,'users/create_user.html',context)

@login_required(login_url='home:handle_login')
def update_user(request,module,id):
    check_permissions(request,module)
    user = User.objects.filter(id=id).first()
    offices = Logistic.objects.all()
    user_account = UserAccount.objects.filter(user=user).first()
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['username']
        
        office = Logistic.objects.filter(id=int(request.POST['office'])).first()
        
        user.is_superuser = request.POST.get('is_admin',False)
        if user.is_superuser:
            user.is_superuser = True
            
        user_account.office = office
            
        user_account.is_sea_export = request.POST.get('is_sea_export',False)
        if user_account.is_sea_export:
            user_account.is_sea_export = True

        user_account.is_sea_import = request.POST.get('is_sea_import',False)
        if user_account.is_sea_import:
            user_account.is_sea_import = True

        user_account.is_air_export = request.POST.get('is_air_export',False)
        if user_account.is_air_export:
            user_account.is_air_export = True

        user_account.is_air_import = request.POST.get('is_air_import',False)
        if user_account.is_air_import:
            user_account.is_air_import = True

        user_account.is_finance = request.POST.get('is_finance',False)
        if user_account.is_finance:
            user_account.is_finance = True

        user_account.is_crm = request.POST.get('is_crm',False)
        if user_account.is_crm:
            user_account.is_crm = True

        user_account.is_bi = request.POST.get('is_bi',False)
        if user_account.is_bi:
            user_account.is_bi = True

        user_account.is_operations = request.POST.get('is_operations',False)
        if user_account.is_operations:
            user_account.is_operations = True

        user_account.can_report = request.POST.get('can_report',False)
        if user_account.can_report:
            user_account.can_report = True

        user_account.see_global_data = request.POST.get('see_global_data',False)
        if user_account.see_global_data:
            user_account.see_global_data = True
        
        user_account.create_global_data = request.POST.get('create_global_data',False)
        if user_account.create_global_data:
            user_account.create_global_data = True
        
        user_account.also_handle_other_work = request.POST.get('also_handle_other_work',False)
        if user_account.also_handle_other_work:
            user_account.also_handle_other_work = True
       
        user_account.is_transportation = request.POST.get('is_transportation',False)
        if user_account.is_transportation:
            user_account.is_transportation = True
            
        user_account.can_delete = request.POST.get('can_delete',False)
        if user_account.can_delete:
            user_account.can_delete = True
       
        user_account.handle_masters = request.POST.get('handle_masters',False)
        if user_account.handle_masters:
            user_account.handle_masters = True
            
        user_account.is_hr = request.POST.get('is_hr',False)
        if user_account.is_hr:
            user_account.is_hr = True
        
        user_account.is_special_access = request.POST.get('is_special_access',False)
        if user_account.is_special_access:
            user_account.is_special_access = True

        user.save()
        user_account.save() 
        
        messages.add_message(request, messages.SUCCESS, f"Success, Existing Employee in {office.company_name} updated Successfully.")
        
        return redirect('masters:user_list', module=module)
       
    context = {
        'module':module,
        'user':user,
        'user_account':user_account,
        'offices':offices
    }
    
    return render(request,'users/user_update.html',context)

@login_required(login_url='home:handle_login')
def user_list(request,module):
    check_permissions(request,module)
    users = User.objects.exclude(id=request.user.id).all()
    context = {
        'users':users,
        'module':module
    }
    return render(request,'users/user_details.html',context)

@login_required(login_url='home:handle_login')
def user_delete(request,module,id):
    check_permissions(request,module)
    users = User.objects.filter(id=id).first()
    users.delete()
    return redirect('masters:user_list', module=module)

# --------------------- Company ---------------------

@login_required(login_url='home:handle_login')
def create_company(request,module):
    check_permissions(request,module)
   
    if request.method == 'POST':     
        
        pre_recievable_invoice = request.POST['pre_recievable_invoice']
        company_gst_code = request.POST['company_gst_code']
        branch_name = request.POST['branch_name']
        tax_policy = request.POST['tax_policy']
        pre_payable_invoice = request.POST['pre_payable_invoice']
        pre_payment_voucher = request.POST['pre_payment_voucher']
        pre_recieve_voucher = request.POST['pre_recieve_voucher']
        gstin_no = request.POST['gstin_no']
        pre_credit_note = request.POST['pre_credit_note']
        pre_debit_note = request.POST['pre_debit_note']
        pre_inquiry = request.POST['pre_inquiry']
        for_company = request.POST['for_company']
        company_name = request.POST['company_name']
        pre_job = request.POST['pre_job']
        vgm_authorized_shipper = request.POST['vgm_authorized_shipper']
        legal_name = request.POST['legal_name']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        branch_email = request.POST['branch_email']
        pin_code = request.POST['pin_code']
        phone = request.POST['phone']
        mbl_prefix = request.POST['mbl_prefix']
        opening_invoice_no = request.POST['opening_invoice_no']
        rcm_cn_prefix = request.POST['rcm_cn_prefix']
        rcm_ri_prefix = request.POST['rcm_ri_prefix']
        open_time = request.POST.get('open_time',None)
        close_time = request.POST.get('close_time',None)
        
        is_connected_to_tally = request.POST.get('is_connected_to_tally',False)
        if is_connected_to_tally:
            is_connected_to_tally = True
        
        is_job_approve_required = request.POST.get('is_job_approve_required',False)
        if is_job_approve_required:
            is_job_approve_required = True
            
        is_rec_inv_approve_required = request.POST.get('is_rec_inv_approve_required',False)
        if is_rec_inv_approve_required:
            is_rec_inv_approve_required = True
        
        is_pay_inv_approve_required = request.POST.get('is_pay_inv_approve_required',False)
        if is_pay_inv_approve_required:
            is_pay_inv_approve_required = True
        
        is_can_approve_required = request.POST.get('is_can_approve_required',False)
        if is_can_approve_required:
            is_can_approve_required = True
        
        is_do_approve_required = request.POST.get('is_do_approve_required',False)
        if is_do_approve_required:
            is_do_approve_required = True
      
        is_fc_approve_required = request.POST.get('is_fc_approve_required',False)
        if is_fc_approve_required:
            is_fc_approve_required = True
        
        is_crn_approve_required = request.POST.get('is_crn_approve_required',False)
        if is_crn_approve_required:
            is_crn_approve_required = True
        
        is_drn_approve_required = request.POST.get('is_drn_approve_required',False)
        if is_drn_approve_required:
            is_drn_approve_required = True
            
        auto_journal = request.POST.get('auto_journal',False)
        if auto_journal:
            auto_journal = True
        
            
        new_company = Logistic(
            pre_recievable_invoice = pre_recievable_invoice,
            company_gst_code = company_gst_code,
            branch_name=branch_name,
            pre_payable_invoice = pre_payable_invoice,
            pre_payment_voucher = pre_payment_voucher,
            pre_recieve_voucher = pre_recieve_voucher,
            pre_credit_note = pre_credit_note,
            pre_inquiry = pre_inquiry,
            pre_debit_note = pre_debit_note,
            for_company = for_company,
            company_name = company_name,
            opening_invoice_no = opening_invoice_no,
            tax_policy=tax_policy,
            pre_job = pre_job,
            vgm_authorized_shipper = vgm_authorized_shipper,
            branch_email=branch_email,
            rcm_cn_prefix=rcm_cn_prefix,
            rcm_ri_prefix=rcm_ri_prefix,
           
            is_connected_to_tally=is_connected_to_tally,
            
            is_job_approve_required=is_job_approve_required,
            is_rec_inv_approve_required=is_rec_inv_approve_required,
            is_pay_inv_approve_required=is_pay_inv_approve_required,
            is_can_approve_required=is_can_approve_required,
            is_do_approve_required=is_do_approve_required,
            is_fc_approve_required=is_fc_approve_required,
            is_crn_approve_required=is_crn_approve_required,
            is_drn_approve_required=is_drn_approve_required,
            auto_journal=auto_journal,
            gstin_no=gstin_no,
            legal_name=legal_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            pin_code=pin_code,
            phone=phone,
            mbl_prefix=mbl_prefix,
       
        )
        if open_time:
            new_company.open_time = open_time
        if close_time:
            new_company.close_time = close_time
        new_company.save()
        
        try:
            company_logo = request.FILES['company_logo']
            new_company.logo = company_logo
        except:
            pass
        
        try:
            company_letter_head = request.FILES['company_letter_head']
            new_company.letter_head = company_letter_head
        except:
            pass
        
        try:
            company_stamp = request.FILES['company_stamp']
            new_company.stamp = company_stamp
        except:
            pass
       
       
        try:
            mbl_final_image = request.FILES['mbl_final_image']
            new_company.mbl_final_image = mbl_final_image
        except:
            pass
        new_company.save()
        
        messages.add_message(request, messages.SUCCESS, f"Success, New Company {company_name} created Successfully.")
    
    context = {
        'module':module
    }
    
    return render(request,'company/create_company.html',context)


@login_required(login_url='home:handle_login')
def company_details(request,module):
    context ={}
    check_permissions(request,module)
  
    companies = Logistic.objects.all()
          
    context['companies']= companies
    context['module']= module
    return render(request,'company/company_details.html',context)


@login_required(login_url='home:handle_login')
def update_company(request,module,id):
    check_permissions(request,module)
    logistics = Logistic.objects.filter(id=id).first()
    if request.method == 'POST':     
        if logistics:
            try:
                company_logo = request.FILES['company_logo']
                logistics.logo = company_logo
            except:
                pass
            
            try:
                company_letter_head = request.FILES['company_letter_head']
                logistics.letter_head = company_letter_head
            except:
                pass
            
            try:
                company_stamp = request.FILES['company_stamp']
                logistics.stamp = company_stamp
            except:
                pass
            
            try:
                mbl_final_image = request.FILES['mbl_final_image']
                logistics.mbl_final_image = mbl_final_image
            except:
                pass
            
            logistics.branch_name = request.POST['branch_name']
            logistics.tax_policy = request.POST['tax_policy']
            logistics.pre_recievable_invoice = request.POST['pre_recievable_invoice']
            logistics.company_gst_code = request.POST['company_gst_code']
            logistics.pre_inquiry = request.POST['pre_inquiry']
            logistics.pre_payable_invoice = request.POST['pre_payable_invoice']
            logistics.pre_payment_voucher = request.POST['pre_payment_voucher']
            logistics.pre_recieve_voucher = request.POST['pre_recieve_voucher']
            logistics.pre_credit_note = request.POST['pre_credit_note']
            logistics.pre_debit_note = request.POST['pre_debit_note']
            logistics.for_company = request.POST['for_company']
            logistics.company_name = request.POST['company_name']
            logistics.pre_job = request.POST['pre_job']
            logistics.branch_email = request.POST['branch_email']
            logistics.gstin_no = request.POST['gstin_no']
            logistics.legal_name = request.POST['legal_name']
            logistics.opening_invoice_no = request.POST['opening_invoice_no']
            logistics.address_line_1 = request.POST['address_line_1']
            logistics.address_line_2 = request.POST['address_line_2']
            logistics.pin_code = request.POST['pin_code']
            logistics.phone = request.POST['phone']
            logistics.vgm_authorized_shipper = request.POST['vgm_authorized_shipper']
            logistics.mbl_prefix = request.POST['mbl_prefix']
            logistics.rcm_cn_prefix = request.POST['rcm_cn_prefix']
            logistics.rcm_ri_prefix = request.POST['rcm_ri_prefix']
            
            open_time = request.POST.get('open_time',None)
            close_time = request.POST.get('close_time',None)
            if open_time:
                logistics.open_time = open_time
            if close_time:
                
                logistics.close_time = close_time
            
            logistics.auto_journal = request.POST.get('auto_journal',False)
            if logistics.auto_journal:
                logistics.auto_journal = True
            
            logistics.is_connected_to_tally = request.POST.get('is_connected_to_tally',False)
            if logistics.is_connected_to_tally:
                logistics.is_connected_to_tally = True
            
            # 
            logistics.is_job_approve_required = request.POST.get('is_job_approve_required',False)
            if logistics.is_job_approve_required:
                logistics.is_job_approve_required = True
            
            # 
            logistics.is_rec_inv_approve_required = request.POST.get('is_rec_inv_approve_required',False)
            if logistics.is_rec_inv_approve_required:
                logistics.is_rec_inv_approve_required = True
            
            # 
            logistics.is_pay_inv_approve_required = request.POST.get('is_pay_inv_approve_required',False)
            if logistics.is_pay_inv_approve_required:
                logistics.is_pay_inv_approve_required = True
            
            # 
            logistics.is_can_approve_required = request.POST.get('is_can_approve_required',False)
            if logistics.is_can_approve_required:
                logistics.is_can_approve_required = True
            
            # 
            logistics.is_do_approve_required = request.POST.get('is_do_approve_required',False)
            if logistics.is_do_approve_required:
                logistics.is_do_approve_required = True
            
            # 
            logistics.is_fc_approve_required = request.POST.get('is_fc_approve_required',False)
            if logistics.is_fc_approve_required:
                logistics.is_fc_approve_required = True
            
            # 
            logistics.is_crn_approve_required = request.POST.get('is_crn_approve_required',False)
            if logistics.is_crn_approve_required:
                logistics.is_crn_approve_required = True
            
            # 
            logistics.is_drn_approve_required = request.POST.get('is_drn_approve_required',False)
            if logistics.is_drn_approve_required:
                logistics.is_drn_approve_required = True
            
            
            
            
            logistics.save()
            
            messages.add_message(request, messages.SUCCESS, f"Success, {logistics.company_name} updated Successfully.")
        
    
    context = {
        'logistics':logistics,
        'module':module,
        'update':True
    }
    
    return render(request,'company/create_company.html',context)

@login_required(login_url='home:handle_login')
def company_delete(request,module,id):
    check_permissions(request,module)
    company = Logistic.objects.filter(id=int(id)).first()
    messages.add_message(request, messages.SUCCESS, f"Success, {company.company_name} deleted Successfully.")
    company.delete()
    return redirect('masters:company_details',module=module)



def check_purchase_invoice(data):
    for i in range(0,len(data)):
        try:
            purchase = InvoicePayable.objects.filter(purchase_invoice_no=data['invoice_no'][i]).first()
            if purchase:
                if int(data['net_amount'][i]) == int(purchase.net_amount):
                    purchase.is_checked = True
                    purchase.save()
                else:
                    print(data['invoice_no'][i])
            else:
                print(data['invoice_no'][i])
        except:
            pass
        
def check_purchase_invoice_bh(data):
    for i in range(0,len(data)):
        purchase = InvoicePayableDetail.objects.filter(invoice_payable__invoice_no=data['invoice_payable'][i]).filter(billing_head__billing_head=data['billing_head'][i]).first()
        if purchase:
            if float(data['total'][i]) == float(purchase.total):
                purchase.is_checked = True
                purchase.save()
            else:
                print(data['invoice_payable'][i])
        else:
            print(data['invoice_payable'][i])



@login_required(login_url='home:handle_login')
def upload_master(request,module):
    check_permissions(request,module)
   
    if request.method == 'POST':
        country_upload = request.POST.get('country_upload',False)
        state_upload = request.POST.get('state_upload',False)
        city_upload = request.POST.get('city_upload',False)
        sea_port_upload = request.POST.get('sea_port_upload',False)
        air_port_upload = request.POST.get('air_port_upload',False)
        location_upload = request.POST.get('location_upload',False)
        currency_upload = request.POST.get('currency_upload',False)
        shipping_line_upload = request.POST.get('shipping_line_upload',False)
        air_line_upload = request.POST.get('air_line_upload',False)
        billing_head_upload = request.POST.get('billing_head_upload',False)
        party_master_upload = request.POST.get('party_master_upload',False)
        job_upload = request.POST.get('job_upload',False)
        rinv_upload = request.POST.get('rinv_upload',False)
        pinv_upload = request.POST.get('pay_upload',False)
        ledger_category_upload = request.POST.get('ledger_category_upload',False)
        crn_upload = request.POST.get('crn_upload',False)
        drn_upload = request.POST.get('drn_upload',False)
        match_file_upload = request.POST.get('match_file_upload',False)
        
        
        if match_file_upload:
            file_type = request.POST['file_type']
            file = request.FILES['match_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                if file_type == "Purchase":
                    check_purchase_invoice(data)
               
                if file_type == "PurchaseBH":
                    check_purchase_invoice_bh(data)
        
        
        # For Country
        if country_upload:
            country_name = request.POST['country_name']
            
            file = request.FILES['country_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[country_name][i]
                    name = name.strip()
                    try:
                        old_check = Country.objects.filter(name=name).first()
                        if not old_check:
                            new_country = Country.objects.create(name=name)
                            new_country.save()
                    except:
                        pass
        
        # For Currency  
        if currency_upload: 
            currency_name_field = request.POST['currency_name']
            currency_short_name_field = request.POST['currency_short_name']
            file = request.FILES['currency_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[currency_name_field][i]
                    name = name.strip()
                    short_name = data[currency_short_name_field][i]
                    short_name = short_name.strip()
                    try:
                        old_check = currency.objects.filter(name=name).first()
                        if not old_check:
                            new_currency = currency.objects.create(name=name,short_name=short_name)
                            new_currency.save()
                    except:
                        pass
            
        # For State 
        if state_upload:
            state_name_field_name = request.POST['state_name']
            gst_code_field_name = request.POST['gst_code']
            file = request.FILES['state_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[state_name_field_name][i]
                    name = name.strip()
                    gst_code = data[gst_code_field_name][i]
                    
                    try:
                        old_check = State.objects.filter(name=name).first()
                        if not old_check:
                            new_state = State.objects.create(name=name,gst_code=gst_code)
                            new_state.save()
                    except:
                        pass                    
        # Sea Ports
        if sea_port_upload:
            sea_port_name_field = request.POST['sea_port_name']
            file = request.FILES['sea_port_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[sea_port_name_field][i]
                    name = name.strip()
                    type =  'Sea'
                    try:
                        old_check = Ports.objects.filter(name=name).filter(type='Sea').first()
                        if not old_check:                
                            new_port = Ports.objects.create(name=name,type=type)
                            new_port.save()
                    except:
                        pass    
        # Air Ports
        if air_port_upload:
            air_port_name_field = request.POST['air_port_name']
            file = request.FILES['air_port_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[air_port_name_field][i]
                    name = name.strip()
                    type =  'Air'
                    try:
                        old_check = Ports.objects.filter(name=name).filter(type='Air').first()
                        if not old_check:                
                            new_port = Ports.objects.create(name=name,type=type)
                            new_port.save()
                    except:
                        pass    
        # For Cities
        if city_upload:
            city_name_field_name = request.POST['city_name']
            file = request.FILES['city_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[city_name_field_name][i]
                    name = name.strip()
                    try:
                        old_check = City.objects.filter(name=name).first()
                        if not old_check:
                            new_city = City.objects.create(name=name)
                            new_city.save()
                    except:
                        pass
        # For Locations 
        if location_upload:
            location_name_field_name = request.POST['location_name']
            file = request.FILES['location_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[location_name_field_name][i]
                    name = name.strip()
                    try:
                        old_check = Location.objects.filter(name=name).first()
                        if not old_check:
                            new_location = Location.objects.create(name=name)
                            new_location.save()
                    except:
                        pass
        # For Shipping Lines 
        if shipping_line_upload:
            shipping_line_name_field_name = request.POST['shipping_line_name']
            file = request.FILES['shipping_line_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[shipping_line_name_field_name][i]
                    line_type = 'Sea'
                    try:
                        name = name.strip()
                        old_check = ShippingLines.objects.filter(name=name).first()
                        if not old_check:
                            new_shipping_line = ShippingLines.objects.create(name=name,type=line_type)
                            new_shipping_line.save()
                    except:
                        pass
        # For Air Lines 
        if air_line_upload:
            air_line_name_field_name = request.POST['air_line_name']
            file = request.FILES['air_line_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[air_line_name_field_name][i]
                    name = name.strip()
                    line_type = 'Air'
                    try:
                        old_check = Airlines.objects.filter(name=name).first()
                        if not old_check:
                            new_air_line = Airlines.objects.create(name=name,type=line_type)
                            new_air_line.save()
                    except:
                        pass
        # For Billing Heads
        if billing_head_upload:
            billing_head_name = request.POST['billing_head_name']
            billing_head_hsn_code = request.POST['billing_head_hsn_code']
            billing_head_gst_code = request.POST['billing_head_gst_code']
            file = request.FILES['billing_head_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    billing_head = data[billing_head_name][i]
                    billing_head = billing_head.strip()
                    hsn_code = data[billing_head_hsn_code][i]
                    try:
                        hsn_code = int(hsn_code)
                    except:
                        pass
                    hsn_code = str(hsn_code)
                    hsn_code = hsn_code.strip()
                    gst = data[billing_head_gst_code][i]
                    try:
                        old_check = BillingHead.objects.filter(billing_head=billing_head).first()
                        if not old_check:
                            new_billing_head = BillingHead.objects.create(billing_head=billing_head,hsn_code=hsn_code,gst=gst)
                            new_billing_head.save()
                    except:
                        pass
        
        # For Party Upload
        if party_master_upload:
            id_party_name = request.POST['id_party_name']
            id_fin_non_fin = request.POST['id_fin_non_fin']
            id_for_station = request.POST['id_for_station']
            id_Prop_company = request.POST['id_Prop_company']
            id_party_type = request.POST['id_party_type']
            id_under = request.POST['id_under']
            id_res_person = request.POST['id_res_person']
            id_party_short_name = request.POST['id_party_short_name']
            id_party_iata_code = request.POST['id_party_iata_code']
            id_corp_address_line1 = request.POST['id_corp_address_line1']
            id_corp_address_line2 = request.POST['id_corp_address_line2']
            id_corp_address_line3 = request.POST['id_corp_address_line3']
            id_corp_country = request.POST['id_corp_country']
            id_corp_state = request.POST['id_corp_state']
            id_corp_city = request.POST['id_corp_city']
            id_corp_email = request.POST['id_corp_email']
            id_corp_website = request.POST['id_corp_website']
            id_corp_gstin = request.POST['id_corp_gstin']
            id_corp_zip = request.POST['id_corp_zip']
            id_corp_fax = request.POST['id_corp_fax']
            id_corp_contact = request.POST['id_corp_contact']
            id_corp_pan = request.POST['id_corp_pan']
            id_bill_address_line1 = request.POST['id_bill_address_line1']
            id_bill_address_line2 = request.POST['id_bill_address_line2']
            id_bill_address_line3 = request.POST['id_bill_address_line3']
            id_bill_country = request.POST['id_bill_country']
            id_bill_state = request.POST['id_bill_state']
            id_bill_city = request.POST['id_bill_city']
            id_bill_email = request.POST['id_bill_email']
            id_bill_website = request.POST['id_bill_website']
            id_bill_gstin = request.POST['id_bill_gstin']
            id_bill_zip = request.POST['id_bill_zip']
            id_bill_fax = request.POST['id_bill_fax']
            id_bill_contact = request.POST['id_bill_contact']
            id_bill_pan = request.POST['id_bill_pan']
            
            file = request.FILES['party_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    party_name = data[id_party_name][i]
                    fin_non_fin = data[id_fin_non_fin][i]
                    for_station = data[id_for_station][i]
                    for_station = for_station.strip()
                    Prop_company = data[id_Prop_company][i]
                    party_type = data[id_party_type][i]
                    under = data[id_under][i]
                    res_person = data[id_res_person][i]
                    party_short_name = data[id_party_short_name][i]
                    party_iata_code = data[id_party_iata_code][i]
                    corp_address_line1 = data[id_corp_address_line1][i]
                    corp_address_line2 = data[id_corp_address_line2][i]
                    corp_address_line3 = data[id_corp_address_line3][i]
                    corp_country = data[id_corp_country][i]
                    corp_state = data[id_corp_state][i]
                    corp_state = corp_state.strip()
                    corp_city = data[id_corp_city][i]
                    corp_email = data[id_corp_email][i]
                    corp_website = data[id_corp_website][i]
                    corp_gstin = data[id_corp_gstin][i]
                    corp_zip = data[id_corp_zip][i]
                    corp_fax = data[id_corp_fax][i]
                    corp_contact = data[id_corp_contact][i]
                    corp_pan = data[id_corp_pan][i]
                    bill_address_line1 = data[id_bill_address_line1][i]
                    bill_address_line2 = data[id_bill_address_line2][i]
                    bill_address_line3 = data[id_bill_address_line3][i]
                    bill_country = data[id_bill_country][i]
                    bill_state = data[id_bill_state][i]
                    bill_state = bill_state.strip()
                    bill_city = data[id_bill_city][i]
                    bill_email = data[id_bill_email][i]
                    bill_website = data[id_bill_website][i]
                    bill_gstin = data[id_bill_gstin][i]
                    bill_zip = data[id_bill_zip][i]
                    bill_fax = data[id_bill_fax][i]
                    bill_contact = data[id_bill_contact][i]
                    bill_pan = data[id_bill_pan][i]
                    
                    check_corp_state = State.objects.filter(name=corp_state).first()
                    if not check_corp_state:
                        corp_state = State.objects.create(name=corp_state)
                        corp_state.save()
                    else:
                        corp_state = check_corp_state
                        
                    check_bill_state = State.objects.filter(name=bill_state).first()
                    if not check_bill_state:
                        bill_state = State.objects.create(name=bill_state)
                        bill_state.save()
                    else:
                        bill_state = check_bill_state
                        
                    try:
                        party = Party.objects.create(
                            party_name = party_name,
                            fin_non_fin = fin_non_fin,
                            for_station = for_station,
                            Prop_company = Prop_company,
                            party_type = party_type,
                            under = under,
                            res_person = res_person,
                            party_short_name = party_short_name,
                            party_iata_code = party_iata_code,
                            corp_address_line1 = corp_address_line1,
                            corp_address_line2 = corp_address_line2,
                            corp_address_line3 = corp_address_line3,
                            corp_country = corp_country,
                            corp_state = corp_state,
                            corp_city = corp_city,
                            corp_email = corp_email,
                            corp_website = corp_website,
                            corp_gstin = corp_gstin,
                            corp_zip = corp_zip,
                            corp_fax = corp_fax,
                            corp_contact = corp_contact,
                            corp_pan = corp_pan,
                            bill_address_line1 = bill_address_line1,
                            bill_address_line2 = bill_address_line2,
                            bill_address_line3 = bill_address_line3,
                            bill_country = bill_country,
                            bill_state = bill_state,
                            bill_city = bill_city,
                            bill_email = bill_email,
                            bill_website = bill_website,
                            bill_gstin = bill_gstin,
                            bill_zip = bill_zip,
                            bill_fax = bill_fax,
                            bill_contact = bill_contact,
                            bill_pan = bill_pan,
                        )
                        party.save()
                    except:
                        pass
        
        # For Job Upload
        if job_upload:
            company_type = request.POST['company_type']
            company_type = Logistic.objects.filter(id=int(company_type)).first()
            id_job_no = request.POST['job_no']
            id_job_date = request.POST['job_date']
            id_module = request.POST['module']
            id_job_type = request.POST['job_type']
            id_freight_term = request.POST['freight_term']
            id_shipping_line = request.POST['shipping_line']
            id_gigm = request.POST['gigm']
            id_ligm = request.POST['ligm']
            id_gigm_date = request.POST['gigm_date']
            id_ligm_date = request.POST['ligm_date']
            id_vessel_voy_name = request.POST['vessel_voy_name']
            id_vessel_voy_date = request.POST['vessel_voy_date']
            id_do_no = request.POST['do_no']
            id_uin = request.POST['uin']
            id_mbl_no = request.POST['mbl_no']
            id_mbl_date = request.POST['mbl_date']
            id_hbl_no = request.POST['hbl_no']
            id_hbl_date = request.POST['hbl_date']
            id_booking_party = request.POST['booking_party']
            id_overseas_agent = request.POST['overseas_agent']
            id_broker = request.POST['broker']
            id_cfs_in_date = request.POST['cfs_in_date']
            id_po_no = request.POST['po_no']
            id_do_date = request.POST['do_date']
            id_stuffing_date = request.POST['stuffing_date']
            id_rail_out_date = request.POST['rail_out_date']
            id_sailing_date = request.POST['sailing_date']
            id_air_line = request.POST['air_line']
            id_docket_no = request.POST['docket_no']
            id_awb_no = request.POST['awb_no']
            id_awb_date = request.POST['awb_date']
            id_flight_no = request.POST['flight_no']
            id_igm_no = request.POST['igm_no']
            id_clearance = request.POST['clearance']
            id_currency_var = request.POST['currency_var']
            id_account = request.POST['account']
            id_shipper = request.POST['shipper']
            id_consignee = request.POST['consignee']
            id_notify_party = request.POST['notify_party']
            id_place_of_reciept = request.POST['place_of_reciept']
            id_goods_reciept = request.POST['goods_reciept']
            id_cargo_nature = request.POST['cargo_nature']
            
            id_port_of_loading = request.POST['port_of_loading']
            id_final_destination = request.POST['final_destination']
            id_forwarder = request.POST['forwarder']
            
            id_port_of_discharge = request.POST['port_of_discharge']
            id_commodity = request.POST['commodity']
            id_container_no = request.POST['container_no']
            id_container_type = request.POST['container_type']
            id_sales_person = request.POST['sales_person']
            id_commodity_type = request.POST['commodity_type']
            id_no_of_packages = request.POST['no_of_packages']
            id_packages_type = request.POST['packages_type']
            id_volume = request.POST['volume']
            id_gross_weight = request.POST['gross_weight']
            id_net_weight = request.POST['net_weight']
            id_cbm = request.POST['cbm']
            id_shipper_invoice_no = request.POST['shipper_invoice_no']
            id_shipper_invoice_date = request.POST['shipper_invoice_date']
            id_eta_date = request.POST['eta_date']
            id_etd_date = request.POST['etd_date']
            id_actual_arrival_pod_date = request.POST['actual_arrival_pod_date']
            id_job_status = request.POST['job_status']
            id_remarks = request.POST['remarks']
            id_ship_bill_no = request.POST['ship_bill_no']
            id_booking_no = request.POST['booking_no']
            id_igm_date = request.POST['igm_date']
            id_status = request.POST['status']
            id_created_on = request.POST['created_on']
            id_cfs_port_name = request.POST['cfs_port_name']
            id_class_name = request.POST['class_name']
            id_importer = request.POST['importer']
            file = request.FILES['job_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
         
                lenOfData = len(data)
                for i in range(0,lenOfData):
                    # try:
                    job_no = data[id_job_no][i]
                
                    job = JobMaster.objects.filter(job_no = job_no).first()
                
                    job_date = data[id_job_date][i] if not data[id_job_date][i] == "None" else None
                    if not job and not job_date == None:
                        module = data[id_module][i] if not data[id_module][i] == "None" else None
                        job_type = data[id_job_type][i] if not data[id_job_type][i] == "None" else None
                        freight_term = data[id_freight_term][i] if not data[id_freight_term][i] == "None" else None
                        shipping_line = data[id_shipping_line][i]
                        shipping_line = ShippingLines.objects.filter(name=shipping_line).first() if not data[id_shipping_line][i] == "None" else None
                    
                        gigm = data[id_gigm][i] if not data[id_gigm][i] =="None" else None
                        ligm = data[id_ligm][i] if not data[id_ligm][i] =="None" else None
                        gigm_date = data[id_gigm_date][i] if not data[id_gigm_date][i] =="None" else None
                        ligm_date = data[id_ligm_date][i] if not data[id_ligm_date][i] =="None" else None
                        vessel_voy_name = data[id_vessel_voy_name][i] if not data[id_vessel_voy_name][i] =="None" else None
                        vessel_voy_date = data[id_vessel_voy_date][i] if not data[id_vessel_voy_date][i] =="None" else None
                        do_no = data[id_do_no][i] if not data[id_do_no][i] =="None" else None
                        mbl_no = data[id_mbl_no][i] if not data[id_mbl_no][i] =="None" else None
                        mbl_date = data[id_mbl_date][i] if not data[id_mbl_date][i] =="None" else None
                        hbl_no = data[id_hbl_no][i] if not data[id_hbl_no][i] =="None" else None
                        hbl_date = data[id_hbl_date][i] if not data[id_hbl_date][i] =="None" else None
                        booking_party = data[id_booking_party][i]
                        booking_party = Party.objects.filter(party_name=booking_party).first() if not data[id_booking_party][i] == "None" else None
                        overseas_agent = data[id_overseas_agent][i]
                        overseas_agent = Party.objects.filter(party_name=overseas_agent).first() if not data[id_overseas_agent][i] == "None" else None
                        broker = data[id_broker][i]
                        broker = Party.objects.filter(party_name=broker).first() if not data[id_broker][i] == "None" else None
                        po_no = data[id_po_no][i] if not data[id_po_no][i] == "None" else None
                        do_date = data[id_do_date][i] if not data[id_do_date][i] == "None" else None
                        stuffing_date = data[id_stuffing_date][i] if not data[id_stuffing_date][i] == "None" else None
                        rail_out_date = data[id_rail_out_date][i] if not data[id_rail_out_date][i] == "None" else None
                        sailing_date = data[id_sailing_date][i] if not data[id_sailing_date][i] == "None" else None
                        air_line = data[id_air_line][i]
                        air_line = Airlines.objects.filter(name=air_line).first() if not data[id_air_line][i] else None
                        docket_no = data[id_docket_no][i] if not data[id_docket_no][i] == "None" else None
                        awb_no = data[id_awb_no][i] if not data[id_awb_no][i] == "None" else None
                        awb_date = data[id_awb_date][i] if not data[id_awb_date][i] == "None" else None
                        flight_no = data[id_flight_no][i] if not data[id_flight_no][i] == "None" else None
                        igm_no = data[id_igm_no][i] if not data[id_igm_no][i] == "None" else None
                        clearance = data[id_clearance][i]
                        clearance = Location.objects.filter(name=clearance).first() if not data[id_clearance][i] == "None" else None
                        currency_var = data[id_currency_var][i]
                        currency_var = currency.objects.filter(name=currency_var).first() if not data[id_currency_var][i] == "None" else None
                        account = data[id_account][i]
                        account = Party.objects.filter(party_name=account).first() if not data[id_account][i] == "None" else None
                        importer = data[id_importer][i]
                        importer = Party.objects.filter(party_name=importer).first() if not data[id_importer][i] == "None" else None
                        forwarder = data[id_forwarder][i]
                        forwarder = Party.objects.filter(party_name=forwarder).first() if not data[id_forwarder][i] == "None" else None
                        shipper = data[id_shipper][i]
                        shipper = Party.objects.filter(party_name=shipper).first() if not data[id_shipper][i] == "None" else None
                        consignee = data[id_consignee][i]
                        consignee = Party.objects.filter(party_name=consignee).first() if not data[id_consignee][i] == "None" else None
                        notify_party = data[id_notify_party][i]
                        notify_party = Party.objects.filter(party_name=notify_party).first() if not data[id_notify_party][i] == "None" else None
                        place_of_reciept = data[id_place_of_reciept][i]
                        place_of_reciept = Location.objects.filter(name=place_of_reciept).first() if not data[id_place_of_reciept][i] == "None" else None
                     
                        port_of_loading = data[id_port_of_loading][i]
                        port_of_loading = Ports.objects.filter(name=port_of_loading).first() if not data[id_port_of_loading][i] == "None" else None
                        final_destination = data[id_final_destination][i]
                        final_destination = Location.objects.filter(name=final_destination).first() if not data[id_final_destination][i] == "None" else None
                       
                        port_of_discharge = data[id_port_of_discharge][i]
                        port_of_discharge = Ports.objects.filter(name=port_of_discharge).first() if not data[id_port_of_discharge][i] == "None" else None
                        commodity = data[id_commodity][i] if not data[id_commodity][i] == "None" else None
                        container_no = data[id_container_no][i] if not data[id_container_no][i] == "None" else None
                        container_type = data[id_container_type][i] if not data[id_container_type][i] == "None" else None
                        sales_person = data[id_sales_person][i] if not data[id_sales_person][i] == "None" else None
                        commodity_type = data[id_commodity_type][i] if not data[id_commodity_type][i] == "None" else None
                        no_of_packages = data[id_no_of_packages][i] if not data[id_no_of_packages][i] == "None" else None
                        packages_type = data[id_packages_type][i] if not data[id_packages_type][i] == "None" else None
                        volume = data[id_volume][i] if not data[id_volume][i] == "None" else None
                        gross_weight = data[id_gross_weight][i] if not data[id_gross_weight][i] == "None" else None
                        net_weight = data[id_net_weight][i] if not data[id_net_weight][i] == "None" else None
                        cbm = data[id_cbm][i] if not data[id_cbm][i] == "None" else None
                        ship_bill_no = data[id_ship_bill_no][i] if not data[id_ship_bill_no][i] == "None" else None
                        booking_no = data[id_booking_no][i] if not data[id_booking_no][i] == "None" else None
                        shipper_invoice_no = data[id_shipper_invoice_no][i] if not data[id_shipper_invoice_no][i] == "None" else None
                        shipper_invoice_date = data[id_shipper_invoice_date][i] if not data[id_shipper_invoice_date][i] == "None" else None
                        cfs_in_date = data[id_cfs_in_date][i] if not data[id_cfs_in_date][i] == "None" else None
                        eta_date = data[id_eta_date][i] if not data[id_eta_date][i] == "None" else None
                        etd_date = data[id_etd_date][i] if not data[id_etd_date][i] == "None" else None
                        actual_arrival_pod_date = data[id_actual_arrival_pod_date][i] if not data[id_actual_arrival_pod_date][i] == "None" else None
                        job_status = data[id_job_status][i] if not data[id_job_status][i] == "None" else None
                        remarks = data[id_remarks][i] if not data[id_remarks][i] == "None" else None
                        igm_date = data[id_igm_date][i] if not data[id_igm_date][i] == "None" else None
                        status = data[id_status][i] if not data[id_status][i] == "None" else None
                        goods_reciept = data[id_goods_reciept][i] if not data[id_goods_reciept][i] == "None" else None
                        cargo_nature = data[id_cargo_nature][i] if not data[id_cargo_nature][i] == "None" else None
                        cfs_port_name = data[id_cfs_port_name][i] if not data[id_cfs_port_name][i] == "None" else None
                        class_name = data[id_class_name][i] if not data[id_class_name][i] == "None" else None
                        uin = data[id_uin][i] if not data[id_uin][i] == "None" else None
                        created_on = data[id_created_on][i] if not data[id_created_on][i] == "None" else None
                        new_job = JobMaster.objects.create(
                            company_type = company_type,
                            job_no = job_no,
                            job_date = job_date,
                            importer = importer,
                            module = module,
                            job_type = job_type,
                            freight_term = freight_term,
                            shipping_line = shipping_line,
                            gigm = gigm,
                            ligm = ligm,
                            cfs_port_name = cfs_port_name,
                            forwarder = forwarder,
                            gigm_date = gigm_date,
                            ligm_date = ligm_date,
                            vessel_voy_name = vessel_voy_name,
                            vessel_voy_date = vessel_voy_date,
                            cfs_in_date = cfs_in_date,
                            mbl_no = mbl_no,
                            mbl_date = mbl_date,
                            hbl_no = hbl_no,
                            hbl_date = hbl_date,
                            booking_party = booking_party,
                            do_no = do_no,
                            overseas_agent = overseas_agent,
                            broker = broker,
                            po_no = po_no,
                            uin = uin,
                            do_date = do_date,
                            stuffing_date = stuffing_date,
                            rail_out_date = rail_out_date,
                            sailing_date = sailing_date,
                            air_line = air_line,
                            docket_no = docket_no,
                            awb_no = awb_no,
                            awb_date = awb_date,
                            flight_no = flight_no,
                            igm_no = igm_no,
                            clearance = clearance,
                            currency = currency_var,
                            account = account,
                            shipper = shipper,
                            consignee = consignee,
                            notify_party = notify_party,
                            place_of_reciept = place_of_reciept,
                            goods_reciept = goods_reciept,
                            cargo_nature = cargo_nature,
                            
                            port_of_loading = port_of_loading,
                            final_destination = final_destination,
                           
                            port_of_discharge = port_of_discharge,
                            commodity = commodity,
                            container_no = container_no,
                            container_type = container_type,
                            sales_person = sales_person,
                            commodity_type = commodity_type,
                            no_of_packages = no_of_packages,
                            packages_type = packages_type,
                            volume = volume,
                            gross_weight = gross_weight,
                            net_weight = net_weight,
                            cbm = cbm,
                            shipper_invoice_no = shipper_invoice_no,
                            shipper_invoice_date = shipper_invoice_date,
                            eta_date = eta_date,
                            etd_date = etd_date,
                            actual_arrival_pod_date = actual_arrival_pod_date,
                            job_status = job_status,
                            remarks = remarks,
                            ship_bill_no = ship_bill_no,
                            booking_no = booking_no,
                            igm_date = igm_date,
                            class_name = class_name,
                            status = status,
                            created_at = created_on,
                            created_by = request.user,
                            is_approved = True,
                        )
                        new_job.save()
                    # except Exception as e:
                    #     message = traceback.format_exc()
                    #     print(message)
                        
           
        # For R. Inv Upload
        if rinv_upload:
            company_type = request.POST['rinv_company_type']
            company_type = Logistic.objects.filter(id=int(company_type)).first()
            id_invoice_no = request.POST.get("rinv_invoice_no",None)
            id_date_of_invoice = request.POST.get("rinv_date_of_invoice",None)
            id_job_no = request.POST.get("rinv_job_no",None)
            id_mode_of_invoice = request.POST.get("rinv_mode_of_invoice",None)
            id_bill_to = request.POST.get("rinv_bill_to",None)
            id_shipper = request.POST.get("rinv_shipper",None)
            id_shipping_line = request.POST.get("rinv_shipping_line",None)
            id_vessel_voyage_id = request.POST.get("rinv_vessel_voyage_id",None)
            id_vessel_voyage_date = request.POST.get("rinv_vessel_voyage_date",None)
            id_hbl_no = request.POST.get("rinv_hbl_no",None)
            id_mbl_no = request.POST.get("rinv_mbl_no",None)
            id_origin = request.POST.get("rinv_origin",None)
            id_destination = request.POST.get("rinv_destination",None)
            id_invoice_currency = request.POST.get("rinv_invoice_currency",None)
            id_currency_ex_rate = request.POST.get("rinv_currency_ex_rate",None)
            id_gross = request.POST.get("rinv_gross",None)
            id_volume = request.POST.get("rinv_volume",None)
            id_nett = request.POST.get("rinv_nett",None)
            id_total_packages = request.POST.get("rinv_total_packages",None)
            id_total_packages_type = request.POST.get("rinv_total_packages_type",None)
            id_total_cbm = request.POST.get("rinv_total_cbm",None)
            id_commodity = request.POST.get("rinv_commodity",None)
            id_commodity_type = request.POST.get("rinv_commodity_type",None)
            id_container_no = request.POST.get("rinv_container_no",None)
            id_container_type = request.POST.get("rinv_container_type",None)
            id_invoice_status = request.POST.get("rinv_invoice_status",None)
            id_flight_no = request.POST.get("rinv_flight_no",None)
            id_awb_no = request.POST.get("rinv_awb_no",None)
            id_docket_no = request.POST.get("rinv_docket_no",None)
            id_consignee = request.POST.get("rinv_consignee",None)
            id_air_line = request.POST.get("rinv_air_line",None)
            id_flight_date = request.POST.get("rinv_flight_date",None)
            id_type_of_invoice = request.POST.get("rinv_type_of_invoice",None)
            id_port_of_loading = request.POST.get("rinv_port_of_loading",None)
            id_port_of_discharge = request.POST.get("rinv_port_of_discharge",None)
           
            id_account_number = request.POST.get("rinv_account_number",None)
            id_gross_amount = request.POST.get("rinv_gross_amount",None)
            id_gst_amount = request.POST.get("rinv_gst_amount",None)
            id_advance_amount = request.POST.get("rinv_advance_amount",None)
            id_net_amount = request.POST.get("rinv_net_amount",None)
            id_remark_on_invoice = request.POST.get("rinv_remark_on_invoice",None)
            id_tax_status = request.POST.get("rinv_tax_status",None)
            id_sales_person = request.POST.get("rinv_sales_person",None)
            id_created_on = request.POST.get("rinv_created_on",None)
            
            id_invoice = request.POST.get('rinv_head_invoice',None)
            id_billing_head = request.POST.get('rinv_head_billing_head',None)
            id_currency = request.POST.get('rinv_head_currency',None)
            id_ex_rate = request.POST.get('rinv_head_ex_rate',None)
            id_rate = request.POST.get('rinv_head_rate',None)
            id_qty_unit = request.POST.get('rinv_head_qty_unit',None)
            id_amount = request.POST.get('rinv_head_amount',None)
            id_gst = request.POST.get('rinv_head_gst',None)
            id_gst_amount = request.POST.get('rinv_head_gst_amount',None)
            id_total = request.POST.get('rinv_head_total',None)
            
            file = request.FILES['rinv_file']
            head_file = request.FILES['rinv_head_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            filename_head = fs.save(head_file.name, head_file)
            if file and head_file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                head_data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename_head,engine='openpyxl')
                
                
                lenOfData = len(data)
                for i in range(0,lenOfData):
                    invoice_no = data[id_invoice_no][i] if not data[id_invoice_no][i] == "None" else None
                    date_of_invoice = data[id_date_of_invoice][i] if not data[id_date_of_invoice][i] == "None" else None
                    job_no = data[id_job_no][i] if not data[id_job_no][i] == "None" else None
                    if job_no:
                        job_no = JobMaster.objects.filter(job_no=job_no).first()
                    mode_of_invoice = data[id_mode_of_invoice][i] if not data[id_mode_of_invoice][i] == "None" else None
                    bill_to = data[id_bill_to][i] if not data[id_bill_to][i] == "None" else None
                    if bill_to:
                        bill_to = Party.objects.filter(party_name=bill_to).first()
                    shipper = data[id_shipper][i] if not data[id_shipper][i] == "None" else None
                    if shipper:
                        shipper = Party.objects.filter(party_name=shipper).first()
                    shipping_line = data[id_shipping_line][i]  if not data[id_shipping_line][i] == "None" else None
                    if shipping_line:
                        shipping_line = ShippingLines.objects.filter(name=shipping_line).first()
                    vessel_voyage_id = data[id_vessel_voyage_id][i] if not data[id_vessel_voyage_id][i] == "None" else None
                    vessel_voyage_date = data[id_vessel_voyage_date][i] if not data[id_vessel_voyage_date][i] == "None" else None
                    hbl_no = data[id_hbl_no][i] if not data[id_hbl_no][i] == "None" else None
                    mbl_no = data[id_mbl_no][i] if not data[id_mbl_no][i] == "None" else None
                    origin = data[id_origin][i] if not data[id_origin][i] == "None" else None
                    if origin:
                        origin = Location.objects.filter(name=origin).first()
                    destination = data[id_destination][i] if not data[id_destination][i] == "None" else None
                    if destination:
                        destination = Location.objects.filter(name=destination).first()
                    invoice_currency = data[id_invoice_currency][i] if not data[id_invoice_currency][i] == "None" else None
                    if invoice_currency:
                        invoice_currency = currency.objects.filter(short_name=invoice_currency).first()
                    currency_ex_rate = data[id_currency_ex_rate][i] if not data[id_currency_ex_rate][i] == "None" else 1
                    gross = data[id_gross][i] if not data[id_gross][i] == "None" else None
                    volume = data[id_volume][i] if not data[id_volume][i] == "None" else None
                    nett = data[id_nett][i] if not data[id_nett][i] == "None" else None
                    total_packages = data[id_total_packages][i] if not data[id_total_packages][i] == "None" else None
                    total_packages_type = data[id_total_packages_type][i] if not data[id_total_packages_type][i] == "None" else None
                    total_cbm = data[id_total_cbm][i] if not data[id_total_cbm][i] == "None" else None
                    commodity = data[id_commodity][i] if not data[id_commodity][i] == "None" else None
                    commodity_type = data[id_commodity_type][i] if not data[id_commodity_type][i] == "None" else None
                    container_no = data[id_container_no][i] if not data[id_container_no][i] == "None" else None
                    container_type = data[id_container_type][i] if not data[id_container_type][i] == "None" else None
                    invoice_status = data[id_invoice_status][i] if not data[id_invoice_status][i] == "None" else None
                    flight_no = data[id_flight_no][i] if not data[id_flight_no][i] == "None" else None
                    awb_no = data[id_awb_no][i] if not data[id_awb_no][i] == "None" else None
                    docket_no = data[id_docket_no][i] if not data[id_docket_no][i] == "None" else None
                    consignee = data[id_consignee][i] if not data[id_consignee][i] == "None" else None
                    if consignee:
                        consignee = Party.objects.filter(party_name=consignee).first()
                    air_line = data[id_air_line][i] if not data[id_air_line][i] == "None" else None
                    if air_line:
                        air_line = Airlines.objects.filter(name=air_line).first()
                    flight_date = data[id_flight_date][i] if not data[id_flight_date][i] == "None" else None
                    type_of_invoice = data[id_type_of_invoice][i] if not data[id_type_of_invoice][i] == "None" else None
                 
                    account_number = data[id_account_number][i] if not data[id_account_number][i] == "None" else None
                    if account_number:
                        account_number = Bank.objects.filter(account_no=account_number).first()
                    
                    
                    port_of_loading = data[id_port_of_loading][i] if not data[id_port_of_loading][i] == "None" else None
                    if port_of_loading:
                        port_of_loading = Ports.objects.filter(name=port_of_loading).first()
                    
                    port_of_discharge = data[id_port_of_discharge][i] if not data[id_port_of_discharge][i] == "None" else None
                    if port_of_discharge:
                        port_of_discharge = Ports.objects.filter(name=port_of_discharge).first()
                        
                    gross_amount = data[id_gross_amount][i] if not data[id_gross_amount][i] == "None" else None
                    gst_amount = data[id_gst_amount][i] if not data[id_gst_amount][i] == "None" else None
                    advance_amount = data[id_advance_amount][i] if not data[id_advance_amount][i] == "None" else None
                    net_amount = data[id_net_amount][i] if not data[id_net_amount][i] == "None" else None
                    remark_on_invoice = data[id_remark_on_invoice][i] if not data[id_remark_on_invoice][i] == "None" else None
                    tax_status = data[id_tax_status][i] if not data[id_tax_status][i] == "None" else None
                    sales_person = data[id_sales_person][i] if not data[id_sales_person][i] == "None" else None
                    created_on = data[id_created_on][i] if not data[id_created_on][i] == "None" else None
                    try:
                        new_rec_invoice = InvoiceReceivable.objects.create(
                            company_type = company_type,
                            invoice_no = invoice_no,
                            date_of_invoice = date_of_invoice,
                            job_no = job_no,
                            mode_of_invoice = mode_of_invoice,
                            bill_to = bill_to,
                            shipper = shipper,
                            shipping_line = shipping_line,
                            vessel_voyage_id = vessel_voyage_id,
                            vessel_voyage_date = vessel_voyage_date,
                            hbl_no = hbl_no,
                            mbl_no = mbl_no,
                            origin = origin,
                            destination = destination,
                            invoice_currency = invoice_currency,
                            currency_ex_rate = currency_ex_rate,
                            gross = gross,
                            volume = volume,
                            nett = nett,
                            total_packages = total_packages,
                            total_packages_type = total_packages_type,
                            total_cbm = total_cbm,
                            commodity = commodity,
                            commodity_type = commodity_type,
                            container_no = container_no,
                            container_type = container_type,
                            invoice_status = invoice_status,
                            flight_no = flight_no,
                            awb_no = awb_no,
                            docket_no = docket_no,
                            consignee = consignee,
                            air_line = air_line,
                            flight_date = flight_date,
                            type_of_invoice = type_of_invoice,
                          
                            port_of_loading = port_of_loading,
                            port_of_discharge = port_of_discharge,
                            account_number = account_number,
                            gross_amount = gross_amount,
                            gst_amount = gst_amount,
                            advance_amount = advance_amount,
                            net_amount = net_amount,
                            remark_on_invoice = remark_on_invoice,
                            tax_status = tax_status,
                            sales_person = sales_person,
                            created_at = created_on,
                            is_approved = True,
                        )
                        new_rec_invoice.save()
                    except Exception as e:
                        message = traceback.format_exc()
                        
        
                
                lenOfHeadData = len(head_data)
                for i in range(0,lenOfHeadData):
                    invoice = head_data[id_invoice][i]
                    invoice = InvoiceReceivable.objects.filter(invoice_no=invoice).first()
                    billing_head = head_data[id_billing_head][i]
                    print(billing_head)
                    billing_head = BillingHead.objects.filter(billing_head=str(billing_head)).first()
                    # print( BillingHead.objects.filter(billing_head=str(billing_head)).first())
                    inv_currency = head_data[id_currency][i]
                    inv_currency = currency.objects.filter(short_name=inv_currency).first()
                    ex_rate = head_data[id_ex_rate][i]
                    rate = head_data[id_rate][i]
                    qty_unit = head_data[id_qty_unit][i]
                    amount = head_data[id_amount][i]
                    gst = head_data[id_gst][i]
                    gst_amount = head_data[id_gst_amount][i]
                    total = head_data[id_total][i]
                    # try:
                    new_rec_invoice_head = InvoiceReceivableDetail.objects.create(
                        invoice_receivable = invoice,
                        billing_head = billing_head,
                        currency = inv_currency,
                        ex_rate = ex_rate,
                        rate = rate,
                        qty_unit = qty_unit,
                        amount = amount,
                        gst = gst,
                        gst_amount = gst_amount,
                        total = total,
                    )
                    new_rec_invoice_head.save()
                    # except Exception as e:
                    #     message = traceback.format_exc()
                    #     print(message)
                      
        
        # For P. Inv Upload
        if pinv_upload:
            company_type = request.POST['pay_company_type']
            company_type = Logistic.objects.filter(id=int(company_type)).first()
            id_purchase_invoice_no = request.POST['pay_inv_purchase_invoice_no']
            id_invoice_no = request.POST['pay_inv_invoice_no']
            id_date_of_invoice = request.POST['pay_inv_date_of_invoice']
            id_job_no = request.POST['pay_inv_job_no']
            id_bill_from = request.POST['pay_inv_bill_from']
            id_shipping_line = request.POST['pay_inv_shipping_line']
            id_invoice_currency = request.POST['pay_inv_invoice_currency']
            id_currency_ex_rate = request.POST['pay_inv_currency_ex_rate']
            id_vessel_voyage_id = request.POST['pay_inv_vessel_voyage_id']
            id_vessel_voyage_date = request.POST['pay_inv_vessel_voyage_date']
            id_air_line = request.POST['pay_inv_air_line']
            id_flight_date = request.POST['pay_inv_flight_date']
            id_invoice_status = request.POST['pay_inv_invoice_status']
            id_account_number = request.POST['pay_inv_account_number']
            id_gross_amount = request.POST['pay_inv_gross_amount']
            id_gst_amount = request.POST['pay_inv_gst_amount']
            id_advance_amount = request.POST['pay_inv_advance_amount']
            id_net_amount = request.POST['pay_inv_net_amount']
            id_remark_on_invoice = request.POST['pay_inv_remark_on_invoice']
            id_sales_person = request.POST['pay_inv_sales_person']
            id_hbl_no = request.POST['pay_inv_hbl_no']
            id_mbl_no = request.POST['pay_inv_mbl_no']
            id_origin = request.POST['pay_inv_origin']
            id_destination = request.POST['pay_inv_destination']
            id_gross = request.POST['pay_inv_gross']
            id_volume = request.POST['pay_inv_volume']
            id_nett = request.POST['pay_inv_nett']
            id_total_packages = request.POST['pay_inv_total_packages']
            id_total_packages_type = request.POST['pay_inv_total_packages_type']
            id_total_cbm = request.POST['pay_inv_total_cbm']
            id_commodity = request.POST['pay_inv_commodity']
            id_commodity_type = request.POST['pay_inv_commodity_type']
            id_container_no = request.POST['pay_inv_container_no']
            id_container_type = request.POST['pay_inv_container_type']
            id_flight_no = request.POST['pay_inv_flight_no']
            id_awb_no = request.POST['pay_inv_awb_no']
            id_docket_no = request.POST['pay_inv_docket_no']
            id_created_on = request.POST['pay_inv_created_on']
            
            
            id_invoice = request.POST.get('pay_inv_head_pay_invoice',None)
            id_billing_head = request.POST.get('pay_inv_head_billing_head',None)
            id_currency = request.POST.get('pay_inv_head_currency',None)
            id_ex_rate = request.POST.get('pay_inv_head_ex_rate',None)
            id_rate = request.POST.get('pay_inv_head_rate',None)
            id_qty_unit = request.POST.get('pay_inv_head_qty_unit',None)
            id_amount = request.POST.get('pay_inv_head_amount',None)
            id_gst = request.POST.get('pay_inv_head_gst',None)
            id_gst_amount = request.POST.get('pay_inv_head_gst_amount',None)
            id_total = request.POST.get('pay_inv_head_total',None)
            
            
            file = request.FILES['pay_file']
            head_file = request.FILES['pay_head_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            filename_head = fs.save(head_file.name, head_file)
            if file and head_file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                head_data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename_head,engine='openpyxl')
                
                
                lenOfData = len(data)
                for i in range(0,lenOfData):
                    invoice_no = data[id_invoice_no][i] if not data[id_invoice_no][i] == "None" else None
                    purchase_invoice_no = data[id_purchase_invoice_no][i] if not data[id_purchase_invoice_no][i] == "None" else None
                    date_of_invoice = data[id_date_of_invoice][i] if not data[id_date_of_invoice][i] == "None" else None
                    job_no = data[id_job_no][i] if not data[id_job_no][i] == "None" else None
                    if job_no:
                        job_no = JobMaster.objects.filter(job_no=job_no).first()
                    
                    bill_from = data[id_bill_from][i] if not data[id_bill_from][i] == "None" else None
                    if bill_from:
                        bill_from = Party.objects.filter(party_name=bill_from).first()
                   
                    shipping_line = data[id_shipping_line][i]  if not data[id_shipping_line][i] == "None" else None
                    if shipping_line:
                        shipping_line = ShippingLines.objects.filter(name=shipping_line).first()
                    vessel_voyage_id = data[id_vessel_voyage_id][i] if not data[id_vessel_voyage_id][i] == "None" else None
                    vessel_voyage_date = data[id_vessel_voyage_date][i] if not data[id_vessel_voyage_date][i] == "None" else None
                    hbl_no = data[id_hbl_no][i] if not data[id_hbl_no][i] == "None" else None
                    mbl_no = data[id_mbl_no][i] if not data[id_mbl_no][i] == "None" else None
                    origin = data[id_origin][i] if not data[id_origin][i] == "None" else None
                    if origin:
                        origin = Location.objects.filter(name=origin).first()
                    destination = data[id_destination][i] if not data[id_destination][i] == "None" else None
                    if destination:
                        destination = Location.objects.filter(name=destination).first()
                    invoice_currency = data[id_invoice_currency][i] if not data[id_invoice_currency][i] == "None" else None
                    if invoice_currency:
                        invoice_currency = currency.objects.filter(short_name=invoice_currency).first()
                    currency_ex_rate = data[id_currency_ex_rate][i] if not data[id_currency_ex_rate][i] == "None" else 1
                    gross = data[id_gross][i] if not data[id_gross][i] == "None" else None
                    volume = data[id_volume][i] if not data[id_volume][i] == "None" else None
                    nett = data[id_nett][i] if not data[id_nett][i] == "None" else None
                    total_packages = data[id_total_packages][i] if not data[id_total_packages][i] == "None" else None
                    total_packages_type = data[id_total_packages_type][i] if not data[id_total_packages_type][i] == "None" else None
                    total_cbm = data[id_total_cbm][i] if not data[id_total_cbm][i] == "None" else None
                    commodity = data[id_commodity][i] if not data[id_commodity][i] == "None" else None
                    commodity_type = data[id_commodity_type][i] if not data[id_commodity_type][i] == "None" else None
                    container_no = data[id_container_no][i] if not data[id_container_no][i] == "None" else None
                    container_type = data[id_container_type][i] if not data[id_container_type][i] == "None" else None
                    invoice_status = data[id_invoice_status][i] if not data[id_invoice_status][i] == "None" else None
                    flight_no = data[id_flight_no][i] if not data[id_flight_no][i] == "None" else None
                    awb_no = data[id_awb_no][i] if not data[id_awb_no][i] == "None" else None
                    docket_no = data[id_docket_no][i] if not data[id_docket_no][i] == "None" else None
                  
                    air_line = data[id_air_line][i] if not data[id_air_line][i] == "None" else None
                    if air_line:
                        air_line = Airlines.objects.filter(name=air_line).first()
                    flight_date = data[id_flight_date][i] if not data[id_flight_date][i] == "None" else None
                   
                 
                    account_number = data[id_account_number][i] if not data[id_account_number][i] == "None" else None
                    if account_number:
                        account_number = Bank.objects.filter(account_no=account_number).first()
                    gross_amount = data[id_gross_amount][i] if not data[id_gross_amount][i] == "None" else 0
                    gst_amount = data[id_gst_amount][i] if not data[id_gst_amount][i] == "None" else 0
                    advance_amount = data[id_advance_amount][i] if not data[id_advance_amount][i] == "None" else 0
                    net_amount = data[id_net_amount][i] if not data[id_net_amount][i] == "None" else 0
                    remark_on_invoice = data[id_remark_on_invoice][i] if not data[id_remark_on_invoice][i] == "None" else None
                    
                    sales_person = data[id_sales_person][i] if not data[id_sales_person][i] == "None" else None
                    created_on = data[id_created_on][i] if not data[id_created_on][i] == "None" else None
                    try:
                        new_pay_invoice = InvoicePayable.objects.create(
                            invoice_no = invoice_no,
                            purchase_invoice_no = purchase_invoice_no,
                            date_of_invoice = date_of_invoice,
                            job_no = job_no,
                            bill_from = bill_from,
                            shipping_line = shipping_line,
                            invoice_currency = invoice_currency,
                            currency_ex_rate = currency_ex_rate,
                            vessel_voyage_id = vessel_voyage_id,
                            vessel_voyage_date = vessel_voyage_date,
                            air_line = air_line,
                            flight_date = flight_date,
                            invoice_status = invoice_status,
                            account_number = account_number,
                            gross_amount = gross_amount,
                            gst_amount = gst_amount,
                            advance_amount = advance_amount,
                            net_amount = net_amount,
                            remark_on_invoice = remark_on_invoice,
                            sales_person = sales_person,
                            company_type = company_type,
                            hbl_no = hbl_no,
                            mbl_no = mbl_no,
                            origin = origin,
                            destination = destination,
                            gross = gross,
                            volume = volume,
                            nett = nett,
                            total_packages = total_packages,
                            total_packages_type = total_packages_type,
                            total_cbm = total_cbm,
                            commodity = commodity,
                            commodity_type = commodity_type,
                            container_no = container_no,
                            container_type = container_type,
                            flight_no = flight_no,
                            awb_no = awb_no,
                            docket_no = docket_no,
                            created_at = created_on
                        )
                        new_pay_invoice.save()
                    except Exception as e:
                        pass
                
        
                
                lenOfHeadData = len(head_data)
                for i in range(0,lenOfHeadData):
                    invoice = head_data[id_invoice][i]
                    invoice = InvoicePayable.objects.filter(invoice_no=invoice).first()
                    billing_head = head_data[id_billing_head][i]
                    billing_head = BillingHead.objects.filter(billing_head=billing_head).first()
                    inv_currency = head_data[id_currency][i]
                    inv_currency = currency.objects.filter(short_name=inv_currency).first()
                    ex_rate = head_data[id_ex_rate][i]
                    rate = head_data[id_rate][i]
                    qty_unit = head_data[id_qty_unit][i]
                    amount = head_data[id_amount][i]
                    gst = head_data[id_gst][i]
                    gst_amount = head_data[id_gst_amount][i]
                    total = head_data[id_total][i]
                    try:
                        new_pay_invoice_head = InvoicePayableDetail.objects.create(
                            invoice_payable = invoice,
                            billing_head = billing_head,
                            currency = inv_currency,
                            ex_rate = ex_rate,
                            rate = rate,
                            qty_unit = qty_unit,
                            amount = amount,
                            gst = gst,
                            gst_amount = gst_amount,
                            total = total,
                        )
                        new_pay_invoice_head.save()
                    except Exception as e:
                        message = traceback.format_exc()
                       
        # For Credit Note Upload
        if crn_upload:
            company_type = request.POST['crn_company_type']
            company_type = Logistic.objects.filter(id=int(company_type)).first()
            id_credit_note_no = request.POST['crn_credit_note_no']
            id_date_of_note = request.POST['crn_date_of_note']
            id_job_no = request.POST['crn_job_no']
            id_invoice_no = request.POST['crn_invoice_no']
            id_hbl_no = request.POST['crn_hbl_no']
            id_mbl_no = request.POST['crn_mbl_no']
            id_invoice_currency = request.POST['crn_invoice_currency']
            id_currency_ex_rate = request.POST['crn_currency_ex_rate']
            id_origin = request.POST['crn_origin']
            id_destination = request.POST['crn_destination']
            id_bill_to = request.POST['crn_bill_to']
            id_shipping_line = request.POST['crn_shipping_line']
            id_vessel_voyage_id = request.POST['crn_vessel_voyage_id']
            id_vessel_voyage_date = request.POST['crn_vessel_voyage_date']
            id_gross = request.POST['crn_gross']
            id_volume = request.POST['crn_volume']
            id_nett = request.POST['crn_nett']
            id_total_packages = request.POST['crn_total_packages']
            id_total_packages_type = request.POST['crn_total_packages_type']
            id_total_cbm = request.POST['crn_total_cbm']
            id_commodity = request.POST['crn_commodity']
            id_commodity_type = request.POST['crn_commodity_type']
            id_container_no = request.POST['crn_container_no']
            id_container_type = request.POST['crn_container_type']
            id_invoice_status = request.POST['crn_invoice_status']
            id_air_line = request.POST['crn_air_line']
            id_flight_date = request.POST['crn_flight_date']
            id_flight_no = request.POST['crn_flight_no']
            id_awb_no = request.POST['crn_awb_no']
            id_docket_no = request.POST['crn_docket_no']
            id_account_number = request.POST['crn_account_number']
            id_gross_amount = request.POST['crn_gross_amount']
            id_gst_amount = request.POST['crn_gst_amount']
            id_advance_amount = request.POST['crn_advance_amount']
            id_net_amount = request.POST['crn_net_amount']
            id_remark_on_note = request.POST['crn_remark_on_note']
            id_created_on = request.POST['crn_created_on']
            id_crn_invoice = request.POST['crn_head_pay_invoice']
            id_billing_head = request.POST['crn_head_billing_head']
            id_currency = request.POST['crn_head_currency']
            id_ex_rate = request.POST['crn_head_ex_rate']
            id_rate = request.POST['crn_head_rate']
            id_qty_unit = request.POST['crn_head_qty_unit']
            id_amount = request.POST['crn_head_amount']
            id_gst = request.POST['crn_head_gst']
            id_gst_amount = request.POST['crn_head_gst_amount']
            id_total = request.POST['crn_head_total']
            
            file = request.FILES['crn_file']
            head_file = request.FILES['crn_head_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            filename_head = fs.save(head_file.name, head_file)
            if file and head_file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                head_data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename_head,engine='openpyxl')
                
                
                lenOfData = len(data)
                for i in range(0,lenOfData):
                    invoice_no = data[id_invoice_no][i] if not data[id_invoice_no][i] == "None" else None
                    credit_note_no = data[id_credit_note_no][i] if not data[id_credit_note_no][i] == "None" else None                   
                    date_of_note = data[id_date_of_note][i] if not data[id_date_of_note][i] == "None" else None
                    job_no = data[id_job_no][i] if not data[id_job_no][i] == "None" else None
                    if job_no:
                        job_no = JobMaster.objects.filter(job_no=job_no).first()
                    
                    bill_to = data[id_bill_to][i] if not data[id_bill_to][i] == "None" else None
         
                    if bill_to:
                        bill_to = Party.objects.filter(party_name=bill_to).first()
            
                   
                    shipping_line = data[id_shipping_line][i]  if not data[id_shipping_line][i] == "None" else None
                    if shipping_line:
                        shipping_line = ShippingLines.objects.filter(name=shipping_line).first()
                        
                    vessel_voyage_id = data[id_vessel_voyage_id][i] if not data[id_vessel_voyage_id][i] == "None" else None
                    vessel_voyage_date = data[id_vessel_voyage_date][i] if not data[id_vessel_voyage_date][i] == "None" else None
                    hbl_no = data[id_hbl_no][i] if not data[id_hbl_no][i] == "None" else None
                    mbl_no = data[id_mbl_no][i] if not data[id_mbl_no][i] == "None" else None
                    origin = data[id_origin][i] if not data[id_origin][i] == "None" else None
                    if origin:
                        origin = Location.objects.filter(name=origin).first()
                    destination = data[id_destination][i] if not data[id_destination][i] == "None" else None
                    if destination:
                        destination = Location.objects.filter(name=destination).first()
                    invoice_currency = data[id_invoice_currency][i] if not data[id_invoice_currency][i] == "None" else None
                    if invoice_currency:
                        invoice_currency = currency.objects.filter(short_name=invoice_currency).first()
                    currency_ex_rate = data[id_currency_ex_rate][i] if not data[id_currency_ex_rate][i] == "None" else 1
                    gross = data[id_gross][i] if not data[id_gross][i] == "None" else None
                    volume = data[id_volume][i] if not data[id_volume][i] == "None" else None
                    nett = data[id_nett][i] if not data[id_nett][i] == "None" else None
                    total_packages = data[id_total_packages][i] if not data[id_total_packages][i] == "None" else None
                    total_packages_type = data[id_total_packages_type][i] if not data[id_total_packages_type][i] == "None" else None
                    total_cbm = data[id_total_cbm][i] if not data[id_total_cbm][i] == "None" else None
                    commodity = data[id_commodity][i] if not data[id_commodity][i] == "None" else None
                    commodity_type = data[id_commodity_type][i] if not data[id_commodity_type][i] == "None" else None
                    container_no = data[id_container_no][i] if not data[id_container_no][i] == "None" else None
                    container_type = data[id_container_type][i] if not data[id_container_type][i] == "None" else None
                    invoice_status = data[id_invoice_status][i] if not data[id_invoice_status][i] == "None" else None
                    flight_no = data[id_flight_no][i] if not data[id_flight_no][i] == "None" else None
                    awb_no = data[id_awb_no][i] if not data[id_awb_no][i] == "None" else None
                    docket_no = data[id_docket_no][i] if not data[id_docket_no][i] == "None" else None
                  
                    air_line = data[id_air_line][i] if not data[id_air_line][i] == "None" else None
                    if air_line:
                        air_line = Airlines.objects.filter(name=air_line).first()
                    flight_date = data[id_flight_date][i] if not data[id_flight_date][i] == "None" else None
                   
                 
                    account_number = data[id_account_number][i] if not data[id_account_number][i] == "None" else None
                    if account_number:
                        account_number = Bank.objects.filter(account_no=account_number).first()
                    gross_amount = data[id_gross_amount][i] if not data[id_gross_amount][i] == "None" else 0
                    gst_amount = data[id_gst_amount][i] if not data[id_gst_amount][i] == "None" else 0
                    advance_amount = data[id_advance_amount][i] if not data[id_advance_amount][i] == "None" else 0
                    net_amount = data[id_net_amount][i] if not data[id_net_amount][i] == "None" else 0
                 
                    
                    created_on = data[id_created_on][i] if not data[id_created_on][i] == "None" else None
                    remark_on_note = data[id_remark_on_note][i] if not data[id_remark_on_note][i] == "None" else None
                    try:
                        new_crn = CreditNote.objects.create(
                            company_type = company_type,
                            credit_note_no = credit_note_no,
                            date_of_note = date_of_note,
                            job_no = job_no,
                            invoice_no = invoice_no,
                            hbl_no = hbl_no,
                            mbl_no = mbl_no,
                            invoice_currency = invoice_currency,
                            currency_ex_rate = currency_ex_rate,
                            origin = origin,
                            destination = destination,
                            bill_to = bill_to,
                            shipping_line = shipping_line,
                            vessel_voyage_id = vessel_voyage_id,
                            vessel_voyage_date = vessel_voyage_date,
                            gross = gross,
                            volume = volume,
                            nett = nett,
                            total_packages = total_packages,
                            total_packages_type = total_packages_type,
                            total_cbm = total_cbm,
                            commodity = commodity,
                            commodity_type = commodity_type,
                            container_no = container_no,
                            container_type = container_type,
                            invoice_status = invoice_status,
                            air_line = air_line,
                            flight_date = flight_date,
                            flight_no = flight_no,
                            awb_no = awb_no,
                            docket_no = docket_no,
                            account_number = account_number,
                            gross_amount = gross_amount,
                            gst_amount = gst_amount,
                            advance_amount = advance_amount,
                            net_amount = net_amount,
                            remark_on_note = remark_on_note,
                            created_at = created_on,
                        )
                        new_crn.save()
                    except Exception as e:
                        message = traceback.format_exc()
                       
                
        
                
                lenOfHeadData = len(head_data)
                for i in range(0,lenOfHeadData):
                    credit_note = head_data[id_crn_invoice][i]
                    credit_note = CreditNote.objects.filter(credit_note_no=credit_note).first()
                    billing_head = head_data[id_billing_head][i]
                    billing_head = BillingHead.objects.filter(billing_head=billing_head).first()
                    inv_currency = head_data[id_currency][i]
                    inv_currency = currency.objects.filter(short_name=inv_currency).first()
                    ex_rate = head_data[id_ex_rate][i]
                    rate = head_data[id_rate][i]
                    qty_unit = head_data[id_qty_unit][i]
                    amount = head_data[id_amount][i]
                    gst = head_data[id_gst][i]
                    gst_amount = head_data[id_gst_amount][i]
                    total = head_data[id_total][i]
                    try:
                        new_crn_head = CreditNoteDetail.objects.create(
                            credit_note = credit_note,
                            billing_head = billing_head,
                            currency = inv_currency,
                            ex_rate = ex_rate,
                            rate = rate,
                            qty_unit = qty_unit,
                            amount = amount,
                            gst = gst,
                            gst_amount = gst_amount,
                            total = total,
                        )
                        new_crn_head.save()
                    except Exception as e:
                        message = traceback.format_exc()
                       
        # For Debit Note Upload
        if drn_upload:
            company_type = request.POST['drn_company_type']
            company_type = Logistic.objects.filter(id=int(company_type)).first()
            id_debit_note_no = request.POST['drn_debit_note_no']
            id_date_of_note = request.POST['drn_date_of_note']
            id_job_no = request.POST['drn_job_no']
            id_invoice_no = request.POST['drn_invoice_no']
            id_hbl_no = request.POST['drn_hbl_no']
            id_mbl_no = request.POST['drn_mbl_no']
            id_invoice_currency = request.POST['drn_invoice_currency']
            id_currency_ex_rate = request.POST['drn_currency_ex_rate']
            id_origin = request.POST['drn_origin']
            id_destination = request.POST['drn_destination']
            id_bill_from = request.POST['drn_bill_from']
            id_shipping_line = request.POST['drn_shipping_line']
            id_vessel_voyage_id = request.POST['drn_vessel_voyage_id']
            id_vessel_voyage_date = request.POST['drn_vessel_voyage_date']
            id_gross = request.POST['drn_gross']
            id_volume = request.POST['drn_volume']
            id_nett = request.POST['drn_nett']
            id_total_packages = request.POST['drn_total_packages']
            id_total_packages_type = request.POST['drn_total_packages_type']
            id_total_cbm = request.POST['drn_total_cbm']
            id_commodity = request.POST['drn_commodity']
            id_commodity_type = request.POST['drn_commodity_type']
            id_container_no = request.POST['drn_container_no']
            id_container_type = request.POST['drn_container_type']
            id_invoice_status = request.POST['drn_invoice_status']
            id_air_line = request.POST['drn_air_line']
            id_flight_date = request.POST['drn_flight_date']
            id_flight_no = request.POST['drn_flight_no']
            id_awb_no = request.POST['drn_awb_no']
            id_docket_no = request.POST['drn_docket_no']
            id_account_number = request.POST['drn_account_number']
            id_gross_amount = request.POST['drn_gross_amount']
            id_gst_amount = request.POST['drn_gst_amount']
            id_advance_amount = request.POST['drn_advance_amount']
            id_net_amount = request.POST['drn_net_amount']
            id_remark_on_note = request.POST['drn_remark_on_note']
            id_created_on = request.POST['drn_created_on']
            id_drn_invoice = request.POST['drn_head_pay_invoice']
            id_billing_head = request.POST['drn_head_billing_head']
            id_currency = request.POST['drn_head_currency']
            id_ex_rate = request.POST['drn_head_ex_rate']
            id_rate = request.POST['drn_head_rate']
            id_qty_unit = request.POST['drn_head_qty_unit']
            id_amount = request.POST['drn_head_amount']
            id_gst = request.POST['drn_head_gst']
            id_gst_amount = request.POST['drn_head_gst_amount']
            id_total = request.POST['drn_head_total']
            
            file = request.FILES['drn_file']
            head_file = request.FILES['drn_head_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            filename_head = fs.save(head_file.name, head_file)
            if file and head_file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                head_data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename_head,engine='openpyxl')
                
                
                lenOfData = len(data)
                for i in range(0,lenOfData):
                    invoice_no = data[id_invoice_no][i] if not data[id_invoice_no][i] == "None" else None
      
                    debit_note_no = data[id_debit_note_no][i] if not data[id_debit_note_no][i] == "None" else None                   
                  
                    date_of_note = data[id_date_of_note][i] if not data[id_date_of_note][i] == "None" else None
                   
                    job_no = data[id_job_no][i] if not data[id_job_no][i] == "None" else None
                    if job_no:
                        job_no = JobMaster.objects.filter(job_no=job_no).first()
                    
                    
                    bill_from = data[id_bill_from][i] if not data[id_bill_from][i] == "None" else None
         
                   
                    if bill_from:
                        bill_from = Party.objects.filter(party_name=bill_from).first()

                
                   
                    shipping_line = data[id_shipping_line][i]  if not data[id_shipping_line][i] == "None" else None
                    if shipping_line:
                        shipping_line = ShippingLines.objects.filter(name=shipping_line).first()
                        
                    vessel_voyage_id = data[id_vessel_voyage_id][i] if not data[id_vessel_voyage_id][i] == "None" else None
                    vessel_voyage_date = data[id_vessel_voyage_date][i] if not data[id_vessel_voyage_date][i] == "None" else None
                    hbl_no = data[id_hbl_no][i] if not data[id_hbl_no][i] == "None" else None
                    mbl_no = data[id_mbl_no][i] if not data[id_mbl_no][i] == "None" else None
                    origin = data[id_origin][i] if not data[id_origin][i] == "None" else None
                    if origin:
                        origin = Location.objects.filter(name=origin).first()
                    destination = data[id_destination][i] if not data[id_destination][i] == "None" else None
                    if destination:
                        destination = Location.objects.filter(name=destination).first()
                    invoice_currency = data[id_invoice_currency][i] if not data[id_invoice_currency][i] == "None" else None
                    if invoice_currency:
                        invoice_currency = currency.objects.filter(short_name=invoice_currency).first()
                    currency_ex_rate = data[id_currency_ex_rate][i] if not data[id_currency_ex_rate][i] == "None" else 1
                    gross = data[id_gross][i] if not data[id_gross][i] == "None" else None
                    volume = data[id_volume][i] if not data[id_volume][i] == "None" else None
                    nett = data[id_nett][i] if not data[id_nett][i] == "None" else None
                    total_packages = data[id_total_packages][i] if not data[id_total_packages][i] == "None" else None
                    total_packages_type = data[id_total_packages_type][i] if not data[id_total_packages_type][i] == "None" else None
                    total_cbm = data[id_total_cbm][i] if not data[id_total_cbm][i] == "None" else None
                    commodity = data[id_commodity][i] if not data[id_commodity][i] == "None" else None
                    commodity_type = data[id_commodity_type][i] if not data[id_commodity_type][i] == "None" else None
                    container_no = data[id_container_no][i] if not data[id_container_no][i] == "None" else None
                    container_type = data[id_container_type][i] if not data[id_container_type][i] == "None" else None
                    invoice_status = data[id_invoice_status][i] if not data[id_invoice_status][i] == "None" else None
                    flight_no = data[id_flight_no][i] if not data[id_flight_no][i] == "None" else None
                    awb_no = data[id_awb_no][i] if not data[id_awb_no][i] == "None" else None
                    docket_no = data[id_docket_no][i] if not data[id_docket_no][i] == "None" else None
                  
                    air_line = data[id_air_line][i] if not data[id_air_line][i] == "None" else None
                    if air_line:
                        air_line = Airlines.objects.filter(name=air_line).first()
                    flight_date = data[id_flight_date][i] if not data[id_flight_date][i] == "None" else None
                   
                 
                    account_number = data[id_account_number][i] if not data[id_account_number][i] == "None" else None
                    if account_number:
                        account_number = Bank.objects.filter(account_no=account_number).first()
                    gross_amount = data[id_gross_amount][i] if not data[id_gross_amount][i] == "None" else 0
                    gst_amount = data[id_gst_amount][i] if not data[id_gst_amount][i] == "None" else 0
                    advance_amount = data[id_advance_amount][i] if not data[id_advance_amount][i] == "None" else 0
                    net_amount = data[id_net_amount][i] if not data[id_net_amount][i] == "None" else 0
                 
                    
                    created_on = data[id_created_on][i] if not data[id_created_on][i] == "None" else None
                    remark_on_note = data[id_remark_on_note][i] if not data[id_remark_on_note][i] == "None" else None
                    try:
                        new_drn = DebitNote.objects.create(
                            company_type = company_type,
                            debit_note_no = debit_note_no,
                            date_of_note = date_of_note,
                            job_no = job_no,
                            invoice_no = invoice_no,
                            hbl_no = hbl_no,
                            mbl_no = mbl_no,
                            invoice_currency = invoice_currency,
                            currency_ex_rate = currency_ex_rate,
                            origin = origin,
                            destination = destination,
                            bill_from = bill_from,
                            shipping_line = shipping_line,
                            vessel_voyage_id = vessel_voyage_id,
                            vessel_voyage_date = vessel_voyage_date,
                            gross = gross,
                            volume = volume,
                            nett = nett,
                            total_packages = total_packages,
                            total_packages_type = total_packages_type,
                            total_cbm = total_cbm,
                            commodity = commodity,
                            commodity_type = commodity_type,
                            container_no = container_no,
                            container_type = container_type,
                            invoice_status = invoice_status,
                            air_line = air_line,
                            flight_date = flight_date,
                            flight_no = flight_no,
                            awb_no = awb_no,
                            docket_no = docket_no,
                            account_number = account_number,
                            gross_amount = gross_amount,
                            gst_amount = gst_amount,
                            advance_amount = advance_amount,
                            net_amount = net_amount,
                            remark_on_note = remark_on_note,
                            created_at = created_on,
                        )
                        new_drn.save()
                    except Exception as e:
                        message = traceback.format_exc()
                        
                
        
                
                lenOfHeadData = len(head_data)
                for i in range(0,lenOfHeadData):
                    debit_note = head_data[id_drn_invoice][i]
                    debit_note = DebitNote.objects.filter(debit_note_no=debit_note).first()
                    
                    billing_head = head_data[id_billing_head][i]
                    billing_head = BillingHead.objects.filter(billing_head=billing_head).first()
                    inv_currency = head_data[id_currency][i]
                    inv_currency = currency.objects.filter(short_name=inv_currency).first()
                    ex_rate = head_data[id_ex_rate][i]
                    rate = head_data[id_rate][i]
                    qty_unit = head_data[id_qty_unit][i]
                    amount = head_data[id_amount][i]
                    gst = head_data[id_gst][i]
                    gst_amount = head_data[id_gst_amount][i]
                    total = head_data[id_total][i]
                    try:
                        
                        new_drn_head = DebitNoteDetail.objects.create(
                            debit_note = debit_note,
                            billing_head = billing_head,
                            currency = inv_currency,
                            ex_rate = ex_rate,
                            rate = rate,
                            qty_unit = qty_unit,
                            amount = amount,
                            gst = gst,
                            gst_amount = gst_amount,
                            total = total,
                        )
                        new_drn_head.save()
                    except Exception as e:
                        message = traceback.format_exc()
                      
                       
        # For Ledger Category
        if ledger_category_upload:
            ledger_category_name_field = request.POST['ledger_category_name']
            ledger_cat_type_field = request.POST['ledger_cat_type']
            file = request.FILES['ledger_category_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            if file:
                data = pd.read_excel(os.path.join(settings.MEDIA_ROOT)+'/'+filename,engine='openpyxl')
                lenOfData = len(data)
                for i in range(0, lenOfData):
                    name = data[ledger_category_name_field][i]
                    type = data[ledger_cat_type_field][i]
                    
                    try:
                        old_check = LedgerCategories.objects.filter(name=name).first()
                        if not old_check:
                            new_ledger_category = LedgerCategories.objects.create(name=name,type=type)
                            new_ledger_category.save()
                    except:
                        pass
            
             
           
    companies = Logistic.objects.all()
    
    context = {
        'module':module,
        'companies':companies,
        
    }
    
    return render(request,'upload_master/upload_master.html',context)

