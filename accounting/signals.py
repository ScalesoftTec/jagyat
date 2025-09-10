from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from accounting.models import *
from django.utils.timezone import localtime

@receiver(post_save, sender=InvoiceReceivable) 
def create_sales_invoice_voucher(sender, instance, created, **kwargs):

    vouchers = Voucher.objects.filter(sales_invoice = instance).all()
    vouchers.delete()

    for detail in instance.recievable_invoice_reference.all():
        vouchers = Voucher.objects.filter(sales_invoice_details = detail).all()
        vouchers.delete()

    if instance.is_deleted or not instance.is_einvoiced:
        return

    currency_ex_rate = 1
    try:
        if not instance.invoice_currency.short_name == "INR":
            currency_ex_rate = round(instance.currency_ex_rate,2)
    except:
        pass

    net_amount = 0
  
    einvoice_date = instance.einvoice_date.date() 

    for detail in instance.recievable_invoice_reference.all():
        vouchers = Voucher.objects.filter(sales_invoice_details = detail).all()
        vouchers.delete()

        amount = round(currency_ex_rate*detail.amount,2)
        total = round(currency_ex_rate*detail.total,2)
        gst_amount = round(currency_ex_rate*detail.gst_amount,2)
        gst_ledger_category = detail.gst_ledger_category
        cgst_sgst = False
        gst = detail.gst

        tally_group = detail.cr_ledger_category
        if detail.billing_head and detail.billing_head.tally_group:
            tally_group = detail.billing_head.tally_group

        createVoucher("Sales",amount,category=tally_group,sales_invoice_details=detail,dr_cr="Credit",date=einvoice_date,company_type=instance.company_type)

        try:
            if instance.bill_to_address.corp_state.gst_code == instance.company_type.company_gst_code:
                cgst_sgst = True
                
        except:
            pass
        
        if gst == 5:
            if cgst_sgst:
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='CGST 2.5% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='SGST 2.5% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales",round((gst_amount),2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='IGST 5% IN',date=einvoice_date,company_type=instance.company_type)
                
        if gst == 12:
            if cgst_sgst:
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='CGST 6% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='SGST 6% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales",round((gst_amount),2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='IGST 12% IN',date=einvoice_date,company_type=instance.company_type)
                
        if gst == 18:
            if cgst_sgst:
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='CGST 9% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='SGST 9% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales",round((gst_amount),2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='IGST 18% IN',date=einvoice_date,company_type=instance.company_type)
       
        if gst == 28:
            if cgst_sgst:
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='CGST 14% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales",round((gst_amount)/2,2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='SGST 14% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales",round((gst_amount),2),category=gst_ledger_category,sales_invoice_details=detail,dr_cr="Credit",gst_type='IGST 28% IN',date=einvoice_date,company_type=instance.company_type)
                

        
        net_amount += total
      
    dr_ledger_category = instance.dr_ledger_category
    if instance.bill_to and instance.bill_to.tally_group:
        dr_ledger_category = instance.bill_to.tally_group

    createVoucher("Sales",round(net_amount,2),category=dr_ledger_category,sales_invoice=instance,dr_cr="Debit",party=instance.bill_to,party_address=instance.bill_to_address)

@receiver(post_save, sender=InvoicePayable) 
def create_purchase_invoice_voucher(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(purchase_invoice = instance).all()
    vouchers.delete()

    for detail in instance.payable_invoice_reference.all():
        vouchers = Voucher.objects.filter(purchase_invoice_details = detail).all()
        vouchers.delete()

    if instance.is_deleted:
        return
    
    currency_ex_rate = 1
    try:
        if not instance.invoice_currency.short_name == "INR":
            currency_ex_rate = round(instance.currency_ex_rate,2)
    except:
        pass


    net_amount = 0
  

    for detail in instance.payable_invoice_reference.all():
        vouchers = Voucher.objects.filter(purchase_invoice_details = detail).all()
        vouchers.delete()

        amount = round(currency_ex_rate*detail.amount,2)
        total = round(currency_ex_rate*detail.total,2)
        gst_amount = round(currency_ex_rate*detail.gst_amount,2)
        gst_ledger_category = detail.gst_ledger_category
        cgst_sgst = False
        gst = detail.gst

        tally_group = detail.dr_ledger_category
        if detail.billing_head and detail.billing_head.tally_group:
            tally_group = detail.billing_head.tally_group

        createVoucher("Purchase",amount,category=tally_group,purchase_invoice_details=detail,dr_cr="Debit",date=instance.date_of_invoice,company_type=instance.company_type)

        try:
            if instance.party_type == "Direct":
                if instance.bill_from_address.corp_state.gst_code == instance.company_type.company_gst_code:
                    cgst_sgst = True
            
            else:
                if instance.vendor.state.gst_code == instance.company_type.company_gst_code:
                    cgst_sgst = True
                
        except:
            pass
        
        if gst == 5:
            if cgst_sgst:
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='CGST 2.5% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='SGST 2.5% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
            else:
                createVoucher("Purchase",round((gst_amount),2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='IGST 5% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
                
        if gst == 12:
            if cgst_sgst:
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='CGST 6% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='SGST 6% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
            else:
                createVoucher("Purchase",round((gst_amount),2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='IGST 12% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
                
        if gst == 18:
            if cgst_sgst:
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='CGST 9% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='SGST 9% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
            else:
                createVoucher("Purchase",round((gst_amount),2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='IGST 18% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
       
        if gst == 28:
            if cgst_sgst:
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='CGST 14% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
                createVoucher("Purchase",round((gst_amount)/2,2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='SGST 14% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
            else:
                createVoucher("Purchase",round((gst_amount),2),category=gst_ledger_category,purchase_invoice_details=detail,dr_cr="Debit",gst_type='IGST 28% OUT',date=instance.date_of_invoice,company_type=instance.company_type)
                

        
        net_amount += total
      
    tds_amount = round((instance.tds_payable * currency_ex_rate),2)

    if instance.party_type == "Direct":

        cr_ledger_category = instance.cr_ledger_category
        if instance.bill_from and instance.bill_from.tally_group:
            cr_ledger_category = instance.bill_from.tally_group

        createVoucher("Purchase",round((net_amount - tds_amount),2),category=cr_ledger_category,purchase_invoice=instance,dr_cr="Credit",party=instance.bill_from,party_address=instance.bill_from_address)

        createVoucher("Purchase",round((tds_amount),2),category=instance.tds_ledger_category,purchase_invoice=instance,dr_cr="Credit",party=instance.bill_from,tds_section=instance.tds_section)
    else:

        cr_ledger_category = instance.cr_ledger_category
        if instance.vendor and instance.vendor.tally_group:
            cr_ledger_category = instance.vendor.tally_group


        createVoucher("Purchase",round((net_amount - tds_amount),2),category=cr_ledger_category,purchase_invoice=instance,dr_cr="Credit",vendor=instance.vendor)

        createVoucher("Purchase",round((tds_amount),2),category=instance.tds_ledger_category,purchase_invoice=instance,dr_cr="Credit",vendor=instance.vendor,tds_section=instance.tds_section)

  
@receiver(post_save, sender=CreditNote) 
def create_crn_voucher(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(crn = instance).all()
    vouchers.delete()

    for detail in instance.credit_note_reference.all():
        vouchers = Voucher.objects.filter(crn_details = detail).all()
        vouchers.delete()
    
    if instance.is_deleted or not instance.is_einvoiced:
        return
    
    einvoice_date = instance.einvoice_date.date() 

    currency_ex_rate = 1
    try:
        if not instance.invoice_currency.short_name == "INR":
            currency_ex_rate = round(instance.currency_ex_rate,2)
    except:
        pass

    net_amount = 0

    for detail in instance.credit_note_reference.all():
        vouchers = Voucher.objects.filter(crn_details = detail).all()
        vouchers.delete()

        amount = round(currency_ex_rate*detail.amount,2)
        total = round(currency_ex_rate*detail.total,2)
        gst_amount = round(currency_ex_rate*detail.gst_amount,2)
        gst_ledger_category = detail.gst_ledger_category
        cgst_sgst = False
        gst = detail.gst
        createVoucher("Sales Return",amount,category=detail.dr_ledger_category,crn_details=detail,dr_cr="Debit",date=einvoice_date,company_type=instance.company_type)

        try:
            if instance.bill_from_address.corp_state.gst_code == instance.company_type.company_gst_code:
                cgst_sgst = True
                
        except:
            pass
        
        if gst == 5:
            if cgst_sgst:
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='CGST 2.5% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='SGST 2.5% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales Return",round((gst_amount),2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='IGST 5% IN',date=einvoice_date,company_type=instance.company_type)
                
        if gst == 12:
            if cgst_sgst:
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='CGST 6% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='SGST 6% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales Return",round((gst_amount),2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='IGST 12% IN',date=einvoice_date,company_type=instance.company_type)
                
        if gst == 18:
            if cgst_sgst:
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='CGST 9% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='SGST 9% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales Return",round((gst_amount),2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='IGST 18% IN',date=einvoice_date,company_type=instance.company_type)
       
        if gst == 28:
            if cgst_sgst:
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='CGST 14% IN',date=einvoice_date,company_type=instance.company_type)
                createVoucher("Sales Return",round((gst_amount)/2,2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='SGST 14% IN',date=einvoice_date,company_type=instance.company_type)
            else:
                createVoucher("Sales Return",round((gst_amount),2),category=gst_ledger_category,crn_details=detail,dr_cr="Debit",gst_type='IGST 28% IN',date=einvoice_date,company_type=instance.company_type)
                

        
        net_amount += total
      
    
    cr_ledger_category = instance.cr_ledger_category
    if instance.bill_to and instance.bill_to.tally_group:
        cr_ledger_category = instance.bill_to.tally_group

    createVoucher("Sales Return",net_amount,category=cr_ledger_category,crn=instance,dr_cr="Credit",party=instance.bill_to,party_address=instance.bill_to_address)

   
@receiver(post_save, sender=DebitNote) 
def create_drn_voucher(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(drn = instance).all()
    vouchers.delete()
    
    for detail in instance.debit_note_reference.all():
        vouchers = Voucher.objects.filter(drn_details = detail).all()
        vouchers.delete()

    if instance.is_deleted:
        return

    currency_ex_rate = 1
    try:
        if not instance.invoice_currency.short_name == "INR":
            currency_ex_rate = round(instance.currency_ex_rate,2)
    except:
        pass

    net_amount = 0

    for detail in instance.debit_note_reference.all():
        vouchers = Voucher.objects.filter(drn_details = detail).all()
        vouchers.delete()

        amount = round(currency_ex_rate*detail.amount,2)
        total = round(currency_ex_rate*detail.total,2)
        gst_amount = round(currency_ex_rate*detail.gst_amount,2)
        gst_ledger_category = detail.gst_ledger_category
        cgst_sgst = False
        gst = detail.gst
        createVoucher("Purchase Return",amount,category=detail.cr_ledger_category,drn_details=detail,dr_cr="Credit",date=instance.date_of_note,company_type=instance.company_type)

        try:
            if instance.party_type == "Direct":
                if instance.bill_from_address.corp_state.gst_code == instance.company_type.company_gst_code:
                    cgst_sgst = True
            else:
                if instance.bill_from_vendor.state.gst_code == instance.company_type.company_gst_code:
                    cgst_sgst = True

                
        except:
            pass
        
        if gst == 5:
            if cgst_sgst:
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='CGST 2.5% OUT',date=instance.date_of_note,company_type=instance.company_type)
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='SGST 2.5% OUT',date=instance.date_of_note,company_type=instance.company_type)
            else:
                createVoucher("Purchase Return",round((gst_amount),2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='IGST 5% OUT',date=instance.date_of_note,company_type=instance.company_type)
                
        if gst == 12:
            if cgst_sgst:
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='CGST 6% OUT',date=instance.date_of_note,company_type=instance.company_type)
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='SGST 6% OUT',date=instance.date_of_note,company_type=instance.company_type)
            else:
                createVoucher("Purchase Return",round((gst_amount),2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='IGST 12% OUT',date=instance.date_of_note,company_type=instance.company_type)
                
        if gst == 18:
            if cgst_sgst:
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='CGST 9% OUT',date=instance.date_of_note,company_type=instance.company_type)
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='SGST 9% OUT',date=instance.date_of_note,company_type=instance.company_type)
            else:
                createVoucher("Purchase Return",round((gst_amount),2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='IGST 18% OUT',date=instance.date_of_note,company_type=instance.company_type)
       
        if gst == 28:
            if cgst_sgst:
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='CGST 14% OUT',date=instance.date_of_note,company_type=instance.company_type)
                createVoucher("Purchase Return",round((gst_amount)/2,2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='SGST 14% OUT',date=instance.date_of_note,company_type=instance.company_type)
            else:
                createVoucher("Purchase Return",round((gst_amount),2),category=gst_ledger_category,drn_details=detail,dr_cr="Credit",gst_type='IGST 28% OUT',date=instance.date_of_note,company_type=instance.company_type)
                

        
        net_amount += total
      

    
    if instance.party_type == "Direct":
        dr_ledger_category = instance.dr_ledger_category
        if instance.bill_from and instance.bill_from.tally_group:
            dr_ledger_category = instance.bill_from.tally_group

        createVoucher("Purchase Return",net_amount,category=dr_ledger_category,drn=instance,dr_cr="Debit",party=instance.bill_from,party_address=instance.bill_from_address)
    else:
        dr_ledger_category = instance.dr_ledger_category
        if instance.bill_from_vendor and instance.bill_from_vendor.tally_group:
            dr_ledger_category = instance.bill_from_vendor.tally_group

        createVoucher("Purchase Return",net_amount,category=dr_ledger_category,drn=instance,dr_cr="Debit",vendor=instance.bill_from_vendor)

    
@receiver(post_save, sender=RecieptVoucher) 
def create_rv_voucher(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(receipt = instance).all()
    vouchers.delete()
    
    if instance.is_deleted:
        return

    cash = None
    if instance.recieve_in == "CASH":
        cash = instance.cash

    bank = instance.bank

    total_bank_charges = instance.bank_charges + instance.bank_charges_cgst + instance.bank_charges_sgst + instance.bank_charges_igst

    if instance.bank_charges:
        createVoucher("Receipt",instance.bank_charges,category=instance.bank_charges_ledger_category,receipt=instance,dr_cr="Debit")

    if instance.bank_charges_cgst:
        createVoucher("Receipt",instance.bank_charges_cgst,category=instance.cgst_ledger_category,receipt=instance,dr_cr="Debit")
    
    if instance.bank_charges_sgst:
        createVoucher("Receipt",instance.bank_charges_sgst,category=instance.sgst_ledger_category,receipt=instance,dr_cr="Debit")
    
    if instance.bank_charges_igst:
        createVoucher("Receipt",instance.bank_charges_igst,category=instance.igst_ledger_category,receipt=instance,dr_cr="Debit")

    if instance.recieve_in == "CASH":
        createVoucher("Receipt",instance.received_amount-total_bank_charges,category=instance.dr_ledger_category,receipt=instance,dr_cr="Debit",cash=cash)
    else:
        createVoucher("Receipt",instance.received_amount-total_bank_charges,category=instance.dr_ledger_category,receipt=instance,dr_cr="Debit",bank=bank)
    
    tds_ledger_category = instance.tds_ledger_category
    createVoucher("Receipt",instance.reciept_tds_amount,category=tds_ledger_category,receipt=instance,dr_cr="Debit",tds_section='TDS RECEIVABLE')
    

    createVoucher("Receipt",instance.adjustment_amount,category=instance.adjustment_ledger_category,receipt=instance,dr_cr="Debit")
    

    for i in instance.rec_voucher_detail.all():



        if i.party_type == "Direct":
            cr_ledger_category = instance.cr_ledger_category
            if i.party and i.party.tally_group:
                cr_ledger_category = i.party.tally_group
                
            createVoucher("Receipt",i.received_amount+i.tds_amount+i.adjustment_amount,category=cr_ledger_category,receipt=instance,dr_cr="Credit",party=i.party,party_address=i.party_address)

        elif i.party_type == "Other":

            cr_ledger_category = instance.cr_ledger_category
            if i.ledger and i.ledger.tally_group:
                cr_ledger_category = i.ledger.tally_group

            createVoucher("Receipt",i.received_amount+i.tds_amount+i.adjustment_amount,category=cr_ledger_category,receipt=instance,dr_cr="Credit",ledger=i.ledger)

        else:

            cr_ledger_category = instance.cr_ledger_category
            if i.vendor and i.vendor.tally_group:
                cr_ledger_category = i.vendor.tally_group

            createVoucher("Receipt",i.received_amount+i.tds_amount+i.adjustment_amount,category=cr_ledger_category,receipt=instance,dr_cr="Credit",vendor=i.vendor)

@receiver(post_save, sender=PaymentVoucher) 
def create_pv_voucher(sender, instance, created, **kwargs):
    
    vouchers = Voucher.objects.filter(payment = instance).all()
    vouchers.delete()
    
    if instance.is_deleted:
        return

    cash = None
    if instance.pay_from == "Cash":
        cash = instance.cash

    bank_charges = instance.bank_charges_cgst + instance.bank_charges_sgst + instance.bank_charges_igst + instance.bank_charges
    cr_amount = instance.paid_amount + bank_charges
    


    
    total_paid_amount = 0
    total_adjustment_amount = 0
    total_tds_amount = 0
    dr_amount = bank_charges
    for i in instance.pay_voucher_detail.all():
        total_adjustment_amount += (i.adjustment_amount)
        total_paid_amount += (i.paid_amount)
        total_tds_amount += (i.tds_amount)
        dr_amount += (i.paid_amount+i.tds_amount)
        if i.party_type == "Direct": 
            createVoucher("Payment",i.paid_amount+i.tds_amount+i.adjustment_amount,category=instance.dr_ledger_category,payment=instance,dr_cr="Debit",party=i.party,party_address=i.party_address)

        elif i.party_type == "Other": 
            createVoucher("Payment",i.paid_amount+i.tds_amount+i.adjustment_amount,category=i.ledger.tally_group,payment=instance,dr_cr="Debit",ledger=i.ledger)

        else:
            createVoucher("Payment",i.paid_amount+i.tds_amount+i.adjustment_amount,category=instance.dr_ledger_category,payment=instance,dr_cr="Debit",vendor=i.vendor)


    if instance.pay_from == "Cash":
        createVoucher("Payment",total_paid_amount + bank_charges,category=instance.cr_ledger_category,payment=instance,dr_cr="Credit",cash=cash)
    else:
        createVoucher("Payment",total_paid_amount + bank_charges,category=instance.cr_ledger_category,payment=instance,dr_cr="Credit",bank=instance.bank)

    
    tds_ledger_category = instance.tds_ledger_category
    createVoucher("Payment",total_tds_amount,category=tds_ledger_category,payment=instance,dr_cr="Credit",tds_section='TDS PAYABLE')

    createVoucher("Payment",total_adjustment_amount,category=instance.adjustment_ledger_category,payment=instance,dr_cr="Credit")


    # If any doesn't match then delete this entry
    if  abs((dr_amount) - (cr_amount)) > 1:
        vouchers = Voucher.objects.filter(payment = instance).all()
        vouchers.delete()

    # Bank Charges Debit Section
    createVoucher("Payment",instance.bank_charges,category=instance.bank_charges_ledger_category,payment=instance,dr_cr="Debit",bank=instance.bank)
    createVoucher("Payment",instance.bank_charges_cgst,category=instance.cgst_ledger_category,payment=instance,dr_cr="Debit",bank=instance.bank)
    createVoucher("Payment",instance.bank_charges_sgst,category=instance.sgst_ledger_category,payment=instance,dr_cr="Debit",bank=instance.bank)
    createVoucher("Payment",instance.bank_charges_igst,category=instance.igst_ledger_category,payment=instance,dr_cr="Debit",bank=instance.bank)
     
@receiver(post_save, sender=ContraVoucher) 
def create_contra_voucher(sender, instance, created, **kwargs):
    
    vouchers = Voucher.objects.filter(contra = instance).all()
    vouchers.delete()
   
    if instance.is_deleted:
        return
    
    if instance.contra_choice == "B2B":
        createVoucher("Contra",instance.amount + instance.bank_charges,category=instance.dr_ledger_category,contra=instance,dr_cr="Debit",bank=instance.account_from)
        createVoucher("Contra",instance.amount,category=instance.cr_ledger_category,contra=instance,dr_cr="Credit",bank=instance.account_to)
        createVoucher("Contra",instance.bank_charges,category=instance.bank_expense_ledger_category,contra=instance,dr_cr="Credit")
        
    if instance.contra_choice == "B2C":
        createVoucher("Contra",instance.amount + instance.bank_charges,category=instance.dr_ledger_category,contra=instance,dr_cr="Debit",bank=instance.account_from)
        createVoucher("Contra",instance.amount,category=instance.cr_ledger_category,contra=instance,dr_cr="Credit",cash=instance.cash)
        createVoucher("Contra",instance.bank_charges,category=instance.bank_expense_ledger_category,contra=instance,dr_cr="Credit")
    
    if instance.contra_choice == "C2B":
        createVoucher("Contra",instance.amount,category=instance.dr_ledger_category,contra=instance,dr_cr="Debit",cash=instance.cash)
        createVoucher("Contra",instance.amount,category=instance.cr_ledger_category,contra=instance,dr_cr="Credit",bank=instance.account_to)
               
       

@receiver(post_save, sender=Journal) 
def create_jv_voucher(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(journal_entry__in = instance.journal_entry.all()).all()
    vouchers.delete()
    vouchers = Voucher.objects.filter(journal = instance).all()
    vouchers.delete()

    if not instance.total_dr_amount == instance.total_cr_amount  or instance.is_deleted:
        return
    
    for i in instance.journal_entry.all():
        if i.ledger and not i.ledger.tally_group:
            instance.error = True
            return
        
        if i.party and not i.party.tally_group:
            instance.error = True
            return
        
        if i.vendor and not i.vendor.tally_group:
            instance.error = True
            return

    for i in instance.journal_entry.all():
        if i.ledger and i.ledger.tally_group:
            createVoucher("Journal",(i.amount),category=i.ledger.tally_group,journal=instance,dr_cr=i.dr_cr,ledger=i.ledger,journal_entry=i)
        
        if i.party and i.party.tally_group:
            createVoucher("Journal",(i.amount),category=i.party.tally_group,journal=instance,dr_cr=i.dr_cr,party=i.party,journal_entry=i)
        
        if i.vendor and i.vendor.tally_group:
            createVoucher("Journal",(i.amount),category=i.vendor.tally_group,journal=instance,dr_cr=i.dr_cr,vendor=i.vendor,journal_entry=i)
        
  

@receiver(post_save, sender=Party) 
def create_party(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(party_opening = instance).all()
    vouchers.delete()
    if instance.opening_balance <= 0:
        return
    if instance.opening_in == "Debit":
        createVoucher("Party Opening",instance.opening_balance,category=instance.tally_group,party_opening=instance,dr_cr="Debit",party=instance)
        createVoucher("Party Opening",instance.opening_balance,category=instance.opening_ledger_category,party_opening=instance,dr_cr="Credit",party=instance)
    else:
        createVoucher("Party Opening",instance.opening_balance,category=instance.opening_ledger_category,party_opening=instance,dr_cr="Debit",party=instance)
        createVoucher("Party Opening",instance.opening_balance,category=instance.tally_group,party_opening=instance,dr_cr="Credit",party=instance)

@receiver(post_save, sender=LedgerMaster) 
def create_ledger_master(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(ledger_opening = instance).all()
    vouchers.delete()
    if instance.opening_balance <= 0:
        return
    if instance.balance_in == "Debit":
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.tally_group,ledger_opening=instance,dr_cr="Debit",ledger=instance)
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.opening_ledger_category,ledger_opening=instance,dr_cr="Credit",ledger=instance)
    else:
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.opening_ledger_category,ledger_opening=instance,dr_cr="Debit",ledger=instance)
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.tally_group,ledger_opening=instance,dr_cr="Credit",ledger=instance)

@receiver(post_save, sender=Bank) 
def create_bank_master(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(bank_opening = instance).all()
    vouchers.delete()
    if instance.opening_balance <= 0:
        return
    if instance.opening_in == "Debit":
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.tally_group,bank_opening=instance,dr_cr="Debit",bank=instance)
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.opening_ledger_category,bank_opening=instance,dr_cr="Credit",bank=instance)
    else:
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.opening_ledger_category,bank_opening=instance,dr_cr="Debit",bank=instance)
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.tally_group,bank_opening=instance,dr_cr="Credit",bank=instance)

@receiver(post_save, sender=Vendor) 
def create_vendor_master(sender, instance, created, **kwargs):
    vouchers = Voucher.objects.filter(vendor_opening = instance).all()
    vouchers.delete()
    if instance.opening_balance <= 0:
        return
    if instance.opening_in == "Debit":
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.tally_group,vendor_opening=instance,dr_cr="Debit",vendor=instance)
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.opening_ledger_category,vendor_opening=instance,dr_cr="Credit",vendor=instance)
    else:
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.opening_ledger_category,vendor_opening=instance,dr_cr="Debit",vendor=instance)
        createVoucher("Ledger Opening",instance.opening_balance,category=instance.tally_group,vendor_opening=instance,dr_cr="Credit",vendor=instance)


# ------------- Delete Receivers --------------
@receiver(pre_delete, sender=PaymentVoucher) 
def pre_delete_pv_voucher(sender, instance, **kwargs):
    try:
        vouchers = Voucher.objects.filter(payment = instance).all()
        vouchers.delete()
    except:
        pass
    
@receiver(pre_delete, sender=RecieptVoucher) 
def pre_delete_rv_voucher(sender, instance, **kwargs):
    try:
        vouchers = Voucher.objects.filter(receipt = instance).all()
        vouchers.delete()
    except:
        pass

@receiver(pre_delete, sender=InvoiceReceivable) 
def pre_delete_sales_voucher(sender, instance, **kwargs):
    try:
        vouchers = Voucher.objects.filter(sales_invoice = instance).all()
        vouchers.delete()
    except:
        pass

@receiver(pre_delete, sender=InvoicePayable) 
def pre_delete_purchase_voucher(sender, instance, **kwargs):
    try:
        vouchers = Voucher.objects.filter(purchase_invoice = instance).all()
        vouchers.delete()
    except:
        pass



@receiver(pre_delete, sender=Journal) 
def pre_delete_jv_voucher(sender, instance, **kwargs):
    try:
        vouchers = Voucher.objects.filter(journal_entry__in = instance.journal_entry.all()).all()
        vouchers.delete()
        vouchers = Voucher.objects.filter(journal = instance).all()
        vouchers.delete()
    except:
        pass


@receiver(pre_delete, sender=ContraVoucher) 
def pre_delete_contra_voucher(sender, instance, **kwargs):
    try:
        vouchers = Voucher.objects.filter(contra = instance).all()
    except:
        pass
        vouchers.delete()