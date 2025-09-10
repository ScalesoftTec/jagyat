from dashboard.models import Logistic
from accounting.models import CreditNote, CreditNoteDetail, DebitNote, DebitNoteDetail, InvoicePayable, InvoicePayableDetail, InvoiceReceivable,InvoiceReceivableDetail
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.units import inch
import num2words
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Paragraph



def local_invoice_pdf(request, id):
    invoice_data = InvoiceReceivable.objects.filter(id=int(id)).first()
    filename = f'dsr_{id}.pdf'
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={filename}'
    c = canvas.Canvas(response)



    setting = Logistic.objects.filter(id=invoice_data.company_type.id).first()
    invoice_heads = InvoiceReceivableDetail.objects.filter(invoice_receivable=invoice_data).order_by('id')

    # ---------------------------- Outer Border Box -----------------------------------
    c.line(25, 820, 575, 820)
    c.line(25, 10, 575, 10)
    c.line(25, 10, 25, 820)
    c.line(575, 820, 575, 10)

 
    header_image = 'media/' + str(setting.letter_head)

  
    c.drawImage(header_image, 28, 715, width=7.54 * inch, height=1.40 * inch)

    c.setFont('Helvetica-Bold', 9)

    c.line(25, 715, 575, 715)
    c.drawString(30, 705, 'Bill TO:')
    c.drawString(30, 692, str(invoice_data.bill_to))
    c.setFont('Helvetica', 9)
    c.drawString(30, 675, str(invoice_data.bill_to.corp_address_line1))
    c.drawString(30, 663, str(invoice_data.bill_to.corp_address_line2))
    c.drawString(30, 651, str(invoice_data.bill_to.corp_address_line3))
    c.drawString(30, 625, 'State Name :')
    c.drawString(85, 625, str(invoice_data.bill_to.corp_state))
    c.drawString(225, 625, 'Code :')
    c.drawString(255, 625, str(invoice_data.bill_to.corp_state.gst_code))  # Dynamic Code for GST Code of State of selected account party 
    c.line(275, 715, 275, 600)

    c.setFont('Helvetica-Bold', 9)

    c.drawString(280, 704, invoice_data.type_of_invoice)
    c.drawString(380, 704, invoice_data.invoice_no)


    c.drawString(520, 704, str(invoice_data.date_of_invoice))

    c.line(275, 699, 575, 699)
    c.setFont('Helvetica', 9)

    c.drawString(280, 688, 'Shipper')
    c.drawString(345, 688, ':')

   
    c.drawString(360, 688, str(invoice_data.job_no.shipper))

   

    if invoice_data.job_no.module == "Air Export" or invoice_data.job_no.module == "Air Import":
        c.drawString(280, 677, 'AWB No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.job_no.awb_no))
        c.drawString(280, 666, 'Docket No')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.job_no.docket_no))
    else:
        c.drawString(280, 677, 'Container No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.job_no.container_no))
        c.drawString(280, 666, 'Container Type')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.job_no.container_type))
    c.drawString(280, 655, 'Consignee')
    c.drawString(345, 655, ':')
    c.drawString(360, 655, str(invoice_data.job_no.consignee))
    c.drawString(280, 644, 'Notify Party')
    c.drawString(345, 644, ':')
    c.drawString(360, 644, str(invoice_data.job_no.notify_party))
    c.drawString(280, 633, 'Job No')
    c.drawString(345, 633, ':')
    c.drawString(360, 633, str(invoice_data.job_no))

    c.line(275, 628, 575, 628)
    c.setFont('Helvetica-Bold', 9)

    if invoice_data.job_no.module == "Sea Import" or invoice_data.job_no.module == "Sea Export":
        c.drawString(280, 618, 'MBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'HBL No.')
    
    elif invoice_data.job_no.module == "Air Import" or invoice_data.job_no.module == "Air Export":
        c.drawString(280, 618, 'AWMBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'AWHBL No.')
    
    
    c.drawString(345, 606, ':')
    c.setFont('Helvetica', 9)
    c.drawString(360, 618, str(invoice_data.job_no.mbl_no))
    c.drawString(360, 606, str(invoice_data.job_no.hbl_no))



    c.line(25, 620, 275, 620)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, 608, 'GSTIN:')
    c.drawString(93, 608, ':')
    c.drawString(98, 608, str(invoice_data.job_no.account.corp_gstin))
    c.line(25, 600, 575, 600)
    c.setFont('Helvetica', 9)
    c.drawString(30, 590, 'Port of Loading')
    c.drawString(93, 590, ':')
    c.drawString(98, 590, str(invoice_data.job_no.port_of_loading))
    c.drawString(210, 590, 'Final Destination: ')
    c.drawString(285, 590, str(invoice_data.job_no.final_destination))
    c.drawString(210, 565, 'Gross Wt:')
    c.drawString(285, 565, str(invoice_data.job_no.gross_weight))

    if invoice_data.job_no.module == 'Air Import' or invoice_data.job_no.module == 'Air Export':
        c.drawString(30, 577, 'Flight No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.job_no.flight_no))
    else:
        c.drawString(30, 577, 'Vessel No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.vessel_voyage_id))
    
    c.drawString(210, 577, 'No of Pkgs:')
    c.drawString(285, 577, str(invoice_data.job_no.no_of_packages+" "+str(invoice_data.job_no.packages_type)))

   

    c.drawString(30, 565, 'Commodity')
    c.drawString(93, 565, ':')
    c.drawString(98, 565, str(invoice_data.job_no.commodity))

    c.line(25, 560, 575, 560)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(26, 548, 'S.No')

    c.line(47, 560, 47, 300)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(85, 548, 'Charges Description')
    c.line(188, 560, 188, 300)
    c.drawString(190, 548, 'SAC')
    c.line(218, 560, 218, 300)
    c.drawString(220, 548, 'Unit')
    c.line(240, 560, 240, 300)
    c.drawString(248, 548, 'Rate')
    c.line(275, 560, 275, 300)
    c.drawString(279, 548, 'Curr.')
    
    c.line(305, 560, 305, 280)
    
    c.drawString(308, 548, 'Ex.Rate')
    c.line(345, 560, 345, 280)
    c.drawString(351, 548, 'Amount')
    c.line(391, 560, 391, 300)
    c.drawString(394, 548, 'IGST')
    c.line(417, 560, 417, 300)
    c.drawString(420, 548, 'CGST')
    c.line(447, 560, 447, 300)
    c.drawString(450, 548, 'SGST')
    c.line(480, 560, 480, 165)
    c.drawString(488, 548, 'Tax Amt')
    c.line(530, 560, 530, 280)
    c.drawString(543, 548, 'Total')
    c.line(25, 540, 575, 540)

    # Assigning Company State GST Code Here
    a = setting.company_gst_code
    
    
    b = str(invoice_data.job_no.account.corp_state.gst_code) # Dynamic GST Code Here for State

    if a == b:
    
        gstapplied = 1
        divide_total_tax = (float(invoice_data.gst_amount) / 2)
        c.drawString(490, 230, str(divide_total_tax))
        c.drawString(490, 215, str(divide_total_tax))
        c.drawString(490, 200, '0.0')

    else:
        gstapplied = 2
        c.drawString(490, 230, '0.0')
        c.drawString(490, 215, '0.0')
        c.drawString(490, 200, str(invoice_data.gst_amount))

    y = 530
    i = 1
    for row in invoice_heads:
        c.setFont('Helvetica', 7)
        c.drawString(32, y, str(i))
        c.drawString(50, y, str(row.billing_head))
        c.drawString(190, y, str(row.billing_head.hsn_code))
        c.drawString(220, y, str(row.qty_unit))
        c.drawString(246, y, str(row.rate))
        c.drawString(279, y, str(row.currency))
        c.drawString(315, y, str(row.ex_rate))
        c.drawString(348, y, str(row.amount))

        a = setting.company_gst_code 
        b = str(invoice_data.job_no.account.corp_state.gst_code) # Dynamic GST Code Here for State


        if a == b:
            gstapplied = 1
            divide_gst = (float(row.gst) / 2)
            if divide_gst != 0:
                c.drawString(420, y, str(divide_gst)+'%')
                c.drawString(450, y, str(divide_gst)+'%')
                c.drawString(397, y, '0.0')
            else:
                c.drawString(420, y, "")
                c.drawString(450, y, "")
                c.drawString(397, y, "")


        else:
            gstapplied = 2
            if row.gst != str(0):
                c.drawString(397, y, str(row.gst)+'%')
            else:
                c.drawString(397, y, "")

        c.drawString(495, y, str(row.gst_amount))
        c.drawString(540, y, str(row.total))

        y = y-10
        i = i+1

    c.line(25, 300, 575, 300)
    c.setFont('Helvetica-Bold', 9)


    c.drawString(30, 290, 'Bank Details')
    c.setFont('Helvetica', 9)
    c.drawString(30, 275, 'A/C NO.')
    c.drawString(89, 275, ':')
    c.drawString(95, 275, str(invoice_data.account_number))

    c.drawString(30, 260, 'Branch Name')
    c.drawString(89, 260, ':')
    branch_nm = str(invoice_data.account_number.branch_name).splitlines()
    y = 260
    i = 0
    for row in branch_nm:
        c.drawString(95, y, branch_nm[i])
        y = y - 15
        i = i + 1
        
    c.drawString(30, 215, 'Beneficiary')
    c.drawString(89, 215, ':')
    c.drawString(95, 215, str(invoice_data.account_number.beneficiary_name))

    c.drawString(30, 200, 'IFSC Code')
    c.drawString(89, 200, ':')
    c.drawString(95, 200, str(invoice_data.account_number.ifsc_code))
    
    c.drawString(30, 185, 'Swift Code')
    c.drawString(89, 185, ':')
    c.drawString(95, 185, str(invoice_data.account_number.swift_code))

    c.setFont('Helvetica-Bold', 9)
    c.line(381, 280, 381, 165)
    c.drawString(308, 287, 'Total')

    c.drawString(385, 245, 'Gross Amount')
    c.drawString(490, 245, str(invoice_data.gross_amount))
    c.drawString(385, 230, 'CGST')
    c.drawString(385, 215, 'SGST')
    c.drawString(385, 200, 'IGST')

    c.drawString(352, 287, str(invoice_data.gross_amount))
    c.drawString(490, 287, str(invoice_data.gst_amount))
    c.drawString(540, 287, str(invoice_data.net_amount))
    c.line(304, 280, 575, 280)

    c.line(381, 185, 575, 185)
    c.drawString(30, 153, 'Amount in Words:')

    a = num2words.num2words(invoice_data.net_amount, lang='en_IN')
    a = a.replace(',','')
    c.setFont('Helvetica', 9)
    c.drawString(110, 153, a.upper() + ' ONLY ')

    c.setFont('Helvetica-Bold', 9)
    c.drawString(385, 172, 'Net Amount')
    c.drawString(490, 172, invoice_data.net_amount)

    c.line(25, 165, 575, 165)

    c.setFont('Helvetica-Bold', 7)
    c.line(25, 140, 575, 140)
    c.drawString(30, 131, "Term and Conditions ")

   
    c.setFont('Helvetica-Bold', 8)
    c.drawString(420, 130, setting.for_company)


    c.setFont('Helvetica-Bold', 5)
    c.drawString(35-3, 120+3, "1.Cargo has not been checked with while issuing this notice. Delivery order will be issued only after cargo is checked/deposited at liner/msil.")
    c.drawString(38-3, 115+3, "Warehouse and RAYZZ GLOBAL LOGISTICS. are not liable for any claim, as a result of delay on part of carriers to check the vessel and issue DO.")
    c.drawString(35-3, 105+3, "2. Please note, once cargo is accepted/delivered, it is deemed to have been accepted in good faith. Any further claim or legal cause will ")
    c.drawString(40-3, 100+3, "not bind 'RAYZZ GLOBAL LOGISTICS' subject to the jurisdiction of the UP Court")
    c.drawString(35-3, 90+3,  "3. Do/Freight payment should be made in advance before D.O. collect/BL issue.")
    c.drawString(35-3, 80+3,  "4. The Cheque/DD should be drawn in favor of ***RAYZZ GLOBAL LOGISTICS *** NEFT/RTGS details given above.")
    c.drawString(35-3, 70+3,  "5. Kindly check all documents details carefully to avoid unnecessary complications.")
    c.drawString(35-3, 60+3,  "6. All cancellation & refunds as per airline/shipping line rules & regulations")
    c.drawString(35-3, 50+3,  "7. This is a computer Generated Invoice, hence no signature required.")
    c.drawString(35-3, 40+3,  "8. All Disputes are subject to UP Jurisdiction.")
    c.drawString(35-3, 30+3,  "9. All bills to be paid on or before due date.")
    c.drawString(35-3, 20+3,  "10. Interest @18% will be charged on delayed payment")
    c.drawString(35-3, 12+3,  "11. E. & O.E.")
    
  
                 


    
    logo = 'media/' +  str(setting.stamp)
    
    c.drawImage(logo, 447, 35, width=1.35 * inch, height=1.20 * inch)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(450, 22, 'Authorised Signatory')
    c.setFont('Helvetica', 8)
    # c.drawString(180, 25, 'This is a Computer generated Invoice and no signature is required')

    c.showPage()
    c.save()
    return response



def createInvoicePDF(request, id):
    buffer=BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
   # Start writing
    invoice_data = InvoiceReceivable.objects.filter(id=int(id)).first()
    invoice_heads = InvoiceReceivableDetail.objects.filter(invoice_receivable=invoice_data).order_by('id')
    setting = Logistic.objects.filter(id=invoice_data.company_type.id).first()

    # ---------------------------- Outer Border Box -----------------------------------
    c.line(25, 820, 575, 820)
    c.line(25, 10, 575, 10)
    c.line(25, 10, 25, 820)
    c.line(575, 820, 575, 10)

 
    header_image = 'media/' + str(setting.letter_head)

  
    c.drawImage(header_image, 28, 715, width=7.54 * inch, height=1.40 * inch)

    c.setFont('Helvetica-Bold', 9)

    c.line(25, 715, 575, 715)
    c.drawString(30, 705, 'Bill TO:')
    c.drawString(30, 692, str(invoice_data.bill_to))
    c.setFont('Helvetica', 9)
    c.drawString(30, 675, str(invoice_data.bill_to.corp_address_line1))
    c.drawString(30, 663, str(invoice_data.bill_to.corp_address_line2))
    c.drawString(30, 651, str(invoice_data.bill_to.corp_address_line3))
    c.drawString(30, 625, 'State Name :')
    c.drawString(85, 625, str(invoice_data.bill_to.corp_state))
    c.drawString(225, 625, 'Code :')
    c.drawString(255, 625, str(invoice_data.bill_to.corp_state.gst_code))  # Dynamic Code for GST Code of State of selected account party 
    c.line(275, 715, 275, 600)

    c.setFont('Helvetica-Bold', 9)

    c.drawString(280, 704, invoice_data.type_of_invoice)
    c.drawString(380, 704, invoice_data.invoice_no)


    c.drawString(520, 704, str(invoice_data.date_of_invoice))

    c.line(275, 699, 575, 699)
    c.setFont('Helvetica', 9)

    c.drawString(280, 688, 'Shipper')
    c.drawString(345, 688, ':')

   
    c.drawString(360, 688, str(invoice_data.job_no.shipper))

   

    if invoice_data.job_no.module == "Air Export" or invoice_data.job_no.module == "Air Import":
        c.drawString(280, 677, 'AWB No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.job_no.awb_no))
        c.drawString(280, 666, 'Docket No')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.job_no.docket_no))
    else:
        c.drawString(280, 677, 'Container No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.job_no.container_no))
        c.drawString(280, 666, 'Container Type')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.job_no.container_type))
    c.drawString(280, 655, 'Consignee')
    c.drawString(345, 655, ':')
    c.drawString(360, 655, str(invoice_data.job_no.consignee))
    c.drawString(280, 644, 'Notify Party')
    c.drawString(345, 644, ':')
    c.drawString(360, 644, str(invoice_data.job_no.notify_party))
    c.drawString(280, 633, 'Job No')
    c.drawString(345, 633, ':')
    c.drawString(360, 633, str(invoice_data.job_no))

    c.line(275, 628, 575, 628)
    c.setFont('Helvetica-Bold', 9)

    if invoice_data.job_no.module == "Sea Import" or invoice_data.job_no.module == "Sea Export":
        c.drawString(280, 618, 'MBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'HBL No.')
    
    elif invoice_data.job_no.module == "Air Import" or invoice_data.job_no.module == "Air Export":
        c.drawString(280, 618, 'AWMBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'AWHBL No.')
    
    
    c.drawString(345, 606, ':')
    c.setFont('Helvetica', 9)
    c.drawString(360, 618, str(invoice_data.job_no.mbl_no))
    c.drawString(360, 606, str(invoice_data.job_no.hbl_no))



    c.line(25, 620, 275, 620)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, 608, 'GSTIN:')
    c.drawString(93, 608, ':')
    c.drawString(98, 608, str(invoice_data.bill_to.corp_gstin))
    c.line(25, 600, 575, 600)
    c.setFont('Helvetica', 9)
    c.drawString(30, 590, 'Port of Loading')
    c.drawString(93, 590, ':')
    c.drawString(98, 590, str(invoice_data.job_no.port_of_loading))
    c.drawString(210, 590, 'Final Destination: ')
    c.drawString(285, 590, str(invoice_data.job_no.final_destination))
    c.drawString(210, 565, 'Gross Wt:')
    c.drawString(285, 565, str(invoice_data.job_no.gross_weight))

    if invoice_data.job_no.module == 'Air Import' or invoice_data.job_no.module == 'Air Export':
        c.drawString(30, 577, 'Flight No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.job_no.flight_no))
    else:
        c.drawString(30, 577, 'Vessel No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.vessel_voyage_id))
    
    c.drawString(210, 577, 'No of Pkgs:')
    c.drawString(285, 577, str(invoice_data.job_no.no_of_packages+" "+str(invoice_data.job_no.packages_type)))

   

    c.drawString(30, 565, 'Commodity')
    c.drawString(93, 565, ':')
    c.drawString(98, 565, str(invoice_data.job_no.commodity))

    c.line(25, 560, 575, 560)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(26, 548, 'S.No')

    c.line(47, 560, 47, 300)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(85, 548, 'Charges Description')
    c.line(188, 560, 188, 300)
    c.drawString(190, 548, 'SAC')
    c.line(218, 560, 218, 300)
    c.drawString(220, 548, 'Unit')
    c.line(240, 560, 240, 300)
    c.drawString(248, 548, 'Rate')
    c.line(275, 560, 275, 300)
    c.drawString(279, 548, 'Curr.')
    
    c.line(305, 560, 305, 280)
    
    c.drawString(308, 548, 'Ex.Rate')
    c.line(345, 560, 345, 280)
    c.drawString(351, 548, 'Amount')
    c.line(391, 560, 391, 300)
    c.drawString(394, 548, 'IGST')
    c.line(417, 560, 417, 300)
    c.drawString(420, 548, 'CGST')
    c.line(447, 560, 447, 300)
    c.drawString(450, 548, 'SGST')
    c.line(480, 560, 480, 165)
    c.drawString(488, 548, 'Tax Amt')
    c.line(530, 560, 530, 280)
    c.drawString(543, 548, 'Total')
    c.line(25, 540, 575, 540)

    # Assigning Company State GST Code Here
    a = setting.company_gst_code
    
    
    b = str(invoice_data.bill_to.corp_state.gst_code) # Dynamic GST Code Here for State

    if a == b:
    
        gstapplied = 1
        divide_total_tax = (float(invoice_data.gst_amount) / 2)
        c.drawString(490, 230, str(divide_total_tax))
        c.drawString(490, 215, str(divide_total_tax))
        c.drawString(490, 200, '0.0')

    else:
        gstapplied = 2
        c.drawString(490, 230, '0.0')
        c.drawString(490, 215, '0.0')
        c.drawString(490, 200, str(invoice_data.gst_amount))

    y = 530
    i = 1
    for row in invoice_heads:
        c.setFont('Helvetica', 7)
        c.drawString(32, y, str(i))
        c.drawString(50, y, str(row.billing_head))
        c.drawString(190, y, str(row.billing_head.hsn_code))
        c.drawString(220, y, str(row.qty_unit))
        c.drawString(246, y, str(row.rate))
        c.drawString(279, y, str(row.currency))
        c.drawString(315, y, str(row.ex_rate))
        c.drawString(348, y, str(row.amount))

        a = setting.company_gst_code 
        b = str(invoice_data.bill_to.corp_state.gst_code) # Dynamic GST Code Here for State


        if a == b:
            gstapplied = 1
            divide_gst = (float(row.gst) / 2)
            if divide_gst != 0:
                c.drawString(420, y, str(divide_gst)+'%')
                c.drawString(450, y, str(divide_gst)+'%')
                c.drawString(397, y, '0.0')
            else:
                c.drawString(420, y, "")
                c.drawString(450, y, "")
                c.drawString(397, y, "")


        else:
            gstapplied = 2
            if row.gst != str(0):
                c.drawString(397, y, str(row.gst)+'%')
            else:
                c.drawString(397, y, "")

        c.drawString(495, y, str(row.gst_amount))
        c.drawString(540, y, str(row.total))

        y = y-10
        i = i+1

    c.line(25, 300, 575, 300)
    c.setFont('Helvetica-Bold', 9)


    c.drawString(30, 290, 'Bank Details')
    c.setFont('Helvetica', 9)
    c.drawString(30, 275, 'A/C NO.')
    c.drawString(89, 275, ':')
    c.drawString(95, 275, str(invoice_data.account_number))

    c.drawString(30, 260, 'Branch Name')
    c.drawString(89, 260, ':')
    branch_nm = str(invoice_data.account_number.branch_name).splitlines()
    y = 260
    i = 0
    for row in branch_nm:
        c.drawString(95, y, branch_nm[i])
        y = y - 15
        i = i + 1
        
    c.drawString(30, 215, 'Beneficiary')
    c.drawString(89, 215, ':')
    c.drawString(95, 215, str(invoice_data.account_number.beneficiary_name))

    c.drawString(30, 200, 'IFSC Code')
    c.drawString(89, 200, ':')
    c.drawString(95, 200, str(invoice_data.account_number.ifsc_code))
    
    c.drawString(30, 185, 'Swift Code')
    c.drawString(89, 185, ':')
    c.drawString(95, 185, str(invoice_data.account_number.swift_code))

    c.setFont('Helvetica-Bold', 9)
    c.line(381, 280, 381, 165)
    c.drawString(308, 287, 'Total')

    c.drawString(385, 245, 'Gross Amount')
    c.drawString(490, 245, str(invoice_data.gross_amount))
    c.drawString(385, 230, 'CGST')
    c.drawString(385, 215, 'SGST')
    c.drawString(385, 200, 'IGST')

    c.drawString(352, 287, str(invoice_data.gross_amount))
    c.drawString(490, 287, str(invoice_data.gst_amount))
    c.drawString(540, 287, str(invoice_data.net_amount))
    c.line(304, 280, 575, 280)

    c.line(381, 185, 575, 185)
    c.drawString(30, 153, 'Amount in Words:')

    a = num2words.num2words(invoice_data.net_amount, lang='en_IN')
    a = a.replace(',','')
    c.setFont('Helvetica', 9)
    c.drawString(110, 153, a.upper() + ' ONLY ')

    c.setFont('Helvetica-Bold', 9)
    c.drawString(385, 172, 'Net Amount')
    c.drawString(490, 172, invoice_data.net_amount)

    c.line(25, 165, 575, 165)

    c.setFont('Helvetica-Bold', 7)
    c.line(25, 140, 575, 140)
    c.drawString(30, 131, "Term and Conditions ")
    p = Paragraph(setting.terms_and_conditions)
    p.wrapOn(c,25,120)
    p.drawOn(c,25,120)
    
    c.setFont('Helvetica-Bold', 8)
    c.drawString(420, 130, setting.for_company)

    
    logo = 'media/' +  str(setting.stamp)
    
    c.drawImage(logo, 447, 35, width=1.35 * inch, height=1.20 * inch)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(450, 22, 'Authorised Signatory')
   
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def credit_note_pdf(request, id):
    invoice_data = CreditNote.objects.filter(id=int(id)).first()
    filename = f'credit_note_{id}.pdf'
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={filename}'
    c = canvas.Canvas(response)

    setting = Logistic.objects.filter(id=invoice_data.company_type.id).first()


    invoice_heads = CreditNoteDetail.objects.filter(credit_note=invoice_data).order_by('id')

    # ---------------------------- Outer Border Box -----------------------------------
    c.line(25, 820, 575, 820)
    c.line(25, 10, 575, 10)
    c.line(25, 10, 25, 820)
    c.line(575, 820, 575, 10)

 
    header_image = 'media/' + str(setting.letter_head)

  
    c.drawImage(header_image, 28, 715, width=7.54 * inch, height=1.40 * inch)

    c.setFont('Helvetica-Bold', 9)

    c.line(25, 715, 575, 715)
    c.drawString(30, 705, 'Bill TO:')
    c.drawString(30, 692, str(invoice_data.bill_to))
    c.setFont('Helvetica', 9)
    c.drawString(30, 675, str(invoice_data.bill_to.corp_address_line1))
    c.drawString(30, 663, str(invoice_data.bill_to.corp_address_line2))
    c.drawString(30, 651, str(invoice_data.bill_to.corp_address_line3))
    c.drawString(30, 625, 'State Name :')
    c.drawString(85, 625, str(invoice_data.bill_to.corp_state))
    c.drawString(225, 625, 'Code :')
    c.drawString(255, 625, str(invoice_data.bill_to.corp_state.gst_code))  # Dynamic Code for GST Code of State of selected account party 
    c.line(275, 715, 275, 600)

    c.setFont('Helvetica-Bold', 9)

    c.drawString(280, 704, 'CREDIT NOTE')
    c.drawString(380, 704, invoice_data.credit_note_no)


    c.drawString(520, 704, str(invoice_data.date_of_note))

    c.line(275, 699, 575, 699)
    c.setFont('Helvetica', 9)

    c.drawString(280, 688, 'Shipper')
    c.drawString(345, 688, ':')

   
    c.drawString(360, 688, str(invoice_data.job_no.shipper))

   

    if invoice_data.job_no.module == "Air Export" or invoice_data.job_no.module == "Air Import":
        c.drawString(280, 677, 'AWB No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.awb_no))
        c.drawString(280, 666, 'Docket No')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.docket_no))
    else:
        c.drawString(280, 677, 'Container No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.container_no))
        c.drawString(280, 666, 'Container Type')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.container_type))
    c.drawString(280, 655, 'Consignee')
    c.drawString(345, 655, ':')
    c.drawString(360, 655, str(invoice_data.job_no.consignee))


    c.line(275, 628, 575, 628)
    c.setFont('Helvetica-Bold', 9)

    if invoice_data.job_no.module == "Sea Import" or invoice_data.job_no.module == "Sea Export":
        c.drawString(280, 618, 'MBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'HBL No.')
    
    elif invoice_data.job_no.module == "Air Import" or invoice_data.job_no.module == "Air Export":
        c.drawString(280, 618, 'AWMBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'AWHBL No.')
    
    
    c.drawString(345, 606, ':')
    c.setFont('Helvetica', 9)
    c.drawString(360, 618, str(invoice_data.job_no.mbl_no))
    c.drawString(360, 606, str(invoice_data.job_no.hbl_no))



    c.line(25, 620, 275, 620)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, 608, 'GSTIN:')
    c.drawString(93, 608, ':')
    c.drawString(98, 608, str(invoice_data.job_no.account.corp_gstin))
    c.line(25, 600, 575, 600)
    c.setFont('Helvetica', 9)
    c.drawString(30, 590, 'Port of Loading')
    c.drawString(93, 590, ':')
    c.drawString(98, 590, str(invoice_data.job_no.port_of_loading))
    c.drawString(210, 590, 'Final Destination: ')
    c.drawString(285, 590, str(invoice_data.job_no.final_destination))
    c.drawString(210, 565, 'Gross Wt:')
    c.drawString(285, 565, str(invoice_data.job_no.gross_weight))

    if invoice_data.job_no.module == 'Air Import' or invoice_data.job_no.module == 'Air Export':
        c.drawString(30, 577, 'Flight No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.job_no.flight_no))
    else:
        c.drawString(30, 577, 'Vessel No')
        
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.vessel_voyage_id))
    
    c.drawString(210, 577, 'No of Pkgs:')
    c.drawString(285, 577, str(invoice_data.job_no.no_of_packages+" "+str(invoice_data.job_no.packages_type)))

   

    c.drawString(30, 565, 'Commodity')
    c.drawString(93, 565, ':')
    c.drawString(98, 565, str(invoice_data.job_no.commodity))

    c.line(25, 560, 575, 560)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(26, 548, 'S.No')

    c.line(47, 560, 47, 300)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(85, 548, 'Charges Description')
    c.line(188, 560, 188, 300)
    c.drawString(190, 548, 'SAC')
    c.line(218, 560, 218, 300)
    c.drawString(220, 548, 'Unit')
    c.line(240, 560, 240, 300)
    c.drawString(248, 548, 'Rate')
    c.line(275, 560, 275, 300)
    c.drawString(279, 548, 'Curr.')
    
    c.line(305, 560, 305, 280)
    
    c.drawString(308, 548, 'Ex.Rate')
    c.line(345, 560, 345, 280)
    c.drawString(351, 548, 'Amount')
    c.line(391, 560, 391, 300)
    c.drawString(394, 548, 'IGST')
    c.line(417, 560, 417, 300)
    c.drawString(420, 548, 'CGST')
    c.line(447, 560, 447, 300)
    c.drawString(450, 548, 'SGST')
    c.line(480, 560, 480, 165)
    c.drawString(488, 548, 'Tax Amt')
    c.line(530, 560, 530, 280)
    c.drawString(543, 548, 'Total')
    c.line(25, 540, 575, 540)

    # Assigning Company State GST Code Here
    a = setting.company_gst_code
    
    
    b = str(invoice_data.job_no.account.corp_state.gst_code) # Dynamic GST Code Here for State

    if a == b:
        gstapplied = 1
        divide_total_tax = (float(invoice_data.gst_amount) / 2)
        c.drawString(490, 230, str(divide_total_tax))
        c.drawString(490, 215, str(divide_total_tax))
        c.drawString(490, 200, '0.0')

    else:
        gstapplied = 2
        c.drawString(490, 230, '0.0')
        c.drawString(490, 215, '0.0')
        c.drawString(490, 200, str(invoice_data.gst_amount))





    y = 530
    i = 1
    for row in invoice_heads:
        c.setFont('Helvetica', 7)
        c.drawString(32, y, str(i))
        c.drawString(50, y, str(row.billing_head))
        c.drawString(190, y, str(row.billing_head.hsn_code))
        c.drawString(220, y, str(row.qty_unit))
        c.drawString(246, y, str(row.rate))
        c.drawString(279, y, str(row.currency))
        c.drawString(315, y, str(row.ex_rate))
        c.drawString(348, y, str(row.amount))

        a = setting.company_gst_code
        b = str(invoice_data.job_no.account.corp_state.gst_code) # Dynamic GST Code Here for State


        if a == b:
            gstapplied = 1
            divide_gst = (float(row.gst) / 2)
            if divide_gst != 0:
                c.drawString(420, y, str(divide_gst)+'%')
                c.drawString(450, y, str(divide_gst)+'%')
                c.drawString(397, y, '0.0')
            else:
                c.drawString(420, y, "")
                c.drawString(450, y, "")
                c.drawString(397, y, "")


        else:
            gstapplied = 2
            if row.gst != str(0):
                c.drawString(397, y, str(row.gst)+'%')
            else:
                c.drawString(397, y, "")

        c.drawString(495, y, str(row.gst_amount))
        c.drawString(540, y, str(row.total))

        y = y-10
        i = i+1

    c.line(25, 300, 575, 300)
    c.setFont('Helvetica-Bold', 9)


    c.drawString(30, 290, 'Bank Details')
    c.setFont('Helvetica', 9)
    c.drawString(30, 275, 'A/C NO.')
    c.drawString(89, 275, ':')
    c.drawString(95, 275, str(invoice_data.account_number))

    c.drawString(30, 260, 'Branch Name')
    c.drawString(89, 260, ':')
    branch_nm = str(invoice_data.account_number.branch_name).splitlines()
    y = 260
    i = 0
    for row in branch_nm:
        c.drawString(95, y, branch_nm[i])
        y = y - 15
        i = i + 1
        
    c.drawString(30, 215, 'Beneficiary')
    c.drawString(89, 215, ':')
    c.drawString(95, 215, str(invoice_data.account_number.beneficiary_name))

    c.drawString(30, 200, 'IFSC Code')
    c.drawString(89, 200, ':')
    c.drawString(95, 200, str(invoice_data.account_number.ifsc_code))
    
    c.drawString(30, 185, 'Swift Code')
    c.drawString(89, 185, ':')
    c.drawString(95, 185, str(invoice_data.account_number.swift_code))

    c.setFont('Helvetica-Bold', 9)
    c.line(381, 280, 381, 165)
    c.drawString(308, 287, 'Total')

    c.drawString(385, 245, 'Gross Amount')
    c.drawString(490, 245, str(invoice_data.gross_amount))
    c.drawString(385, 230, 'CGST')
    c.drawString(385, 215, 'SGST')
    c.drawString(385, 200, 'IGST')

    c.drawString(352, 287, str(invoice_data.gross_amount))
    c.drawString(490, 287, str(invoice_data.gst_amount))
    c.drawString(540, 287, str(invoice_data.net_amount))
    c.line(304, 280, 575, 280)

    c.line(381, 185, 575, 185)
    c.drawString(30, 153, 'Amount in Words:')

    a = num2words.num2words(invoice_data.net_amount, lang='en_IN')
    a = a.replace(',','')
    c.setFont('Helvetica', 9)
    c.drawString(110, 153, a.upper() + ' ONLY ')

    c.setFont('Helvetica-Bold', 9)
    c.drawString(385, 172, 'Net Amount')
    c.drawString(490, 172, invoice_data.net_amount)

    c.line(25, 165, 575, 165)

    c.setFont('Helvetica-Bold', 7)
    c.line(25, 140, 575, 140)
    c.drawString(30, 131, "Term and Conditions ")

   
    c.setFont('Helvetica-Bold', 8)
    c.drawString(420, 130, setting.for_company)


    c.setFont('Helvetica-Bold', 5)
    c.drawString(35-3, 120+3, "1.Cargo has not been checked with while issuing this notice. Delivery order will be issued only after cargo is checked/deposited at liner/msil.")
    c.drawString(38-3, 115+3, "Warehouse and RAYZZ GLOBAL LOGISTICS. are not liable for any claim, as a result of delay on part of carriers to check the vessel and issue DO.")
    c.drawString(35-3, 105+3, "2. Please note, once cargo is accepted/delivered, it is deemed to have been accepted in good faith. Any further claim or legal cause will ")
    c.drawString(40-3, 100+3, "not bind 'RAYZZ GLOBAL LOGISTICS' subject to the jurisdiction of the UP Court")
    c.drawString(35-3, 90+3,  "3. Do/Freight payment should be made in advance before D.O. collect/BL issue.")
    c.drawString(35-3, 80+3,  "4. The Cheque/DD should be drawn in favor of ***RAYZZ GLOBAL LOGISTICS *** NEFT/RTGS details given above.")
    c.drawString(35-3, 70+3,  "5. Kindly check all documents details carefully to avoid unnecessary complications.")
    c.drawString(35-3, 60+3,  "6. All cancellation & refunds as per airline/shipping line rules & regulations")
    c.drawString(35-3, 50+3,  "7. This is a computer Generated Invoice, hence no signature required.")
    c.drawString(35-3, 40+3,  "8. All Disputes are subject to UP Jurisdiction.")
    c.drawString(35-3, 30+3,  "9. All bills to be paid on or before due date.")
    c.drawString(35-3, 20+3,  "10. Interest @18% will be charged on delayed payment")
    c.drawString(35-3, 12+3,  "11. E. & O.E.")
    
  
                 


    
    logo = 'media/' +  str(setting.stamp)
    
    c.drawImage(logo, 447, 35, width=1.35 * inch, height=1.20 * inch)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(450, 22, 'Authorised Signatory')
    c.setFont('Helvetica', 8)
    # c.drawString(180, 25, 'This is a Computer generated Invoice and no signature is required')

    c.showPage()
    c.save()
    return response


def debit_note_pdf(request, id):
    invoice_data = DebitNote.objects.filter(id=int(id)).first()
    filename = f'debit_note_{id}.pdf'
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={filename}'
    c = canvas.Canvas(response)

    invoice_heads = DebitNoteDetail.objects.filter(debit_note=invoice_data).order_by('id')
    
    setting = Logistic.objects.filter(id=invoice_data.company_type.id).first()

    # ---------------------------- Outer Border Box -----------------------------------
    c.line(25, 820, 575, 820)
    c.line(25, 10, 575, 10)
    c.line(25, 10, 25, 820)
    c.line(575, 820, 575, 10)

 
    header_image = 'media/' + str(setting.letter_head)

  
    c.drawImage(header_image, 28, 715, width=7.54 * inch, height=1.40 * inch)

    c.setFont('Helvetica-Bold', 9)

    c.line(25, 715, 575, 715)
    c.drawString(30, 705, 'Bill TO:')
    c.drawString(30, 692, str(invoice_data.bill_from))
    c.setFont('Helvetica', 9)
    c.drawString(30, 675, str(invoice_data.bill_from.corp_address_line1))
    c.drawString(30, 663, str(invoice_data.bill_from.corp_address_line2))
    c.drawString(30, 651, str(invoice_data.bill_from.corp_address_line3))
    c.drawString(30, 625, 'State Name :')
    c.drawString(85, 625, str(invoice_data.bill_from.corp_state))
    c.drawString(225, 625, 'Code :')
    c.drawString(255, 625, str(invoice_data.bill_from.corp_state.gst_code))  # Dynamic Code for GST Code of State of selected account party 
    c.line(275, 715, 275, 600)

    c.setFont('Helvetica-Bold', 9)

    c.drawString(280, 704, 'DEBIT NOTE')
    c.drawString(380, 704, invoice_data.debit_note_no)


    c.drawString(520, 704, str(invoice_data.date_of_note))

    c.line(275, 699, 575, 699)
    c.setFont('Helvetica', 9)

    c.drawString(280, 688, 'Shipper')
    c.drawString(345, 688, ':')

   
    c.drawString(360, 688, str(invoice_data.job_no.shipper))

   

    if invoice_data.job_no.module == "Air Export" or invoice_data.job_no.module == "Air Import":
        c.drawString(280, 677, 'AWB No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.awb_no))
        c.drawString(280, 666, 'Docket No')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.docket_no))
    else:
        c.drawString(280, 677, 'Container No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.container_no))
        c.drawString(280, 666, 'Container Type')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.container_type))
    c.drawString(280, 655, 'Consignee')
    c.drawString(345, 655, ':')
    c.drawString(360, 655, str(invoice_data.job_no.consignee))
   

    c.line(275, 628, 575, 628)
    c.setFont('Helvetica-Bold', 9)

    if invoice_data.job_no.module == "Sea Import" or invoice_data.job_no.module == "Sea Export":
        c.drawString(280, 618, 'MBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'HBL No.')
    
    elif invoice_data.job_no.module == "Air Import" or invoice_data.job_no.module == "Air Export":
        c.drawString(280, 618, 'AWMBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'AWHBL No.')
    
    
    c.drawString(345, 606, ':')
    c.setFont('Helvetica', 9)
    c.drawString(360, 618, str(invoice_data.job_no.mbl_no))
    c.drawString(360, 606, str(invoice_data.job_no.hbl_no))



    c.line(25, 620, 275, 620)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, 608, 'GSTIN:')
    c.drawString(93, 608, ':')
    c.drawString(98, 608, str(invoice_data.job_no.account.corp_gstin))
    c.line(25, 600, 575, 600)
    c.setFont('Helvetica', 9)
    c.drawString(30, 590, 'Port of Loading')
    c.drawString(93, 590, ':')
    c.drawString(98, 590, str(invoice_data.job_no.port_of_loading))
    c.drawString(210, 590, 'Final Destination: ')
    c.drawString(285, 590, str(invoice_data.job_no.final_destination))
    c.drawString(210, 565, 'Gross Wt:')
    c.drawString(285, 565, str(invoice_data.job_no.gross_weight))

    if invoice_data.job_no.module == 'Air Import' or invoice_data.job_no.module == 'Air Export':
        c.drawString(30, 577, 'Flight No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.job_no.flight_no))
    else:
        c.drawString(30, 577, 'Vessel No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.vessel_voyage_id))
    
    c.drawString(210, 577, 'No of Pkgs:')
    c.drawString(285, 577, str(invoice_data.job_no.no_of_packages+" "+str(invoice_data.job_no.packages_type)))

   

    c.drawString(30, 565, 'Commodity')
    c.drawString(93, 565, ':')
    c.drawString(98, 565, str(invoice_data.job_no.commodity))

    c.line(25, 560, 575, 560)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(26, 548, 'S.No')

    c.line(47, 560, 47, 300)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(85, 548, 'Charges Description')
    c.line(188, 560, 188, 300)
    c.drawString(190, 548, 'SAC')
    c.line(218, 560, 218, 300)
    c.drawString(220, 548, 'Unit')
    c.line(240, 560, 240, 300)
    c.drawString(248, 548, 'Rate')
    c.line(275, 560, 275, 300)
    c.drawString(279, 548, 'Curr.')
    
    c.line(305, 560, 305, 280)
    
    c.drawString(308, 548, 'Ex.Rate')
    c.line(345, 560, 345, 280)
    c.drawString(351, 548, 'Amount')
    c.line(391, 560, 391, 300)
    c.drawString(394, 548, 'IGST')
    c.line(417, 560, 417, 300)
    c.drawString(420, 548, 'CGST')
    c.line(447, 560, 447, 300)
    c.drawString(450, 548, 'SGST')
    c.line(480, 560, 480, 165)
    c.drawString(488, 548, 'Tax Amt')
    c.line(530, 560, 530, 280)
    c.drawString(543, 548, 'Total')
    c.line(25, 540, 575, 540)

    # Assigning Company State GST Code Here
    a = setting.company_gst_code
    
    
    b = str(invoice_data.job_no.account.corp_state.gst_code) # Dynamic GST Code Here for State

    if a == b:
        gstapplied = 1
        divide_total_tax = (float(invoice_data.gst_amount) / 2)
        c.drawString(490, 230, str(divide_total_tax))
        c.drawString(490, 215, str(divide_total_tax))
        c.drawString(490, 200, '0.0')

    else:
        gstapplied = 2
        c.drawString(490, 230, '0.0')
        c.drawString(490, 215, '0.0')
        c.drawString(490, 200, str(invoice_data.gst_amount))





    y = 530
    i = 1
    for row in invoice_heads:
        c.setFont('Helvetica', 7)
        c.drawString(32, y, str(i))
        c.drawString(50, y, str(row.billing_head))
        c.drawString(190, y, str(row.billing_head.hsn_code))
        c.drawString(220, y, str(row.qty_unit))
        c.drawString(246, y, str(row.rate))
        c.drawString(279, y, str(row.currency))
        c.drawString(315, y, str(row.ex_rate))
        c.drawString(348, y, str(row.amount))

        a = setting.company_gst_code
        b = str(invoice_data.job_no.account.corp_state.gst_code) # Dynamic GST Code Here for State


        if a == b:
            gstapplied = 1
            divide_gst = (float(row.gst) / 2)
            if divide_gst != 0:
                c.drawString(420, y, str(divide_gst)+'%')
                c.drawString(450, y, str(divide_gst)+'%')
                c.drawString(397, y, '0.0')
            else:
                c.drawString(420, y, "")
                c.drawString(450, y, "")
                c.drawString(397, y, "")


        else:
            gstapplied = 2
            if row.gst != str(0):
                c.drawString(397, y, str(row.gst)+'%')
            else:
                c.drawString(397, y, "")

        c.drawString(495, y, str(row.gst_amount))
        c.drawString(540, y, str(row.total))

        y = y-10
        i = i+1

    c.line(25, 300, 575, 300)
    c.setFont('Helvetica-Bold', 9)


    c.drawString(30, 290, 'Bank Details')
    c.setFont('Helvetica', 9)
    c.drawString(30, 275, 'A/C NO.')
    c.drawString(89, 275, ':')
    c.drawString(95, 275, str(invoice_data.account_number))

    c.drawString(30, 260, 'Branch Name')
    c.drawString(89, 260, ':')
    branch_nm = str(invoice_data.account_number.branch_name).splitlines()
    y = 260
    i = 0
    for row in branch_nm:
        c.drawString(95, y, branch_nm[i])
        y = y - 15
        i = i + 1
        
    c.drawString(30, 215, 'Beneficiary')
    c.drawString(89, 215, ':')
    c.drawString(95, 215, str(invoice_data.account_number.beneficiary_name))

    c.drawString(30, 200, 'IFSC Code')
    c.drawString(89, 200, ':')
    c.drawString(95, 200, str(invoice_data.account_number.ifsc_code))
    
    c.drawString(30, 185, 'Swift Code')
    c.drawString(89, 185, ':')
    c.drawString(95, 185, str(invoice_data.account_number.swift_code))

    c.setFont('Helvetica-Bold', 9)
    c.line(381, 280, 381, 165)
    c.drawString(308, 287, 'Total')

    c.drawString(385, 245, 'Gross Amount')
    c.drawString(490, 245, str(invoice_data.gross_amount))
    c.drawString(385, 230, 'CGST')
    c.drawString(385, 215, 'SGST')
    c.drawString(385, 200, 'IGST')

    c.drawString(352, 287, str(invoice_data.gross_amount))
    c.drawString(490, 287, str(invoice_data.gst_amount))
    c.drawString(540, 287, str(invoice_data.net_amount))
    c.line(304, 280, 575, 280)

    c.line(381, 185, 575, 185)
    c.drawString(30, 153, 'Amount in Words:')

    a = num2words.num2words(invoice_data.net_amount, lang='en_IN')
    a = a.replace(',','')
    c.setFont('Helvetica', 9)
    c.drawString(110, 153, a.upper() + ' ONLY ')

    c.setFont('Helvetica-Bold', 9)
    c.drawString(385, 172, 'Net Amount')
    c.drawString(490, 172, invoice_data.net_amount)

    c.line(25, 165, 575, 165)

    c.setFont('Helvetica-Bold', 7)
    c.line(25, 140, 575, 140)
    c.drawString(30, 131, "Term and Conditions ")

   
    c.setFont('Helvetica-Bold', 8)
    c.drawString(420, 130, setting.for_company)


    c.setFont('Helvetica-Bold', 5)
    c.drawString(35-3, 120+3, "1.Cargo has not been checked with while issuing this notice. Delivery order will be issued only after cargo is checked/deposited at liner/msil.")
    c.drawString(38-3, 115+3, "Warehouse and RAYZZ GLOBAL LOGISTICS. are not liable for any claim, as a result of delay on part of carriers to check the vessel and issue DO.")
    c.drawString(35-3, 105+3, "2. Please note, once cargo is accepted/delivered, it is deemed to have been accepted in good faith. Any further claim or legal cause will ")
    c.drawString(40-3, 100+3, "not bind 'RAYZZ GLOBAL LOGISTICS' subject to the jurisdiction of the UP Court")
    c.drawString(35-3, 90+3,  "3. Do/Freight payment should be made in advance before D.O. collect/BL issue.")
    c.drawString(35-3, 80+3,  "4. The Cheque/DD should be drawn in favor of ***RAYZZ GLOBAL LOGISTICS *** NEFT/RTGS details given above.")
    c.drawString(35-3, 70+3,  "5. Kindly check all documents details carefully to avoid unnecessary complications.")
    c.drawString(35-3, 60+3,  "6. All cancellation & refunds as per airline/shipping line rules & regulations")
    c.drawString(35-3, 50+3,  "7. This is a computer Generated Invoice, hence no signature required.")
    c.drawString(35-3, 40+3,  "8. All Disputes are subject to UP Jurisdiction.")
    c.drawString(35-3, 30+3,  "9. All bills to be paid on or before due date.")
    c.drawString(35-3, 20+3,  "10. Interest @18% will be charged on delayed payment")
    c.drawString(35-3, 12+3,  "11. E. & O.E.")
    
  
                 


    
    logo = 'media/' +  str(setting.stamp)
    
    c.drawImage(logo, 447, 35, width=1.35 * inch, height=1.20 * inch)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(450, 22, 'Authorised Signatory')
    c.setFont('Helvetica', 8)
    # c.drawString(180, 25, 'This is a Computer generated Invoice and no signature is required')

    c.showPage()
    c.save()
    return response

def invoice_payable_pdf(request, id):
    invoice_data = InvoicePayable.objects.filter(id=int(id)).first()
    filename = f'invoice_payable_{id}.pdf'
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={filename}'
    c = canvas.Canvas(response)

    invoice_heads = InvoicePayableDetail.objects.filter(invoice_payable=invoice_data).order_by('id')
    setting = Logistic.objects.filter(id=invoice_data.company_type.id).first()

    # ---------------------------- Outer Border Box -----------------------------------
    c.line(25, 820, 575, 820)
    c.line(25, 10, 575, 10)
    c.line(25, 10, 25, 820)
    c.line(575, 820, 575, 10)

    
 
    header_image = 'media/' + str(setting.letter_head)

  
    c.drawImage(header_image, 28, 715, width=7.54 * inch, height=1.40 * inch)

    c.setFont('Helvetica-Bold', 9)

    c.line(25, 715, 575, 715)
    c.drawString(30, 705, 'Bill From:')
    c.drawString(30, 692, str(invoice_data.bill_from))
    c.setFont('Helvetica', 9)
    c.drawString(30, 675, str(invoice_data.bill_from.corp_address_line1))
    c.drawString(30, 663, str(invoice_data.bill_from.corp_address_line2))
    c.drawString(30, 651, str(invoice_data.bill_from.corp_address_line3))
    c.drawString(30, 625, 'State Name :')
    c.drawString(85, 625, str(invoice_data.bill_from.corp_state))
    c.drawString(225, 625, 'Code :')
    c.drawString(255, 625, str(invoice_data.job_no.account.corp_state.gst_code))  # Dynamic Code for GST Code of State of selected account party 
    c.line(275, 715, 275, 600)

    c.setFont('Helvetica-Bold', 9)

    c.drawString(280, 704, 'TAX INVOICE')
    c.drawString(380, 704, invoice_data.invoice_no)


    c.drawString(520, 704, str(invoice_data.date_of_invoice))

    c.line(275, 699, 575, 699)
    c.setFont('Helvetica', 9)

    c.drawString(280, 688, 'Shipper')
    c.drawString(345, 688, ':')

   
    c.drawString(360, 688, str(invoice_data.job_no.shipper))

   

    if invoice_data.job_no.module == "Air Export" or invoice_data.job_no.module == "Air Import":
        c.drawString(280, 677, 'AWB No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.job_no.awb_no))
        c.drawString(280, 666, 'Docket No')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.job_no.docket_no))
    else:
        c.drawString(280, 677, 'Container No')
        c.drawString(345, 677, ':')
        c.drawString(360, 677, str(invoice_data.job_no.container_no))
        c.drawString(280, 666, 'Container Type')
        c.drawString(345, 666, ':')
        c.drawString(360, 666, str(invoice_data.job_no.container_type))
    c.drawString(280, 655, 'Consignee')
    c.drawString(345, 655, ':')
    c.drawString(360, 655, str(invoice_data.job_no.consignee))
    # c.drawString(280, 644, 'Notify Party')
    # c.drawString(345, 644, ':')
    # c.drawString(360, 644, str(invoice_data.job_no.))
    # c.drawString(280, 633, 'Job No')
    # c.drawString(345, 633, ':')
    # c.drawString(360, 633, str(invoice_data.job_no))

    c.line(275, 628, 575, 628)
    c.setFont('Helvetica-Bold', 9)

    if invoice_data.job_no.module == "Sea Import" or invoice_data.job_no.module == "Sea Export":
        c.drawString(280, 618, 'MBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'HBL No.')
    
    elif invoice_data.job_no.module == "Air Import" or invoice_data.job_no.module == "Air Export":
        c.drawString(280, 618, 'AWMBL No.')
        c.drawString(345, 618, ':')
        c.drawString(280, 606, 'AWHBL No.')
    
    
    c.drawString(345, 606, ':')
    c.setFont('Helvetica', 9)
    c.drawString(360, 618, str(invoice_data.job_no.mbl_no))
    c.drawString(360, 606, str(invoice_data.job_no.hbl_no))



    c.line(25, 620, 275, 620)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, 608, 'GSTIN:')
    c.drawString(93, 608, ':')
    c.drawString(98, 608, str(invoice_data.job_no.account.corp_gstin))
    c.line(25, 600, 575, 600)
    c.setFont('Helvetica', 9)
    c.drawString(30, 590, 'Port of Loading')
    c.drawString(93, 590, ':')
    c.drawString(98, 590, str(invoice_data.job_no.port_of_loading))
    c.drawString(210, 590, 'Final Destination: ')
    c.drawString(285, 590, str(invoice_data.job_no.final_destination))
    c.drawString(210, 565, 'Gross Wt:')
    c.drawString(285, 565, str(invoice_data.job_no.gross_weight))

    if invoice_data.job_no.module == 'Air Import' or invoice_data.job_no.module == 'Air Export':
        c.drawString(30, 577, 'Flight No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.job_no.flight_no))
    else:
        c.drawString(30, 577, 'Vessel No')
        c.drawString(93, 577, ':')
        c.drawString(98, 577, str(invoice_data.vessel_voyage_id))
    
    c.drawString(210, 577, 'No of Pkgs:')
    c.drawString(285, 577, str(invoice_data.job_no.no_of_packages+" "+str(invoice_data.job_no.packages_type)))

   

    c.drawString(30, 565, 'Commodity')
    c.drawString(93, 565, ':')
    c.drawString(98, 565, str(invoice_data.job_no.commodity))

    c.line(25, 560, 575, 560)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(26, 548, 'S.No')

    c.line(47, 560, 47, 300)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(85, 548, 'Charges Description')
    c.line(188, 560, 188, 300)
    c.drawString(190, 548, 'SAC')
    c.line(218, 560, 218, 300)
    c.drawString(220, 548, 'Unit')
    c.line(240, 560, 240, 300)
    c.drawString(248, 548, 'Rate')
    c.line(275, 560, 275, 300)
    c.drawString(279, 548, 'Curr.')
    
    c.line(305, 560, 305, 280)
    
    c.drawString(308, 548, 'Ex.Rate')
    c.line(345, 560, 345, 280)
    c.drawString(351, 548, 'Amount')
    c.line(391, 560, 391, 300)
    c.drawString(394, 548, 'IGST')
    c.line(417, 560, 417, 300)
    c.drawString(420, 548, 'CGST')
    c.line(447, 560, 447, 300)
    c.drawString(450, 548, 'SGST')
    c.line(480, 560, 480, 165)
    c.drawString(488, 548, 'Tax Amt')
    c.line(530, 560, 530, 280)
    c.drawString(543, 548, 'Total')
    c.line(25, 540, 575, 540)

    # Assigning Company State GST Code Here
    a = setting.company_gst_code
    
    
    b = str(invoice_data.job_no.account.corp_state.gst_code) # Dynamic GST Code Here for State

    if a == b:
        gstapplied = 1
        divide_total_tax = (float(invoice_data.gst_amount) / 2)
        c.drawString(490, 230, str(divide_total_tax))
        c.drawString(490, 215, str(divide_total_tax))
        c.drawString(490, 200, '0.0')

    else:
        gstapplied = 2
        c.drawString(490, 230, '0.0')
        c.drawString(490, 215, '0.0')
        c.drawString(490, 200, str(invoice_data.gst_amount))





    y = 530
    i = 1
    for row in invoice_heads:
        c.setFont('Helvetica', 7)
        c.drawString(32, y, str(i))
        c.drawString(50, y, str(row.billing_head))
        c.drawString(190, y, str(row.billing_head.hsn_code))
        c.drawString(220, y, str(row.qty_unit))
        c.drawString(246, y, str(row.rate))
        c.drawString(279, y, str(row.currency))
        c.drawString(315, y, str(row.ex_rate))
        c.drawString(348, y, str(row.amount))

       
        a = setting.company_gst_code
        b = str(invoice_data.job_no.account.corp_state.gst_code)

        if a == b:
            gstapplied = 1
            divide_gst = (float(row.gst) / 2)
            if divide_gst != 0:
                c.drawString(420, y, str(divide_gst)+'%')
                c.drawString(450, y, str(divide_gst)+'%')
                c.drawString(397, y, '0.0')
            else:
                c.drawString(420, y, "")
                c.drawString(450, y, "")
                c.drawString(397, y, "")


        else:
            gstapplied = 2
            if row.gst != str(0):
                c.drawString(397, y, str(row.gst)+'%')
            else:
                c.drawString(397, y, "")

        c.drawString(495, y, str(row.gst_amount))
        c.drawString(540, y, str(row.total))

        y = y-10
        i = i+1

    c.line(25, 300, 575, 300)
    c.setFont('Helvetica-Bold', 9)


    c.drawString(30, 290, 'Bank Details')
    c.setFont('Helvetica', 9)
    c.drawString(30, 275, 'A/C NO.')
    c.drawString(89, 275, ':')
    c.drawString(95, 275, str(invoice_data.account_number))

    c.drawString(30, 260, 'Branch Name')
    c.drawString(89, 260, ':')
    branch_nm = str(invoice_data.account_number.branch_name).splitlines()
    y = 260
    i = 0
    for row in branch_nm:
        c.drawString(95, y, branch_nm[i])
        y = y - 15
        i = i + 1
        
    c.drawString(30, 215, 'Beneficiary')
    c.drawString(89, 215, ':')
    c.drawString(95, 215, str(invoice_data.account_number.beneficiary_name))

    c.drawString(30, 200, 'IFSC Code')
    c.drawString(89, 200, ':')
    c.drawString(95, 200, str(invoice_data.account_number.ifsc_code))
    
    c.drawString(30, 185, 'Swift Code')
    c.drawString(89, 185, ':')
    c.drawString(95, 185, str(invoice_data.account_number.swift_code))

    c.setFont('Helvetica-Bold', 9)
    c.line(381, 280, 381, 165)
    c.drawString(308, 287, 'Total')

    c.drawString(385, 245, 'Gross Amount')
    c.drawString(490, 245, str(invoice_data.gross_amount))
    c.drawString(385, 230, 'CGST')
    c.drawString(385, 215, 'SGST')
    c.drawString(385, 200, 'IGST')

    c.drawString(352, 287, str(invoice_data.gross_amount))
    c.drawString(490, 287, str(invoice_data.gst_amount))
    c.drawString(540, 287, str(invoice_data.net_amount))
    c.line(304, 280, 575, 280)

    c.line(381, 185, 575, 185)
    c.drawString(30, 153, 'Amount in Words:')

    a = num2words.num2words(invoice_data.net_amount, lang='en_IN')
    a = a.replace(',','')
    c.setFont('Helvetica', 9)
    c.drawString(110, 153, a.upper() + ' ONLY ')

    c.setFont('Helvetica-Bold', 9)
    c.drawString(385, 172, 'Net Amount')
    c.drawString(490, 172, invoice_data.net_amount)

    c.line(25, 165, 575, 165)

    c.setFont('Helvetica-Bold', 7)
    c.line(25, 140, 575, 140)
    c.drawString(30, 131, "Term and Conditions ")

   
    c.setFont('Helvetica-Bold', 8)
    c.drawString(420, 130, setting.for_company)


    c.setFont('Helvetica-Bold', 5)
    c.drawString(35-3, 120+3, "1.Cargo has not been checked with while issuing this notice. Delivery order will be issued only after cargo is checked/deposited at liner/msil.")
    c.drawString(38-3, 115+3, "Warehouse and RAYZZ GLOBAL LOGISTICS. are not liable for any claim, as a result of delay on part of carriers to check the vessel and issue DO.")
    c.drawString(35-3, 105+3, "2. Please note, once cargo is accepted/delivered, it is deemed to have been accepted in good faith. Any further claim or legal cause will ")
    c.drawString(40-3, 100+3, "not bind 'RAYZZ GLOBAL LOGISTICS' subject to the jurisdiction of the UP Court")
    c.drawString(35-3, 90+3,  "3. Do/Freight payment should be made in advance before D.O. collect/BL issue.")
    c.drawString(35-3, 80+3,  "4. The Cheque/DD should be drawn in favor of ***RAYZZ GLOBAL LOGISTICS *** NEFT/RTGS details given above.")
    c.drawString(35-3, 70+3,  "5. Kindly check all documents details carefully to avoid unnecessary complications.")
    c.drawString(35-3, 60+3,  "6. All cancellation & refunds as per airline/shipping line rules & regulations")
    c.drawString(35-3, 50+3,  "7. This is a computer Generated Invoice, hence no signature required.")
    c.drawString(35-3, 40+3,  "8. All Disputes are subject to UP Jurisdiction.")
    c.drawString(35-3, 30+3,  "9. All bills to be paid on or before due date.")
    c.drawString(35-3, 20+3,  "10. Interest @18% will be charged on delayed payment")
    c.drawString(35-3, 12+3,  "11. E. & O.E.")
    
  
                 


    
    logo = 'media/' +  str(setting.stamp)
    
    c.drawImage(logo, 447, 35, width=1.35 * inch, height=1.20 * inch)

    c.setFont('Helvetica-Bold', 9)
    c.drawString(450, 22, 'Authorised Signatory')
    c.setFont('Helvetica', 8)
    # c.drawString(180, 25, 'This is a Computer generated Invoice and no signature is required')

    c.showPage()
    c.save()
    return response



