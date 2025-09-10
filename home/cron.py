from accounting.views import EmailMultiAlternatives,EmailThread,strip_tags,render_to_string,settings
from masters.models import JobMaster,MBLMaster,VGMMaster,CargoArrivalNotice,DeliveryOrder,DSR,FreightCertificate
from accounting.models import InvoiceReceivable,InvoicePayable,RecieptVoucher,PaymentVoucher
from dashboard.models import Logistic
from datetime import date

def todayUpdates():
    logistic = Logistic.objects.all()
    for i in logistic:
        jobs =JobMaster.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        mbls = MBLMaster.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        vgms = VGMMaster.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        cans = CargoArrivalNotice.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        dos = DeliveryOrder.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        dsrs = DSR.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        fcs = FreightCertificate.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        inv_rec = InvoiceReceivable.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        inv_pay = InvoicePayable.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        rec_vou = RecieptVoucher.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        pay_vou = PaymentVoucher.objects.filter(created_at = date.today()).filter(company_type__id = i.id).all()
        
        subject = f"Today Updates For {i.company_name} ({i.branch_name})"
        to_email = [i.branch_email,]
        html_content = render_to_string("email/today_update.html",{
            'jobs':jobs,
            'mbls':mbls,
            'vgms':vgms,
            'cans':cans,
            'dos':dos,
            'dsrs':dsrs,
            'fcs':fcs,
            'inv_rec':inv_rec,
            'inv_pay':inv_pay,
            'rec_vou':rec_vou,
            'pay_vou':pay_vou,
            'company':i,
            'today_date':date.today(),
        })
        text_content = strip_tags(html_content)
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            subject=subject,
            body = text_content,
            from_email = from_email,
            to=to_email
        )
        msg.attach_alternative(html_content,"text/html")
        EmailThread(msg).start()
        
def pendingInvoices():
    invoices = InvoiceReceivable.objects.filter(pending_amount__gte = 0).filter(due_date__lte = date.today()).all()
    for i in invoices:
        subject = f"Alert Pending Invoice"
        to_email = [i.branch_email,]
        html_content = render_to_string("email/invoice_due_alert.html",{
            'invoice':i
        })
        text_content = strip_tags(html_content)
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            subject=subject,
            body = text_content,
            from_email = from_email,
            to=to_email
        )
        msg.attach_alternative(html_content,"text/html")
        EmailThread(msg).start()