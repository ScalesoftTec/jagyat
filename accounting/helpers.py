from accounting.models import *
from masters.models import *
from django.shortcuts import HttpResponse
from datetime import datetime
from django.db.models import Q

def addLedgerToSalesInvoice(request):
    # invoice = LoanPaymentRecord.objects.all()
    # for i in invoice:
    #     try:
    #         i.save()
    #     except:
    #         pass
        
        
    # invoice = Loan.objects.all()
    # for i in invoice:
    #     try:
    #         i.save()
    #     except:
    #         pass
        
        
    # invoice = DebitNote.objects.all()
    # for i in invoice:
    #     try:
    #         i.save()
    #     except:
    #         pass
   
    # invoice = IndirectExpense.objects.all()
    # for i in invoice:
    #     try:
    #         i.save()
    #     except:
    #         pass
   
    invoice = ContraVoucher.objects.all()
    bank_category = LedgerCategory.objects.filter(id=4).first()
    cash_category = LedgerCategory.objects.filter(id=5).first()
    for i in invoice:
        
        if i.contra_choice == "B2C":
            i.cr_ledger_category = bank_category
            i.dr_ledger_category = cash_category
            i.save()
            
        if i.contra_choice == "C2B":
            i.cr_ledger_category = cash_category
            i.dr_ledger_category = bank_category
            
            i.save()
        
    invoice = PaymentVoucher.objects.all()
    for i in invoice:
        if i.pay_from == "Cash":
            i.cr_ledger_category = cash_category
            i.save()
    
        
    invoice = RecieptVoucher.objects.all()
    for i in invoice:
        try:
            if i.recieve_in == 'Cash':
                i.dr_ledger_category = cash_category
                i.save()
        except:
            pass
    
    # invoice = CreditNote.objects.all()
    # for i in invoice:
    #     try:
    #         i.save()
    #     except:
    #         pass
    # invoice = InvoiceReceivable.objects.all()
    # for i in invoice:
    #     try:
    #         i.save()
    #     except:
    #         pass
        
    # invoice = InvoicePayable.objects.all()
    # for i in invoice:
    #     try:
    #         i.save()
    #     except:
    #         pass
    return HttpResponse(f" no. of sales invoices altered")

def addLedgerToCRN(request):
    
        
    return HttpResponse(f"no. of credit notes altered")


def addLedgerToPurchaseInvoice(request):
    return HttpResponse(f"no. of contra altered")


def addLedgerToRecieptVoucher(request):

    return HttpResponse(f"no. of reciepts altered")




def addLedgerToPaymentVoucher(request):
   
    return HttpResponse(f" no. of payments altered")



