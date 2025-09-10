from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect, HttpResponse
from dashboard.models import Logistic
from masters.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from masters.models import *
import calendar
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from io import BytesIO
import xlsxwriter
from django.urls import reverse
from django.template.loader import render_to_string
from accounting.models import Manifest, ManifestChargesToCollect,ManifestChargesToPay,ManifestOurCharges,ManifestYourCharges
from accounting.forms import ManifestForm
from dashboard.views import check_permissions,EmailThread
import num2words
# Create your views here.




# Operation Booking Master
@login_required(login_url='home:handle_login')
def create_booking_master(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = BookingMasterForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.instance.company_type = request.user.user_account.office
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Booking {form.instance.booking_no} Created.")
        return redirect('operations:create_booking_master',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'booking_master/create.html',context)

@login_required(login_url='home:handle_login')
def booking_master_details(request,module):
    context ={}
    check_permissions(request,module)
    booking_master = BookingMaster.objects.prefetch_related('job_booking').select_related('shipper','consignee','pol','pod','fpod','shipping_line').all()
    
    
    current_month = datetime.now().month
    new_month=current_month-3
    current_year = datetime.now().year
    new_year = current_year
    if new_month < 0:
        new_month = 13 + new_month
        new_year -= 1
    
    if new_month == 0:
        new_month = 12 + new_month
        new_year -= 1

    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(new_year,new_month,1)

    to_date = date(current_year,current_month,end_day)
  
    
    
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        
        from_date = datetime.strptime(str(from_date),"%Y-%m-%d").date()
        to_date = datetime.strptime(str(to_date),"%Y-%m-%d").date()
        
    booking_master = booking_master.filter(booking_date__range=[from_date,to_date]).all()
    
    if module == 'sea_export':
        booking_master = booking_master.filter(module='Sea Export')
    if module == 'sea_import':
        booking_master = booking_master.filter(module='Sea Import')
    if module == 'air_export':
        booking_master = booking_master.filter(module='Air Export')
    if module == 'air_import':
        booking_master = booking_master.filter(module='Air Import')


    context['from_date']= from_date
    context['to_date']= to_date
    context['booking_master']= booking_master
    context['module']= module
    return render(request,'booking_master/details.html',context)

@login_required(login_url='home:handle_login')
def all_booking_master_details(request,module):
    context ={}
    check_permissions(request,module)
    booking_master = BookingMaster.objects.prefetch_related('job_booking').select_related('shipper','consignee','pol','pod','fpod','shipping_line').all()
    
    
    current_month = datetime.now().month
    new_month=current_month-3
    current_year = datetime.now().year
    new_year = current_year
    if new_month < 0:
        new_month = 13 + new_month
        new_year -= 1
    
    if new_month == 0:
        new_month = 12 + new_month
        new_year -= 1

    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(new_year,new_month,1)

    to_date = date(current_year,current_month,end_day)
  
    
    
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        
        from_date = datetime.strptime(str(from_date),"%Y-%m-%d").date()
        to_date = datetime.strptime(str(to_date),"%Y-%m-%d").date()
        
    booking_master = booking_master.filter(booking_date__range=[from_date,to_date]).all()
    
    context['from_date']= from_date
    context['to_date']= to_date
    context['booking_master']= booking_master
    context['module']= module
    return render(request,'booking_master/details.html',context)

@login_required(login_url='home:handle_login')
def booking_master_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(BookingMaster, id = id)
    
    form = BookingMasterForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        form.instance.company_type = request.user.user_account.office

        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:booking_master_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'booking_master/create.html',context)

@login_required(login_url='home:handle_login')
def booking_master_delete(request,module,id):
    check_permissions(request,module)
    booking_master = BookingMaster.objects.filter(id=int(id)).first()
    booking_master.delete()
    return redirect('operations:booking_master_details',module=module)

# Job
    
def job_transhipments(request,job):
    total_rows = int(request.POST['total_transhipment_rows'])
    transhipments = JobTranshipment.objects.filter(job__id=job.id).all()
    transhipments.delete()
    for i  in range(1,total_rows+1):
        transhipment_is_active = request.POST[f'transhipment_is_active-{i}']
        port = request.POST[f'transhipment_port-{i}']
        if port:
            port = Ports.objects.filter(id=port).first()
        if transhipment_is_active == 'yes' and port:
            eta_date = request.POST[f'transhipment_eta_date-{i}']
            etd_date = request.POST[f'transhipment_etd_date-{i}']
            vessel_voyage = request.POST[f'transhipment_vessel_voyage-{i}']
            new_transhipment = JobTranshipment.objects.create(
                job=job,
                port = port,
                vessel_voyage = vessel_voyage,
            )
            if eta_date:
                new_transhipment.eta_date = eta_date
            if etd_date:
                new_transhipment.etd_date = etd_date
            new_transhipment.save()
    
def job_invoice(request,job):
    total_rows = int(request.POST['total_job_invoice_details_rows'])
    invoices = JobInvoice.objects.filter(job__id=job.id).all()
    invoices.delete()
    for i  in range(1,total_rows+1):
        job_invoice_details_is_active = request.POST[f'job_invoice_details_is_active-{i}']
    
        invoice_no = request.POST[f'invoice_no-{i}']
        if job_invoice_details_is_active == 'yes' and invoice_no:
            invoice_date = request.POST.get(f'invoice_date-{i}',None)
            
            value = request.POST.get(f'value-{i}',0)
            if not value:
                value = 0
            curr = request.POST[f'curr-{i}']
            net_wt = request.POST[f'net_wt-{i}']
            ship_bill_no = request.POST[f'ship_bill_no-{i}']
            ship_bill_type = request.POST[f'ship_bill_type-{i}']
            ship_bill_date = request.POST.get(f'ship_bill_date-{i}',None)
            
            new_invoice = JobInvoice.objects.create(
                job=job,
                invoice_no = invoice_no,
                value = value,
                curr = curr,
                net_wt = net_wt,
                ship_bill_no = ship_bill_no,
                ship_bill_type = ship_bill_type,
              
            )
            if ship_bill_date:
                new_invoice.ship_bill_date = ship_bill_date
            if invoice_date:
                new_invoice.invoice_date = invoice_date
            new_invoice.save()

def job_container(request,job):
    total_rows = int(request.POST['total_job_container_details_rows'])
    job_containers = JobContainer.objects.filter(job__id=job.id).filter(hbl=None).all()
    job_containers.delete()
    for i in range(1,total_rows+1):
        job_container_details_is_active = request.POST[f'job_container_details_is_active-{i}']
    
        job_container_no = request.POST[f'container_no-{i}']
        if job_container_details_is_active == 'yes' and job_container_no:
          
            container_type = request.POST[f'container_type-{i}']
            gross_wt = request.POST[f'gross_wt-{i}']
            line_seal = request.POST[f'line_seal-{i}']
            net_wt=request.POST[f'net_wt-{i}']
            total_package=request.POST[f'total_package-{i}']
            cbm=request.POST[f'cbm-{i}']
            trailor_no = request.POST[f'trailor_no-{i}']
            gta = request.POST[f'gta-{i}']
            pickup_date = request.POST[f'pickup_date-{i}']
            excfs_date = request.POST[f'excfs_date-{i}']
            in_fac_date = request.POST[f'in_fac_date-{i}']
            activity_date = request.POST[f'activity_date-{i}']
            fac_out_date = request.POST[f'fac_out_date-{i}']
            return_date = request.POST[f'return_date-{i}']
            cfs_in_date = request.POST[f'cfs_in_date-{i}']
            railout_date = request.POST[f'railout_date-{i}']
            train_no = request.POST[f'train_no-{i}']
            shipper_seal_no = request.POST[f'shipper_seal_no-{i}']
            new_seal_no = request.POST[f'new_seal_no-{i}']
            stuffing_date = request.POST[f'stuffing_date-{i}']
            icd_handover_date = request.POST[f'icd_handover_date-{i}']
            delivery_date = request.POST[f'delivery_date-{i}']
            port_handover_date = request.POST[f'port_handover_date-{i}']
            belong_to = request.POST.get(f'belong_to-{i}',None)
            place_of_unloading = request.POST.get(f'place_of_unloading-{i}',None)
            if place_of_unloading:
                place_of_unloading = Location.objects.filter(id=int(place_of_unloading)).first()
            place_of_loading = request.POST[f'place_of_loading-{i}']
            if place_of_loading:
                place_of_loading = Location.objects.filter(id=int(place_of_loading)).first()
           
            new_job_container = JobContainer.objects.create(
                job=job,
                job_container_no = job_container_no,
                container_type = container_type,
                gross_wt = gross_wt,
                line_seal = line_seal,
                net_wt=net_wt,
                total_package=total_package,
                cbm=cbm,
                trailor_no = trailor_no,
                gta = gta,
                train_no = train_no,
                belong_to = belong_to,
                
            )
            
            if shipper_seal_no:
                new_job_container.shipper_seal_no = shipper_seal_no
            if new_seal_no:
                new_job_container.new_seal_no = new_seal_no
            if stuffing_date:
                new_job_container.stuffing_date = stuffing_date
            if icd_handover_date:
                new_job_container.icd_handover_date = icd_handover_date
            if port_handover_date:
                new_job_container.port_handover_date = port_handover_date
            
            if delivery_date:
                new_job_container.delivery_date = delivery_date
            
            if pickup_date:
                new_job_container.pickup_date = pickup_date
            if excfs_date:
                new_job_container.excfs_date = excfs_date
            if in_fac_date:
                new_job_container.in_fac_date = in_fac_date
            if activity_date:
                new_job_container.activity_date = activity_date
            if fac_out_date:
                new_job_container.fac_out_date = fac_out_date
            if cfs_in_date:
                new_job_container.cfs_in_date = cfs_in_date
            if railout_date:
                new_job_container.railout_date = railout_date
            if place_of_unloading:
                new_job_container.place_of_unloading = place_of_unloading
            if place_of_loading:
                new_job_container.place_of_loading = place_of_loading
            if return_date:
                new_job_container.return_date = return_date
            new_job_container.save()


def job_hbl(request,job):
    
    total_rows = int(request.POST['total_job_hbl_details_rows'])
    
    
    for i in range(1,total_rows+1):
        job_hbl_details_is_active = request.POST[f'job_hbl_details_is_active-{i}']
       
        total_job_hbl_container_details_rows = int(request.POST[f'total_job_hbl_container_details_rows-{i}'])
        job_hbl_details_is_deleted = request.POST[f'job_hbl_details_is_deleted-{i}']
       

        job_hbl_details_is_update = request.POST[f'job_hbl_details_is_update-{i}']
       

        if job_hbl_details_is_deleted == "yes":
            job_hbl_details_id = request.POST[f'job_hbl_details_id-{i}']
         
            hbl = JobHBL.objects.filter(id=int(job_hbl_details_id)).first()
            hbl.delete()
            continue

        # Value
        job_hbl_no = request.POST[f'job_hbl_no-{i}']
        job_hbl_date = request.POST[f'job_hbl_date-{i}']
        hbl_account = request.POST[f'hbl_account-{i}']
        hbl_shipper = request.POST[f'hbl_shipper-{i}']
        hbl_consignee = request.POST[f'hbl_consignee-{i}']
        mbl_no = request.POST[f'hbl_mbl_no-{i}']
        vessel_name = request.POST[f'hbl_vessel_name-{i}']
        commodity = request.POST[f'hbl_commodity-{i}']
        commodity_type = request.POST[f'hbl_commodity_type-{i}']
        no_of_packages = request.POST[f'hbl_no_of_packages-{i}']
        packages_type = request.POST[f'hbl_packages_type-{i}']
        volume = request.POST[f'hbl_volume-{i}']
        net_weight = request.POST[f'hbl_net_weight-{i}']
        gross_weight = request.POST[f'hbl_gross_weight-{i}']
        hbl = None

        if job_hbl_details_is_update == "yes" and job_hbl_details_is_active == "yes":
            job_hbl_details_id = request.POST[f'job_hbl_details_id-{i}']
            hbl = JobHBL.objects.filter(id=int(job_hbl_details_id)).first()
            hbl.job_hbl_no = job_hbl_no
            hbl.mbl_no = mbl_no
            hbl.vessel_name = vessel_name
            hbl.commodity = commodity
            hbl.commodity_type = commodity_type
            hbl.no_of_packages = no_of_packages
            hbl.packages_type = packages_type
            hbl.volume = volume
            hbl.net_weight = net_weight
            hbl.gross_weight = gross_weight
            hbl.save()

        elif job_hbl_details_is_update == "no" and job_hbl_details_is_active == "yes":
            if job_hbl_no:
                hbl = JobHBL.objects.create(
                    job = job,
                    job_hbl_no = job_hbl_no,
                    mbl_no=mbl_no,
                    vessel_name=vessel_name,
                    commodity = commodity,
                    commodity_type = commodity_type,
                    no_of_packages = no_of_packages,
                    packages_type = packages_type,
                    volume = volume,
                    net_weight = net_weight,
                    gross_weight = gross_weight,
                )

        if job_hbl_details_is_active == "yes" and hbl:

            if hbl_account:
                hbl_account = Party.objects.filter(id=int(hbl_account)).first()
                hbl.hbl_account = hbl_account
            if hbl_shipper:
                hbl_shipper = Party.objects.filter(id=int(hbl_shipper)).first()
                hbl.hbl_shipper = hbl_shipper
            if hbl_consignee:
                hbl_consignee = Party.objects.filter(id=int(hbl_consignee)).first()
                hbl.hbl_consignee = hbl_consignee
            if job_hbl_date:
                hbl.job_hbl_date = job_hbl_date
            hbl.save()

            for j in range(1,total_job_hbl_container_details_rows+1):
                job_hbl_container_details_is_active = request.POST[f'job_hbl_container_details_is_active-{i}{j}']
                job_hbl_container_details_is_deleted = request.POST[f'job_hbl_container_details_is_deleted-{i}{j}']
                job_hbl_container_details_is_update = request.POST[f'job_hbl_container_details_is_update-{i}{j}']
                
                if job_hbl_container_details_is_deleted == "yes":
                    job_hbl_container_details_id = request.POST[f'job_hbl_container_details_id-{i}{j}']
                    container = JobContainer.objects.filter(id=int(job_hbl_container_details_id)).first()
                    container.delete()

                # Value
                job_container_no = request.POST[f'job_hbl_container_no-{i}{j}']
                container_type = request.POST[f'job_hbl_container_type-{i}{j}']
                line_seal = request.POST[f'job_hbl_line_seal-{i}{j}']
                pickup_date = request.POST[f'job_hbl_pickup_date-{i}{j}']
                in_fac_date = request.POST[f'job_hbl_in_fac_date-{i}{j}']
                fac_out_date = request.POST[f'job_hbl_fac_out_date-{i}{j}']
                return_date = request.POST[f'job_hbl_return_date-{i}{j}']
                cfs_in_date = request.POST[f'job_hbl_cfs_in_date-{i}{j}']

            
                railout_date = request.POST[f'job_hbl_railout_date-{i}{j}']

                stuffing_date = request.POST[f'job_hbl_stuffing_date-{i}{j}']
                icd_handover_date = request.POST[f'job_hbl_icd_handover_date-{i}{j}']
                delivery_date = request.POST[f'job_hbl_delivery_date-{i}{j}']
                gross_weight=request.POST[f"job_hbl_gross_wt-{i}{j}"]

                port_handover_date = request.POST[f'job_hbl_port_handover_date-{i}{j}']

                container = None
                if job_hbl_container_details_is_update == "yes" and job_hbl_container_details_is_active == "yes":
                    job_hbl_container_details_id = request.POST[f'job_hbl_container_details_id-{i}{j}']
                    container = JobContainer.objects.filter(id=int(job_hbl_container_details_id)).first()
                    container.job_container_no = job_container_no
                    container.container_type = container_type
                    container.line_seal = line_seal
                    container.gross_wt = gross_weight
                    container.save()

                elif job_hbl_container_details_is_update == "no" and job_hbl_container_details_is_active == "yes":
                    if job_container_no:
                        container = JobContainer.objects.create(
                            job=job,
                            hbl = hbl,
                            job_container_no = job_container_no,
                            container_type = container_type,    
                            line_seal = line_seal,
                            gross_wt = gross_weight
                        )
                    

                if job_hbl_container_details_is_active == "yes" and container:
                    
                        if stuffing_date:
                            container.stuffing_date = stuffing_date
                        if icd_handover_date:
                            container.icd_handover_date = icd_handover_date
                        if port_handover_date:
                            container.port_handover_date = port_handover_date
                        
                        if delivery_date:
                            container.delivery_date = delivery_date
                        
                        if pickup_date:
                            container.pickup_date = pickup_date
                        
                        if in_fac_date:
                            container.in_fac_date = in_fac_date
                        
                        if fac_out_date:
                            container.fac_out_date = fac_out_date
                        if cfs_in_date:
                            container.cfs_in_date = cfs_in_date
                        if railout_date:
                            container.railout_date = railout_date
                        
                        if return_date:
                            container.return_date = return_date

                        if gross_weight:
                            container.gross_wt = gross_weight
                        container.save()


def air_job_hbl(request,job):
    
    total_rows = int(request.POST['total_job_hbl_details_rows'])
    
    
    for i in range(1,total_rows+1):
        job_hbl_details_is_active = request.POST[f'job_hbl_details_is_active-{i}']
       
        total_job_hbl_container_details_rows = int(request.POST[f'total_job_hbl_container_details_rows-{i}'])
        job_hbl_details_is_deleted = request.POST[f'job_hbl_details_is_deleted-{i}']
       

        job_hbl_details_is_update = request.POST[f'job_hbl_details_is_update-{i}']
       

        if job_hbl_details_is_deleted == "yes":
            job_hbl_details_id = request.POST[f'job_hbl_details_id-{i}']
         
            hbl = JobHBL.objects.filter(id=int(job_hbl_details_id)).first()
            hbl.delete()
            continue

        # Value
        job_hbl_no = request.POST[f'job_hbl_no-{i}']
        job_hbl_date = request.POST[f'job_hbl_date-{i}']
        hbl_account = request.POST[f'hbl_account-{i}']
        hbl_shipper = request.POST[f'hbl_shipper-{i}']
        hbl_consignee = request.POST[f'hbl_consignee-{i}']
        mbl_no = request.POST[f'hbl_mbl_no-{i}']
        vessel_name = request.POST[f'hbl_vessel_name-{i}']
        commodity = request.POST[f'hbl_commodity-{i}']
        commodity_type = request.POST[f'hbl_commodity_type-{i}']
        no_of_packages = request.POST[f'hbl_no_of_packages-{i}']
        packages_type = request.POST[f'hbl_packages_type-{i}']
        volume = request.POST[f'hbl_volume-{i}']
        net_weight = request.POST[f'hbl_net_weight-{i}']
        gross_weight = request.POST[f'hbl_gross_weight-{i}']
        chargeable_weight = request.POST[f'hbl_chargeable_weight-{i}']
        hbl = None


        if job_hbl_details_is_update == "yes" and job_hbl_details_is_active == "yes":
            job_hbl_details_id = request.POST[f'job_hbl_details_id-{i}']
            hbl = JobHBL.objects.filter(id=int(job_hbl_details_id)).first()
            hbl.job_hbl_no = job_hbl_no
            hbl.mbl_no = mbl_no
            hbl.vessel_name = vessel_name
            hbl.commodity = commodity
            hbl.commodity_type = commodity_type
            hbl.no_of_packages = no_of_packages
            hbl.packages_type = packages_type
            hbl.volume = volume
            hbl.net_weight = net_weight
            hbl.gross_weight = gross_weight
            hbl.chargeable_weight = chargeable_weight
            hbl.save()

        elif job_hbl_details_is_update == "no" and job_hbl_details_is_active == "yes":
            if job_hbl_no:
                hbl = JobHBL.objects.create(
                    job = job,
                    job_hbl_no = job_hbl_no,
                    mbl_no=mbl_no,
                    vessel_name=vessel_name,
                    commodity = commodity,
                    commodity_type = commodity_type,
                    no_of_packages = no_of_packages,
                    packages_type = packages_type,
                    volume = volume,
                    net_weight = net_weight,
                    gross_weight = gross_weight,
                    chargeable_weight = chargeable_weight
                )

        if job_hbl_details_is_active == "yes" and hbl:

            if hbl_account:
                hbl_account = Party.objects.filter(id=int(hbl_account)).first()
                hbl.hbl_account = hbl_account
            if hbl_shipper:
                hbl_shipper = Party.objects.filter(id=int(hbl_shipper)).first()
                hbl.hbl_shipper = hbl_shipper
            if hbl_consignee:
                hbl_consignee = Party.objects.filter(id=int(hbl_consignee)).first()
                hbl.hbl_consignee = hbl_consignee
            if job_hbl_date:
                hbl.job_hbl_date = job_hbl_date
            hbl.save()

            for j in range(1,total_job_hbl_container_details_rows+1):
                job_hbl_container_details_is_active = request.POST[f'job_hbl_container_details_is_active-{i}{j}']
                job_hbl_container_details_is_deleted = request.POST[f'job_hbl_container_details_is_deleted-{i}{j}']
                job_hbl_container_details_is_update = request.POST[f'job_hbl_container_details_is_update-{i}{j}']
                
                if job_hbl_container_details_is_deleted == "yes":
                    job_hbl_container_details_id = request.POST[f'job_hbl_container_details_id-{i}{j}']
                    container = JobContainer.objects.filter(id=int(job_hbl_container_details_id)).first()
                    container.delete()

                # Value
                job_container_no = request.POST[f'job_hbl_container_no-{i}{j}']
                container_type = request.POST[f'job_hbl_container_type-{i}{j}']
                line_seal = request.POST[f'job_hbl_line_seal-{i}{j}']
                pickup_date = request.POST[f'job_hbl_pickup_date-{i}{j}']
                in_fac_date = request.POST[f'job_hbl_in_fac_date-{i}{j}']
                fac_out_date = request.POST[f'job_hbl_fac_out_date-{i}{j}']
                return_date = request.POST[f'job_hbl_return_date-{i}{j}']
                cfs_in_date = request.POST[f'job_hbl_cfs_in_date-{i}{j}']

            
                

                stuffing_date = request.POST[f'job_hbl_stuffing_date-{i}{j}']
                icd_handover_date = request.POST[f'job_hbl_icd_handover_date-{i}{j}']
                delivery_date = request.POST[f'job_hbl_delivery_date-{i}{j}']
                gross_weight=request.POST[f"job_hbl_gross_wt-{i}{j}"]

                port_handover_date = request.POST[f'job_hbl_port_handover_date-{i}{j}']

                container = None
                if job_hbl_container_details_is_update == "yes" and job_hbl_container_details_is_active == "yes":
                    job_hbl_container_details_id = request.POST[f'job_hbl_container_details_id-{i}{j}']
                    container = JobContainer.objects.filter(id=int(job_hbl_container_details_id)).first()
                    container.job_container_no = job_container_no
                    container.container_type = container_type
                    container.line_seal = line_seal
                    container.gross_wt = gross_weight
                    container.save()

                elif job_hbl_container_details_is_update == "no" and job_hbl_container_details_is_active == "yes":
                    if job_container_no:
                        container = JobContainer.objects.create(
                            job=job,
                            hbl = hbl,
                            job_container_no = job_container_no,
                            container_type = container_type,    
                            line_seal = line_seal,
                            gross_wt = gross_weight
                        )
                    

                if job_hbl_container_details_is_active == "yes" and container:
                    
                        if stuffing_date:
                            container.stuffing_date = stuffing_date
                        if icd_handover_date:
                            container.icd_handover_date = icd_handover_date
                        if port_handover_date:
                            container.port_handover_date = port_handover_date
                        
                        if delivery_date:
                            container.delivery_date = delivery_date
                        
                        if pickup_date:
                            container.pickup_date = pickup_date
                        
                        if in_fac_date:
                            container.in_fac_date = in_fac_date
                        
                        if fac_out_date:
                            container.fac_out_date = fac_out_date
                        if cfs_in_date:
                            container.cfs_in_date = cfs_in_date
                       
                        
                        if return_date:
                            container.return_date = return_date

                        if gross_weight:
                            container.gross_wt = gross_weight
                        container.save()


@login_required(login_url='home:handle_login')
def create_job(request,module):
    context ={}
    check_permissions(request,module)
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
           
            if not request.user.user_account.create_global_data:
                form.instance.company_type = request.user.user_account.office
            
            if form.instance.module == "Sea Export":
                all_approve_application_handlers = DocumentHandler.objects.filter(company_type = form.instance.company_type).filter(is_sea_ex_job=True).all()
            if form.instance.module == "Sea Import":
                all_approve_application_handlers = DocumentHandler.objects.filter(company_type = form.instance.company_type).filter(is_sea_im_job=True).all()
            if form.instance.module == "Air Export":
                all_approve_application_handlers = DocumentHandler.objects.filter(company_type = form.instance.company_type).filter(is_air_ex_job=True).all()
            if form.instance.module == "Air Import":
                all_approve_application_handlers = DocumentHandler.objects.filter(company_type = form.instance.company_type).filter(is_air_im_job=True).all()
            if form.instance.module == "Transport":
                all_approve_application_handlers = DocumentHandler.objects.filter(company_type = form.instance.company_type).filter(is_transport_job=True).all()
            
            if form.instance.company_type.is_job_approve_required:
                minimum_worker = []
                for handler in all_approve_application_handlers:
                    handler_count = len(JobMaster.objects.filter(is_approved=False).filter(application_handler__id=handler.user.id).all())
                    
                    minimum_worker.append({
                        'user':handler.user,
                        'counts':handler_count
                    })
                
                minimum_pos = 0
                for count in range (0,len(minimum_worker)-1):
                    if minimum_worker[count]['counts'] >  minimum_worker[count+1]['counts']:
                        minimum_pos = count+1
            
                handler = DocumentHandler.objects.filter(user=minimum_worker[minimum_pos]['user']).first()
                form.instance.application_handler = handler
                
            else:
                form.instance.is_approved = True
            
            form.save()
            job_transhipments(request,form.instance)
            job_invoice(request,form.instance)
            job_container(request,form.instance)
            if module == "sea_export" or module == 'sea_import':
                job_hbl(request,form.instance)

            if module == "air_export" or module == 'air_import':
                air_job_hbl(request,form.instance)
            
            messages.add_message(request, messages.SUCCESS, f"Success, {form.instance.job_no} New Job Created.")
            return redirect('operations:create_job',module=module)
        
    
    context['form']= form
    context['module']= module
    # context['last_job']= last_job
    # context['jobs_current_len_of_companies']= dumps(current_len_of_companies)
    return render(request,'job/job_create.html',context)



@login_required(login_url='home:handle_login')
def all_job_details(request,module):
    context = {}
    check_permissions(request,module)
    jobs = JobMaster.objects.exclude(Q(job_status='Cancel') | Q(job_status = "Close") | Q(is_deleted = True)).select_related('created_by','shipper','company_type','consignee','importer','port_of_loading','port_of_discharge','application_handler','alternate_company','shipping_line','booking_party','place_of_reciept','place_of_loading','place_of_unloading','account','account_address','created_by','updated_by','account_manager','account_manager__role','final_destination').prefetch_related('job_container','job_hbl','hbl_location').all()
   
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()

    current_month = datetime.now().month
    new_month=current_month-3
    current_year = datetime.now().year
    new_year = current_year
    if new_month < 0:
        new_month = 13 + new_month
        new_year -= 1
    
    if new_month == 0:
        new_month = 12 + new_month
        new_year -= 1

    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(new_year,new_month,1)

    to_date = date(current_year,current_month,end_day)
  
    
    

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        
    jobs = jobs.filter(job_date__range=[from_date,to_date]).all()
    
    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user).all()
    
    
    # if module == "sea_export":
    #     jobs = jobs.filter(module="Sea Export").all()
    # if module == "sea_import":
    #     jobs = jobs.filter(module="Sea Import").all()
    # if module == "air_export":
    #     jobs = jobs.filter(module="Air Export").all()
    # if module == "air_import":
    #     jobs = jobs.filter(module="Air Import").all()
    # if module == "transportation":
    #     jobs = jobs.filter(module="Transport").all()
              
              
    context['jobs']= jobs
    context['module']= module
    context['all_jobs'] = True
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    return render(request,'job/job_details.html',context)



@login_required(login_url='home:handle_login')
def job_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(JobMaster, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:job_details',module=module)
    created_by = obj.created_by
    company_type = obj.company_type
    application_handler = obj.application_handler
    
    form = JobForm(instance = obj, job=obj, update=True)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=obj, job=obj, update=True)
        
        if form.is_valid():
            form.instance.created_by = created_by
            form.instance.updated_by = request.user
            if not request.user.user_account.create_global_data:
                form.instance.company_type = company_type
            
            if form.instance.company_type.is_job_approve_required:
                form.instance.application_handler = application_handler
            else:
                form.instance.is_approved = True
            job_transhipments(request,form.instance)
            job_invoice(request,form.instance)
            job_container(request,form.instance)
            if module == 'air_import' or module == 'air_export':
                air_job_hbl(request,form.instance)
            else :
                job_hbl(request,form.instance)
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Success, {form.instance.job_no} Updated Successfully.")
            return redirect('operations:job_details',module=module)
        
   
          
    context['form']= form
    context['data']= obj
    context['module']= module
    context['update']= True
    context['job_container']= obj.job_container.filter(hbl=None).all()
    return render(request,'job/job_create.html',context)


@login_required(login_url='home:handle_login')
def close_job_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(JobMaster, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:job_details',module=module)
    created_by = obj.created_by
    company_type = obj.company_type
    application_handler = obj.application_handler
    
    form = JobForm(instance = obj)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=obj)
        
        if form.is_valid():
            form.instance.created_by = created_by
            form.instance.updated_by = request.user
            if not request.user.user_account.create_global_data:
                form.instance.company_type = company_type
            
            if form.instance.company_type.is_job_approve_required:
                form.instance.application_handler = application_handler
            else:
                form.instance.is_approved = True
            job_transhipments(request,form.instance)
            job_invoice(request,form.instance)
            job_container(request,form.instance)
            job_hbl(request,form.instance)
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Success, {form.instance.job_no} Updated Successfully.")
            return redirect('operations:closed_jobs',module=module)
        
   
          
    context['form']= form
    context['data']= obj
    context['module']= module
    context['update']= True
    context['job_container']= obj.job_container.filter(hbl=None).all()
    return render(request,'job/job_create.html',context)


@login_required(login_url='home:handle_login')
def job_details(request,module):
    context = {}
    check_permissions(request,module)
    jobs = JobMaster.objects.exclude(Q(job_status='Cancel') | Q(job_status = "Close") | Q(is_deleted = True)).select_related('created_by','shipper','company_type','consignee','importer','port_of_loading','port_of_discharge','application_handler','alternate_company','shipping_line','booking_party','place_of_reciept','place_of_loading','place_of_unloading','account','account_address','created_by','updated_by','account_manager','account_manager__role','final_destination').prefetch_related('job_container','job_hbl','hbl_location').all()
   
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()

    current_month = datetime.now().month
    new_month=current_month-3
    current_year = datetime.now().year
    new_year = current_year
    if new_month < 0:
        new_month = 13 + new_month
        new_year -= 1
    
    if new_month == 0:
        new_month = 12 + new_month
        new_year -= 1

    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(new_year,new_month,1)

    to_date = date(current_year,current_month,end_day)
  
    
    

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        
    jobs = jobs.filter(job_date__range=[from_date,to_date]).all()
    
    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user).all()
    
    
    if module == "sea_export":
        jobs = jobs.filter(module="Sea Export").all()
    if module == "sea_import":
        jobs = jobs.filter(module="Sea Import").all()
    if module == "air_export":
        jobs = jobs.filter(module="Air Export").all()
    if module == "air_import":
        jobs = jobs.filter(module="Air Import").all()
    if module == "transportation":
        jobs = jobs.filter(module="Transport").all()
              
              
    context['jobs']= jobs
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    return render(request,'job/job_details.html',context)

@login_required(login_url='home:handle_login')
def job_pending_approve_details(request,module):
    context = {}
    check_permissions(request,module)
    
    application_handler = DocumentHandler.objects.filter(user__id=request.user.id).first()
    jobs = JobMaster.objects.filter(is_approved=False).filter(is_deleted=False).filter(application_handler=application_handler).all()
    
    if module == "sea_export":
        jobs = jobs.filter(module="Sea Export").all()
    if module == "sea_import":
        jobs = jobs.filter(module="Sea Import").all()
    if module == "air_export":
        jobs = jobs.filter(module="Air Export").all()
    if module == "air_import":
        jobs = jobs.filter(module="Air Import").all()
    if module == "transportation":
        jobs = jobs.filter(module="Transport").all()
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()
              
    context['jobs']= jobs
    context['module']= module

    return render(request,'job/job_pending_approve_details.html',context)



@login_required(login_url='home:handle_login')
def approve_job(request,module,id):
    check_permissions(request,module)
   
    if request.method == "POST":
        job_no = request.POST['verify_job_no']
        job = JobMaster.objects.filter(id=int(id)).first()
        if job.job_no == job_no:
            job.is_approved = True
            job.save()
            messages.add_message(request, messages.SUCCESS, f"Success, {job.job_no} is approved.")
        else:
            messages.add_message(request, messages.SUCCESS, f"Fail, {job.job_no} is not approved.")
        return redirect('operations:job_pending_approve_details',module=module)
    return redirect('operations:job_pending_approve_details',module=module)
              

@login_required(login_url='home:handle_login')
def closed_jobs(request,module):
    context = {}
    check_permissions(request,module)
    jobs = JobMaster.objects.filter(job_status = "Close").filter(is_deleted = False).select_related('created_by','shipper','company_type','consignee','port_of_loading','port_of_discharge','application_handler','alternate_company','shipping_line','booking_party','place_of_reciept','place_of_loading','place_of_unloading','account','account_address').prefetch_related('job_container').all()
   
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()

    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        
    jobs = jobs.filter(job_date__range=[from_date,to_date]).all()
    
    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user).all()
    
    
    if module == "sea_export":
        jobs = jobs.filter(module="Sea Export").all()
    if module == "sea_import":
        jobs = jobs.filter(module="Sea Import").all()
    if module == "air_export":
        jobs = jobs.filter(module="Air Export").all()
    if module == "air_import":
        jobs = jobs.filter(module="Air Import").all()
    if module == "transportation":
        jobs = jobs.filter(module="Transport").all()
              
              
    context['jobs']= jobs
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    return render(request,'job/closed_jobs.html',context)



@login_required(login_url='home:handle_login')
def cancelled_jobs(request,module):
    context = {}
    check_permissions(request,module)
    jobs = JobMaster.objects.filter(Q(is_deleted=True) | Q(job_status="Cancel")).select_related('created_by','shipper','company_type','consignee','port_of_loading','port_of_discharge','application_handler','alternate_company','shipping_line','booking_party','place_of_reciept','place_of_loading','place_of_unloading','account','account_address').prefetch_related('job_container').all()
   
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()

    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        
    jobs = jobs.filter(job_date__range=[from_date,to_date]).all()
    
    if not request.user.user_account.also_handle_other_work:
        jobs = jobs.filter(created_by=request.user).all()
    
    
    if module == "sea_export":
        jobs = jobs.filter(module="Sea Export").all()
    if module == "sea_import":
        jobs = jobs.filter(module="Sea Import").all()
    if module == "air_export":
        jobs = jobs.filter(module="Air Export").all()
    if module == "air_import":
        jobs = jobs.filter(module="Air Import").all()
    if module == "transportation":
        jobs = jobs.filter(module="Transport").all()
              
              
    context['jobs']= jobs
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    return render(request,'job/cancelled_jobs.html',context)

@login_required(login_url='home:handle_login')
def reterive_cancelled_jobs(request,module,id):
    context = {}
    check_permissions(request,module)
    jobs = JobMaster.objects.all()
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        jobs = jobs.filter(Q(company_type=company) | Q(alternate_company=company)).all()
        
    jobs = jobs.filter(id=id).first()
    
    if JobMaster.objects.filter(job_no = jobs.job_no).filter(is_deleted = False).exists() :
        messages.error(request, "An Active Job Already Exists with this Job Number")
        return redirect(reverse('operations:cancelled_jobs', kwargs={'module': module}))

    else:
        if jobs.job_status == 'Cancel':
            jobs.job_status = 'Open'
        if jobs.is_deleted == True:
            jobs.is_deleted = False
            jobs.deleted_by = None
        jobs.save()
        messages.success(request, "Job reterived Successfully")
        return redirect(reverse('operations:cancelled_jobs', kwargs={'module': module}))
    
   
    
    
    
    
    if module == "sea_export":
        jobs = jobs.filter(module="Sea Export").all()
    if module == "sea_import":
        jobs = jobs.filter(module="Sea Import").all()
    if module == "air_export":
        jobs = jobs.filter(module="Air Export").all()
    if module == "air_import":
        jobs = jobs.filter(module="Air Import").all()
    if module == "transportation":
        jobs = jobs.filter(module="Transport").all()
              
              
    context['jobs']= jobs
    context['module']= module
    return render(request,'job/cancelled_jobs.html',context)

@login_required(login_url='home:handle_login')
def job_delete(request,module,id):
    check_permissions(request,module)
    job = JobMaster.objects.filter(id=int(id)).first()
    job.is_deleted = True
    job.deleted_by = request.user
    job.save()
    return redirect('operations:job_details',module=module)


# CAN Form
@login_required(login_url='home:handle_login')
def create_can(request,module):
    context ={}
    check_permissions(request,module)
  
    current_month = str(datetime.now().month).zfill(2)
    current_year = str(datetime.now().year)[2:]
    current_length = len(CargoArrivalNotice.objects.all())
    can_no = "PCTICAN"+current_month+current_year
    
    
    
    form = CargoArrivalForm(request.POST or None)
    if form.is_valid():
        arr_no = can_no+str(current_length).zfill(3)
        already_check = CargoArrivalNotice.objects.filter(arrival_notice_no=arr_no).all()
        duplicate = False
        if len(already_check) > 0:
            duplicate = True
            
        while duplicate:
            current_length += 1
            arr_no = can_no+str(current_length).zfill(3)
            already_check = CargoArrivalNotice.objects.filter(arrival_notice_no=arr_no).first()
            if not already_check:
                duplicate = False
        
        form.instance.arrival_notice_no = arr_no
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Cargo Arrival Notice Created.")
        return redirect('operations:create_can',module=module)
    
    context['form']= form
    context['module']= module
    
    return render(request,'cargo_arrival/can_create.html',context)


@login_required(login_url='home:handle_login')
def can_details(request,module):
    context ={}
    check_permissions(request,module)

    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    cans = CargoArrivalNotice.objects.select_related('company_type','job','created_by','shipping_line','hbl').all()
    if not request.user.user_account.see_global_data:
        cans = cans.filter(company_type=company).all()
  
    if request.method == 'POST':
        
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
          
      
    cans = cans.filter(date__range = [from_date,to_date]).all()
            
    if not request.user.user_account.also_handle_other_work:
        cans = cans.filter(created_by=request.user).all()
          
    context['cans']= cans
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    return render(request,'cargo_arrival/can_details.html',context)


@login_required(login_url='home:handle_login')
def can_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(CargoArrivalNotice, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:can_details',module=module)
    
    form = CargoArrivalForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    arrival_notice_no = obj.arrival_notice_no
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.arrival_notice_no = arrival_notice_no
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:can_details',module=module)
    
    
    
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'cargo_arrival/can_create.html',context)


@login_required(login_url='home:handle_login')
def can_delete(request,module,id):
    check_permissions(request,module)
    can = CargoArrivalNotice.objects.filter(id=int(id)).first()
    can.delete()
    return redirect('operations:can_details',module=module)

@login_required(login_url='home:handle_login')
def can_pdf(request,id):
    can = CargoArrivalNotice.objects.filter(id=int(id)).first()
    total_collect = 0
    try:
        for i in can.job.manifest_job.first().manifest_charges_collect.all():
            total_collect += i.total
    except:
        total_collect = 0
    context = {
        'data':can,
        'total_collect':total_collect,

    }
    return render(request,'cargo_arrival/pdf.html',context)

# VGM Form
    
@login_required(login_url='home:handle_login')
def create_vgm(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = VGMForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
            
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New VGM Created.")
        return redirect('operations:create_vgm',module=module)

 
    
    context['form']= form
    context['module']= module
    
    return render(request,'vgm/vgm_create.html',context)


@login_required(login_url='home:handle_login')
def vgm_details(request,module):
    context ={}
    check_permissions(request,module)
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        vgms = VGMMaster.objects.filter(company_type=company).all()
    else:
        vgms = VGMMaster.objects.all()
    
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
            vgms = VGMMaster.objects.filter(job__job_date__gte = start_date).filter(job__job_date__lte = end_date).filter(company_type=company).all()
        else:
            vgms = VGMMaster.objects.filter(job__job_date__gte = start_date).filter(job__job_date__lte = end_date).all()
            
    if not request.user.user_account.also_handle_other_work:
        vgms = vgms.filter(created_by=request.user).all()
        
          
    context['vgms']= vgms
    context['module']= module
    context['current_month']= current_month
    return render(request,'vgm/vgm_details.html',context)


@login_required(login_url='home:handle_login')
def vgm_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(VGMMaster, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:vgm_details',module=module)
    
    created_by = obj.created_by
    company_type = obj.company_type
    form = VGMForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:vgm_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'vgm/vgm_create.html',context)


@login_required(login_url='home:handle_login')
def vgm_delete(request,module,id):
    check_permissions(request,module)
    vgm = VGMMaster.objects.filter(id=int(id)).first()
    vgm.delete()
    return redirect('operations:vgm_details',module=module)

# Delivery Order
    
@login_required(login_url='home:handle_login')
def create_do(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = DeliveryOrderForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Delivery Order Created.")
        return redirect('operations:create_do',module=module)
    
    context['form']= form
    context['module']= module
    
    return render(request,'delivery_order/do_create.html',context)


@login_required(login_url='home:handle_login')
def do_details(request,module):
    context ={}
    check_permissions(request,module)

    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    orders = DeliveryOrder.objects.select_related('company_type','job','created_by').all()
    if not request.user.user_account.see_global_data:
        orders = orders.filter(company_type=company).all()
  
    if request.method == 'POST':
        
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
          
      
    orders = orders.filter(date__range = [from_date,to_date]).all()
            
    if not request.user.user_account.also_handle_other_work:
        orders = orders.filter(created_by=request.user).all()
          
    context['orders']= orders
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),'%Y-%m-%d')
    context['to_date']= datetime.strptime(str(to_date),'%Y-%m-%d')
    return render(request,'delivery_order/do_details.html',context)


@login_required(login_url='home:handle_login')
def do_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(DeliveryOrder, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:do_details',module=module)
    
    created_by = obj.created_by
    company_type = obj.company_type
    form = DeliveryOrderForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:do_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'delivery_order/do_create.html',context)


@login_required(login_url='home:handle_login')
def do_delete(request,module,id):
    check_permissions(request,module)
    do = DeliveryOrder.objects.filter(id=int(id)).first()
    do.delete()
    return redirect('operations:do_details',module=module)


@login_required(login_url='home:handle_login')
def do_pdf(request,id):
    do = DeliveryOrder.objects.filter(id=int(id)).first()
    
    context = {
        'data':do,

    }
    return render(request,'delivery_order/pdf.html',context)

# Freight Certificate
    
@login_required(login_url='home:handle_login')
def create_fc(request,module):
    context ={}

    check_permissions(request,module)
  
    form = FreightCertificateForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Freight Certificate Created.")
        return redirect('operations:create_fc',module=module)
    
    context['form']= form
    context['module']= module
    
    return render(request,'freight_certificate/fc_create.html',context)


@login_required(login_url='home:handle_login')
def fc_details(request,module):
    context ={}
    check_permissions(request,module)
    
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        certificates = FreightCertificate.objects.filter(company_type=company).all()
    else:
        certificates = FreightCertificate.objects.all()
    
    
    
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
            certificates = FreightCertificate.objects.filter(job__job_date__gte = start_date).filter(job__job_date__lte = end_date).filter(company_type=company).all()
        else:
            certificates = FreightCertificate.objects.filter(job__job_date__gte = start_date).filter(job__job_date__lte = end_date).all()
        
    if not request.user.user_account.also_handle_other_work:
        certificates = certificates.filter(created_by=request.user).all()
          
    context['certificates']= certificates
    context['module']= module
    context['current_month']= current_month
    return render(request,'freight_certificate/fc_details.html',context)


@login_required(login_url='home:handle_login')
def fc_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(FreightCertificate, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:fc_details',module=module)
    
    form = FreightCertificateForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:fc_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'freight_certificate/fc_create.html',context)


@login_required(login_url='home:handle_login')
def fc_delete(request,module,id):
    check_permissions(request,module)
    fc = FreightCertificate.objects.filter(id=int(id)).first()
    fc.delete()
    return redirect('operations:fc_details',module=module)

from django.contrib.sites.models import Site

from accounting.utils import generate_pdf
def fc_pdf(request,id):
    template_path = 'freight_certificate/pdf2.html'
    fc = FreightCertificate.objects.filter(id=int(id)).first()
    domain = Site.objects.get_current().domain



    total_gross_wt=[]
    for i in fc.hbl_options.all():
   
        for j in i.job_container_hbl.all():
            try:
                print(j.gross_wt)
                total_gross_wt.append((float(j.gross_wt)))
            except:
                total_gross_wt=""

    
    # try:
    #    gross_w=[int(float(i.gross_wt.split(' ')[0])) for i in fc.job.job_container.all()]
    #    grss_w=sum(gross_w)
    # except:
    #     grss_w=0
    
    context = {
        'data':fc,
        'total_gross_wt':sum(total_gross_wt),
        
        'domain':domain
      
    }
    
    return generate_pdf(request,template_path,context)


# Master Bill Of Lading
    
@login_required(login_url='home:handle_login')
def create_mbl(request,module):
    context ={}

    check_permissions(request,module)
  

    form = MBLForm()
    if request.method == 'POST':
        form = MBLForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
           

            if not request.user.user_account.create_global_data:
                form.instance.company_type = request.user.user_account.office
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Success, New MBL Created.")
            return redirect('operations:create_mbl',module=module)

    context['form']= form
    context['module']= module
 
    
    return render(request,'mbl/mbl_create.html',context)


@login_required(login_url='home:handle_login')
def mbl_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    
    mbls = MBLMaster.objects.select_related('company_type','job_no','created_by','consigned_name','exporter_name').all()

    if not request.user.user_account.see_global_data:
        mbls = mbls.filter(company_type=company).all()
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    if request.method == 'POST':
       
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
            
        
    mbls = mbls.filter(date__range = [from_date,to_date]).all()
    
            
    if not request.user.user_account.also_handle_other_work:
        mbls = mbls.filter(created_by=request.user).all()
          
    context['mbls']= mbls
    context['module']= module
    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d").date()
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d").date()
    return render(request,'mbl/mbl_details.html',context)


@login_required(login_url='home:handle_login')
def mbl_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(MBLMaster, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:mbl_details',module=module)
    
    form = MBLForm( instance = obj)
    created_by = obj.created_by
    is_duplicate = obj.is_duplicate
    duplicate_check = obj.duplicate_check
    company_type = obj.company_type
    if request.method == "POST":
        form = MBLForm(request.POST,request.FILES, instance = obj)
        if form.is_valid():
            form.instance.created_by = created_by
            form.instance.updated_by = request.user
            form.instance.is_duplicate = is_duplicate
            form.instance.duplicate_check = duplicate_check

            
            if not request.user.user_account.create_global_data:
                form.instance.company_type = company_type
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
            return redirect('operations:mbl_details',module=module)
            
    context['form']= form
    context['module']= module
    context['id']= id
    context['update']= True
    return render(request,'mbl/mbl_create.html',context)


@login_required(login_url='home:handle_login')
def mbl_delete(request,module,id):
    check_permissions(request,module)
    mbl = MBLMaster.objects.filter(id=int(id)).first()
    mbl.delete()
    
    return redirect('operations:mbl_details',module=module)





@login_required(login_url='home:handle_login')
def mbl_duplicate(request,module,id):
    check_permissions(request,module)
    mbl_obj=MBLMaster.objects.filter(id=int(id)).first()
    mbl_obj.duplicate_check=True
    mbl_obj.save()
    new_mbl=MBLMaster.objects.create(
        company_type=mbl_obj.company_type,
        mbl_no=mbl_obj.mbl_no,
        date=mbl_obj.date,
        job_no=mbl_obj.job_no,
        exporter_name=mbl_obj.exporter_name,
        exporter_address=mbl_obj.exporter_address,
        consigned_name=mbl_obj.consigned_name,
        notify_party=mbl_obj.notify_party,
        notify_party_address=mbl_obj.notify_party_address,
        mtd_number=mbl_obj.mtd_number,
        shipment_ref_no=mbl_obj.shipment_ref_no,
        type=mbl_obj.type,
        executed_at=mbl_obj.executed_at,
        shipper_board_date=mbl_obj.shipper_board_date,
        movement_type=mbl_obj.movement_type,
        freight_type=mbl_obj.freight_type,
        total_weight=mbl_obj.total_weight,
        total_packages=mbl_obj.total_packages,
        carrier=mbl_obj.carrier,
        currency=mbl_obj.currency,
        freight=mbl_obj.freight,
        no_of_o_mtd=mbl_obj.no_of_o_mtd,
        freight_charge_amt=mbl_obj.freight_charge_amt,
        freight_payable_at=mbl_obj.freight_payable_at,
        export_references=mbl_obj.export_references,
        forwarding_agent=mbl_obj.forwarding_agent,
        point_and_country_of_origin=mbl_obj.point_and_country_of_origin,
        loading_pier=mbl_obj.loading_pier,
        domestic_routing=mbl_obj.domestic_routing,
        pre_carriage_by=mbl_obj.pre_carriage_by,
        ocean_vessel=mbl_obj.ocean_vessel,
        port_of_loading_export=mbl_obj.port_of_loading_export,
        place_of_delivery=mbl_obj.place_of_delivery,
        place_of_receipt=mbl_obj.place_of_receipt,
        voyage_no=mbl_obj.voyage_no,
        port_of_discharge=mbl_obj.port_of_discharge,
        declared_value=mbl_obj.declared_value,
        agent_name=mbl_obj.agent_name,
        agent_address=mbl_obj.agent_address,
        marks_and_number=mbl_obj.marks_and_number,
        no_of_packages=mbl_obj.no_of_packages,
        description_of_commodities=mbl_obj.description_of_commodities,
        gross_weight=mbl_obj.gross_weight,
        measurement=mbl_obj.measurement,
        mbl_type=mbl_obj.mbl_type,
        is_duplicate=True,
        

    )
    new_mbl.save()
    messages.success(request,f'MBL Duplicate Created {mbl_obj.id}')
    return redirect('operations:mbl_update',module=module,id=mbl_obj.id)

# DSR
    
@login_required(login_url='home:handle_login')
def create_dsr(request,module):
    context ={}


    check_permissions(request,module)
  
    form = DSRForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New DSR Created.")
        return redirect('operations:create_dsr',module=module)
    else:
        print('-----',form.errors.as_json)
    
    context['form']= form
    context['module']= module
    
    return render(request,'dsr/dsr_create.html',context)


   
def send_dsr(request,module,data,from_url):
   
    # to_email = [data['party_email'],]
    to_email = ['sg330415@gmail.com',]
    subject = f"DSR Report From {data['data'][0].company_type.company_name}  - {data['data'][0].company_type.branch_name}"
    html_content = render_to_string("dsr/dsr_email.html",{
        'data':data['data'],
        'first_data':data['data'][0],
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
    EmailThread(msg).start()
    return redirect(f'operations:{from_url}',module=module)



def job_list_export_excel(jobs):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name='DSR')

    cell_format2 = workbook.add_format({ 'font_color': 'black','bg_color':"#feff37","align":"center",'border':1,'border_color':'black'})
    cell_format2_wc = workbook.add_format({'font_color': '#ffffff',"align":"center","bg_color":"#245a64",'border':1,'border_color':'black'})
    worksheet.set_column(0, 20, 20)
    worksheet.write("A1","DATE",cell_format2)
    worksheet.write("B1","JOB NO.",cell_format2)
    worksheet.write("C1","CNEE",cell_format2)
    worksheet.write("D1","SHIPPER",cell_format2)
    worksheet.write("E1","POL",cell_format2)
    worksheet.write("F1","POD",cell_format2)
    worksheet.write("G1","EQUIP",cell_format2)
    worksheet.write("H1","S/L",cell_format2)
    worksheet.write("I1","F.POD",cell_format2)
    worksheet.write("J1","HBL NO.",cell_format2)
    worksheet.write("K1","MBL NO.",cell_format2)
    worksheet.write("L1","CONT. NO.",cell_format2)
    worksheet.write("M1","VSL/VOY.",cell_format2)
    worksheet.write("N1","NO. OF PACKAGES",cell_format2)
    worksheet.write("O1","STATUS",cell_format2)
    worksheet.write("P1","RAIL OUT",cell_format2)
    worksheet.write("Q1","SALES PERSON",cell_format2)
    start_index = 2

    

    for data in jobs:
        job = data.job
        len_of_con=data.job_container_hbl.count()
    

        if job.job_date:
            worksheet.write(f"A{start_index}", f"{datetime.strftime(job.job_date,'%d.%m.%Y')}", cell_format2_wc)
            
        worksheet.write(f"B{start_index}", f"{job.job_no}", cell_format2_wc)
        worksheet.write(f"C{start_index}", f"{data.hbl_consignee}", cell_format2_wc)
        worksheet.write(f"D{start_index}", f"{data.hbl_shipper}", cell_format2_wc)
        worksheet.write(f"E{start_index}", f"{job.port_of_loading}", cell_format2_wc)
        worksheet.write(f"F{start_index}", f"{job.port_of_discharge}", cell_format2_wc)  
        worksheet.write(f"H{start_index}", f"{job.shipping_line}", cell_format2_wc)
        worksheet.write(f"I{start_index}", f"{job.final_destination}", cell_format2_wc)
        worksheet.write(f"J{start_index}", f"{data.job_hbl_no}", cell_format2_wc)
        worksheet.write(f"K{start_index}", f"{data.mbl_no}", cell_format2_wc)
        

        worksheet.write(f"M{start_index}", f"{job.vessel_voy_name}", cell_format2_wc)
        worksheet.write(f"N{start_index}", f"{job.no_of_packages}", cell_format2_wc)
        worksheet.write(f"O{start_index}", f"{job.status}", cell_format2_wc)
        

        worksheet.write(f"Q{start_index}", f"{job.account_manager}", cell_format2_wc)
        
      
        container_no=[]
        eqp_type=[]
        rail_out_datee=[]
        
        d1 = ""
        d2 = ""
        d3 = ""
       
        
        for j in data.job_container_hbl.all():
          
            container_no.append(j.job_container_no)
            d1=(" / ".join(container_no))
            
            eqp_type.append(j.container_type)
            d2=(" / ".join(eqp_type))
            
            rail_out_datee.append(str(j.railout_date))
            d3=(" / ".join(rail_out_datee))
            

        worksheet.write(f"G{start_index}",f"{d2}",cell_format2_wc)
        worksheet.write(f"L{start_index}",f"{d1}",cell_format2_wc)
        worksheet.write(f"P{start_index}",f"{d3}",cell_format2_wc)
        start_index += 1
            
        
   
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="DSR-job.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

# return the response
    return response



@login_required(login_url='home:handle_login')
def dsr_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    if not request.user.user_account.see_global_data:
        dsrs = DSR.objects.filter(company_type=company).all()
    else:
        dsrs = DSR.objects.all()
    
    if not request.user.user_account.also_handle_other_work:
        dsrs = dsrs.filter(created_by=request.user).all()
    
    if request.method == "POST" and request.POST['action_type'] == "EXPORT DSR":
        selected_fields = request.POST['selected_fields']
        selected_fields = selected_fields.split(',')
        party_dsr = []
        for i in selected_fields:
            
            hbl = JobHBL.objects.filter(job=int(i)).first()
            party_dsr.append(
                hbl
            )

        job_list_export_excel(party_dsr)
        
        
    if request.method == "POST" and request.POST['action_type'] == "SEND DSR":
        selected_fields = request.POST['selected_fields']
        selected_fields = selected_fields.split(',')
        party_dsr = []
        for i in selected_fields:
            dsr = DSR.objects.filter(id=int(i)).first()
            flag = 0
            for j in party_dsr:
                if dsr.job.account:
                    if dsr.job.account.party_name == j['party']:
                        flag = 1
                        j['data'].append(dsr)
                       
                            
            if flag == 0:
                if dsr.job:
                    if dsr.job.account_address:
                        party_dsr.append({'party':dsr.job.account_address.party.party_name,'party_email':dsr.job.account_address.corp_email.strip(),'data':[dsr]})

        for i in party_dsr:
            send_dsr(request,module,i,"dsr_details")
                            
        
          
    context['dsrs']= dsrs
    context['module']= module
    return render(request,'dsr/dsr_details.html',context)


@login_required(login_url='home:handle_login')
def dsr_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(DSR, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:dsr_details',module=module)
    
    form = DSRForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:dsr_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'dsr/dsr_create.html',context)


@login_required(login_url='home:handle_login')
def dsr_delete(request,module,id):
    check_permissions(request,module)
    dsr = DSR.objects.filter(id=int(id)).first()
    dsr.delete()
    return redirect('operations:dsr_details',module=module)



@login_required(login_url='home:handle_login')
def dsr_hbl_details(request,module):
    context ={}
    check_permissions(request,module)
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    dsrs = JobHBL.objects.select_related('job','hbl_consignee','hbl_shipper','job__company_type','job__port_of_loading','job__port_of_discharge','job__final_destination','job__account_manager').all()

    if not request.user.user_account.see_global_data:
        dsrs = JobHBL.objects.filter(job__company_type=company).all()
    
    if not request.user.user_account.also_handle_other_work:
        dsrs = dsrs.filter(created_by=request.user).all()
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    from_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
            
    dsrs = dsrs.filter(job__job_date__range=[from_date,to_date]).all()
    
    context['from_date']= datetime.strptime(str(from_date),"%Y-%m-%d").date()
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d").date()
    context['dsrs']= dsrs
    context['module']= module
    return render(request,'dsr/dsr_hbl_details.html',context)

@login_required(login_url='home:handle_login')
def dsr_actions(request,module):
    if request.method == "POST" and request.POST['action_type'] == "EXPORT DSR":
        selected_fields = request.POST['selected_fields']
        selected_fields = selected_fields.split(',')
        party_dsr = []
        print("Exported")
        for i in selected_fields:
            hbl = JobHBL.objects.filter(id=int(i)).first()
            print(hbl)
            party_dsr.append(
                hbl
            )
        return job_list_export_excel(party_dsr)
        
        
    if request.method == "POST" and request.POST['action_type'] == "SEND DSR":
        selected_fields = request.POST['selected_fields']
        selected_fields = selected_fields.split(',')
        party_dsr = []
        for i in selected_fields:
            dsr = DSR.objects.filter(id=int(i)).first()
            flag = 0
            for j in party_dsr:
                if dsr.job.account:
                    if dsr.job.account.party_name == j['party']:
                        flag = 1
                        j['data'].append(dsr)
                       
                            
            if flag == 0:
                if dsr.job:
                    if dsr.job.account_address:
                        party_dsr.append({'party':dsr.job.account_address.party.party_name,'party_email':dsr.job.account_address.corp_email.strip(),'data':[dsr]})

        for i in party_dsr:
            send_dsr(request,module,i,"dsr_details")

    return redirect('operations:dsr_hbl_details',module=module)
                            

# Booking Form
    
@login_required(login_url='home:handle_login')
def create_booking(request,module):
    context ={}
    check_permissions(request,module)
  
    form = TransportBookingForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New Booking Created.")
        return redirect('operations:create_booking',module=module)
    
    context['form']= form
    context['module']= module
    
    return render(request,'booking/booking_create.html',context)


@login_required(login_url='home:handle_login')
def booking_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    bookings = TransportBooking.objects.all()
    
    
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
        
        
        bookings = TransportBooking.objects.filter(created_at__gte = start_date).filter(created_at__lte = end_date).all()
        
      
            
    if not request.user.user_account.see_global_data:
        bookings = bookings.filter(company_type=company).all()
    
            
    if not request.user.user_account.also_handle_other_work:
        bookings = bookings.filter(created_by=request.user).all()
          
    context['bookings']= bookings
    context['module']= module
    context['current_month']= current_month
    return render(request,'booking/booking_details.html',context)


@login_required(login_url='home:handle_login')
def booking_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(TransportBooking, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:booking_details',module=module)
    
    form = TransportBookingForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:booking_details',module=module)
    
    
    
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'booking/booking_create.html',context)


@login_required(login_url='home:handle_login')
def booking_delete(request,module,id):
    check_permissions(request,module)
    booking = TransportBooking.objects.filter(id=int(id)).first()
    booking.delete()
    return redirect('operations:booking_details',module=module)


# GR Form
    
def handle_backload_gr(id):
    gr_data = GRMaster.objects.filter(id=id).first()
    gr = GRMaster.objects.create(
            job=gr_data.job,
            gr_date=gr_data.gr_date,
            company_type=gr_data.company_type,
            gr_backloaded = True,
            trailor_no = gr_data.trailor_no,
            driver = gr_data.driver,
            container_no = gr_data.container_no,
        )
    gr.save()
    
@login_required(login_url='home:handle_login')
def create_gr(request,module):
    context ={}
    check_permissions(request,module)
    
    form = GRForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        if not request.user.user_account.create_global_data:
            form.instance.company_type = request.user.user_account.office
        form.save()
        if form.instance.back_loading == "YES":
            handle_backload_gr(form.instance.id)
            form.instance.is_backloaded = True
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, New GR Created.")
        return redirect('operations:create_gr',module=module)
    
    context['form']= form
    context['module']= module
    
    return render(request,'gr/gr_create.html',context)


@login_required(login_url='home:handle_login')
def gr_details(request,module):
    context ={}
    check_permissions(request,module)
    
    company = Logistic.objects.filter(id=request.user.user_account.office.id).first()
    grs = GRMaster.objects.select_related('company_type','created_by','job','consignor','consignee').prefetch_related('invoice_gr').all()

    current_month = datetime.now().month
    current_year = datetime.now().year
    _,end_day = calendar.monthrange(current_year, current_month)
    start_date = date(current_year,current_month,1)
    to_date = date(current_year,current_month,end_day)
    from_to_date = to_date + timedelta(days=1)
    
    if request.method == 'POST':
        
        start_date = request.POST['from_date']
        to_date = request.POST['to_date']
        from_to_date = datetime.strptime(to_date,'%Y-%m-%d').date() + timedelta(days=1)
            
    grs = grs.filter(gr_date__range =[start_date,from_to_date]).all()

    if not request.user.user_account.see_global_data:
        grs = grs.filter(company_type=company).all()
            
    if not request.user.user_account.also_handle_other_work:
        grs = grs.filter(created_by=request.user).all()

    context['grs']= grs
    context['module']= module
    context['from_date']= datetime.strptime(str(start_date),"%Y-%m-%d")
    context['to_date']= datetime.strptime(str(to_date),"%Y-%m-%d")
    return render(request,'gr/gr_details.html',context)


@login_required(login_url='home:handle_login')
def gr_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
  
    obj = get_object_or_404(GRMaster, id = id)
    
    if not request.user.user_account.also_handle_other_work and not obj.created_by == request.user:
        messages.add_message(request, messages.SUCCESS, f"You are not authenticated to perform this action")
        return redirect('operations:gr_details',module=module)
    
    form = GRForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    company_type = obj.company_type
    is_backloaded = obj.is_backloaded
    gr_backloaded = obj.gr_backloaded
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user
        form.instance.is_backloaded = is_backloaded
        form.instance.gr_backloaded = gr_backloaded
        if not request.user.user_account.create_global_data:
            form.instance.company_type = company_type
        
        if form.instance.back_loading == "YES" and not is_backloaded:
            handle_backload_gr(form.instance.id)
            form.instance.is_backloaded = True
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:gr_details',module=module)
    
    
    
    context['form']= form
    context['module']= module
    context['update']= True
    return render(request,'gr/gr_create.html',context)


@login_required(login_url='home:handle_login')
def gr_delete(request,module,id):
    check_permissions(request,module)
    gr = GRMaster.objects.filter(id=int(id)).first()

    gr.delete()
    return redirect('operations:gr_details',module=module)

# ------------------Rate Master----------------

def handle_rate_bh(request,id):
    rate = RateMaster.objects.filter(id=id).first()
    rate_heads = RateMasterDetails.objects.filter(rate__id = id).all()
    rate_heads.delete()
    
    total_heads = int(request.POST['rate_head_total'])
    for i in range(1,total_heads+1):
        is_active = request.POST[f'active-{i}']
        if is_active == "yes":
            billing_head = request.POST[f'bill_head-{i}']
            billing_head = BillingHead.objects.filter(id=int(billing_head)).first()
            bh_type = request.POST[f'type-{i}']
            amount = request.POST[f'rate-{i}']
            
            new_rate_head = RateMasterDetails.objects.create(
                rate = rate,
                billing_head = billing_head,
                bh_type = bh_type,
                amount = amount,
                net_amount = amount,
            )
            new_rate_head.save()

    
@login_required(login_url='home:handle_login')
def create_rate(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = RateMasterForm()
    
    if request.method == "POST":
        form = RateMasterForm(request.POST,request.FILES)
        
    
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        
        handle_rate_bh(request,form.instance.id)
        
        messages.add_message(request, messages.SUCCESS, f"Success, New Rate Created.")
        return redirect('operations:create_rate',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'rate/rate_create.html',context)


@login_required(login_url='home:handle_login')
def rate_details(request,module):
    context ={}
    check_permissions(request,module)
    
    rates = RateMaster.objects.select_related('carrier','pol','pod','fpd').filter(to_date__gte = date.today()).all()
          
    context['rates']= rates
    context['today']= date.today()
    context['module']= module
    return render(request,'rate/rate_details.html',context)

@login_required(login_url='home:handle_login')
def rate_old_details(request,module):
    context ={}
    check_permissions(request,module)
    rates = RateMaster.objects.select_related('carrier','pol','pod','fpd').filter(to_date__lt = date.today()).all()
    context['rates']= rates
    context['today']= date.today()
    context['module']= module
    context['old']= True
    return render(request,'rate/rate_details.html',context)


@login_required(login_url='home:handle_login')
def rate_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(RateMaster, id = id)
    

    
    form = RateMasterForm(instance = obj)
    if request.method == 'POST':
        form = RateMasterForm(request.POST, request.FILES, instance=obj)
    
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        handle_rate_bh(request,form.instance.id)
        
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('operations:rate_details',module=module)
          
    context['form']= form
    context['data']= obj
    context['module']= module
    context['update']= True
    return render(request,'rate/rate_create.html',context)

@login_required(login_url='home:handle_login')
def rate_delete(request,module,id):
    check_permissions(request,module)
    rate_obj = RateMaster.objects.filter(id=int(id)).first()
    rate_obj.delete()
    return redirect('operations:rate_details',module=module)

    
@login_required(login_url='home:handle_login')
def rate_duplicate(request,module,id):
    check_permissions(request,module)
    rate_obj = RateMaster.objects.filter(id=int(id)).first()
    new_rate = RateMaster.objects.create(
        carrier = rate_obj.carrier,
        ac_type = rate_obj.ac_type,
        size = rate_obj.size,
        pol = rate_obj.pol,
        pod = rate_obj.pod,
        fpd = rate_obj.fpd,
        from_date = rate_obj.from_date,
        to_date = rate_obj.to_date,
        ammendment = rate_obj.ammendment,
        basic_charges = rate_obj.basic_charges,
        oth_charges = rate_obj.oth_charges,
        ramp_charges = rate_obj.ramp_charges,
        line_door_charges = rate_obj.line_door_charges,
        trucking_charges = rate_obj.trucking_charges,
        net_charges = rate_obj.net_charges,
    )
    new_rate.save()
    
    for i in rate_obj.rate_details.all():
        new_rate_head = RateMasterDetails.objects.create(
            rate = new_rate,
            billing_head = i.billing_head,
            bh_type = i.bh_type,
            amount = i.amount,
            net_amount = i.net_amount,
        )
        new_rate_head.save()
        
    messages.success(request,f'Rate Duplicate Created {new_rate.id}')
    
    return redirect('operations:rate_update',module=module,id=new_rate.id)

 

# ------------------Manifest----------------

def manifest_to_collect(request,update,instance):
    
    manifest = ManifestChargesToCollect.objects.filter(manifest=instance).all()
    manifest.delete()
    
    total_rows = int(request.POST['total_collect_rows'])
    for i in range(1,total_rows+1):
        is_active = request.POST[f'is_collect_active-{i}']
        if is_active == 'yes':
            billing_head = request.POST[f'collect_billing_head-{i}']
            if billing_head:
                billing_head = BillingHead.objects.filter(id=int(billing_head)).first()
            curr = request.POST[f'collect_currency-{i}']
            if curr:
                curr = currency.objects.filter(id=int(curr)).first()
            qty = request.POST.get(f'collect_qty-{i}',None)
            ex_rate = request.POST.get(f'collect_ex_rate-{i}',None)
            rate = request.POST.get(f'collect_rate-{i}',None)
            total = request.POST.get(f'collect_total-{i}',None)
            if billing_head and curr and qty and ex_rate and rate and total:
                new_collect = ManifestChargesToCollect.objects.create(
                    manifest = instance,
                    billing_head = billing_head,
                    curr = curr,
                    ex_rate = ex_rate,
                    rate = rate,
                    total = total,
                    qty = qty,
                )
                new_collect.save()

def manifest_to_pay(request,update,instance):
    
    manifest = ManifestChargesToPay.objects.filter(manifest=instance).all()
    manifest.delete()
    
    total_rows = int(request.POST['total_pay_rows'])
    for i in range(1,total_rows+1):
        is_active = request.POST[f'is_pay_active-{i}']
        if is_active == 'yes':
            billing_head = request.POST[f'pay_billing_head-{i}']
            if billing_head:
                billing_head = BillingHead.objects.filter(id=int(billing_head)).first()
            curr = request.POST[f'pay_currency-{i}']
            if curr:
                curr = currency.objects.filter(id=int(curr)).first()
            qty = request.POST.get(f'pay_qty-{i}',None)
            ex_rate = request.POST.get(f'pay_ex_rate-{i}',None)
            rate = request.POST.get(f'pay_rate-{i}',None)
            total = request.POST.get(f'pay_total-{i}',None)
            if billing_head and curr and qty and ex_rate and rate and total:
                new_pay = ManifestChargesToPay.objects.create(
                    manifest = instance,
                    billing_head = billing_head,
                    curr = curr,
                    ex_rate = ex_rate,
                    rate = rate,
                    total = total,
                    qty = qty,
                )   
                new_pay.save() 

def manifest_to_our(request,update,instance):
    
    manifest = ManifestOurCharges.objects.filter(manifest=instance).all()
    manifest.delete()
    
    total_rows = int(request.POST['total_our_rows'])
    for i in range(1,total_rows+1):
        is_active = request.POST[f'is_our_active-{i}']
        if is_active == 'yes':
            billing_head = request.POST[f'our_billing_head-{i}']
            if billing_head:
                billing_head = BillingHead.objects.filter(id=int(billing_head)).first()
            curr = request.POST[f'our_currency-{i}']
            if curr:
                curr = currency.objects.filter(id=int(curr)).first()
            qty = request.POST.get(f'our_qty-{i}',None)
            ex_rate = request.POST.get(f'our_ex_rate-{i}',None)
            rate = request.POST.get(f'our_rate-{i}',None)
            total = request.POST.get(f'our_total-{i}',None)
            if billing_head and curr and qty and ex_rate and rate and total:
                new_our = ManifestOurCharges.objects.create(
                    manifest = instance,
                    billing_head = billing_head,
                    curr = curr,
                    ex_rate = ex_rate,
                    rate = rate,
                    total = total,
                    qty = qty,
                )   
                new_our.save() 

def manifest_to_your(request,update,instance):
    
    manifest = ManifestYourCharges.objects.filter(manifest=instance).all()
    manifest.delete()
    
    total_rows = int(request.POST['total_your_rows'])
    for i in range(1,total_rows+1):
        is_active = request.POST[f'is_your_active-{i}']
        if is_active == 'yes':
            billing_head = request.POST[f'your_billing_head-{i}']
            if billing_head:
                billing_head = BillingHead.objects.filter(id=int(billing_head)).first()
            curr = request.POST[f'your_currency-{i}']
            if curr:
                curr = currency.objects.filter(id=int(curr)).first()
            qty = request.POST.get(f'your_qty-{i}',None)
            ex_rate = request.POST.get(f'your_ex_rate-{i}',None)
            rate = request.POST.get(f'your_rate-{i}',None)
            total = request.POST.get(f'your_total-{i}',None)
            if billing_head and curr and qty and ex_rate and rate and total:
                new_your = ManifestYourCharges.objects.create(
                    manifest = instance,
                    billing_head = billing_head,
                    curr = curr,
                    ex_rate = ex_rate,
                    rate = rate,
                    total = total,
                    qty = qty,
                )   
                new_your.save() 

@login_required(login_url='home:handle_login')
def create_manifest(request,module):
    context ={}
    
    check_permissions(request,module)
  
    form = ManifestForm(request.POST or None)
    if form.is_valid():
        form.instance.created_by = request.user
        form.save()
        manifest_to_collect(request,False,form.instance)
        manifest_to_pay(request,False,form.instance)
        manifest_to_our(request,False,form.instance)
        manifest_to_your(request,False,form.instance)
        messages.add_message(request, messages.SUCCESS, f"Success, New Manifest Created.")
        return redirect('dashboard:create_manifest',module=module)
    
    context['form']= form
    context['module']= module
    return render(request,'manifest/manifest_create.html',context)


@login_required(login_url='home:handle_login')
def manifest_details(request,module):
    context ={}
    check_permissions(request,module)
  
    data = Manifest.objects.select_related('customer','job_no','customer_address','manifest_currency').all()
          
    context['data']= data
    context['module']= module
    return render(request,'manifest/manifest_details.html',context)


@login_required(login_url='home:handle_login')
def manifest_update(request,module,id):
    context ={}
    check_permissions(request,module)
  
    obj = get_object_or_404(Manifest, id = id)
    
    form = ManifestForm(request.POST or None, instance = obj)
    created_by = obj.created_by
    if form.is_valid():
        form.instance.created_by = created_by
        form.instance.updated_by = request.user

        form.save()
        manifest_to_collect(request,True,form.instance)
        manifest_to_pay(request,True,form.instance)
        manifest_to_our(request,True,form.instance)
        manifest_to_your(request,True,form.instance)
        messages.add_message(request, messages.SUCCESS, f"Success, Updated Successfully.")
        return redirect('dashboard:manifest_details',module=module)
          
    context['form']= form
    context['module']= module
    context['update']= True
    context['data']= obj
    return render(request,'manifest/manifest_create.html',context)

@login_required(login_url='home:handle_login')
def manifest_delete(request,module,id):
    check_permissions(request,module)
    manifest = Manifest.objects.filter(id=int(id)).first()
    manifest.delete()
    return redirect('dashboard:manifest_details',module=module)


def manifest_pdf(request,id):
    manifest = Manifest.objects.filter(id=int(id)).first()
    total_collect = 0
    total_pay = 0
    total_our_charges = 0
    total_your_charges = 0
   
    for i in manifest.manifest_charges_collect.all():
        total_collect += float(i.total)
   
    for i in manifest.manifest_charges_pay.all():
        total_pay += float(i.total)
   
    for i in manifest.manifest_our_charges.all():
        total_our_charges += float(i.total)
   
    for i in manifest.manifest_your_charges.all():
        total_your_charges += float(i.total)
    total_amount = round(total_collect - total_pay - total_your_charges)
    amount_in_words = num2words.num2words(abs(total_amount), lang='en_IN')
    context = {
        'data':manifest,
        'total_collect':total_collect,
        'total_pay':total_pay,
        'total_our_charges':total_our_charges,
        'total_your_charges':total_your_charges,
        'total_amount':total_amount,
        'amount_in_words':amount_in_words.upper(),
    }
    return render(request,'manifest/pdf.html',context)
    
