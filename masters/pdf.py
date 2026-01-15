from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.units import inch
from django.contrib.sites.models import Site
from masters.models import DSR, MBLMaster, VGMMaster, GRMaster,CargoArrivalNotice
from dashboard.models import Logistic
from reportlab.graphics import shapes
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import ParagraphStyle
from datetime import datetime

# DSR

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def dsr_pdf(request, id):
    setting = Logistic.objects.first()

    response = HttpResponse(content_type='application/pdf')
    filename = f'dsr_{id}.pdf'
    response['Content-Disposition'] = f'filename={filename}'
    c = canvas.Canvas(response)

    # _______________________ get object ___________________

    dsr_detail = DSR.objects.filter(id=int(id)).first()


    
    logo = 'media/' + str(setting.letter_head)
    c.drawImage(logo, 29, 720, width=7.51 * inch, height=1.40 * inch)

    c.line(50, 680, 550, 680)

    c.setFont('Helvetica-Bold', 13)
    c.drawString(280, 650, 'DSR')
    c.line(280, 647, 307, 647)

    c.setFont('Helvetica', 11)
    c.drawString(50, 600, 'Job No')
    c.drawString(100, 600, ':-')
    c.drawString(110, 600, str(dsr_detail.job))
    c.drawString(50, 570, 'HBL Date')
    c.drawString(100, 570, ':-')
    c.drawString(110, 570, str(dsr_detail.job.hbl_date))

    c.drawString(50, 540, 'POL')
    c.drawString(100, 540, ':-')
    c.drawString(110, 540, str(dsr_detail.job.port_of_loading))
    c.drawString(50, 510, 'POD')
    c.drawString(100, 510, ':-')
    c.drawString(110, 510, str(dsr_detail.job.port_of_discharge))
    c.drawString(50, 480, 'MODE')
    c.drawString(100, 480, ':-')
    c.drawString(110, 480, str(dsr_detail.dsr_mode))
    c.drawString(50, 450, 'CNEE')
    c.drawString(100, 450, ':-')
    c.drawString(110, 450, str(dsr_detail.cnee))
    c.drawString(50, 420, 'Shipper')
    c.drawString(100, 420, ':-')
    c.drawString(110, 420, str(dsr_detail.job.shipper))
    c.drawString(50, 390, 'Equip:')
    c.drawString(100, 390, ':-:')
    c.drawString(110, 390, str(dsr_detail.equip))
    c.drawString(50, 360, 'S/L')
    c.drawString(100, 360, ':-')
    c.drawString(110, 360, str(dsr_detail.shipping_line))

    c.drawString(310, 600, 'F.POD')
    c.drawString(365, 600, ':-')
    c.drawString(375, 600, str(dsr_detail.fpod))

    c.drawString(310, 570, 'HBL No')
    c.drawString(365, 570, ':-')
    c.drawString(375, 570, str(dsr_detail.job.hbl_no))

    c.drawString(310, 540, 'MBL No')
    c.drawString(365, 540, ':-')
    c.drawString(375, 540, str(dsr_detail.job.mbl_no))

    c.drawString(310, 510, 'Cont No')
    c.drawString(365, 510, ':-')
    c.drawString(375, 510, str(dsr_detail.container_no))

    c.drawString(310, 480, 'VSL / VOY')
    c.drawString(365, 480, ':-')
    c.drawString(375, 480, str(dsr_detail.vessel_voyage))

    c.drawString(310, 450, 'Status')
    c.drawString(365, 450, ':-')
    c.drawString(375, 450, str(dsr_detail.status))

    c.drawString(310, 420, 'B/L')
    c.drawString(365, 420, ':-')
    c.drawString(375, 420, str(dsr_detail.bl))

    c.drawString(310, 390, 'Sales')
    c.drawString(365, 390, ':-')
    c.drawString(375, 390, str(dsr_detail.sales))


    c.showPage()
    c.save()
    return response


def vgm_pdf(request, id):
    vgm = VGMMaster.objects.get(id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="vgm.pdf"'
    c = canvas.Canvas(response)

    c.setFont('Helvetica-Bold', 8)
   
    c.line(13, 720, 13, 395)
    c.line(60, 720, 60, 395)
    c.line(390, 720, 390, 395)
    c.line(585, 720, 585, 395)

    c.drawString(13,785,"INFORMATION ABOUT VERIFIED GROSS")
    c.line(13, 782, 180, 782)
    
    c.drawString(500,785,"Annex - 1")
    c.line(500, 782, 537, 782)
    
    c.drawString(13,730,"MASS OF CONTAINER")
    c.line(13, 728, 100, 728)
    
    # For Table
    c.line(13, 720, 585, 720)
    
    c.drawString(16,705,"Sr. No.")
    
    c.drawString(150,705,"Details of Information")
    c.drawString(400,705,"Particulars")
    
    c.line(13, 700, 585, 700)
   
    # Row 1
    c.line(13, 680, 585, 680)
    
    c.drawString(16,685,"1.")
    
    c.drawString(70,685,"Name of the shipper")
    c.drawString(400,685,f"{vgm.shipper}")
    
    c.line(13, 660, 585, 660)
    
    # Row 2
    c.line(13, 625, 585, 625)
    
    c.drawString(16,665,"2.")
    
    c.drawString(70,665,"Shipper Registration/Licence No. (IEC No/CIN No)**")
    c.drawString(400,665,f"{vgm.shipper_licence_no}")
    
    
    c.line(13, 605, 585, 605)
    
    # Row 3
    c.line(13, 585, 585, 585)
    
    
    c.line(13, 565, 585, 565)
    
    
    c.drawString(16,645,"3.")
    
    c.drawString(70,645,"Name and Designation of the official of the shipper")
    c.drawString(70,635,"authorised to sign document")
    c.drawString(400,645,f"{vgm.auth_shipper_name}")
    c.drawString(400,635,f"{vgm.auth_shipper_designation}")
    
    # Row 4
    c.line(13, 545, 585, 545)
    
    
    c.line(13, 525, 585, 525)
    
    
    c.drawString(16,610,"4.")
    
    c.drawString(70,610,"24x7 contact details of authorised official of shipper")
   
   
    c.drawString(400,610,f"{vgm.shipper_contact}")
    
    # Row 5
    c.line(13, 525, 585, 525)
    
    
    c.line(13, 505, 585, 505)
    
    
    c.drawString(16,590,"5.")
    
    c.drawString(70,590,"Booking No./Container No.")
   
   
    c.drawString(400,590,f"{vgm.booking_cont_no}")
    
    # Row 6
    c.line(13, 505, 585, 505)
    
    
    c.line(13, 485, 585, 485)
    
    
    c.drawString(16,570,"6.")
    
    c.drawString(70,570,"Container Size (TEU/FEU/Other)")
   
   
    c.drawString(400,570,f"{vgm.container_size}")
    
    # Row 7
    c.line(13, 485, 585, 485)
    
    

    
    
    c.drawString(16,550,"7.")
    
    c.drawString(70,550,"Maximum permissible weight of container as per CSS plate")
   
   
    c.drawString(400,550,f"{vgm.max_permissible_weight} KGS.")
    
    # Row 8
   
    
    c.line(13, 440, 585, 440)
    
    
    c.drawString(16,530,"8.")
    
    c.drawString(70,530,"Verified gross mass of container (method-1/method-2)")
   
   
    c.drawString(400,530,f"{vgm.verified_gross_mass}")
    
    
    # Row 9

    
    
    c.line(13, 415, 585, 415)
    c.line(13, 395, 585, 395)
    
    
    c.drawString(16,510,"9.")
    c.drawString(70,510,"Date and time of weighing")
    c.drawString(400,510,f"{vgm.date_of_weighing} {vgm.time_of_weighing}")
    
    
    
    
    c.drawString(16,490,"10.")
    c.drawString(70,490,"Weighing slip no.")
    c.drawString(400,490,f"{vgm.weighing_slip_no}")
    
    
    c.drawString(16,470,"11.")
    
    c.drawString(70,470,"Weighbridge registration no. & Address of Weighbridge")
   
   
    c.drawString(400,470,f"{vgm.weighbridge_register_no}")
    c.drawString(400,460,f"{vgm.weighbridge_address}")
    
    
    c.drawString(16,420,"12.")
    
    c.drawString(70,420,"Type (Normal/Reefer/Hazardous/others)")
   
   
    c.drawString(400,420,f"{vgm.vgm_type}")
    
    
    c.drawString(16,400,"13.")
    
    c.drawString(70,400,"If Hazardous, UN No, IMDG class")
   
   
    c.drawString(400,400,f"{vgm.vgm_class}")
    
  
    
    c.drawString(400,365,"Signature  of authorised person of shipper")
    c.drawString(400,350,f"Name:- {vgm.company_type.vgm_authorized_shipper}")
 
    
  
    
    c.showPage()
    c.save()
    return response



def AWB_pdf(request,id):
    
    air_mbl = MBLMaster.objects.filter(id=id).first()
    domain = Site.objects.get_current().domain
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="local_invoice.pdf"'

    if air_mbl.type == "HBL":
        copies = ['ORIGINAL 2 (FOR CONSIGNEE)','ORIGINAL 3 (FOR SHIPPER)','COPY 4 (DELIVERY RECEIPT)','COPY 5 (FOR DESTINATION)','COPY 9 (FOR AGENT)','COPY 10 (EXTRA COPY FOR CARRIER)','COPY 11 (EXTRA COPY FOR CARRIER)']
    else:
        copies = ['ORIGINAL 1 (FOR CARRIER)','ORIGINAL 2 (FOR CONSIGNEE)','ORIGINAL 3 (FOR SHIPPER)','COPY 4 (DELIVERY RECEIPT)','COPY 5 (FOR AIRPORT OF DESTINATION)','COPY 6 (FOR THIRD CARRIER)','COPY 7 (FOR SECOND CARRIER)','COPY 9 (FOR AGENT)','COPY 10 (EXTRA COPY FOR CARRIER)','COPY 11 (EXTRA COPY FOR CARRIER)']

    c = canvas.Canvas(response)
    for copy in copies:

        c.line(12,834, 12,10)                               #left first up to down
        c.line(577,818,577,10)                              #right last up to down
        c.line(12, 10, 577, 10)                             #last bottom line
        c.line(12,834,298,834)                              #upper first half line
        c.line(12,458,577,458)                              #mid upper half
        c.line(12,500,577,500)                              #line above handling information
        c.line(298,834,298,500)                             #half line top to line above handling info
        c.line(12,818,577,818)                              #second left to right full line 
        if air_mbl.type == "HBL":
            c.line(155,802,577,802)                             #shipper account number
        else:
            c.line(155,802,298,802)                             #shipper account number
        
        c.line(155,802,155,818)
        c.line(12,550,577,550)                              #mid table upper line
        c.line(12,525,577,525)
        c.line(40,550,40,525)
        c.line(190,550,190,525)
        c.line(220,550,220,525)
        c.line(275,550,275,525)
        c.line(40,537,190,537)
        c.line(115,537,115,550)

        c.line(155,745,155,728)
        c.line(155,728,298,728)

        c.line(330,525,330,550)                             #these are the lines in the to by column
        c.line(360,525,360,550)
        c.line(405,525,405,550)
        c.line(451,525,451,550)
        c.line(514,525,514,550)

        c.line(360,542,451,542)
        c.line(360,534,451,534)

        c.line(383,525,383,542)
        c.line(428,525,428,542)

        c.line(13,250,577,250)                              #horizontal table bottom line
        c.line(130,500,130,525)
        c.line(165,513,255,513)
        c.line(165,513,165,525)
        c.line(255,513,255,525)
        c.line(380,500,380,525)
        c.line(210,500,210,513)

        c.line(298,660,577,660)
        c.line(298,590,577,590)

        c.line(12,745,298,745)
        c.line(12,675,298,675)
        c.line(12,630,298,630)
        c.line(12,590,298,590)
        c.line(155,630,155,590)

        #3rd section lines
        #right portion
        c.line(230,10,230,250)                                  #mid standing line
        c.line(230,170,577,170)
        c.line(230,60,577,60)
        #left portion
        c.line(12,38,335,38)
        c.line(335,38,335,10)

        c.line(12,63,230,63)
        c.line(12,88,230,88)
        c.line(12,113,230,113)
        c.line(12,138,230,138)
        c.line(12,163,230,163)
        c.line(12,190,230,190)
        c.line(12,220,230,220)

        c.line(31,236,71,236)
        c.line(31,236,31,250)
        c.line(71,236,71,250)

        c.line(92,236,150,236)
        c.line(92,236,92,250)
        c.line(150,236,150,250)

        c.line(171,236,211,236)
        c.line(171,236,171,250)
        c.line(211,236,211,250)

        c.line(84,206,158,206)
        c.line(84,206,84,220)
        c.line(158,206,158,220)
        
        c.line(99,176,143,176)
        c.line(99,176,99,190)
        c.line(143,176,143,190)

        c.line(69,151,173,151)
        c.line(69,151,69,163)
        c.line(173,151,173,163)

        c.line(66,126,176,126)
        c.line(66,126,66,138)
        c.line(176,126,176,138)

        c.line(27,76,106,76)
        c.line(27,76,27,88)
        c.line(106,76,106,88)

        c.line(136,76,215,76)
        c.line(136,76,136,88)
        c.line(215,76,215,88)

        c.line(17,51,116,51)
        c.line(17,51,17,63)
        c.line(116,63,116,51)

        c.line(126,51,225,51)
        c.line(126,51,126,63)
        c.line(225,51,225,63)

        c.line(126,25,225,25)
        c.line(126,25,126,38)
        c.line(225,25,225,38)

        c.line(121,126,121,10)            #reference line
        c.line(121,138,121,151)
        c.line(121,176,121,163)
        c.line(121,190,121,206)
        c.line(121,236,121,220)



        #middle table all lines
        # -------------------------
        c.line(12,430,577,430)
        c.line(124,447,174,447)
        c.line(12,273,98,273)
        c.line(331,273,405,273)
        #|||||||
        c.line(48,250,48,458)
        c.line(98,250,98,458)
        c.line(110,250,110,458)
        c.line(116,250,116,458)
        c.line(124,250,124,447)
        c.line(174,250,174,458)
        c.line(181,250,181,458)
        c.line(249,250,249,458)
        c.line(255,250,255,458)
        c.line(325,250,325,458)
        c.line(331,250,331,458)
        c.line(405,250,405,458)
        c.line(411,250,411,458)

        if air_mbl.type == 'HBL':
            try:
                logo = f'{air_mbl.company_type.letter_head.url}' 
                c.drawImage(logo, 300, 670, width=3.7 * inch, height=1.3 * inch)
            except:
                pass

        if air_mbl.type == 'MBL':
            try:
                c.setFont('Helvetica-Bold', 9)
                c.drawString(306,773, f'{air_mbl.airline.name}')

                c.setFont('Helvetica', 8)
                j=760
                for i in air_mbl.airline_address.splitlines():
                    c.drawString(306,j,i)
                    j -= 9
            except:
                pass


        c.setFont('Helvetica-Bold', 9)
        if air_mbl.type == "HBL":
            c.drawString(15,822, 'HOUSE AIRWAY BILL NO:')
        else:
            c.drawString(15,822, 'MASTER AIRWAY BILL NO:')

        c.drawString(350,822, copy)

        if air_mbl.type == "HBL":
            c.drawString(306,807,"MASTER AIRWAYBILL NO:")

        c.setFont('Helvetica', 9)
        c.drawString(15,808,"Shipper's Name & Address")
        c.drawString(15,736,"Consignee's Name & Address")
        c.setFont('Helvetica', 7.7)
        c.drawString(175,810,"Shipper's Account Number")
        c.drawString(175,737,"Consignee's Account Number")
        c.setFont('Helvetica-Bold', 8)
        c.drawString(306,793,"Issued By")
        c.setFont('Helvetica-Bold', 11)
        
        c.setFont('Helvetica-Bold', 7)
        # c.drawString(302,695,"PLOT NO. 18, D-50, AASHRAY APARTMENTS, DILSHAD COLONY (EAST), NEW")
        # c.drawString(302,684,"DELHI- 110095 (INDIA)")
        # c.drawString(302,674,"TEL: +91 11 49878387 E-Mail: heera@dtriumphlogistics.com Web:")
        # c.drawString(302,665,"www.dtriumphlogistics.com GSTIN: 07AAICD7487K1ZZ PAN: AAICD7487K")
        c.setFont('Helvetica', 6.5)
        c.drawString(300,654,"It is agreed that the goods described herein are accepted in apparent good order and condition")
        c.setFont('Helvetica', 6.6)
        c.drawString(300,646,"(except as noted) for carriage SUBJECT TO THE CONDITIONS OF CONTRACT ON THE")
        c.drawString(300,638,"REVERSE HEREOF. ALL GOODS MAYBE CARRIED BY ANY OTHER MEANS INCLUDING")
        c.drawString(300,630,"ROAD OR ANY OTHER CARRIER UNLESS SPECIFIC CONTRARY INSTRUCTIONS ARE")
        c.drawString(300,622,"GIVEN HEREON BY THE SHIPPER, AND SHIPPER AGREES THAT THE SHIPMENT MAY")
        c.drawString(300,614,"BE CARRIED VIA INTERMEDIATE STOPPING PLACES WHICH THE CARRIER DEEMS")
        c.drawString(300,606,"APPROPRIATE.THE SHIPPERS ATTENTION IS DRAWN TO THE NOTICE CONCERNING")
        c.drawString(300,599,"CARRIER'S LIMITATION OF LIABILITY. Shipper may increase such limitation of liability by")
        c.drawString(300,592,"declaring a higher value for carriage and paying a supplemental charge if required.")
        c.setFont('Helvetica', 6.8)
        c.drawString(17,667,"Issuing Carrier's Agents Name & City")
        c.setFont('Helvetica', 9)
        # c.drawString(17,650,"DTRIUMPH LOGISTICS INDIA PRIVATE LIMITED")
        c.setFont('Helvetica', 8)
        c.drawString(17,621,"Agent's IATA Code ")
        c.drawString(165,621,"Account No")
        c.drawString(17,580,"Airport of Departure (Addr. of First Carrier) and Requested Routing")
        c.drawString(302,580,"Accounting Information:")
        # c.drawString(365,563,"******FREIGHT PREPAID******")
        c.setFont('Helvetica', 9)
        # c.drawString(20,563,"NEW DELHI")
        c.setFont('Helvetica', 7)
        c.drawString(15,542,"To")
        c.drawString(194,542,"To")
        c.drawString(225,542,"By")
        c.drawString(262,542,"To")
        c.drawString(282,542,"By")
        c.setFont('Helvetica', 5.9)
        c.drawString(52,542,"By First Carrier")
        c.drawString(119,542,"Routing and Destination")
        c.setFont('Helvetica', 6.6)
        c.drawString(382,517,"INSURANCE - If Carrier offers insurance, and such insurance")
        c.drawString(382,509,"is requested in accordance with the conditions thereof, indicate")
        c.setFont('Helvetica', 6.3)
        c.drawString(382,502,'amount to be insured in figures in box marked "Amount of Insurance"')
        c.setFont('Helvetica', 8)
        c.drawString(34,517,"Airport of Destination")
        c.drawString(16,491,"Handling Information")
        c.drawString(302,517,"Amount of Insurance")
        c.setFont('Helvetica', 7.4)
        c.drawString(135,517,"Flight")
        c.drawString(174,517,"For Carrier Use only")
        c.drawString(259,517,"Flight/Date")
        c.drawString(299,542,"Currency")
        c.setFont('Helvetica', 7.2)
        c.drawString(453,543,"Declared Value of")
        c.drawString(516,543,"Declared Value for")
        c.drawString(464,537,"Carriage")
        c.drawString(524,537,"Customs")
        c.setFont('Helvetica', 7)
        c.drawString(335,543,"CHGS")
        c.drawString(336,536,"Code")
        c.drawString(343,529,"0")
        c.setFont('Helvetica', 6)
        c.drawString(366,544,"WT")
        c.drawString(388,544,"VAL")
        c.drawString(420,544,"Other")
        c.drawString(364,536,"PPD")
        c.drawString(388,536,"Col")
        c.drawString(411,536,"PPD")
        c.drawString(434,536,"Col")
        c.setFont('Helvetica-Bold', 9)
        
        if air_mbl.freight_type == "Prepaid":
            c.drawString(364,526,"X")
            c.drawString(411,526,"X")
        
        if air_mbl.freight_type == "Collect":
            c.drawString(390,526,"X")
            c.drawString(435,526,"X")
        
        c.setFont('Helvetica', 8.2)
        c.drawString(235,162,"Shipper certifies that the particulars on the face hereof are correct at and that insofar as any")
        c.drawString(235,154,"part of the consignment contains dangerous goods, such part is properly described by name")
        c.drawString(235,146,"and is in proper condition for carriage by air according to the applicable Dangerous Goods")
        c.drawString(235,138,"Regulations.")
        if air_mbl.signature_for:
            c.drawString(330,107,f"{air_mbl.signature_for}")
        c.setFont('Helvetica-Bold', 9)
        if air_mbl.signature_company:
            c.drawString(300,120,f"{air_mbl.signature_company}")
        c.setFont('Helvetica-Bold', 8)
        c.drawString(235,240,"Other Charges")
        c.setFont('Helvetica', 8)
        c.drawString(235,51,"Executed on (Date)")
        c.drawString(235,29,"Total Collect Charges")
        c.drawString(355,51,"at (Place)")
        c.drawString(430,51,"Signature of Issuing Carrier or Its Agent")    
        c.setFont('Helvetica', 7)
        c.drawString(72,154,"Total Other Charges Due Agent")
        c.drawString(100,448,"Kg")
        c.drawString(100,439,"Lb")
        c.setFont('Helvetica', 7.1)
        c.drawString(128,55,"CC Charges in Dest,Currency")
        c.drawString(70,130,"Total Other Charges Due Carrier")
        c.setFont('Helvetica', 7.3)
        c.drawString(20,55,"Currency Conversion Rates")
        c.drawString(101,418,"K")
        c.drawString(117,418,"Q")
        c.setFont('Helvetica', 8)
        c.drawString(114,181,"Tax")
        c.drawString(91,210,"Valuation Charge")
        c.drawString(95,241,"Weight Charge")
        c.drawString(37,241,"Prepaid")
        c.drawString(28,226,"AS AGREED")
        c.drawString(178,241,"Collect")
        c.drawString(168,226,"AS AGREED")
        # c.drawString(345,413,"AS AGREED")
        
        c.drawString(438,449,"Nature and Quantity of Goods")
        c.drawString(440,440,"(Incl. Dimensions of volume)")
        c.drawString(125,450,"Rate Class")
        c.drawString(128,440,"Commodity")
        c.drawString(134,432,"Item No")
        c.drawString(19,450,"No.of")
        c.drawString(17,442,"Pieces")
        c.drawString(21,433,"RCP")
        c.setFont('Helvetica',9)
        c.drawString(15,29,"For Carrier's Use only at")
        c.drawString(40,20,"Destination")
        c.drawString(130,29,"Charges in Destination")
        c.drawString(38,79,"Total Prepaid")
        c.drawString(148,79,"Total Collect")
        c.drawString(355,442,"Total")
        c.drawString(279,448,"Rate")
        c.drawString(271,438,"Charges")
        c.drawString(190,448,"Chargeable")
        c.drawString(198,438,"Weight")
        c.drawString(61,446,"Gross")
        c.drawString(60,437,"Weight")
        
        


        if air_mbl:
            if air_mbl.mbl_no:
                c.setFont('Helvetica-Bold', 9)
                if air_mbl.type == "HBL":
                    c.drawString(140,822, air_mbl.mbl_Document_no)
                else:
                    c.drawString(140,822, air_mbl.mbl_no)
        
            if air_mbl.exporter_name:
                c.setFont('Helvetica', 9)
                c.drawString(20,796,air_mbl.exporter_name.party_name +",")
                
            if air_mbl.exporter_address:
                j=786
                c.setFont('Helvetica', 8)
                for i in air_mbl.exporter_address.splitlines():
                    c.drawString(20,j,i)
                    j -= 9
            
            if air_mbl.consigned_name:
                c.setFont('Helvetica', 8)
                c.drawString(20,720,air_mbl.consigned_name.party_name +",")
                
            if air_mbl.consigned_address:
                j=710
                c.setFont('Helvetica', 8)
                for i in air_mbl.consigned_address.splitlines():
                    c.drawString(20,j,i)
                    j -= 9
            
            
            
            if air_mbl.notify_party:
                c.setFont('Helvetica', 9)
                c.drawString(20,720,air_mbl.notify_party.party_name +",")        
                j=710
                c.setFont('Helvetica', 8)
                for i in air_mbl.notify_party_address.splitlines():
                    c.drawString(20,j,i)
                    j -= 9
            
            if air_mbl.agent_name:
                c.setFont('Helvetica', 8)
                c.drawString(20,657,air_mbl.agent_name.party_name +",")        
                j=647
                c.setFont('Helvetica', 7)
                for i in air_mbl.agent_address.splitlines():
                    c.drawString(20,j,i)
                    j -= 9

            if air_mbl.agent_iata_code:
                c.setFont('Helvetica', 8)
                c.drawString(17,607,air_mbl.agent_iata_code)        

            
            if air_mbl.account_no:
                c.setFont('Helvetica', 8)
                c.drawString(165,607,air_mbl.account_no)        

            
            
            
            if air_mbl.mbl_Document_no:
                c.setFont('Helvetica', 9)
                if air_mbl.type == "HBL":
                    c.drawString(510,807,air_mbl.mbl_no)

            if air_mbl.origin_to:
                c.setFont('Helvetica', 9)
            
                c.drawString(16,530,air_mbl.origin_to)
            
            if air_mbl.carrier_name:
                c.setFont('Helvetica', 8)
            
                c.drawString(47,528,air_mbl.carrier_name)
        
            if air_mbl.currency:
                c.setFont('Helvetica', 8)
                c.drawString(300,528,air_mbl.currency.short_name)
            
            if air_mbl.declared_value:
                c.setFont('Helvetica', 8)
                c.drawString(470,528,air_mbl.declared_value)
            
            if air_mbl.declared_value_customs:
                c.setFont('Helvetica', 8)
                c.drawString(530,528,air_mbl.declared_value_customs)
            
            if air_mbl.valuation_charge:
                c.setFont('Helvetica', 9)
                c.drawString(20,200,air_mbl.valuation_charge)
            
            if air_mbl.accounting_information:
                c.setFont('Helvetica', 7)
                j=570
                for i in air_mbl.accounting_information.splitlines():
                    c.drawString(310,j,i)
                    j -= 8
            
            if air_mbl.departure_airport:
                c.setFont('Helvetica', 9)
                c.drawString(40,563,f"{air_mbl.departure_airport}")
                
            if air_mbl.destination_airport:
                c.setFont('Helvetica', 9)
                c.drawString(50,505,air_mbl.destination_airport)
            
            if air_mbl.handling_information:
                j=481
                c.setFont('Helvetica', 8)
                for i in air_mbl.handling_information.splitlines():
                    c.drawString(30,j,i)
                    j -= 9



            if air_mbl.marks_and_number:
                j=419
                c.setFont('Helvetica', 9)
                total_pieces=0
                for i in air_mbl.marks_and_number.splitlines():
                
                    c.drawString(23,j,i)
                    try:
                        total_pieces += int(i)
                    except:
                        pass
                    j -= 10
                c.drawString(20,258,str(total_pieces))


            if air_mbl.gross_weight:
                j=419
                c.setFont('Helvetica', 9)
                total_gross_weight=0
                for i in air_mbl.gross_weight.splitlines():
                    c.drawString(62,j,i)
                    try:
                        total_gross_weight += float(i)
                    except:
                        pass
                    j -= 10
                c.drawString(58,258,str(total_gross_weight))


            if air_mbl.chargeable_weight:
                j=419
                c.setFont('Helvetica', 9)
                for i in air_mbl.chargeable_weight.splitlines():
                    c.drawString(200,j,i)
                    j -= 10
            count = 0
            if air_mbl.rate_charges:
                j=419
                c.setFont('Helvetica', 9)
                for i in air_mbl.rate_charges.splitlines():
                    c.drawString(270,j,i)
                    count += 1
                    j -= 10

        
            
            total_charge = 0
            if air_mbl.total_charges:
                j=419
                c.setFont('Helvetica', 8)
                for i in air_mbl.total_charges.splitlines():
                    if is_number(i):
                        total_charge += float(i)

                    c.drawString(345,j,i)
                    j -= 10

            if total_charge:
                c.drawString(345,260,f"{total_charge}")
            else:
                c.drawString(345,260,f"AS AGREED")


            if air_mbl.date:
                c.setFont('Helvetica-Bold', 9)
                c.drawString(240,65,str(air_mbl.date))



            if air_mbl.executed_at:
                c.drawString(358,65,air_mbl.executed_at)


            if air_mbl.bl_type == "ORIGINAL":
                # logo = 'http://dtriumph.easyfreightlook.com/static/Image/rayzz_stamp.PNG'
                # c.drawImage(logo, 498, 65, width=1 * inch, height=1 * inch)
                pass

            
            if air_mbl.flight_no:
                c.setFont('Helvetica',8)
                c.drawString(135,502,str(air_mbl.flight_no))
            if air_mbl.flight_date:
                c.setFont('Helvetica',8)
                c.drawString(250,502,str(air_mbl.flight_date))
            if air_mbl.description_of_commodities:
                # c.drawString(425,418,"AS AGREEDDDDDDDDDDDDDD")
                j=418
                c.setFont('Helvetica', 9)
                for i in air_mbl.description_of_commodities.splitlines():
                    c.drawString(417,j,i[:38])
                    j -= 12



        c.showPage()
    c.save()

    return response


def mbl_pdf(request, id):
    all_mbl = MBLMaster.objects.filter(id=id).first()
    response = HttpResponse(content_type='application/pdf')
    filename = f"{all_mbl.mbl_no}.pdf"
    response['Content-Disposition'] = f'filename="{filename}"'
    c = canvas.Canvas(response)

    # *************************** GUI Part ******************************
    # c.setFont('Helvetica-Bold', 11)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, 790, 'OCEAN BILL OF LADING')
    c.setFont('Helvetica-Bold', 7)
    c.drawString(360, 790, 'BILL OF LADING FOR COMBINED MULTIMODAL TRANSPORT')

    c.line(13, 785, 585, 785)
    c.line(13, 20, 585, 20)
    c.line(13, 20, 13, 785)
    c.line(585, 785, 585, 20)
    
    c.rotate(45)
    c.setFillColorCMYK(0,0,0,0.3)
    c.setFont('Helvetica-Bold',50)
    
    if all_mbl.mbl_type == "Draft":
        c.drawString(380,0.5*inch,'DRAFT')
    elif all_mbl.mbl_type == "Final":
        c.drawString(340,0.2*inch,'ORIGINAL')
    elif all_mbl.mbl_type == "Non Negotiable":
        c.setFont('Helvetica-Bold',30)
        c.drawString(340,0.2*inch,'NON-NEGOTIABLE')
    
    c.rotate(-45)
    c.setFillColorCMYK(0,0,0,1)
    
    
    
    

    c.line(310, 785, 310, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 778, 'SHIPPER')
    c.setFont('Helvetica', 8)

    # SH_EX_L1 = data2[0][6]
    #
    c.drawString(15, 765, str(all_mbl.exporter_name))
    st = str(all_mbl.exporter_address).splitlines()
    y = 755
    i = 0
    for row in st:
        c.drawString(15, y, st[i])
        y = y - 10
        i = i + 1

    c.setFont('Helvetica-Bold', 7)
    # c.line(435, 780, 580, 780)
    # c.line(435, 765, 580, 765)
    # c.line(435, 780, 435, 765)
    # c.line(580, 780, 580, 765)
    c.drawString(315, 775, 'BOOKING NO.')
    c.setFont('Helvetica-Bold', 8)
    c.drawString(315, 763, str(all_mbl.mbl_Document_no))

    # c.line(435, 760, 580, 760)
    # c.line(435, 745, 580, 745)
    # c.line(435, 760, 435, 745)
    # c.line(580, 760, 580, 745)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(450, 775, 'BILL OF LANDING NO.')
    c.setFont('Helvetica-Bold', 8)
    c.drawString(450, 763, str(all_mbl.mbl_no))
    c.line(310, 760, 585, 760)
    
    c.line(445, 785, 445, 760)

    # c.setFont('Helvetica-Bold', 16)
    # c.drawString(427, 715, 'R K C L')
    # c.setFont('Helvetica', 8)
    # c.drawString(409, 705, 'We can move mountains')
    # c.setFont('Helvetica-Bold', 9)
    # # c.drawString(415, 695, 'AN ISO : 900:2015')
    
    # logo = 'http://rkclindo.easyfreightlook.com/static/Image/bl_pic.jpeg'


   
    domain = Site.objects.get_current().domain
    setting = Logistic.objects.filter(id=all_mbl.company_type.id).first()
    logo = f'{setting.logo.url}' 

   
 
    
    
    # c.setFont('Helvetica-Bold', 20)
    c.setFont('Helvetica', 20)
    if all_mbl.mbl_type == "Draft":
        # c.drawString(380, 674, 'DRAFT - BL')
        # c.drawImage(logo, 320, 650, width=3.5 * inch, height=1.35 * inch)
        c.drawImage(logo, 400, 680, width=1.3 * inch, height=1.10 * inch)
    elif all_mbl.mbl_type == "Final" or all_mbl.bl_type == "Non Negotiable":
        c.drawImage(logo, 400, 680, width=1.3* inch, height=1.10 * inch)
    elif all_mbl.mbl_type == "Shipping Instruction":
        c.drawString(350, 674, 'Shipping Instruction')
    else:
        c.drawString(380, 674, 'DRAFT - BL')


    c.setFont('Helvetica-Bold', 9)
    c.drawString(410, 670, 'FMC NO. 03119')
   
    # c.setFont('Helvetica', 7)
    # c.drawString(325, 666, 'JI. Trembesi Blok The Mansion Kemayoran Bougenville Tower Fontana Lantai, ')
    # c.drawString(345, 658, ' 36 J2 Jakarta Utara - 14410 Mob. No.:- +62 812 1172 8864, ')
    # c.drawString(335, 649, 'E-mail: saurav@rkclindonesia.com , Web: www.rkcontainerline.co.in')
    # c.drawString(355, 640, 'GSTIN:- 07AAHCRO122L1Zl , CIN No.:- U74999DL2014PTC270792')
    # c.setFont('Helvetica-Bold', 8)
    # c.drawString(362, 631, 'Registration No. :- MYO/DGS/1987/JAN/2022')

    c.line(310, 650, 585, 650)

    # c.line(310, 593, 585, 593)
    c.setFont('Helvetica-Bold', 6)
    # c.setFont('Helvetica', 6)
    c.drawString(312, 641, 'Taken in charge in apparently good condition herein at the place of receipt for transport and')
    c.drawString(312, 634, 'delivery as mentiioned above unless otherwise stated. The MTO in accordance with the')
    c.drawString(312, 628, 'provisions contained in the MTD undertakes to perform or to procure the performance of the')
    c.drawString(312, 622, 'multimodal transport from the place at which the goods are taken in charge, to the place')
    c.drawString(312, 615, 'designated for delivery and assumes responsibility for such transport.')
    c.setFont('Helvetica-Bold', 6)
    c.drawString(312, 600, 'One of the MTD(s) must be surrendered, duly endorsed in exchange for the goods.In witness')
    c.drawString(312, 593, 'where of the original MTD all of this tenure and date have been signed in the number indicated')
    c.drawString(312, 586, 'below one of which being accomplished the other(s) to be void')

    c.setFont('Helvetica-Bold', 7)
    c.line(13, 720, 310, 720)

    c.drawString(15, 713, 'CONSIGNEE')
    c.setFont('Helvetica', 8)
    # CONS_L1 = data2[0][8]

    c.drawString(15, 700, str(all_mbl.consigned_name))
    con = str(all_mbl.consigned_address).splitlines()
    y = 690
    i = 0
    for row in con:
        c.drawString(15, y, con[i])
        y = y - 10
        i = i + 1

    c.line(13, 650, 310, 650)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 643, 'NOTIFY PARTY')
    c.setFont('Helvetica', 8)

    c.drawString(15, 628, str(all_mbl.notify_party))
    np = str(all_mbl.notify_party_address).splitlines()
    y = 618
    i = 0
    for row in np:
        c.drawString(15, y, np[i])
        y = y - 10
        i = i + 1

    c.line(13, 570, 310, 570)
    c.line(310, 580, 585, 580)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 562, 'PRE-CARRIAGE BY')
    c.setFont('Helvetica', 8)
    c.drawString(40, 549, str(all_mbl.pre_carriage_by))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(192, 562, 'PLACE OF RECIEPT')
    c.setFont('Helvetica', 8)
    c.drawString(200, 549, str(all_mbl.place_of_receipt))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(312, 570, 'AGENT AT DESTINATION ')
    c.setFont('Helvetica', 8)
    c.drawString(315, 560, str(all_mbl.agent_name))
    fa = str(all_mbl.agent_address).splitlines()
    y = 550
    i = 0
    for row in fa:
        c.drawString(315, y, fa[i])
        y = y - 10
        i = i + 1

    c.line(13, 543, 310, 543)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 535, 'VESSEL')
    c.setFont('Helvetica', 8)
    c.drawString(40, 521, str(all_mbl.ocean_vessel))

   
    c.setFont('Helvetica-Bold', 7)
    c.drawString(192, 535, 'PORT OF LOADING')
    c.setFont('Helvetica', 8)
    c.drawString(200, 521, str(all_mbl.port_of_loading_export))

    c.line(13, 515, 585, 515)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 506, 'PORT OF DISCHARGE')
    c.setFont('Helvetica', 8)
    c.drawString(40, 494, str(all_mbl.port_of_discharge))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(192, 506, 'PLACE OF DELIVERY')
    c.setFont('Helvetica', 8)
    c.drawString(200, 493, str(all_mbl.place_of_delivery))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(312, 506, 'MODE / MEANS OF TRANSPORT')
    c.setFont('Helvetica', 8)
    c.drawString(320, 493, str(all_mbl.movement_type))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(442, 506, 'ROUTE / PLACE OF TRANSSHIPMENT')
    c.setFont('Helvetica', 8)
    c.drawString(457, 493, str(all_mbl.domestic_routing))

    c.line(13, 490, 585, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 480, 'MARKS AND NO')
    c.setFont('Helvetica', 7.5)

    flag = 0

    max_length = 27
    actual_max_length = 0
    
    # containers = all_mbl.job_no.job_container.all()
    containers = all_mbl.container_options.all()
    
   


    mn = str(all_mbl.marks_and_number).splitlines()
    y = 460
    i = 0
    
    if len(mn) > max_length:
        flag = 1
    
    if len(mn) > actual_max_length:
        actual_max_length = len(mn) 

    for row in mn:
        if y >= 190:
            c.drawString(15, y, row)
            y = y - 10
            i = i + 1
        else:
            pass


    # c.line(135, 490, 135, 180)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(132, 480, 'NO. OF PKGS')
    c.setFont('Helvetica', 7.5)
    no_of_pkg = str(all_mbl.total_packages).splitlines()
    y = 460
    i = 0
    if len(no_of_pkg) > max_length:
        flag = 1

    if len(no_of_pkg) > actual_max_length:
        actual_max_length = len(no_of_pkg)

    for row in no_of_pkg:
        if y >= 190:
            c.drawString(130, y, row)
            y = y - 10
            i = i + 1
        else:
            pass
    # c.drawString(132, 460, NO_OF_CONT_L1)
    
    c.line(190, 570, 190, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(255, 480, 'DESCRIPTION OF GOODS')
    c.setFont('Helvetica', 7.5)
    des_good = str(all_mbl.description_of_commodities).splitlines()
    y = 460
    i = 0
    if len(des_good) > max_length:
        flag = 1
    
    if len(des_good) > actual_max_length:
        actual_max_length = len(des_good)

    for row in des_good:
        if y >= 190:
            c.drawString(220, y, row)
            y = y - 10
            i = i + 1
        else:
            pass
    
    c.line(440, 515, 440, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(450, 480, 'GROSS WT')
    c.setFont('Helvetica', 7.5)
    grs_wt = str(all_mbl.gross_weight).splitlines()
    y = 460
    i = 0
    if len(grs_wt) > max_length:
        flag = 1

    if len(grs_wt) > actual_max_length:
        actual_max_length = len(grs_wt)

    for row in grs_wt:
        if y >= 190:
            c.drawString(450, y, row)
            y = y - 10
            i = i + 1
        else:
            pass
    
    
    c.setFont('Helvetica-Bold', 7)
    c.drawString(522, 480, 'MEASUREMENT')
    c.setFont('Helvetica', 7.5)
    mes = str(all_mbl.measurement).splitlines()
    y = 460
    i = 0
    if len(mes) > max_length:
        flag = 1

    if len(mes) > actual_max_length:
        actual_max_length = len(mes)

    for row in mes:
        if y >= 190:
            c.drawString(522, y, row)
            y = y - 10
            i = i + 1
        else:
            pass


    
    
    if len(containers) + actual_max_length <= max_length:
        y = 400 - (actual_max_length*10)
        c.drawString(25, y, 'CONTAINER NO.S')
        c.drawString(100, y, 'C.SEAL NO.')
        c.drawString(175, y, 'CONT TYPE')
        c.drawString(225, y, 'TOTAL PKG')
        c.drawString(290, y, 'GR.WT(KG)')
        c.drawString(355, y, 'NET WT(KG)')
        c.drawString(420, y, 'CBM')
        y -= 7
        c.setFont('Helvetica', 12)
        c.drawString(25, y, '--------- -----')
        c.drawString(100, y, '------- --')
        c.drawString(175, y, '---- -----')
        c.drawString(225, y, '----- ----')
        c.drawString(290, y, '---------')
        c.drawString(355, y, '---- ------')
        c.drawString(420, y, '----')
        c.setFont('Helvetica', 7)
        for container in containers:
            y -= 10
            c.drawString(25, y, f'{container.job_container_no}')
            c.drawString(100, y, f'{container.line_seal}')
            c.drawString(175, y, f'{container.container_type}')
            c.drawString(225, y, f'{container.total_package}')
            c.drawString(290, y, f'{container.gross_wt}')
            c.drawString(355, y, f'{container.net_wt}')
            c.drawString(420, y, f'{container.cbm}')

    
    else:
        flag = 1

    c.line(13, 475, 585, 475)

    c.line(429, 180, 585, 180)

    c.setFont('Helvetica', 9)
    # c.drawString(180, 167, 'Particulars above furnished by shipper/consignor')
    
    c.setFont('Helvetica-Bold', 7)
    c.drawString(432, 167, 'SHIPPED ON BOARD DATE ')
    c.setFont('Helvetica', 8)
    
    try:
        format_date1=datetime.strptime(str(all_mbl.shipper_board_date),"%Y-%m-%d")
        shipped_board_date=format_date1.strftime("%d-%m-%Y")
    except:
        shipped_board_date="None"
    c.drawString(432,157,(shipped_board_date))

    c.line(13, 150, 585, 150)
    c.setFont('Helvetica-Bold', 7)

    c.drawString(20, 137, 'FREIGHT TERMS')
    c.setFont('Helvetica', 9)
    c.drawString(25, 124, str(all_mbl.freight_type))

    c.line(143, 150, 143, 120)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(175, 137, 'FREIGHT PAYABLE AT')
    c.setFont('Helvetica', 9)
    c.drawString(175, 124, str(all_mbl.freight_payable_at))

    c.line(286, 150, 286, 120)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(300, 137, 'NUMBER OF ORIGINAL BL(S)')
    c.setFont('Helvetica', 9)
    c.drawString(305, 124, str(all_mbl.no_of_o_mtd))

    c.line(429, 180, 429, 120)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(434, 137, 'PLACE AND DATE OF ISSUE')
    c.setFont('Helvetica', 9)
    PLACE_OF_ISSUE_V = str(all_mbl.executed_at)
    c.drawString(434, 124, PLACE_OF_ISSUE_V)
    format_date2=datetime.strptime(str(all_mbl.date),"%Y-%m-%d")
    date=format_date2.strftime("%d-%m-%Y")
    c.drawString(500, 124, str(date))

    c.line(13, 120, 585, 120)
    c.setFont('Helvetica-Bold', 7)

    c.drawString(15, 110, 'OTHER PARTICULARS (IF ANY) / DELIVERY AGENT')
    c.setFont('Helvetica', 9)
    # PLACE_OF_ISSUE_V = 'DELHI'
    # c.drawString(15,90, str(all_mbl.agent_name))
    # c.drawString(15, 80, str(all_mbl.agent_address))

    c.setFont('Helvetica-Bold', 7)
    if all_mbl.bl_type == "Final" or all_mbl.bl_type == "Non Negotiable":
        c.drawString(431, 110, 'For R K Container Line Pvt Ltd')
        
        logo = 'http://rkclindo.easyfreightlook.com/static/Image/RK_Stamp.jpg'
        c.drawImage(logo, 450, 23, width=1.35 * inch, height=1.20 * inch)

    c.line(370, 20, 370, 120)
    c.drawString(380, 110, 'FOR RK CONTAINER LINE PVT LTD')
    c.drawString(500, 50, 'As agent for the Carrier')
    c.drawString(500, 30, 'Authorised Signature')

    c.line(13, 20, 585, 20)
    if flag == 1:
        c.showPage()
        # *************************** GUI Part ******************************
        c.line(13, 785, 585, 785)
        c.line(13, 20, 585, 20)
        c.line(13, 20, 13, 785)
        c.line(585, 785, 585, 20)
        
        c.rotate(45)
        c.setFillColorCMYK(0,0,0,0.3)
        c.setFont('Helvetica-Bold',50)
        
        if all_mbl.mbl_type == "Draft":
            c.drawString(380,0.5*inch,'DRAFT')
        elif all_mbl.mbl_type == "Final":
            c.drawString(340,0.2*inch,'ORIGINAL')
        elif all_mbl.mbl_type == "Non Negotiable":
            c.setFont('Helvetica-Bold',30)
            c.drawString(340,0.2*inch,'NON-NEGOTIABLE')
        
        c.rotate(-45)
        c.setFillColorCMYK(0,0,0,1)

        c.setFont('Helvetica-Bold', 15)
        c.drawString(170, 790, 'ANNEXURE FOR B/L NO: ' + str(all_mbl.mbl_no))

        c.setFont('Helvetica-Bold', 7)
        c.drawString(25, 775, 'MARKS AND NUMBERS')
        c.setFont('Helvetica', 7)
        mn = str(all_mbl.marks_and_number).splitlines()
        length = len(mn)
        y = 755
        i = 28
        while (i < length):
            c.drawString(15, y, mn[i])
            y = y - 10
            i = i + 1

        # c.line(135, 785, 135, 20)
        c.setFont('Helvetica-Bold',7)
        c.drawString(137, 775, 'NO. OF PKGS')
        c.setFont('Helvetica', 7)
        no_of_pkg = str(all_mbl.no_of_packages).splitlines()
        length = len(no_of_pkg)
        y = 755
        i = 27
        while (i < length):
            c.drawString(140, y, no_of_pkg[i])
            y = y - 10
            i = i + 1
            
            
        


        # c.line(190, 785, 190, 20)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(255, 775, 'DESCRIPTION OF GOODS')
        c.setFont('Helvetica', 7)
        des_good1 = str(all_mbl.description_of_commodities).splitlines()
        length = len(des_good1)
        y = 755
        i = 27
        while (i < length):
            c.drawString(200, y, des_good1[i])
            y = y - 10
            i = i + 1

        # c.drawString(200, 755, DESC_GOOD_L1)

        # c.line(455, 785, 455, 20)
        
        c.setFont('Helvetica-Bold', 7)
        c.drawString(456, 775, 'GROSS WEIGHT')
        c.setFont('Helvetica', 7)
        grs_wt = str(all_mbl.gross_weight).splitlines()
        length = len(grs_wt)
        y = 755
        i = 27
        while (i < length):
            c.drawString(462, y, grs_wt[i])
            y = y - 10
            i = i + 1

        # c.line(520, 785, 520, 20)
        
        c.setFont('Helvetica-Bold', 7)
        c.drawString(522, 775, 'MEASUREMENT')
        c.setFont('Helvetica', 7)
        mes = str(all_mbl.measurement).splitlines()
        length = len(mes)
        y = 755
        i = 27
        while (i < length):
            c.drawString(522, y, mes[i])
            y = y - 10
            i = i + 1

        c.line(13, 770, 585, 770)


        if len(containers) + actual_max_length > max_length and containers:
            y = 755 - ((actual_max_length - max_length) *10)


            c.drawString(25, y, 'CONTAINER NO.S')
            c.drawString(100, y, 'C.SEAL NO.')
            c.drawString(175, y, 'CONT TYPE')
            c.drawString(225, y, 'TOTAL PKG')
            c.drawString(290, y, 'GR.WT(KG)')
            c.drawString(355, y, 'NET WT(KG)')
            c.drawString(420, y, 'CBM')
            y -= 7
            c.setFont('Helvetica', 12)
            c.drawString(25, y, '--------- -----')
            c.drawString(100, y, '------- --')
            c.drawString(175, y, '---- -----')
            c.drawString(225, y, '----- ----')
            c.drawString(290, y, '---------')
            c.drawString(355, y, '---- ------')
            c.drawString(420, y, '----')

            
            c.setFont('Helvetica', 7)
            for container in containers:
                y -= 10
                c.drawString(25, y, f'{container.job_container_no}')
                c.drawString(100, y, f'{container.line_seal}')
                c.drawString(175, y, f'{container.container_type}')
                c.drawString(225, y, f'{container.total_package}')
                c.drawString(290, y, f'{container.gross_wt}')
                c.drawString(355, y, f'{container.net_wt}')
                c.drawString(420, y, f'{container.cbm}')

    c.showPage()
    c.save()
    return response


def print_mbl_pdf(request, id):
    all_mbl = MBLMaster.objects.filter(id=id).first()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="local_invoice.pdf"'
    c = canvas.Canvas(response)

    # *************************** GUI Part ******************************
    # c.setFont('Helvetica-Bold', 11)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, 805, 'OCEAN BILL OF LADING')
    c.setFont('Helvetica-Bold', 7)
    c.drawString(360, 805, 'BILL OF LADING FOR COMBINED MULTIMODAL TRANSPORT')

    c.line(13, 800, 585, 800)
    c.line(13, 20, 585, 20)
    c.line(13, 20, 13, 800)
    c.line(585, 800, 585, 20)
    
    c.rotate(45)
    c.setFillColorCMYK(0,0,0,0.3)
    c.setFont('Helvetica-Bold',50)
    
    # if all_mbl.mbl_type == "Draft":
    #     c.drawString(380,0.5*inch,'DRAFT')
    # elif all_mbl.mbl_type == "Final":
    #     c.drawString(340,0.2*inch,'ORIGINAL')
    # elif all_mbl.mbl_type == "Non Negotiable":
    #     c.setFont('Helvetica-Bold',30)
    #     c.drawString(340,0.2*inch,'NON-NEGOTIABLE')
    
    c.rotate(-45)
    c.setFillColorCMYK(0,0,0,1)
    
    
    
    

    c.line(310, 800, 310, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 790, 'SHIPPER')
    c.setFont('Helvetica', 8)

    # SH_EX_L1 = data2[0][6]
    #
    c.drawString(15, 775, str(all_mbl.exporter_name))
    st = str(all_mbl.exporter_address).splitlines()
    y = 765
    i = 0
    for row in st:
        c.drawString(15, y, st[i])
        y = y - 10
        i = i + 1

    c.setFont('Helvetica-Bold', 7)
    # c.line(435, 780, 580, 780)
    # c.line(435, 765, 580, 765)
    # c.line(435, 780, 435, 765)
    # c.line(580, 780, 580, 765)
    c.drawString(315, 792, 'BOOKING NO.')
    c.setFont('Helvetica-Bold',8 )
    c.drawString(315, 783, str(all_mbl.mbl_Document_no))

    # c.line(435, 760, 580, 760)
    # c.line(435, 745, 580, 745)
    # c.line(435, 760, 435, 745)
    # c.line(580, 760, 580, 745)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(450, 792, 'BILL OF LANDING NO.')
    c.setFont('Helvetica-Bold', 8)
    c.drawString(450, 783, str(all_mbl.mbl_no))
    c.line(310, 780, 585, 780)
    
    c.line(445, 800, 445, 780)

    # c.setFont('Helvetica-Bold', 16)
    # c.drawString(427, 715, 'R K C L')
    # c.setFont('Helvetica', 8)
    # c.drawString(409, 705, 'We can move mountains')
    # c.setFont('Helvetica-Bold', 9)
    # # c.drawString(415, 695, 'AN ISO : 900:2015')
    
    # logo = 'http://rkclindo.easyfreightlook.com/static/Image/bl_pic.jpeg'

    # c.setFont('Helvetica', 7)
    # c.drawString(325, 666, 'JI. Trembesi Blok The Mansion Kemayoran Bougenville Tower Fontana Lantai, ')
    # c.drawString(345, 658, ' 36 J2 Jakarta Utara - 14410 Mob. No.:- +62 812 1172 8864, ')
    # c.drawString(335, 649, 'E-mail: saurav@rkclindonesia.com , Web: www.rkcontainerline.co.in')
    # c.drawString(355, 640, 'GSTIN:- 07AAHCRO122L1Zl , CIN No.:- U74999DL2014PTC270792')
    # c.setFont('Helvetica-Bold', 8)
    # c.drawString(362, 631, 'Registration No. :- MYO/DGS/1987/JAN/2022')

    # c.setFont('Helvetica-Bold', 9)
    # c.drawString(410, 670, 'FMC NO. 03119')

    c.line(310, 650, 585, 650)

    # c.line(310, 593, 585, 593)
    c.setFont('Helvetica-Bold', 6)
    # c.setFont('Helvetica', 6)
    c.drawString(312, 641, 'Taken in charge in apparently good condition herein at the place of receipt for transport and')
    c.drawString(312, 634, 'delivery as mentiioned above unless otherwise stated. The MTO in accordance with the')
    c.drawString(312, 628, 'provisions contained in the MTD undertakes to perform or to procure the performance of the')
    c.drawString(312, 622, 'multimodal transport from the place at which the goods are taken in charge, to the place')
    c.drawString(312, 615, 'designated for delivery and assumes responsibility for such transport.')
    c.setFont('Helvetica-Bold', 6)
    c.drawString(312, 600, 'One of the MTD(s) must be surrendered, duly endorsed in exchange for the goods.In witness')
    c.drawString(312, 593, 'where of the original MTD all of this tenure and date have been signed in the number indicated')
    c.drawString(312, 586, 'below one of which being accomplished the other(s) to be void')

    c.setFont('Helvetica-Bold', 7)
    c.line(13, 720, 310, 720)

    c.drawString(15, 713, 'CONSIGNEE')
    c.setFont('Helvetica', 8)
    # CONS_L1 = data2[0][8]

    c.drawString(15, 700, str(all_mbl.consigned_name))
    con = str(all_mbl.consigned_address).splitlines()
    y = 690
    i = 0
    for row in con:
        c.drawString(15, y, con[i])
        y = y - 10
        i = i + 1

    c.line(13, 650, 310, 650)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 643, 'NOTIFY PARTY')
    c.setFont('Helvetica', 8)

    c.drawString(15, 628, str(all_mbl.notify_party))
    np = str(all_mbl.notify_party_address).splitlines()
    y = 618
    i = 0
    for row in np:
        c.drawString(15, y, np[i])
        y = y - 10
        i = i + 1

    c.line(13, 570, 310, 570)
    c.line(310, 580, 585, 580)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 562, 'PRE-CARRIAGE BY')
    c.setFont('Helvetica', 8)
    c.drawString(40, 549, str(all_mbl.pre_carriage_by))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(192, 562, 'PLACE OF RECIEPT')
    c.setFont('Helvetica', 8)
    c.drawString(200, 549, str(all_mbl.place_of_receipt))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(312, 570, 'AGENT AT DESTINATION ')
    c.setFont('Helvetica', 8)
    c.drawString(315, 560, str(all_mbl.agent_name))
    fa = str(all_mbl.agent_address).splitlines()
    y = 550
    i = 0
    for row in fa:
        c.drawString(315, y, fa[i])
        y = y - 10
        i = i + 1

    c.line(13, 543, 310, 543)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 535, 'VESSEL')
    c.setFont('Helvetica', 8)
    c.drawString(40, 521, str(all_mbl.ocean_vessel))

   
    c.setFont('Helvetica-Bold', 7)
    c.drawString(192, 535, 'PORT OF LOADING')
    c.setFont('Helvetica', 8)
    c.drawString(200, 521, str(all_mbl.port_of_loading_export))

    c.line(13, 515, 585, 515)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 506, 'PORT OF DISCHARGE')
    c.setFont('Helvetica', 8)
    c.drawString(40, 494, str(all_mbl.port_of_discharge))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(192, 506, 'PLACE OF DELIVERY')
    c.setFont('Helvetica', 8)
    c.drawString(200, 493, str(all_mbl.place_of_delivery))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(312, 506, 'MODE / MEANS OF TRANSPORT')
    c.setFont('Helvetica', 8)
    c.drawString(320, 493, str(all_mbl.movement_type))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(442, 506, 'ROUTE / PLACE OF TRANSSHIPMENT')
    c.setFont('Helvetica', 8)
    c.drawString(457, 493, str(all_mbl.domestic_routing))

    c.line(13, 490, 585, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(15, 480, 'MARKS AND NO.')
    c.setFont('Helvetica', 7.5)

    flag = 0

    max_length = 27
    actual_max_length = 0
    # containers = all_mbl.job_no.job_container.all()
    containers = all_mbl.container_options.all()


    mn = str(all_mbl.marks_and_number).splitlines()
    y = 460
    i = 0
    
    if len(mn) > max_length:
        flag = 1
    
    if len(mn) > actual_max_length:
        actual_max_length = len(mn) 

    for row in mn:
        if y >= 190:
            c.drawString(15, y, row)
            y = y - 10
            i = i + 1
        else:
            pass


    # c.line(135, 490, 135, 180)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(132, 480, 'NO. OF PKGS')
    c.setFont('Helvetica', 7.5)
    no_of_pkg = str(all_mbl.total_packages).splitlines()
    y = 460
    i = 0
    if len(no_of_pkg) > max_length:
        flag = 1

    if len(no_of_pkg) > actual_max_length:
        actual_max_length = len(no_of_pkg)

    for row in no_of_pkg:
        if y >= 190:
            c.drawString(130, y, row)
            y = y - 10
            i = i + 1
        else:
            pass
    # c.drawString(132, 460, NO_OF_CONT_L1)
    
    c.line(190, 570, 190, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(255, 480, 'DESCRIPTION OF GOODS')
    c.setFont('Helvetica', 7.5)
    des_good = str(all_mbl.description_of_commodities).splitlines()
    y = 460
    i = 0
    if len(des_good) > max_length:
        flag = 1
    
    if len(des_good) > actual_max_length:
        actual_max_length = len(des_good)

    for row in des_good:
        if y >= 190:
            c.drawString(220, y, row)
            y = y - 10
            i = i + 1
        else:
            pass
    
    c.line(440, 515, 440, 490)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(450, 480, 'GROSS WT')
    c.setFont('Helvetica', 7.5)
    grs_wt = str(all_mbl.gross_weight).splitlines()
    y = 460
    i = 0
    if len(grs_wt) > max_length:
        flag = 1

    if len(grs_wt) > actual_max_length:
        actual_max_length = len(grs_wt)

    for row in grs_wt:
        if y >= 190:
            c.drawString(450, y, row)
            y = y - 10
            i = i + 1
        else:
            pass
    
    
    c.setFont('Helvetica-Bold', 7)
    c.drawString(522, 480, 'MEASUREMENT')
    c.setFont('Helvetica', 7.5)
    mes = str(all_mbl.measurement).splitlines()
    y = 460
    i = 0
    if len(mes) > max_length:
        flag = 1

    if len(mes) > actual_max_length:
        actual_max_length = len(mes)

    for row in mes:
        if y >= 190:
            c.drawString(522, y, row)
            y = y - 10
            i = i + 1
        else:
            pass

    if len(containers) + actual_max_length <= max_length:
        y = 400 - (actual_max_length*10)
        c.drawString(25, y, 'CONTAINER NO.S')
        c.drawString(100, y, 'C.SEAL NO.')
        c.drawString(175, y, 'CONT TYPE')
        c.drawString(225, y, 'TOTAL PKG')
        c.drawString(290, y, 'GR.WT(KG)')
        c.drawString(355, y, 'NET WT(KG)')
        c.drawString(420, y, 'CBM')
        y -= 7
        c.setFont('Helvetica', 12)
        c.drawString(25, y, '--------- -----')
        c.drawString(100, y, '------- --')
        c.drawString(175, y, '---- -----')
        c.drawString(225, y, '----- ----')
        c.drawString(290, y, '---------')
        c.drawString(355, y, '---- ------')
        c.drawString(420, y, '----')
        c.setFont('Helvetica', 7)
        for container in containers:
            y -= 10
            c.drawString(25, y, f'{container.job_container_no}')
            c.drawString(100, y, f'{container.line_seal}')
            c.drawString(175, y, f'{container.container_type}')
            c.drawString(225, y, f'{container.total_package}')
            c.drawString(290, y, f'{container.gross_wt}')
            c.drawString(355, y, f'{container.net_wt}')
            c.drawString(420, y, f'{container.cbm}')


    
    else:
        flag = 1

    c.line(13, 475, 585, 475)

    c.line(429, 180, 585, 180)

    c.setFont('Helvetica', 9)
    # c.drawString(180, 167, 'Particulars above furnished by shipper/consignor')
    
    c.setFont('Helvetica-Bold', 7)
    c.drawString(432, 167, 'SHIPPED ON BOARD DATE ')
    c.setFont('Helvetica', 8)
    format_date1=datetime.strptime(str(all_mbl.shipper_board_date),"%Y-%m-%d")
    shipped_board_date=format_date1.strftime("%d-%m-%Y")
    c.drawString(432,157,(shipped_board_date))

    c.line(13, 150, 585, 150)
    c.setFont('Helvetica-Bold', 7)

    c.drawString(20, 137, 'FREIGHT TERMS')
    c.setFont('Helvetica', 9)
    c.drawString(25, 124, str(all_mbl.freight_type))

    c.line(143, 150, 143, 120)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(175, 137, 'FREIGHT PAYABLE AT')
    c.setFont('Helvetica', 9)
    c.drawString(175, 124, str(all_mbl.freight_payable_at))

    c.line(286, 150, 286, 120)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(300, 137, 'NUMBER OF ORIGINAL BL(S)')
    c.setFont('Helvetica', 9)
    c.drawString(305, 124, str(all_mbl.no_of_o_mtd))

    c.line(429, 180, 429, 120)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(434, 137, 'PLACE AND DATE OF ISSUE')
    c.setFont('Helvetica', 9)
    PLACE_OF_ISSUE_V = str(all_mbl.executed_at)
    c.drawString(434, 124, PLACE_OF_ISSUE_V)
    format_date2=datetime.strptime(str(all_mbl.date),"%Y-%m-%d")
    date=format_date2.strftime("%d-%m-%Y")
    c.drawString(500, 124, str(date))

    c.line(13, 120, 585, 120)
    c.setFont('Helvetica-Bold', 7)

    c.drawString(15, 110, 'OTHER PARTICULARS (IF ANY) / DELIVERY AGENT ')
    c.setFont('Helvetica', 9)
    # PLACE_OF_ISSUE_V = 'DELHI'
    # c.drawString(15, 40, PLACE_OF_ISSUE_V)

    c.setFont('Helvetica-Bold', 7)
    if all_mbl.bl_type == "Final" or all_mbl.bl_type == "Non Negotiable":
        c.drawString(431, 110, 'For R K Container Line Pvt Ltd')
        
        # logo = 'http://rkclindo.easyfreightlook.com/static/Image/RK_Stamp.jpg'
        # c.drawImage(logo, 450, 23, width=1.35 * inch, height=1.20 * inch)
    c.line(370, 20, 370, 120)
    c.drawString(380, 110, 'FOR RK CONTAINER LINE PVT LTD')
    c.drawString(500, 50, 'As agent for the Carrier')
    c.drawString(500, 30, 'Authorised Signature')


    c.line(13, 20, 585, 20)
    if flag == 1:
        c.showPage()
        # *************************** GUI Part ******************************
        c.line(13, 785, 585, 785)
        c.line(13, 20, 585, 20)
        c.line(13, 20, 13, 785)
        c.line(585, 785, 585, 20)
        
        # c.rotate(45)
        # c.setFillColorCMYK(0,0,0,0.3)
        # c.setFont('Helvetica-Bold',50)
        
        # if all_mbl.mbl_type == "Draft":
        #     c.drawString(380,0.5*inch,'DRAFT')
        # elif all_mbl.mbl_type == "Final":
        #     c.drawString(340,0.2*inch,'ORIGINAL')
        # elif all_mbl.mbl_type == "Non Negotiable":
        #     c.setFont('Helvetica-Bold',30)
        #     c.drawString(340,0.2*inch,'NON-NEGOTIABLE')
        
        # c.rotate(-45)
        # c.setFillColorCMYK(0,0,0,1)

        c.setFont('Helvetica-Bold', 15)
        c.drawString(170, 790, 'ANNEXURE FOR B/L NO: ' + str(all_mbl.mbl_no))

        c.setFont('Helvetica-Bold', 7)
        c.drawString(25, 775, 'MARKS AND NUMBERS')
        c.setFont('Helvetica', 7)
        mn = str(all_mbl.marks_and_number).splitlines()
        length = len(mn)
        y = 755
        i = 28
        while (i < length):
            c.drawString(15, y, mn[i])
            y = y - 10
            i = i + 1

        # c.line(135, 785, 135, 20)
        c.setFont('Helvetica-Bold',7)
        c.drawString(137, 775, 'NO. OF PKGS')
        c.setFont('Helvetica', 7)
        no_of_pkg = str(all_mbl.no_of_packages).splitlines()
        length = len(no_of_pkg)
        y = 755
        i = 27
        while (i < length):
            c.drawString(140, y, no_of_pkg[i])
            y = y - 10
            i = i + 1
            
            
        


        # c.line(190, 785, 190, 20)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(255, 775, 'DESCRIPTION OF GOODS')
        c.setFont('Helvetica', 7)
        des_good1 = str(all_mbl.description_of_commodities).splitlines()
        length = len(des_good1)
        y = 755
        i = 27
        while (i < length):
            c.drawString(200, y, des_good1[i])
            y = y - 10
            i = i + 1

        # c.drawString(200, 755, DESC_GOOD_L1)

        # c.line(455, 785, 455, 20)
        
        c.setFont('Helvetica-Bold', 7)
        c.drawString(456, 775, 'GROSS WEIGHT')
        c.setFont('Helvetica', 7)
        grs_wt = str(all_mbl.gross_weight).splitlines()
        length = len(grs_wt)
        y = 755
        i = 27
        while (i < length):
            c.drawString(462, y, grs_wt[i])
            y = y - 10
            i = i + 1

        # c.line(520, 785, 520, 20)
        
        c.setFont('Helvetica-Bold', 7)
        c.drawString(522, 775, 'MEASUREMENT')
        c.setFont('Helvetica', 7)
        mes = str(all_mbl.measurement).splitlines()
        length = len(mes)
        y = 755
        i = 27
        while (i < length):
            c.drawString(522, y, mes[i])
            y = y - 10
            i = i + 1

        c.line(13, 770, 585, 770)


        if len(containers) + actual_max_length > max_length and containers:
            y = 755 - ((actual_max_length - max_length) *10)


            c.drawString(25, y, 'CONTAINER NO.S')
            c.drawString(120, y, 'C.SEAL NO.')
            c.drawString(175, y, 'CONT TYPE')
            c.drawString(225, y, 'TOTAL PKG')
            c.drawString(290, y, 'GR.WT(KG)')
            c.drawString(355, y, 'NET WT(KG)')
            c.drawString(420, y, 'CBM')
            y -= 7
            c.setFont('Helvetica', 12)
            c.drawString(25, y, '--------- -----')
            c.drawString(120, y, '------- --')
            c.drawString(175, y, '---- -----')
            c.drawString(225, y, '----- ----')
            c.drawString(290, y, '---------')
            c.drawString(355, y, '---- ------')
            c.drawString(420, y, '----')

            
            c.setFont('Helvetica', 7)
            for container in containers:
                y -= 10
                c.drawString(25, y, f'{container.job_container_no}')
                c.drawString(120, y, f'{container.line_seal}')
                c.drawString(175, y, f'{container.container_type}')
                c.drawString(225, y, f'{container.total_package}')
                c.drawString(290, y, f'{container.gross_wt}')
                c.drawString(355, y, f'{container.net_wt}')
                c.drawString(420, y, f'{container.cbm}')



    c.showPage()
    c.save()
    return response


def gr_pdf(request, id):
    gr = GRMaster.objects.get(id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="gr-{gr.gr_date}.pdf"'
    c = canvas.Canvas(response)
    domain = Site.objects.get_current().domain
    setting = Logistic.objects.filter(id=gr.company_type.id).first()
    stamp = f'{setting.stamp.url}' 
    # Top Row
    
    copy_list = ['Consignor Copy','Consignee Copy','Driver Copy','Sale Tax Copy','Office Copy']
    for copy in copy_list:
        c.setFont('Helvetica-Bold', 8)
    
        c.drawString(20,790,"GST No.")
        c.drawString(20,777,"PAN No. :-")
    
        c.drawString(62,790,"09AACCP4486A1ZH")
        c.drawString(62,777,"AACCP4486A")
    
        c.drawString(260,790,"Goods Consignment Note")
        
        c.setFont('Helvetica-Bold', 10)
        c.drawString(450,805,copy)
        if gr.job:
            c.drawString(440,790,f"JOB NO. {gr.job.job_no}")
        
        # Second Row
        c.setFillColorRGB(1,0,0)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(220,750,"PINKCITY LOGISTICS LIMITED")
        c.setFillColorRGB(0,0,0)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(180,730,"H.O. : V6 04 ANSALS GARG ENCLAVE,122/235 SAROJNI NAGAR,")
        c.drawString(230,720,"KANPUR - 208 012 UTTAR PRADESH,")
        c.drawString(200,710,"TEL : 0512 2216976,2217001 FAX : +91 512 2234911,")
        
        # Rectangle Text and shape
        c.rect(425,685, 140, 40, fill=0)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(435,710,"G.R. No.")
        c.drawString(435,690,"Date")
        
        if gr.gr_no:
            c.drawString(490,710,f"{gr.gr_no}")
        
        if gr.gr_date:
            c.drawString(490,690,f"{gr.gr_date}")
        
        # Third Row
        c.setFont('Helvetica-Bold', 9)
        c.drawString(20,665,"From :")
        c.setFont('Helvetica', 12)
        if gr.pickup_from and gr.drop_location:
            c.drawString(60,665,f"{gr.pickup_from.name}  To  {gr.drop_location.name}")
        
        c.setFont('Helvetica-Bold', 9)
        c.drawString(435,665,"TRL N.o. :")
        c.setFont('Helvetica', 12)
        c.drawString(480,665,f"{gr.trailor_no}")
        
        # FOURTH ROW
        c.setFont('Helvetica-Bold', 9)
        
        if gr.job_type:
            job_type = gr.job_type
        else:
            job_type = "Empty Container"
       
        if gr.import_export == 'EXPORT' and gr.drop_location and gr.pickup_from:   
            c.drawString(20,645,f"{job_type} picked up from {gr.drop_location.name} for factory stuffing at {gr.pickup_from.name}")
            c.drawString(20,630,f"on date Time :")
       
        if gr.import_export == 'IMPORT' and gr.pickup_from and gr.drop_location:   
            c.drawString(20,645,f"{job_type} picked up from {gr.pickup_from.name} for Fac. Stuff/DeStuff at {gr.drop_location.name},")
            c.drawString(20,630,f"on date Time : {gr.stuffing_date} {gr.time}")
        
        
        # Fifth Row
        c.setFont('Helvetica-Bold', 9)
        
        # Sixth Row
        c.setFont('Helvetica-Bold', 9)
        c.drawString(20,580,"Address :")
        st = []
        if gr.consignor_address:
            st = str(gr.consignor_address).splitlines()
            y = 580
            if gr.consignor:
                i = 0
            else:
                i=1
                st = st[1:]
                
            for row in st:
                c.drawString(80, y, row)
                y = y - 10
                i = i + 1
        
        c.drawString(20,605,"Consignor :")
        if gr.consignor:
            c.drawString(80,605,f"{gr.consignor.party_name}")
        else:
            if gr.consignor_address:
                st = str(gr.consignor_address).splitlines()
                c.drawString(80,605,f"{st[0]}")
                
        c.setFont('Helvetica-Bold', 9)
        c.drawString(360,580,"Address :")
        st = []
        if gr.consignee_address:
            st = str(gr.consignee_address).splitlines()
            y = 580
            if gr.consignee:
                i = 0
            else:
                i=1
                st = st[1:]
            for row in st:
                c.drawString(420, y, row)
                y = y - 10
                i = i + 1
        
        c.setFont('Helvetica-Bold', 9)
        c.drawString(360,605,"Consignee :")
        if gr.consignee:
            c.drawString(420,605,f"{gr.consignee.party_name}")
        else:
            if gr.consignee_address:
                st = str(gr.consignee_address).splitlines()
                c.drawString(420,605,f"{st[0]}")
        
                
        # Table
    
        c.line(60, 560, 60, 330)
        c.line(280, 560, 280, 300)
        c.line(340, 560, 340, 300)
        c.line(400, 560, 400, 300)
        c.line(500, 560, 500, 300)
        # Horizontal Line
        c.line(20, 535, 570, 535) # Top Head Line
        c.line(20, 330, 280, 330) # Bottom Line 1
        c.rect(20,300, 550, 260, fill=0)
        
        # Table Heads Text
        c.setFont('Helvetica-Bold', 7)
        c.drawString(25,550,"No. of")  #Row 1
        c.drawString(25,540,"Articles") #Row 1
        
        if gr.drop_location:
            c.drawString(25,314,f"Delivery At : {gr.drop_location.name}")  #Row 1 Bottom 
        
        desc_row = ['CONT. NO.','SEAL NO.','S/LINE','BKG. NO.','FPD','GST TO BE BORNE & PAID BY PARTY UNDER','REVERSE CHARGES','Challan/Invoice No','P.M. No.']
        c.drawString(110,550,"DESCRIPTION(SAID TO CONTAIN)") # Row 2
        y = 510
        for i in range(0,len(desc_row)):
            c.drawString(70,y,desc_row[i]) #Rate List Draw
            if desc_row[i] == 'GST TO BE BORNE & PAID BY PARTY UNDER':
                y -= 10
            else:
                y -= 20
        
        if gr.container_no:
            c.drawString(120,510,f"{gr.container_no}")  #Values Desc
            
        if gr.seal_no:
            c.drawString(120,490,f"{gr.seal_no}")  #Values Desc
       
        if gr.job:
            if gr.job.shipping_line:
                c.drawString(120,470,f"{gr.job.shipping_line.name}")  #Values Desc
        
        if gr.job:
            if gr.job.booking_no:
                c.drawString(120,450,f"{gr.job.booking_no}")  #Values Desc
       
        if gr.fpd:
            c.drawString(120,430,f"{gr.fpd.name}")  #Values Desc
            
        if gr.consignor:
            c.drawString(160,400,f"{gr.consignor.party_name}")  #Values Desc
            
        c.drawString(285,550,"Actual Weight")  #Row 3
        c.drawString(300,540,"Kgs") #Row 3
        
        c.line(280, 510, 340, 510) # Act. Weight
        c.drawString(282,500,"Charged Weight")  #Row 3
        c.drawString(300,490,"Kgs") #Row 3
        c.line(280, 483, 340, 483) # Act. Weight
        c.line(280, 415, 340, 415) # Act. Weight
        c.drawString(295,405,"Value of")  #Row 3
        c.drawString(300,395,"goods") #Row 3
        c.line(280, 390, 340, 390) # Act. Weight
        
        
        c.drawString(360,550,"RATE")  #Row 4
        
        c.drawString(430,550,"FREIGHT")  #Row 5
        c.drawString(430,520,"FIXED")  #Row 5
        c.drawString(430,540,"Rs.") #Row 5
        c.drawString(485,540,"P.") #Row 5
        c.line(480, 535, 480, 300) #Before P Vertical Line
        rates_list = ['','Statistical C.','Risk C.','S.C.','Hamali','Service Tax','Sub Total','Advance','Net Payable','Total']
        y = 515
        for i in range(0,10):
            c.drawString(350,y+10,rates_list[i]) #Rate List Draw
            if i == 1 or i == 7:
                c.line(340, y, 570, y) # After P Horizontal
        
            else:
                if not i == 9:
                    c.line(340, y, 500, y) # After P Horizontal
            
            y -= 23
        
        
        c.drawString(530,547,"To Pay") #Row 6
        c.rect(515,545, 10, 10, fill=0)
        c.drawString(510,515,"Rs.") #Row 6
        
        c.drawString(530,473,"PAID") #Row 6
        c.rect(515,470, 10, 10, fill=0)
        c.drawString(510,420,"Rs.") #Row 6
        c.drawString(510,375,"MR NO") #Row 6
    
        c.drawString(530,323,"BILLED") #Row 6
        c.rect(515,320, 10, 10, fill=0)
        
        # After Table 
        c.setFont('Helvetica', 7)
        if gr.gr_backloaded:
            c.drawString(20,285,f"1. All receiptable charges should be in the name of Consignor / Consignee")
            
        if gr.job:
            if gr.job.account and gr.job.account_address and not gr.gr_backloaded:
                    c.drawString(20,285,f"1. All receiptable charges should be in the name of M/S {gr.job.account.party_name} GSTNO :- {gr.job.account_address.corp_gstin}")
        # c.drawString(20,275,"taxable services has not been taken under the provision of the CENVAT credit Rules 2004")
        
        c.setFont('Helvetica-Bold', 7)
        c.drawString(430,285,"For PINKCITY LOGISTICS LIMITED")
        # Stamp Here ------------
        try:
            c.drawImage(stamp, 490, 245, width=0.5 * inch, height=0.5 * inch)
        except:
            pass
        
        # After Table 2nd Row
        c.drawString(20,235,"PAYMENT")
        c.drawString(470,235,"Booking Clerk/Manager")
        c.setFont('Helvetica', 7)
        c.drawString(22,223,"*CHEQUE / DRAFT SHALL BE ISSUED IN FAVOUR OF OWNER OF THE VEHICLE :- M/s Pinkcity Logistics Limited")
        c.rect(20,220, 370, 12, fill=0)
        
        
        # After Table 3 Row
        c.setFont('Helvetica', 7)
        c.drawString(20,200,"All goods booked at Owner's Risk Subject to terms & Conditions given overleaf.")
        c.drawString(20,190,"No responsibility for Leakage & Breakage.")
    
        c.setFont('Helvetica', 7)
        c.drawString(22,178,"VALID FOR DELIVERY OF GOODS")
        c.rect(20,175, 120, 12, fill=0)
        c.setFont('Helvetica', 7)
        
        c.setFont('Helvetica', 7)
        if gr.driver:
            c.drawString(20,145,f"Driver Name : {gr.driver.driver_name}")
            c.drawString(20,135,f"Mobile No : {gr.driver.phone_1}")
        else:
            c.drawString(20,145,f"Driver Name : ")
            c.drawString(20,135,f"Mobile No : ")
            
        c.drawString(20,125,"Port Wt. Dt :")
        
        if gr.remarks:
            c.drawString(20,115,f"Remark : {gr.remarks}")
        else:
            c.drawString(20,115,"Remark :")
        
        
        if gr.factory_address:
            c.drawString(20,105,f"Factory Address : {gr.factory_address}")
        else:
            c.drawString(20,105,"Factory Address : ")
        
        c.setFont('Helvetica-Bold', 7)
        #c.drawString(120,85,"All receiptable charges should be in the name of M/s YASH PAKKA LIMITED with GSTNO 09AAACY0482H1Z8")
        if gr.person_name:
            c.drawString(20,70,f"Contact Person Name : {gr.person_name}")
        else:
            c.drawString(20,70,"Contact Person Name : ")
       
        if gr.mobile_no:
            c.drawString(20,60,f"Contact Mobile No : {gr.mobile_no}")
        else:
            c.drawString(20,60,"Contact Mobile No :")
            
        
        c.drawString(180,30,"COMPUTER GENERATED LR, SIGNATURE NOT REQUIRED")
        
        c.showPage()
    c.save()
    return response




def can_pdf(request, id):
    data = CargoArrivalNotice.objects.filter(id=id).first()
    flag = 0
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="can_{data.id}.pdf"'
    c = canvas.Canvas(response)
    domain = Site.objects.get_current().domain
    setting = Logistic.objects.filter(id=data.company_type.id).first()
    
    c.line(25, 820, 575, 820)
    c.line(25, 10, 575, 10)
    c.line(25, 10, 25, 820)
    c.line(575, 820, 575, 10)
    
    logo = f'{setting.letter_head.url}' 
    c.drawImage(logo, 40, 730, width=5 * inch, height=1.1 * inch,mask="auto")
    c.rect(410,780, 150, 20, fill=0) #LEFT RECT
    
    c.line(25, 715, 575, 715) # H1
    c.setFont("Helvetica-Bold",11)
    c.drawString(30,700,f"ARRIVAL NOTICE NO. : {data.arrival_notice_no}")
    c.drawString(415,785,f"CARGO ARRIVAL NOTICE")
    
    c.line(93, 695, 93, 500) # Divide Start Line Vertical Top
    c.line(300, 695, 300, 500) # Divide Middle Line Vertical Top
    c.line(375, 695, 375, 500) # Divide End Line Vertical Top
    c.setFont("Helvetica-Bold",8)
    c.line(25, 695, 575, 695) # H2  Full
    
    # RIGHT HALF CONTENT START
    c.drawString(305,685,"POL :")
    c.drawString(305,670,"POD :")
    c.drawString(305,655,"FINAL DEST. :")
    c.drawString(305,640,"CARRIER :")
    c.drawString(305,625,"VESSEL :")
    c.drawString(305,610,"MASTER B/L :")
    c.drawString(305,595,"HOUSE B/L :")
    c.drawString(305,580,"AMS :")
    c.drawString(305,565,"ORIGIN :")
    c.drawString(305,550,"CARGO LOC.:")
    c.drawString(305,535,"FREIGHT TYPE:")
    c.drawString(305,520,"IT :")
    c.drawString(305,505,"IT LOCATION :")
    # RIGHT HALF CONTENT END
    
    table_limit = 38
     
    c.setFont("Helvetica",8)
    if data.pol:
        c.drawString(380,685,f"{data.pol.name}")
           
    if data.etd:
        c.drawString(500,685,f"ETD : {data.etd}")    
    
    
    if data.pod:
        c.drawString(380,670,f"{data.pod.name}")
           
    if data.eta:
        c.drawString(500,670,f"ETA : {data.eta}")  
    
    if data.fpd_date:     
        c.drawString(500,655,f"Date : {data.fpd_date}")   
         
    if data.final_destination:
        c.drawString(380,655,f"{data.final_destination.name}")
        
    if data.shipping_line:
        c.drawString(380,640,f"{data.shipping_line.name}")
        
    if data.vessel_voyage:
        c.drawString(380,625,f"{data.vessel_voyage}")
        
    if data.mbl:
        c.drawString(380,610,f"{data.mbl}")
               
    if data.mbl_date:
        c.drawString(500,610,f"Date : {data.mbl_date}")
        
    if data.hbl:
        c.drawString(380,595,f"{data.hbl} / {data.hbl.bl_type}")
 
        
        
    if data.hbl_date:
        c.drawString(500,595,f"Date : {data.hbl_date}")
        
    if data.ams_hbl:
        c.drawString(380,580,f"{data.ams_hbl}")
    
    if data.job:
        if data.job.ams_date:
            c.drawString(500,580,f"Date : {data.job.ams_date}")
   
    if data.pol:
        c.drawString(380,565,f"{data.pol.name}")
   
    

        
    if data.freight_location:
        c.drawString(380,550,f"{data.freight_location.name}")
        
    if data.firm_code:
        c.drawString(500,550,f"Firm Code : {data.firm_code}")
        
    if data.job.freight_term:
        c.drawString(380,535,f"{data.firm_cofreight_termde}")
   
            
    if data.it_no:
        c.drawString(380,520,f"{data.it_no}")
        
    if data.it_location:
        c.drawString(380,505,f"{data.it_location}")
        
    if data.it_date:
        c.drawString(500,505,f"Date : {data.it_date}")
        
        
    c.setFont("Helvetica-Bold",7)
    
    c.drawString(30,685,"SHIPPER :")
    c.setFont("Helvetica",8)
    if data.shipper:
        c.drawString(96,685,f"{data.shipper.party_name}")
    if data.notify_party_2_location:
        st = str(data.notify_party_2_location).splitlines()
        y = 675
        i = 0
        for row in st:
            c.drawString(96, y, row)
            y = y - 10
            i = i + 1
    
    c.setFont("Helvetica-Bold",8)
    
    
    
    
    c.drawString(30,620,"CONSIGNEE :")
    c.setFont("Helvetica",8)
    if data.consignee:
        c.drawString(96,620,f"{data.consignee}")
        
    c.setFont("Helvetica-Bold",8)
    
    c.setFont("Helvetica",8)
    if data.consignee_location:
        st = str(data.consignee_location).splitlines()
        y = 610
        i = 0
        for row in st:
            c.drawString(96, y, row)
            y = y - 10
            i = i + 1
        
        
    
    c.setFont("Helvetica-Bold",8)
    
    c.line(300, 680, 575, 680) # H3 Full
    c.line(300, 665, 575, 665) # H4  Full
    
    c.line(300, 650, 575, 650) # H5 1  Half Right
    c.line(25, 635, 575, 635) # H6 1  Half Right
    c.line(300, 620, 575, 620) # H7 1  Half Right
    c.line(300, 605, 575, 605) # H8 Full
    c.drawString(30,560,"NOTIFY :")
    c.setFont("Helvetica",8)
    
    if data.notify_party_1:
        c.drawString(96,560,f"{data.notify_party_1.party_name}")
        
    if data.notify_party_1_location:
        st = str(data.notify_party_1_location).splitlines()
        y = 550
        i = 0
        for row in st:
            c.drawString(96, y, row)
            y = y - 10
            i = i + 1

    if data.move_type:
        c.drawString(96,505,f'{data.move_type}')
    
    c.setFont("Helvetica-Bold",8)
    c.line(300, 590, 575, 590) # H9 1  Half Right
    c.line(25, 575, 575, 575) # H10 1  Half Right
    c.line(300, 560, 575, 560) # H11 Full
    c.line(300, 545, 575, 545) # H11 Full

    c.line(300, 530, 575, 530) # H12 1  Half Right
    c.line(25, 515, 575, 515) # H13 Half
    c.line(25, 500, 575, 500) # H14 Full
    c.drawString(30,505,"MOVE TYPE :")
    
    c.setFont("Helvetica",8)
   
   
        
    c.setFont("Helvetica-Bold",8)
    # Table Part
    c.line(25, 485, 575, 485) # H15 Full
    c.drawString(30,490,"MARKS & NO.S")
    
    c.setFont("Helvetica",8)
    if data.marks:
        marks = str(data.marks).splitlines()
        length = len(marks)
        
        if length > table_limit:
            flag = 1
        
        y = 475
        i = 0
        for row in marks[:table_limit]:
            
            c.drawString(30, y, row)
            y = y - 10
            i = i + 1
           
    
    c.setFont("Helvetica-Bold",8)
    
    c.line(110, 500, 110, 100) # AFTER MARKS AND NO.S Line Vertical Top
    
    c.drawString(115,490,"PKGS")
    
    c.setFont("Helvetica",8)
    if data.no_of_packages:
        no_of_packages = str(data.no_of_packages).splitlines()
        length = len(no_of_packages)
        
        if length > table_limit:
            flag = 1
        
        y = 475
        i = 0
        for row in no_of_packages[:table_limit]:
            
            c.drawString(115, y, row)
            y = y - 10
            i = i + 1
            
    
    c.setFont("Helvetica-Bold",8)
    c.line(155, 500, 155, 100) # AFTER PKGS Line Vertical Top
    
    c.drawString(260,490,"DESCRIPTION OF GOODS")
    
    c.setFont("Helvetica",9)
    if data.desc_of_packages:
        desc_of_packages = str(data.desc_of_packages).splitlines()
        length = len(desc_of_packages)
        
        if length > table_limit:
            flag = 1
        
        y = 475
        i = 0
        for row in desc_of_packages[:table_limit]:
            
            c.drawString(160, y, row)
            y = y - 10
            i = i + 1
        
    
    c.setFont("Helvetica-Bold",8)
    c.line(455, 500, 455, 100) # AFTER DESC Line Vertical Top
    
    c.drawString(460,490,"KGS")
    
    c.setFont("Helvetica",8)
    if data.gross_weight:
        gross_weight = str(data.gross_weight).splitlines()
        length = len(gross_weight)
        
        if length > table_limit:
            flag = 1
        
        y = 475
        i = 0
        for row in gross_weight[:table_limit]:
           
            c.drawString(460, y, row)
            y = y - 10
            i = i + 1
           
    
    c.setFont("Helvetica-Bold",8)
    
    c.line(515, 500, 515, 100) # AFTER KGS Line Vertical Top
    
    c.drawString(520,490,"CBM")
    
    c.setFont("Helvetica",8)
    if data.measurement:
        measurement = str(data.measurement).splitlines()
        length = len(measurement)
        
        if length > table_limit:
            flag = 1
        
        y = 475
        i = 0
        for row in measurement[:table_limit]:
            if y >= 120:
                c.drawString(520, y, row)
                y = y - 10
                i = i + 1
            else:
                pass
    
    c.setFont("Helvetica-Bold",8)
  
    c.line(25, 100, 575, 100) # H16 Full
    
    # c.rect(40,80, 200, 60, fill=0) #LEFT RECT
    # c.drawString(90,128,"BILLING")
    # c.drawString(180,128,"USD")
    # c.drawString(90,108,"TOTAL COLLECT")
    
    # try:
    #     for i in data.job.manifest_job.first().manifest_charges_collect.all():
    #         total_collect += i.total
    # except:
    #     total_collect = 0
    
    # c.drawString(180,108,f"{total_collect}")
    # c.line(40, 120, 240, 120) # LEFT RECT HORIZONTAL 1
    # c.line(40, 100, 240, 100) # LEFT RECT HORIZONTAL 2
    # c.line(170, 140, 170, 100)  # LEFT RECT VERTICAL 1
    # c.drawString(53,87,"ORIGINAL BILL OF LADING REQUIRED")
    # c.drawString(50,70,"PLEASE MAKE ALL CHECKS TO PINKCITY")
    # c.drawString(50,60,"TRANSOCEANIC INC.")
    
    # c.rect(300,40, 250, 100, fill=0) # RIGHT RECT
    # c.drawString(382,128,"PLEASE TRANSFER")
    # c.drawString(355,118,"PINKCITY TRANSOCEANIC INC.")
    
    # c.drawString(305,105,"A/C # - 237034433238")
    # c.drawString(305,90,"BANK OF AMERICA, NA")
    # c.drawString(305,75,"222 BROADWAY, NEWYORK")
    # c.drawString(305,60,"SWIFT CODE - BOFAUS3N")
    # c.drawString(305,45,"ROUTING NUMBER - 053000196")
  
  
    c.drawString(30,60,"All collected charges and only original B/L must be surrendered prior release of cargo.")
    c.drawString(80,20,"REGS OFF :  10DB DESHIRE LANE, MORRISVILLE, NC 27560, NORTH CAROLINA, TEL: +1(919)521-5270")
    
    
    
    if flag == 1:
        c.showPage()
        
        
        
        # *************************** GUI Part ******************************
        c.line(13, 785, 585, 785)
        c.line(13, 20, 585, 20)
        c.line(13, 20, 13, 785)
        c.line(585, 785, 585, 20)
        
    
        
        c.setFont('Helvetica', 15)
        c.drawString(400, 790, 'REF # -' + str(data.arrival_notice_no))
        
        
        c.line(155, 785, 155, 20)
        c.setFont('Helvetica-Bold',8)
        c.drawString(15, 775, 'MARKS & NO.S')
        c.setFont('Helvetica',8)
        if data.marks:
            marks = str(data.marks).splitlines()
            length = len(marks)
            y = 755
        
            
                
            for row in marks[table_limit:]:
                c.drawString(15, y, row)
                y = y - 10
      
        c.line(110, 785, 110, 20) # AFTER MARKS AND NO.S Line Vertical Top
        c.setFont('Helvetica-Bold',8)
        c.drawString(115,775,"PKGS")        
        c.setFont('Helvetica',8)
        no_of_pkg = str(data.no_of_packages).splitlines()
        length = len(no_of_pkg)
        y = 755
        i = 35
        if length >= 28:
                flag = 1
        
        for row in no_of_pkg[table_limit:]:
            c.drawString(33, y, row)
            y = y - 10
   
            
        c.setFont('Helvetica-Bold',8)
        c.drawString(245, 775, 'DESCRIPTION OF GOODS ')
        c.setFont('Helvetica',8)
        
        if data.desc_of_packages:
            desc_of_packages = str(data.desc_of_packages).splitlines()
            y = 755
   
            length = len(desc_of_packages)
            
            for row in desc_of_packages[table_limit:]:
        
                c.drawString(160, y, row)
                y = y - 10
         
            
        c.line(480, 785, 480, 20)
        c.setFont('Helvetica-Bold',8)
        c.drawString(483, 775, 'KGS')
        c.setFont('Helvetica',8)
        if data.gross_weight:
            gross = str(data.gross_weight).splitlines()
            length = len(gross)
            y = 755
   
  
            
            for row in gross[table_limit:]:
                c.drawString(483, y, row)
                y = y - 10
        
            
        
        

        c.line(528, 785, 528, 20)
        c.setFont('Helvetica-Bold',8)
        c.drawString(537, 775, 'CBM')
        c.setFont('Helvetica',8)
 
        
        if data.measurement:
            mes = str(data.measurement).splitlines()
            length = len(mes)
            y = 755
   
       
            
            for row in mes[table_limit:]:
                c.drawString(532, y, row)
                y = y - 10
     
            
        
        
        

        c.line(13, 770, 585, 770)
        
    
    c.showPage()
    c.save()
    return response

