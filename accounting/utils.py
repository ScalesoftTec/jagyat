
from django.http import HttpResponse
from django.template.loader import get_template
import os
from django.conf import settings
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from accounting.models import InvoiceReceivable, CreditNote, RecieptVoucher, PaymentVoucher, ContraVoucher
from masters.models import JobMaster, MBLMaster
from datetime import datetime, date
from dashboard.models import SequenceSettings

def link_callback(uri, rel):
 
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL       
        sRoot = settings.STATIC_ROOT    
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT 

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
            
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path



def generate_pdf(request,template_path,data):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(data)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def send_generate_pdf(request,template_path,data):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(data)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response.getvalue()



def count_sales_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(voucher_type='Proforma Sales').filter(company_type=self.company_type).filter(from_date__lte=self.date_of_invoice).filter(to_date__gte=self.date_of_invoice).first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = InvoiceReceivable.objects.filter(date_of_invoice__gte = from_date).filter(date_of_invoice__lte=to_date).count()
    else:
        current_length = InvoiceReceivable.objects.filter(date_of_invoice__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = InvoiceReceivable.objects.filter(invoice_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.invoice_no = voucher_no
    self.save()

def count_tax_sales_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(voucher_type='Tax Sales').filter(company_type=self.company_type).filter(from_date__lte=self.date_of_invoice).filter(to_date__gte=self.date_of_invoice).first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = InvoiceReceivable.objects.filter(is_einvoiced=True).filter(date_of_invoice__gte = from_date).filter(date_of_invoice__lte=to_date).count()
    else:
        current_length = InvoiceReceivable.objects.filter(is_einvoiced=True).filter(date_of_invoice__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = InvoiceReceivable.objects.filter(is_einvoiced=True).filter(final_invoice_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.final_invoice_no = voucher_no
    self.save()

def count_crn_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(voucher_type='Proforma Credit Note').filter(company_type=self.company_type).filter(from_date__lte=self.date_of_note).filter(to_date__gte=self.date_of_note).first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = CreditNote.objects.filter(date_of_note__gte = from_date).filter(date_of_note__lte=to_date).count()
    else:
        current_length = CreditNote.objects.filter(date_of_note__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = CreditNote.objects.filter(credit_note_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.credit_note_no = voucher_no
    self.save()

def count_tax_crn_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(voucher_type='Taxx Credit Note').filter(company_type=self.company_type).filter(from_date__lte=self.date_of_note).filter(to_date__gte=self.date_of_note).first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = CreditNote.objects.filter(is_einvoiced=True).filter(date_of_note__gte = from_date).filter(date_of_note__lte=to_date).count()
    else:
        current_length = CreditNote.objects.filter(is_einvoiced=True).filter(date_of_note__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = CreditNote.objects.filter(is_einvoiced=True).filter(final_invoice_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.final_invoice_no = voucher_no
    self.save()

def count_receipts_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(voucher_type='Receipt').filter(company_type=self.company_type).filter(from_date__lte=self.voucher_date).filter(to_date__gte=self.voucher_date).first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = RecieptVoucher.objects.filter(voucher_date__gte = from_date).filter(voucher_date__lte=to_date).count()
    else:
        current_length = RecieptVoucher.objects.filter(voucher_date__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True

    
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = RecieptVoucher.objects.filter(voucher_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.voucher_no =  voucher_no
    self.save()

def count_payment_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(voucher_type='Payment').filter(company_type=self.company_type).filter(from_date__lte=self.voucher_date).filter(to_date__gte=self.voucher_date).first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = PaymentVoucher.objects.filter(voucher_date__gte = from_date).filter(voucher_date__lte=to_date).count()
    else:
        current_length = PaymentVoucher.objects.filter(voucher_date__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True

    
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = PaymentVoucher.objects.filter(voucher_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.voucher_no =  voucher_no
    self.save()

def count_contra_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(voucher_type='Contra').filter(company_type=self.company_type).filter(from_date__lte=self.voucher_date).filter(to_date__gte=self.voucher_date).first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = ContraVoucher.objects.filter(voucher_date__gte = from_date).filter(voucher_date__lte=to_date).count()
    else:
        current_length = ContraVoucher.objects.filter(voucher_date__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True

    
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = ContraVoucher.objects.filter(voucher_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.voucher_no =  voucher_no
    self.save()

def count_job_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(company_type=self.company_type).filter(from_date__lte=self.job_date).filter(to_date__gte=self.job_date)

    if instance.company_type.separate_job_count_mode_wise:
        if instance.module.startswith('Sea'):
            voucher_setting = voucher_setting.filter(voucher_type='Sea Job').first()
        if instance.module.startswith('Air'):
            voucher_setting = voucher_setting.filter(voucher_type='Air Job').first()
        if instance.module.startswith('Transport'):
            voucher_setting = voucher_setting.filter(voucher_type='Transport Job').first()

    elif instance.company_type.separate_job_count_module_wise:
        if instance.module == 'Sea Export':
            voucher_setting = voucher_setting.filter(voucher_type='Sea Export Job').first()
       
        if instance.module == 'Sea Import':
            voucher_setting = voucher_setting.filter(voucher_type='Sea Import Job').first()
       
        if instance.module == 'Air Export':
            voucher_setting = voucher_setting.filter(voucher_type='Air Export Job').first()
       
        if instance.module == 'Air Import':
            voucher_setting = voucher_setting.filter(voucher_type='Air Import Job').first()
        
        if instance.module == 'Transport':
            voucher_setting = voucher_setting.filter(voucher_type='Transport Job').first()

    else:
        voucher_setting = voucher_setting.filter(voucher_type='Job').first()

       



    prefix = ''
    suffix = ''
    no_of_zero = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date

    if voucher_setting:
        current_length = JobMaster.objects.filter(job_date__gte = from_date).filter(job_date__lte=to_date).count()
    else:
        current_length = JobMaster.objects.filter(job_date__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    is_duplicate = True

    
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = JobMaster.objects.filter(job_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.job_no = voucher_no
    self.save()

def count_mbl_no(instance):
    self = instance
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
    current_financial_date = date(current_year, 4, 1)
    
    voucher_setting = SequenceSettings.objects.filter(company_type=self.company_type).filter(from_date__lte=self.created_at.date()).filter(to_date__gte=self.created_at.date())

    if instance.job_no.module.startswith('Sea'):
        voucher_setting = voucher_setting.filter(voucher_type='Sea MBL').first()
    if instance.job_no.module.startswith('Air'):
        voucher_setting = voucher_setting.filter(voucher_type='Air MBL').first()

    prefix = ''
    suffix = ''
    no_of_zero = 0
    skip_count = 0
    from_date = current_financial_date
    to_date = current_financial_date
    if voucher_setting:
        prefix = voucher_setting.prefix or ''
        suffix = voucher_setting.suffix or ''
        no_of_zero = voucher_setting.zero_length or 0
        from_date = voucher_setting.from_date
        to_date = voucher_setting.to_date
        skip_count = voucher_setting.skip_count or 0

    
    current_length = MBLMaster.objects.filter(is_duplicate=False).count() + skip_count
    
    if current_length == 0:
        current_length = 1

    is_duplicate = True

    
    while is_duplicate:
        voucher_no = prefix + str(current_length).zfill(no_of_zero) + suffix
            
        voucher = MBLMaster.objects.filter(mbl_no=voucher_no).count()
        if voucher == 0:
            is_duplicate = False
        else:
            current_length += 1
            
    self.mbl_no = voucher_no
    self.save()

