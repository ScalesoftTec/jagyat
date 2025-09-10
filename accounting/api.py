from accounting.models import IrisInvoiceSetting,InvoiceReceivable,CreditNote
import requests
from datetime import datetime,timedelta,date
from django.db.models import Q
import json
import pytz
from dashboard.models import Logistic

def login_and_get_token(request):
    instance = IrisInvoiceSetting.objects.first()
    if not instance:
        return
    
    if not instance.login_url or not instance.email or not instance.password:
        return
    
    email = instance.email
    password = instance.password
    
    api_body = {
	"email":email,
	"password":password
    }
    flag = 0
    if instance.token_date:
        later_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        first_time = instance.token_date
        difference = later_time - first_time
        seconds_in_day = 24 * 60 * 60
        (min,sec) = divmod(difference.days * seconds_in_day + difference.seconds, 60)
        hours_difference = round(min / 60,2)
        if hours_difference > 7:
            flag = 1
    else:
        flag = 1
        
    if flag == 1:
        res = requests.post(instance.login_url,json=api_body)
        data = dict(json.loads((res.text)))
        if res.status_code == 200 and data['status'] == "SUCCESS":
            if data['response']['token']:
                instance.token = data['response']['token']
                instance.token_date = datetime.now()
                instance.company_id = data['response']["companyid"]
                instance.username = data['response']["username"]
                instance.password_expiry_date = data['response']["passWordExpiredDate"]
                instance.save()
    

def add_invoice_recievable_irn(request,id):
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    if not invoice:
        return "NO INVOICE FOUND"
    
    if not invoice.company_type or not invoice.company_type.gstin_no:
        return "NO COMPANY DETAIL FOUND IN INVOICE"
    
    if not invoice.type_of_invoice:
        return "TYPE OF INVOICE IS NOT SELECTED"
    
    if not invoice.bill_to_address.corp_state:
        return "NO BILL TO STATE FOUND"
    INTER = "INTER"
    INTRA = "INTRA"
    intra_or_inter = INTER
    if invoice.company_type.company_gst_code == invoice.bill_to_address.corp_state.gst_code:
        intra_or_inter = INTRA
        
    if invoice.category == "SEWOP" or invoice.category == "SEWP":
        intra_or_inter = INTER
        
    ri_or_bs = invoice.type_of_invoice
    if ri_or_bs == "TAX INVOICE":
        ri_or_bs = "RI"
    elif ri_or_bs == "BILL OF SUPPLY":
        ri_or_bs = "BS"
    else:
        ri_or_bs = "RI"
        
    
    if not invoice.company_type.legal_name:
        return "COMPANY LEGAL NAME NOT FOUND"
    
    if len(invoice.recievable_invoice_reference.all()) <= 0:
        return "NO ITEMS FOUND IN INVOICE"
    
    if not invoice.company_type.address_line_1:
        return "NO PRIMARY ADDRESS FOUND FOR COMPANY"
    
    if not invoice.bill_to_address.corp_gstin:
      
        return "NO GSTIN FOUND FOR BILL TO PARTY"
    
    if not  invoice.bill_to.party_name:
        return "NO BILL TO PARTY NAME FOUND"
    
    if not invoice.bill_to_address.corp_address_line1:
        return "NO BILL TO PRIMARY ADDRESS FOUND"
    
    if not invoice.bill_to_address.corp_state.name:
        return "NO BILL TO STATE FOUND"
    
    if not invoice.bill_to_address.corp_state.gst_code:
        return "NO BILL TO STATE GST CODE FOUND"
    
    total_taxable_amount = 0
    
    igst_amount = 0
    cgst_amount = 0
    sgst_amount = 0
    item_list = []
    rndOffAmt = 0
    index = 0
    for  i in invoice.recievable_invoice_reference.all():
        if i.total < 0:
            rndOffAmt = i.total
            continue
        
        try:
            if i.billing_head.billing_head == "ROUND OFF":
                rndOffAmt = i.total
                continue
        except:
            pass
        
        index += 1
        
        if intra_or_inter == INTER:
            igst_amount += i.gst_amount
            
        elif intra_or_inter == INTRA:
            cgst_amount += (i.gst_amount / 2)
            sgst_amount += (i.gst_amount / 2)
            
        item_tax_value = 0
        
        
        total_taxable_amount += i.amount
        item_tax_value += i.amount
        
        igst_rate = 0
        cgst_rate = 0
        sgst_rate = 0
        iamt = 0
        camt = 0
        samt = 0
        
        if intra_or_inter == INTER:
            igst_rate = i.gst
            iamt = i.gst_amount
        elif intra_or_inter == INTRA:
            cgst_rate = i.gst / 2
            sgst_rate = i.gst / 2
            camt = round((i.gst_amount / 2),2)
            samt = round((i.gst_amount / 2),2)

        isService = "Y"
        if not i.billing_head.is_service:
            isService = "N"
    
        item_details = {
                'num':index,
                'hsnCd':i.billing_head.hsn_code,
                'qty':i.qty_unit,
                'unitPrice':i.rate,
                'sval':i.amount,
                'txval':item_tax_value,
                'rt':i.gst,
                'irt':igst_rate,
                'iamt':iamt,
                'crt':cgst_rate,
                'camt':camt,
                'srt':sgst_rate,
                'samt':samt,
                'itmVal':i.total,
                'txp':i.tax_applicable,
                'isServc':isService,
                'PrdDesc':f"{i.billing_head.billing_head}",
                
            }
        item_list.append(item_details)
        
    reverse_charge = "N"
    if invoice.type_of_invoice == "RCM":
        reverse_charge = "Y"
    else:
        reverse_charge = "N"
        
    total_taxable_amount = round(total_taxable_amount,2)
    igst_amount = round(igst_amount,2)
    cgst_amount = round(cgst_amount,2)
    sgst_amount = round(sgst_amount,2)
   
   
    current_financial_date = invoice.company_type.financial_from
    
    prefix = invoice.company_type.pre_recievable_invoice
   
    current_length  = InvoiceReceivable.objects.filter(is_einvoiced=True).filter(old_invoice=False).filter(company_type__company_gst_code=invoice.company_type.company_gst_code).filter(date_of_invoice__gte = current_financial_date).count()
    if current_length == 0:
        current_length = 1
    
    duplicate = True
    while duplicate:
        company_invoice_no = prefix + str(current_length).zfill(4)
        
        already_invoice_no = InvoiceReceivable.objects.filter(final_invoice_no = company_invoice_no).first()
    
        if not already_invoice_no:
            duplicate = False
            
        else:
            current_length += 1

    invoice_no = prefix + str(current_length).zfill(4)
        
    
    
    
    if invoice.category == "B2CS" or invoice.category == "B2CL":
        bgstin = "URP"
    else:
        bgstin = invoice.bill_to_address.corp_gstin
    
    bgstin = bgstin.strip()
    userGSTIN = invoice.company_type.gstin_no
    sloc = invoice.company_type.branch_name
    sdst = invoice.company_type.branch_name
    sstcd = invoice.company_type.company_gst_code
    spin = invoice.company_type.pin_code
    sbnm = invoice.company_type.address_line_1

    bstcd = invoice.bill_to_address.corp_state.gst_code
    
    if invoice.category.startswith("EX"):
        bstcd = "96"
        
    # if invoice.final_invoice_no:
    #     invoice_no = invoice.final_invoice_no
    
    
    # if invoice.einvoice_date:
    #     invoice_date = invoice.einvoice_date.date().strftime('%d-%m-%Y')
    
    # return invoice_no
    invoice_date = invoice.date_of_invoice.strftime('%d-%m-%Y')
    invoice_no = invoice.invoice_no
    api_body = {
        "userGstin": userGSTIN,
        "supplyType": "O",
        "ntr": intra_or_inter,
        "docType":ri_or_bs,
        "catg":invoice.category,
        "dst":"O",
        "trnTyp": "REG",
        "no": invoice_no,
        "dt": invoice_date,
        "rchrg":reverse_charge,
        "pos": bstcd,
        "sgstin": userGSTIN,
        "slglNm": invoice.company_type.legal_name,
        "sbnm": sbnm,
        "sloc": sloc,
        "sdst": sdst,
        "sstcd": sstcd,
        "spin": spin,
        "bgstin": bgstin,
        "blglNm": invoice.bill_to.party_name,
        "bbnm": invoice.bill_to_address.corp_address_line1,
        "bloc": invoice.bill_to_address.corp_state.name,
        "bdst": invoice.bill_to_address.corp_city,
        "bstcd": bstcd,
        "bpin": str(invoice.bill_to_address.corp_zip).strip(),
        "totdisc": 0,
        "tottxval": total_taxable_amount,
        "totiamt": igst_amount,
        "totcamt": cgst_amount,
        "totsamt": sgst_amount,
        "rndOffAmt": rndOffAmt,
        "totinvval": invoice.net_amount,
        "taxSch": 'GST',
        "genIrn": True,
        "itemList": item_list
    }
    
    
    invoice.json_data = str(api_body)
    invoice.save()
   
    instance = IrisInvoiceSetting.objects.first()
    if not instance:
        return "E-INVOICE SETTING NOT FOUND"
    
    if not instance.add_inv_url or not instance.token:
        return "E-INVOICE API URL NOT FOUND"
    
    api = instance.add_inv_url
    headers = {
        "X-Auth-Token":instance.token,
        "companyId":instance.company_id,
        "product":"ONYX"
    }
    if not ri_or_bs == 'BS':
        res = requests.post(api,json=api_body,headers=headers)
        res = json.loads(res.text)
        
        status = res['status']
        try:
            response = res['response']
            
            if status == "SUCCESS":
                if response['qrCode']:
                    invoice.qr_code = response['qrCode']
                    
                if not invoice.category == "B2CS" and not invoice.category == "B2CL":
                
                    if response['ackDt'] and not invoice.category == "B2CS" and not invoice.category == "B2CL":
                        invoice.einvoice_date = invoice.date_of_invoice
                    if response['signedQrCode'] and not invoice.category == "B2CS" and not invoice.category == "B2CL":
                        invoice.signed_qr_code = response['signedQrCode']
                    if response['irn'] and not invoice.category == "B2CS" and not invoice.category == "B2CL":
                        invoice.irn_no = response['irn']
                else:
                    invoice.einvoice_date = invoice.date_of_invoice
                        

                if response['ackNo']:
                    invoice.ack_no = response['ackNo']
                if response['id']:
                    invoice.einvoice_id = response['id']
                invoice.is_einvoiced = True
                invoice.final_invoice_no = invoice_no
                invoice.save()
                return f"SUCCESS - E-Invoice Created for {invoice.invoice_no}"
            else:
                return "FAIL"
        except:
            
            return f"FAIL {res}"
        
    if ri_or_bs == 'BS':
        invoice.is_einvoiced = True
        invoice.einvoice_date = invoice.date_of_invoice
   
        invoice.final_invoice_no = invoice_no
        invoice.save()
        return f"SUCCESS - BOS Move To E-Invoice for {invoice.invoice_no}"
    
   


def add_credit_note_irn(request,id):
    invoice = CreditNote.objects.filter(id=id).first()
    if not invoice:
        return "NO Credit Note FOUND"
    
    if not invoice.company_type or not invoice.company_type.gstin_no:
        return "NO COMPANY DETAIL FOUND IN CREDIT NOTE"
    
  
    
    if not invoice.bill_to_address.corp_state:
        return "NO BILL TO STATE FOUND"
    
    INTER = "INTER"
    INTRA = "INTRA"
    intra_or_inter = INTER
    if invoice.company_type.company_gst_code == invoice.bill_to_address.corp_state.gst_code:
        intra_or_inter = INTRA
        
    
    if not invoice.company_type.legal_name:
        return "COMPANY LEGAL NAME NOT FOUND"
    
    if len(invoice.credit_note_reference.all()) <= 0:
        return "NO ITEMS FOUND IN INVOICE"
    
    if not invoice.company_type.address_line_1:
        return "NO PRIMARY ADDRESS FOUND FOR COMPANY"
    
    if not invoice.bill_to_address.corp_gstin:
      
        return "NO GSTIN FOUND FOR BILL TO PARTY"
    
    if not  invoice.bill_to.party_name:
        return "NO BILL TO PARTY NAME FOUND"
    
    if not invoice.bill_to_address.corp_address_line1:
        return "NO BILL TO PRIMARY ADDRESS FOUND"
    
    if not invoice.bill_to_address.corp_state.name:
        return "NO BILL TO STATE FOUND"
    
    if not invoice.bill_to_address.corp_state.gst_code:
        return "NO BILL TO STATE GST CODE FOUND"
    
    total_taxable_amount = 0

    igst_amount = 0
    cgst_amount = 0
    sgst_amount = 0
    item_list = []
    
    for index, i in enumerate(invoice.credit_note_reference.all()):
        if intra_or_inter == INTER:
            igst_amount += i.gst_amount
            
        elif intra_or_inter == INTRA:
            cgst_amount += (i.gst_amount / 2)
            sgst_amount += (i.gst_amount / 2)
            
        item_tax_value = 0
       
        
        total_taxable_amount += i.amount
        item_tax_value += i.amount
        
        igst_rate = 0
        cgst_rate = 0
        sgst_rate = 0
        iamt = 0
        camt = 0
        samt = 0

        isService = "Y"
        if not i.billing_head.is_service:
            isService = "N"
        
        if intra_or_inter == INTER:
            igst_rate = i.gst
            iamt = i.gst_amount
        elif intra_or_inter == INTRA:
            cgst_rate = i.gst / 2
            sgst_rate = i.gst / 2
            camt = round((i.gst_amount / 2),2)
            samt = round((i.gst_amount / 2),2)
    
        item_details = {
                'num':index + 1,
                'hsnCd':i.billing_head.hsn_code,
                'qty':i.qty_unit,
                'unitPrice':i.rate,
                'sval':i.amount,
                'txval':item_tax_value,
                'rt':i.gst,
                'irt':igst_rate,
                'iamt':iamt,
                'crt':cgst_rate,
                'camt':camt,
                'srt':sgst_rate,
                'samt':samt,
                'itmVal':i.total,
                'txp':i.tax_applicable,
                'isServc':isService,
                'PrdDesc':f"{i.billing_head.billing_head}",
            }
        item_list.append(item_details)
        
    reverse_charge = "N"
    if invoice.is_rcm:
        reverse_charge = "Y"
    else:
        reverse_charge = "N"
        
    total_taxable_amount = round(total_taxable_amount,2)
    igst_amount = round(igst_amount,2)
    cgst_amount = round(cgst_amount,2)
    sgst_amount = round(sgst_amount,2)
    
  
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month < 4:
        current_year -= 1
   
    current_financial_date = date(current_year, 4, 1)
    last_financial_date = date(current_year, 4, 1)
    
    

    
    current_length  = CreditNote.objects.filter(is_einvoiced=True).filter(company_type__company_gst_code=invoice.company_type.company_gst_code).filter(einvoice_date__gte = current_financial_date).filter(is_deleted=False).count()
    
    # if invoice.date_of_note < current_financial_date:
    #     current_length  = CreditNote.objects.exclude(is_rcm=True).filter(Q(is_einvoiced=True)|Q(is_cancel=True)).filter(company_type__company_gst_code=invoice.company_type.company_gst_code).filter(date_of_note__gte = last_financial_date).filter(date_of_note__lt = current_financial_date).filter(is_deleted=False).count() 
        
    current_length += 1
    invoice_no = invoice.company_type.pre_credit_note + str(current_length).zfill(4)
    already_invoice_no = CreditNote.objects.filter(final_invoice_no = invoice_no).first()
    duplicate = False
    if already_invoice_no:
        duplicate = True
    while duplicate:
        company_invoice_no = invoice.company_type.pre_credit_note + str(current_length).zfill(4)
        
        already_invoice_no = CreditNote.objects.filter(final_invoice_no = company_invoice_no).first()
    
        if not already_invoice_no:
            duplicate = False
            
        else:
            current_length += 1
            
    invoice_no = invoice.company_type.pre_credit_note + str(current_length).zfill(4)
        
  
    
    
    if invoice.category == "B2CS" or invoice.category == "B2CL":
        bgstin = "URP"
    else:
        bgstin = invoice.bill_to_address.corp_gstin
    
    if not invoice.invoice_date:
        return "Ref Invoice Date Not Found"
    
    
    bgstin = bgstin.strip()
    format = '%Y-%m-%d'
    
  
    
    ref_date = datetime.strptime(str(invoice.invoice_date),format).date()
    ref_invoice_date = ref_date.strftime('%d-%m-%Y')

    
    userGSTIN = invoice.company_type.gstin_no
    sloc = invoice.company_type.branch_name
    sdst = invoice.company_type.branch_name
    sstcd = invoice.company_type.company_gst_code
    spin = invoice.company_type.pin_code
    sbnm = invoice.company_type.address_line_1
    
    if invoice.category.startswith("EX"):
        bstcd = "96"
    else:
        bstcd =  invoice.bill_to_address.corp_state.gst_code
    
    invoice_date = invoice.date_of_note.strftime('%d-%m-%Y')
    invoice_no = invoice.credit_note_no
    api_body = {
        "userGstin": userGSTIN,
        "supplyType": "O",
        "ntr": intra_or_inter,
        "docType":"C",
        "catg":invoice.category,
        "dst":"O",
        "trnTyp": "REG",
        "no": invoice_no,
        "dt": invoice_date,
        "refinum": invoice.invoice_no,
        "refidt": ref_invoice_date,
        "rchrg":reverse_charge,
        "pos": bstcd,
        "sgstin": userGSTIN,
        "slglNm": invoice.company_type.legal_name,
        "sbnm": sbnm,
        
        "sloc":sloc,
        "sdst": sdst,
        "sstcd": sstcd,
        "spin":spin,
    
        "bgstin": bgstin,
        "blglNm": invoice.bill_to.party_name,
        "bbnm": invoice.bill_to_address.corp_address_line1,
        "bloc": invoice.bill_to_address.corp_state.name,
        "bdst": invoice.bill_to_address.corp_city,
        "bstcd": bstcd,
        "bpin": str(invoice.bill_to_address.corp_zip).strip(),
        "totdisc": 0,
        "tottxval": total_taxable_amount,
        "totiamt": igst_amount,
        "totcamt": cgst_amount,
        "totsamt": sgst_amount,
        "rndOffAmt": 0,
        "totinvval": invoice.net_amount,
        "taxSch": 'GST',
        "genIrn": True,
        "itemList": item_list
    }
   
    
    instance = IrisInvoiceSetting.objects.first()
    if not instance:
        return "E-INVOICE SETTING NOT FOUND"
    
    if not instance.add_inv_url or not instance.token:
        return "E-INVOICE API URL NOT FOUND"
    
    api = instance.add_inv_url
    headers = {
        "X-Auth-Token":instance.token,
        "companyId":instance.company_id,
        "product":"ONYX"
    }
    
    res = requests.post(api,json=api_body,headers=headers)
    res = json.loads(res.text)
    
    status = res['status']
    try:
        response = res['response']
        
        if status == "SUCCESS":
            if response['qrCode']:
                invoice.qr_code = response['qrCode']
                
            if not invoice.category == "B2CS" and not invoice.category == "B2CL":
            
                if response['ackDt'] and not invoice.category == "B2CS" and not invoice.category == "B2CL":
                    invoice.einvoice_date = invoice.date_of_note
                if response['signedQrCode'] and not invoice.category == "B2CS" and not invoice.category == "B2CL":
                    invoice.signed_qr_code = response['signedQrCode']
                if response['irn'] and not invoice.category == "B2CS" and not invoice.category == "B2CL":
                    invoice.irn_no = response['irn']
            else:
                invoice.einvoice_date = invoice.date_of_note
                    
            if response['ackNo']:
                invoice.ack_no = response['ackNo']
            if response['id']:
                invoice.einvoice_id = response['id']
            invoice.is_einvoiced = True
            invoice.final_invoice_no = invoice_no
            invoice.save()
            return f"SUCCESS - E-Invoice Created for {invoice.credit_note_no}"
        else:
            return "FAIL"
    except:
        
        return f"FAIL {res}"
        
    
    
    
    

def cancel_invoice_irn(request,id):
    invoice = InvoiceReceivable.objects.filter(id=id).first()
    if not invoice:
        return "NO INVOICE FOUND"
    
    irn = invoice.irn_no
    userGstin = invoice.company_type.gstin_no
    
    api_body = {
    "irn":irn,
	"cnlRsn":"1",
	"cnlRem":"Wrong entry",
	"userGstin":userGstin
    }
    instance = IrisInvoiceSetting.objects.first()
    if not instance:
        return "E-INVOICE SETTING NOT FOUND"
    
    if not instance.cancel_irn_url or not instance.token:
        return "CANCEL IRN URL NOT FOUND"
    api = instance.cancel_irn_url
    headers = {
        "X-Auth-Token":instance.token,
        "companyId":instance.company_id,
        "product":"ONYX"
    }
    
    res = requests.post(api,json=api_body,headers=headers)
    res = json.loads(res.text)
        
    status = res['status']
    try:
        response = res['response']
        
        if status == "SUCCESS":
            invoice.is_einvoiced = True
            invoice.is_deleted = True
            invoice.deleted_by = request.user
            invoice.is_cancel = True
            invoice.save()
            return res['message']
            
   
        if status == "FAILURE":
            message = ""
            for i in res['errors']:
                message += f"{i['msg']} ,"
            return message
            
       
    except:
        message = ""
        for i in res['errors']:
            message += f"{i['msg']} ,"
        return message
