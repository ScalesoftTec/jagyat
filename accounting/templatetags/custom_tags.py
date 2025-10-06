from datetime import datetime,date,timedelta
from django import template
import base64
import requests
import num2words
from accounting.models import ManifestChargesToPay,ManifestChargesToCollect,RecieptVoucherDetails,InvoiceReceivable,InvoicePayable,IndirectExpense
from masters.models import JobContainer,JobMaster
from itertools import zip_longest
from django.db.models import Sum


register = template.Library()

@register.filter
def absolute(value):
    try:
        return abs(value)
    except:
        return value
    
@register.filter
def zip_my_list(value=[],args=[]):    
    try:
        if not value:
            value = []
        if not args:
            args = [] 
    except:
        value = []
        args = []
    return zip_longest(value,args)


@register.filter
def days_until(date):
    delta = date - date.today()
    return delta.days

@register.filter
def num_to_text(number):
    amount_in_words = num2words.num2words(number, lang='en_IN')
    amount_in_words = amount_in_words.replace(',','')
    amount_in_words = amount_in_words.replace('-',' ')
    return amount_in_words.upper()

@register.filter
def get_first_word(text : str):
    text = text.split(" ")
    return text[0]


@register.filter
def manifest_payable(id : int):
    payable_sum = 0
    payables = ManifestChargesToPay.objects.select_related('manifest','manifest__job_no').filter(manifest__job_no__id = id).values('total').aggregate(Sum('total'))
    
    if payables['total__sum']:
        payable_sum = payables['total__sum']
    
    return payable_sum

@register.filter
def manifest_collect(id : int):
    collect_sum = 0
    collects = ManifestChargesToCollect.objects.select_related('manifest','manifest__job_no').filter(manifest__job_no__id = id).values('total').aggregate(Sum('total'))
    if collects['total__sum']:
        collect_sum = collects['total__sum']

    return collect_sum

@register.filter
def check_container_return(id : int):
    job_container = JobContainer.objects.filter(job__id = id).values('delivery_date').all()
    flag = False
    for i in job_container:
        if not i['delivery_date']:
            flag = True
            break
    return flag

@register.filter
def get_all_reciepts(id : int):
    reciepts = RecieptVoucherDetails.objects.filter(invoice__id = id).all()

    return list(reciepts)


def funGetInrSales(id):
    job = JobMaster.objects.filter(id = id).first()
    sum = 0
    for i in job.recievable_invoice_job.all():
        if i.invoice_currency:
            if i.invoice_currency.short_name == "INR" or not i.invoice_currency:
                sum += round((float(i.gross_amount)),2)
        else:
            sum += round((float(i.gross_amount)),2)
            
    return round(sum,2)

def funGetNonInrSales(id):
    job = JobMaster.objects.filter(id = id).first()
    sum = 0
    for i in job.recievable_invoice_job.all():
        if i.invoice_currency:
            if not i.invoice_currency.short_name == "INR":
                sum += round((float(i.gross_amount * i.currency_ex_rate)),2)
    return round(sum,2)

@register.filter
def get_inr_sales(id : int):
    return funGetInrSales(id)



@register.filter
def get_non_inr_sales(id : int):
    
    return funGetNonInrSales(id)

@register.filter
def get_total_sales(id : int):
    inr_sales = funGetInrSales(id)
    non_inr_sales = funGetNonInrSales(id)
    return inr_sales + non_inr_sales

def funGetInrPurchase(id):
    job = JobMaster.objects.filter(id = id).first()
    sum = 0
    for i in job.payable_invoice_job.all():
        if i.invoice_currency:
            if i.invoice_currency.short_name == "INR":
                sum += round((float(i.gross_amount)),2)
        else:
            sum += round((float(i.gross_amount)),2)
            
    return round(sum,2)

def funGetNonInrPurchase(id):
    job = JobMaster.objects.filter(id = id).first()
    sum = 0
    for i in job.payable_invoice_job.all():
        if i.invoice_currency:
            if not i.invoice_currency.short_name == "INR":
                sum += round((float(i.gross_amount * i.currency_ex_rate)),2)
    return round(sum,2)


def funGetIndirectPurchase(id):
    job = JobMaster.objects.filter(id = id).first()
    sum = 0
    for i in job.indirect_exp_job.all():
        sum += round((float(i.gross_amount)),2)
       
    return round(sum,2)


def funGetTrailorPurchase(id):
    job = JobMaster.objects.filter(id = id).first()
    sum = 0
    for i in job.trailor_exp_job.all():
        sum += round((float(i.net_amount)),2)
       
    return round(sum,2)

@register.filter
def get_inr_purchase(id : int):
    return funGetInrPurchase(id)


@register.filter
def get_non_inr_purchase(id : int):
    return funGetNonInrPurchase(id)

@register.filter
def get_indirect_exp_sum(id : int):
    return funGetIndirectPurchase(id)

@register.filter
def get_trailor_exp_sum(id : int):
    return funGetTrailorPurchase(id)

@register.filter
def get_total_purchase(id : int):
    inr_purchase = funGetInrPurchase(id)
    non_inr_purchase = funGetNonInrPurchase(id)
    indirect_purchase = funGetIndirectPurchase(id)
    trailor_purchase = funGetTrailorPurchase(id)
    return inr_purchase + non_inr_purchase + indirect_purchase + trailor_purchase

@register.filter
def get_profit_loss(id : int):
    inr_sales = funGetInrSales(id)
    non_inr_sales = funGetNonInrSales(id)
    inr_purchase = funGetInrPurchase(id)
    non_inr_purchase = funGetNonInrPurchase(id)
    indirect_purchase = funGetIndirectPurchase(id)
    trailor_purchase = funGetTrailorPurchase(id)
    
    profit_loss = (inr_sales + non_inr_sales) - (inr_purchase + non_inr_purchase + trailor_purchase + indirect_purchase)
    
    return profit_loss

@register.filter
def get_profit_loss_percent(id : int):
    inr_sales = funGetInrSales(id)
    non_inr_sales = funGetNonInrSales(id)
    inr_purchase = funGetInrPurchase(id)
    non_inr_purchase = funGetNonInrPurchase(id)
    indirect_purchase = funGetIndirectPurchase(id)
    trailor_purchase = funGetTrailorPurchase(id)
    
    profit_loss = (inr_sales + non_inr_sales) - (inr_purchase + non_inr_purchase + trailor_purchase + indirect_purchase)

    try:
        percent_profilt_loss = (profit_loss / (inr_sales + non_inr_sales)) * 100
    except:
        percent_profilt_loss = 0
    
    return round(percent_profilt_loss,2)

def get_non_tax_amount_in_invoice_payable(id):
    invoice = InvoicePayable.objects.filter(id=id).first()
    total_gst_amount = 0
    for i in invoice.payable_invoice_reference.all():
        if i.gst_amount <= 0:
            total_gst_amount += i.total
    return round(total_gst_amount,2)

def get_non_tax_amount_in_expense(id):
    invoice = IndirectExpense.objects.filter(id=id).first()
    total_gst_amount = 0
    for i in invoice.indirect_expense_reference.all():
        if i.gst_amount > 0:
            total_gst_amount += i.total
    return round(total_gst_amount,2)

def get_non_tax_amount_in_invoice_recievable(id):
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    total_gst_amount = 0
    for i in invoice.recievable_invoice_reference.all():
        if i.gst_amount > 0:
            total_gst_amount += i.total
    return round(total_gst_amount,2)

@register.filter
def get_non_tax_amount_ri(id : int):
    total_non_gst_amount = get_non_tax_amount_in_invoice_recievable(id)
    return total_non_gst_amount


@register.filter
def get_non_tax_amount_pi(id : int):
    total_non_gst_amount = get_non_tax_amount_in_invoice_payable(id)
    return total_non_gst_amount

@register.filter
def get_non_tax_amount_expense(id : int):
    total_non_gst_amount = get_non_tax_amount_in_expense(id)
    return total_non_gst_amount


def get_per_tax_in_invoice_recievable(id,percent):
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    total_per_amount = 0
    for i in invoice.recievable_invoice_reference.all():
        if int(i.gst) == percent:
            total_per_amount += i.gst_amount
    return round(total_per_amount,2)

def get_per_tax_in_invoice_payable(id,percent):
    invoice = InvoicePayable.objects.filter(id=id).first()
    total_per_amount = 0
    for i in invoice.payable_invoice_reference.all():
        if int(i.gst) == percent:
            total_per_amount += i.gst_amount
    return round(total_per_amount,2)

def get_per_tax_in_expense(id,percent):
    invoice = IndirectExpense.objects.filter(id=id).first()
    total_per_amount = 0
    for i in invoice.indirect_expense_reference.all():
        if int(i.gst) == percent:
            total_per_amount += i.gst_amount
    return round(total_per_amount,2)



@register.filter
def get_5_tax_ri(id : int):
    total_5_gst_amount = get_per_tax_in_invoice_recievable(id,5)
    return total_5_gst_amount

def get_gst_tax_ri(id,percent,mode):
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    total_amount = 0
    if mode == "CS":
        for i in invoice.recievable_invoice_reference.filter(gst=percent).all():
            if invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                total_amount += i.gst_amount
        total_amount = total_amount/2
    if mode == "I":
        for i in invoice.recievable_invoice_reference.filter(gst=percent).all():
            if not invoice.bill_to_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                total_amount += i.gst_amount
                
                
    return round((total_amount),2)

def get_gst_tax_pi(id,percent,mode):
    try:
        invoice = InvoicePayable.objects.filter(id=id).first()
        total_amount = 0
        if mode == "CS":
            for i in invoice.payable_invoice_reference.filter(gst=percent).all():
                if invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                    total_amount += i.gst_amount
            total_amount = total_amount/2
            
        if mode == "I":
            for i in invoice.payable_invoice_reference.filter(gst=percent).all():
                if not invoice.bill_from_address.corp_state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                    total_amount += i.gst_amount
                    
                    
        return round((total_amount),2)
    except:
        return 0

def get_gst_tax_expense(id,percent,mode):
    try:
        invoice = IndirectExpense.objects.filter(id=id).first()
        total_amount = 0
        if mode == "CS":
            for i in invoice.indirect_expense_reference.filter(gst=percent).all():
                if invoice.vendor.state.gst_code == invoice.company_type.company_gst_code and not i.billing_head.always_igst:
                    total_amount += i.gst_amount
            total_amount = total_amount/2
            
        if mode == "I":
            for i in invoice.indirect_expense_reference.filter(gst=percent).all():
                if not invoice.vendor.state.gst_code == invoice.company_type.company_gst_code or i.billing_head.always_igst:
                    total_amount += i.gst_amount
                    
                    
        return round((total_amount),2)
    except:
        return 0

@register.filter
def get_5_csgst_tax_ri(id : int):
    total_amount = get_gst_tax_ri(id,5.0,'CS')
    return total_amount

@register.filter
def get_5_igst_tax_ri(id : int):
    total_amount = get_gst_tax_ri(id,5.0,'I')
    return total_amount

@register.filter
def get_5_csgst_tax_pi(id : int):
    total_amount = get_gst_tax_pi(id,5.0,'CS')
    return total_amount

@register.filter
def get_5_igst_tax_pi(id : int):
    total_amount = get_gst_tax_pi(id,5.0,'I')
    return total_amount

@register.filter
def get_5_csgst_tax_expense(id : int):
    total_amount = get_gst_tax_expense(id,5.0,'CS')
    return total_amount

@register.filter
def get_5_igst_tax_expense(id : int):
    total_amount = get_gst_tax_expense(id,5.0,'I')
    return total_amount

@register.filter
def get_12_csgst_tax_ri(id : int):
    total_amount = get_gst_tax_ri(id,12.0,'CS')
    return total_amount

@register.filter
def get_12_igst_tax_ri(id : int):
    total_amount = get_gst_tax_ri(id,12.0,'I')
    return total_amount

@register.filter
def get_12_csgst_tax_pi(id : int):
    total_amount = get_gst_tax_pi(id,12.0,'CS')
    return total_amount

@register.filter
def get_12_igst_tax_pi(id : int):
    total_amount = get_gst_tax_pi(id,12.0,'I')
    return total_amount

@register.filter
def get_12_csgst_tax_expense(id : int):
    total_amount = get_gst_tax_expense(id,12.0,'CS')
    return total_amount

@register.filter
def get_12_igst_tax_expense(id : int):
    total_amount = get_gst_tax_expense(id,12.0,'I')
    return total_amount

@register.filter
def get_18_csgst_tax_ri(id : int):
    total_amount = get_gst_tax_ri(id,18.0,'CS')
    return total_amount

@register.filter
def get_18_igst_tax_ri(id : int):
    total_amount = get_gst_tax_ri(id,18.0,'I')
    return total_amount

@register.filter
def get_18_csgst_tax_pi(id : int):
    total_amount = get_gst_tax_pi(id,18.0,'CS')
    return total_amount

@register.filter
def get_18_igst_tax_pi(id : int):
    total_amount = get_gst_tax_pi(id,18.0,'I')
    return total_amount

@register.filter
def get_18_csgst_tax_expense(id : int):
    total_amount = get_gst_tax_expense(id,18.0,'CS')
    return total_amount

@register.filter
def get_18_igst_tax_expense(id : int):
    total_amount = get_gst_tax_expense(id,18.0,'I')
    return total_amount

@register.filter
def get_12_tax_ri(id : int):
    total_12_gst_amount = get_per_tax_in_invoice_recievable(id,12)
    return total_12_gst_amount

@register.filter
def get_18_tax_ri(id : int):
    total_18_gst_amount = get_per_tax_in_invoice_recievable(id,18)
    return total_18_gst_amount

@register.filter
def get_5_tax_pi(id : int):
    total_12_gst_amount = get_per_tax_in_invoice_payable(id,5)
    return total_12_gst_amount

@register.filter
def get_12_tax_pi(id : int):
    total_12_gst_amount = get_per_tax_in_invoice_payable(id,12)
    return total_12_gst_amount

@register.filter
def get_18_tax_pi(id : int):
    total_18_gst_amount = get_per_tax_in_invoice_payable(id,18)
    return total_18_gst_amount

@register.filter
def get_5_tax_expense(id : int):
    total_12_gst_amount = get_per_tax_in_expense(id,5)
    return total_12_gst_amount

@register.filter
def get_12_tax_expense(id : int):
    total_12_gst_amount = get_per_tax_in_expense(id,12)
    return total_12_gst_amount

@register.filter
def get_18_tax_expense(id : int):
    total_18_gst_amount = get_per_tax_in_expense(id,18)
    return total_18_gst_amount



@register.filter
def to_base64(url):
    return "data:image/png;base64, " + str(base64.b64encode(requests.get(url).content))

@register.filter
def get_irn_cancel_applicable(einvoice_date):
    current_datetime = datetime.now()
    format = "%Y-%m-%d %H:%M:%S"
    dt = current_datetime - datetime.strptime(str(einvoice_date)[:19],format)    
    return (dt.total_seconds() / 3660) < 12



@register.filter
def calculate_tax_by_bh(id :int):
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    
    total_csgst_5 = 0
    total_csgst_12 = 0
    total_csgst_18 = 0
    total_igst_5 = 0
    total_igst_12 = 0
    total_igst_18 = 0
    user_gst_code = invoice.bill_to_address.corp_state.gst_code
    company_gst_code = invoice.company_type.company_gst_code
    if invoice.type_of_invoice == "RCM":
        company_gst_code = "09"
        
    for head in invoice.recievable_invoice_reference.all():
        if head.gst == 5:
            if user_gst_code == company_gst_code and not head.billing_head.always_igst:
                total_csgst_5 += head.gst_amount / 2
            else:
                total_igst_5 += head.gst_amount
        
        if head.gst == 12:
            if user_gst_code == company_gst_code and not head.billing_head.always_igst:
                total_csgst_12 += head.gst_amount / 2
            else:
                total_igst_12 += head.gst_amount
        
        if head.gst == 18:
            if user_gst_code == company_gst_code and not head.billing_head.always_igst:
                total_csgst_18 += head.gst_amount / 2
            else:
                total_igst_18 += head.gst_amount
                
   
    
    data = [
        {
            'name':"CGST OUTPUT 2.5%",
            "amount":round(total_csgst_5)
        },
        {
            'name':"SGST OUTPUT 2.5%",
            "amount":round(total_csgst_5)
        },
        {
            'name':"IGST OUTPUT 5%",
            "amount":round(total_igst_5)
        },
        {
            'name':"CGST OUTPUT 6%",
            "amount":round(total_csgst_12)
        },
        {
            'name':"SGST OUTPUT 6%",
            "amount":round(total_csgst_12)
        },
        {
            'name':"IGST OUTPUT 12%",
            "amount":round(total_igst_12)
        },
        {
            'name':"CGST OUTPUT 9%",
            "amount":round(total_csgst_18)
        },
        {
            'name':"SGST OUTPUT 9%",
            "amount":round(total_csgst_18)
        },
        {
            'name':"IGST OUTPUT 18%",
            "amount":round(total_igst_18)
        },
    ]
    
    return data
        
        
            