from django.forms.models import inlineformset_factory
from django import forms
from accounting.models import ContraVoucher, DebitNote, InvoicePayable, InvoiceReceivable, CreditNote, PaymentVoucher, RecieptVoucher,IndirectExpense,Manifest,TrailorExpense,Loan,Salary,Journal
from masters.models import Party,GRMaster,JobHBL,JobMaster

class SalaryForm(forms.ModelForm):
   
    class Meta:
        model = Salary
        exclude = ('net_amount',)
        widgets = {
            "company_type":forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            "employee":forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            "salary_currency":forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            # "bank":forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            "date":forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
            "basic":forms.NumberInput(attrs={'class':'form-control','required':True,'step':0.001}),
            "tds_amount":forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.001}),
            "esi_amount":forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.001}),
            "pf_amount":forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.001}),
    
            
        }

class IndirectOnAccountRecieptVoucherForm(forms.ModelForm):
   
    class Meta:
        model = RecieptVoucher
        exclude = ()
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
           
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'recieve_in': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'cash': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'voucher_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'voucher_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'to_bank': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'instrument_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'particular': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'received_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01}),
            'received_amount_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'advance_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':"0.01",'required':True}),
            'narration': forms.TextInput(attrs={'class': 'form-control form-control-sm'}), 
            'bank_charges' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
        }

class LoanForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            'company_type':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'category':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'loan_no':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'loan_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'loan_type':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'rate_type':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'start_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'end_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            
            'bank':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'loan_duration':forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True}),
            'principal_amount':forms.NumberInput(attrs={'step':0.00001,'class':'form-control form-control-sm','required':True}),
            'interest_rate':forms.NumberInput(attrs={'step':0.00001,'class':'form-control form-control-sm','required':True}),
            'interest_amount':forms.NumberInput(attrs={'step':0.00001,'class':'form-control form-control-sm','required':True,'readonly':True}),
            'total_amount':forms.NumberInput(attrs={'step':0.00001,'class':'form-control form-control-sm','required':True,'readonly':True}),
            'monthly_emi':forms.NumberInput(attrs={'step':0.00001,'class':'form-control form-control-sm','required':True,'readonly':True}),
            'paid_tenure':forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True}),
        }

class ManifestForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = Manifest
        fields = '__all__'
        widgets = {
           
            'company_type':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'job_no':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'manifest_no':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'manifest_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'manifest_currency':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'manifest_ex_rate':forms.NumberInput(attrs={'class':'form-control form-control-sm'}),
            'customer':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'customer_address':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'payment':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'payment_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
            
            
            
        }

class TrailorExpenseForm(forms.ModelForm):
   
    class Meta:
        model = TrailorExpense
        fields = '__all__'
        widgets = {
            'company_type':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'job_no':forms.Select(attrs={'class':'form-control form-control-sm','required':False}),
            'trailor_no':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'driver':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'container_no':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cash_expense':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'card_expense':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'pump_expense':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'own_hire':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            
            'net_amount':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'fast_card_expense':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'remarks':forms.Textarea(attrs={'class':'form-control form-control-sm','rows':3})
            
            
        }

class IndirectExpenseForm(forms.ModelForm):
    class Meta:
        model = IndirectExpense
        fields = '__all__'
        widgets = {
            'job_no':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'company_type':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'vendor':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'bill_no':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'bill_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'due_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'remarks':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'gross_amount':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'gst_amount':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'advance_amount':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'net_amount':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'currency_ex_rate':forms.NumberInput(attrs={'step':0.001,'class':'form-control form-control-sm','required':True}),
            'tds_amount':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'tds_section': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'tds_percentage': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'invoice_currency':forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            

            
        }

class InvoiceReceivableForm(forms.ModelForm):
    bill_to = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    shipper = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    
    gr_options = forms.ModelMultipleChoiceField(queryset=GRMaster.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
    hbl_options = forms.ModelMultipleChoiceField(queryset=JobHBL.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
    
    job_no = forms.ModelChoiceField(queryset=JobMaster.objects.exclude(job_status="Closed").exclude(is_deleted=True).all(),required=True,widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = InvoiceReceivable
        exclude = ()

        widgets = {
            'invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
           
            'date_of_invoice': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'detention_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
            'detention_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'mode_of_invoice': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'job_no': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'invoice_currency': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'currency_ex_rate': forms.NumberInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'quotation': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'bill_to': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'bill_to_address': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'shipper_address': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'shipper': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'is_proforma': forms.CheckboxInput(),
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'journal': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'gst_applicable': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'invoice_status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'container_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'type_of_container': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'account_number': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'gross_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'gst_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'net_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'remark_on_invoice': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'cols': 10}),
            'type_of_invoice': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'tds_section': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'tds_percentage': forms.NumberInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'deductible_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'tds_payable': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
        }

class AmmendInvoiceReceivableForm(forms.ModelForm):
    
    class Meta:
        model = InvoiceReceivable
        fields = [
            'final_invoice_no',
            'category',
            'einvoice_date',
            'mode_of_invoice',
            'bill_to',
            'bill_to_address',
            'inv_type_2',
            'invoice_status',
            'gross_amount',
            'gst_amount',
            'advance_amount',
            'net_amount',
            'remark_on_invoice',
            'type_of_invoice',
        ]

        widgets = {
            'final_invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'einvoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True,}, format="%Y-%m-%d"),
            'mode_of_invoice': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'bill_to': forms.Select(attrs={'class': 'form-control form-control-sm','disabled':True}),
            'bill_to_address': forms.Select(attrs={'class': 'form-control form-control-sm','disabled':True}),
            'inv_type_2': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'invoice_status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'gross_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'gst_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'advance_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'net_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'remark_on_invoice': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'cols': 10}),
            'type_of_invoice': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
        }

class InvoicePayableForm(forms.ModelForm):
    bill_from = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    
    job_no = forms.ModelChoiceField(queryset=JobMaster.objects.exclude(job_status="Closed").exclude(is_deleted=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = InvoicePayable
        fields = '__all__'

        widgets = {
            'invoice_no': forms.HiddenInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'purchase_invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required':True}),
            'date_of_invoice': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'job_no': forms.Select(attrs={'class': 'form-control form-control-sm','required':False}),
            'bill_from': forms.Select(attrs={'class': 'form-control form-control-sm', 'required':True}),
            'bill_from_address': forms.Select(attrs={'class': 'form-control form-control-sm', 'required':True}),
            'invoice_currency': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'currency_ex_rate': forms.NumberInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'round_off': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.001}),
           
            
            'due_date': forms.DateInput(attrs={'type': 'date', 'required':True, 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
            'invoice_status': forms.Select(attrs={'class': 'form-control form-control-sm',}),
            
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'party_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'vendor': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            
            'is_rcm': forms.CheckboxInput(),
           
            
          
           
            'gross_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'gst_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            
            'tds_payable': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'net_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'remark_on_invoice': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'cols': 10}),
            'tax_status': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'tds_section': forms.Select(attrs={'class': 'form-control form-control-sm'}),

            'tds_percentage': forms.NumberInput(attrs={'class': 'form-control form-control-sm','required':True}),
            
            
            # 'invoice_file_1':forms.FileInput(attrs={}),
            # 'invoice_file_2':forms.FileInput(attrs={}),
            # 'invoice_file_3':forms.FileInput(attrs={}),
            # 'invoice_file_4':forms.FileInput(attrs={}),
            # 'invoice_file_5':forms.FileInput(attrs={}),
            
        }

class CreditNoteForm(forms.ModelForm):
    bill_to = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=True,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    reference_invoice = forms.ModelChoiceField(queryset=InvoiceReceivable.objects.filter(is_einvoiced=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm','required':False}))
    hbl_options = forms.ModelMultipleChoiceField(queryset=JobHBL.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
    
    job_no = forms.ModelChoiceField(queryset=JobMaster.objects.exclude(job_status="Closed").exclude(is_deleted=True).all(),required=True,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = CreditNote
        exclude = ()

        widgets = {
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'account_number': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'credit_note_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','readonly':True}),
            'date_of_note': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':False}, format="%Y-%m-%d"),
            'job_no': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'invoice_currency': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'currency_ex_rate': forms.NumberInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'is_final': forms.CheckboxInput(attrs={}),
            'is_rcm': forms.CheckboxInput(attrs={}),
            
            'hbl_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'mbl_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'origin': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'destination': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'bill_to': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'bill_to_address': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'flight_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'awb_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'docket_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'shipper': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'shipper_address': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            
            
            'gross': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'volume': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'nett': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'total_packages': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'total_packages_type': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'total_cbm': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'commodity': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'commodity_type': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'container_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'container_type': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'invoice_status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            
            
            'shipping_line': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'vessel_voyage_id': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'vessel_voyage_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
           
            
            'air_line': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'flight_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
            'account_number': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'gross_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'gst_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'advance_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'net_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'remark_on_note': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'cols': 10}),
            
        }

class AmmendCreditNoteForm(forms.ModelForm):
 
    class Meta:
        model = CreditNote
        fields = [
            'category',
            'final_invoice_no',
            'einvoice_date',
            'bill_to',
            'bill_to_address',
            'gross_amount',
            'gst_amount',
            'advance_amount',
            'net_amount',
            'is_rcm',
        ]

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'final_invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'einvoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'bill_to': forms.Select(attrs={'class': 'form-control form-control-sm','disabled':True}),
            'bill_to_address': forms.Select(attrs={'class': 'form-control form-control-sm','disabled':True}),
            'gross_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'gst_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'advance_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'net_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'is_rcm': forms.CheckboxInput(attrs={}),
           
        }

class DebitNoteForm(forms.ModelForm):
    bill_from = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    
    job_no = forms.ModelChoiceField(queryset=JobMaster.objects.exclude(job_status="Closed").exclude(is_deleted=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = DebitNote
        exclude = ()

        widgets = {
            'debit_note_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'date_of_note': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'bill_from_vendor': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'party_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'job_no': forms.Select(attrs={'class': 'form-control form-control-sm','required':False}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'invoice_currency': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'currency_ex_rate': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}), 
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'bill_from': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'bill_from_address': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'invoice_status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'account_number': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'gross_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'gst_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'advance_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'net_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'remark_on_note': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'cols': 10}),
            
        }

class RecieptVoucherForm(forms.ModelForm):
    
    class Meta:
        model = RecieptVoucher
        exclude = ()
        widgets = {
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'voucher_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':"Generate After Save",'readonly':True}),
            'voucher_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'recieve_in': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'bank': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'cash': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'instrument_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'narration': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'advance_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01,'required':True,'min':'1','readonly':True}),
            'bank_charges' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_cgst' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_sgst' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_igst' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_tax' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
        }

class PaymentVoucherForm(forms.ModelForm):
    party_name = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = PaymentVoucher
        exclude = ()

        widgets = {
            'voucher_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Generate After Save','readonly':True}),
            'vendor': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'party_name': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'party_address': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'payment_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'pay_from': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
           
            'bank_clearing_date_payment': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}, format="%Y-%m-%d"),
            'voucher_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'from_bank': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'bank': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'cash': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'to_party_bank': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
           
            'instrument_no': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
          
            'no_of_days': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'narration': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'tds': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01}),
            'payment_tds_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01,'required':True}),
            'paid_amount': forms.HiddenInput(attrs={'class': 'form-control form-control-sm'}),
            'net_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01,'required':True}),
            'advance_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01,'required':True}),
            'adjustment_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01,'required':True}),
            'bank_charges' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_cgst' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_sgst' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_igst' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            'bank_charges_tax' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            
        }

class ContraVoucherForm(forms.ModelForm):
    class Meta:
        model = ContraVoucher
        exclude = ()

        widgets = {
            'voucher_date' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'bank_cash_from' : forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'bank_cash_to' : forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'account_from' : forms.Select(attrs={'class':'form-control form-control-sm'}),
            'account_to' : forms.Select(attrs={'class':'form-control form-control-sm'}),
            'contra_choice' : forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'company_type' : forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'cash' : forms.Select(attrs={'class':'form-control form-control-sm'}),
            'amount' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True}),
            'instrument_no' : forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'bank_charges' : forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.01}),
            
            
        }

class JournalVoucherForm(forms.ModelForm):
    class Meta:
        model = Journal
        exclude = ()

        widgets = {
            'date' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'company_type': forms.Select(attrs={'class':'form-control form-control-sm','required':True}),
            'total_dr_amount': forms.HiddenInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.001,'readonly':True}),
            'total_cr_amount': forms.HiddenInput(attrs={'class':'form-control form-control-sm','required':True,'step':0.001,'readonly':True}),
            'description': forms.Textarea(attrs={'class':'form-control form-control-sm','required':True,'rows':2}),
            
        }


