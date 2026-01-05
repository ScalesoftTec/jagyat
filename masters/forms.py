from django import forms

from masters.models import *

from django.db.models import Q



class PartyForm(forms.ModelForm):
    party_type =   forms.ModelMultipleChoiceField(queryset=PartyType.objects.all(),required=False,
                                                    widget=forms.SelectMultiple(attrs={'class': 'select2 w-100 form-control', 'required':True}))
# widget=forms.SelectMultiple(attrs={'class': 'select2', 'required': False})
    class Meta:
        model = Party
        fields = '__all__'
        widgets = {
            'party_name': forms.TextInput(attrs={'class': 'form-control'}),
            'alias': forms.TextInput(attrs={'class': 'form-control'}),
            'bl_type': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'fin_non_fin': forms.Select(attrs={'class': 'form-control'}),
            'for_station': forms.Select(attrs={'class': 'form-control'}),
            'party_company_type': forms.Select(attrs={'class': 'form-control'}),
            'tally_under': forms.Select(attrs={'class': 'form-control'}),
            'under': forms.Select(attrs={'class': 'form-control'}),
            'account_manager': forms.Select(attrs={'class': 'form-control'}),
            'party_short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'registered_gst': forms.TextInput(attrs={'class': 'form-control'}),
            'registered_address': forms.Textarea(attrs={'class': 'form-control','rows':3}),
            'party_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 10}),
            'iec_code': forms.TextInput(attrs={'class': 'form-control'}),
            'cin_number': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_transfered_to_tally': forms.CheckboxInput(),
            'kyc_form': forms.FileInput(attrs={'type':'file','class': 'form-control'}),
            'photo_id': forms.FileInput(attrs={'type':'file','class': 'form-control'}),
            'gst_certificate': forms.FileInput(attrs={'type':'file','class': 'form-control'}),
            'other_document': forms.FileInput(attrs={'type':'file','class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            
             'opening_balance': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01}),
            'opening_in': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'opening_date': forms.DateInput(attrs={'type':'date','class': 'form-control form-control-sm'}),
          
          
        }



# class PartyForm(forms.ModelForm):
#     party_type =   forms.ModelMultipleChoiceField(queryset=PartyType.objects.all(),required=False,
#                                                     widget=forms.CheckboxSelectMultiple(attrs={'required':False}))

#     class Meta:
#         model = Party
#         fields = '__all__'
#         widgets = {
#             'party_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'alias': forms.TextInput(attrs={'class': 'form-control'}),
#             'bl_type': forms.TextInput(attrs={'class': 'form-control'}),
#             'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
#             'fin_non_fin': forms.Select(attrs={'class': 'form-control'}),
#             'for_station': forms.TextInput(attrs={'class': 'form-control'}),
#             'party_company_type': forms.Select(attrs={'class': 'form-control'}),
#             'tally_under': forms.Select(attrs={'class': 'form-control'}),
#             'under': forms.Select(attrs={'class': 'form-control'}),
#             'account_manager': forms.Select(attrs={'class': 'form-control'}),
#             'party_short_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'registered_gst': forms.TextInput(attrs={'class': 'form-control'}),
#             'registered_address': forms.Textarea(attrs={'class': 'form-control','rows':3}),
           
#             'party_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 10}),
#             'iec_code': forms.TextInput(attrs={'class': 'form-control'}),
#             'cin_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'credit_days': forms.NumberInput(attrs={'class': 'form-control'}),
#             'is_transfered_to_tally': forms.CheckboxInput(),
#             'kyc_form': forms.FileInput(attrs={'type':'file','class': 'form-control'}),
#             'photo_id': forms.FileInput(attrs={'type':'file','class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={}),
          
#         }



class PartyAddressForm(forms.ModelForm):
    class Meta:
        model = PartyAddress
        fields = '__all__'
        widgets = {
            'party': forms.Select(attrs={'class': 'form-control'}),
          
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_address_line3': forms.TextInput(attrs={'class': 'form-control'}),

            'corp_country': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_state': forms.Select(attrs={'class': 'form-control'}),
            'corp_city': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_email': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_website': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_gstin': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_zip': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_fax': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'corp_pan': forms.TextInput(attrs={'class': 'form-control'}),

         
          
        }


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_code': forms.TextInput(attrs={'class': 'form-control'})
        }

class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = '__all__'
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class BillingHeadForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=BillingHead.objects.filter(is_head=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = BillingHead
        fields = '__all__'
        exclude = ['sales_head','purchase_head']
        widgets = {
            'billing_head': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'alias': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'hsn_code': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'gst': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'under': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'tally_group': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'always_igst': forms.CheckboxInput(attrs={}),
            'is_head': forms.CheckboxInput(attrs={}),
            'is_service': forms.CheckboxInput(attrs={}),
            'is_disabled': forms.CheckboxInput(attrs={})
        }

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
        widgets = {
            'vendor_name' : forms.TextInput(attrs={'class':'form-control'}),
            'address_line1' : forms.TextInput(attrs={'class':'form-control'}),
            'address_line2' : forms.TextInput(attrs={'class':'form-control'}),
            'address_line3' : forms.TextInput(attrs={'class':'form-control'}),
            'country' : forms.TextInput(attrs={'class':'form-control'}),
            'state' : forms.Select(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            'tel' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'gstin' : forms.TextInput(attrs={'class':'form-control'}),
            'zip' : forms.TextInput(attrs={'class':'form-control'}),
            'fax' : forms.TextInput(attrs={'class':'form-control'}),
            'contact' : forms.TextInput(attrs={'class':'form-control'}),
            'pan' : forms.TextInput(attrs={'class':'form-control'}),
            'remarks' : forms.TextInput(attrs={'class':'form-control'}),
            
            'opening_balance': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01}),
            'opening_in': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'opening_date': forms.DateInput(attrs={'type':'date','class': 'form-control form-control-sm'}),
          
        }

class LedgerCategoriesForm(forms.ModelForm):
    class Meta:
        model = LedgerCategories
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm form-control form-control-sm-sm','required':True}),
            'type': forms.Select(attrs={'class': 'form-control form-control-sm form-control form-control-sm-sm','required':True}),
            'parent': forms.Select(attrs={'class': 'form-control form-control-sm form-control form-control-sm-sm'}),
            'include_in': forms.Select(attrs={'class': 'form-control form-control-sm form-control form-control-sm-sm'}),
            'head_type': forms.Select(attrs={'class': 'form-control form-control-sm form-control form-control-sm-sm'}),
            
        }

class LedgerSubCategoriesForm(forms.ModelForm):
    class Meta:
        model = LedgerSubCategories
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'category': forms.Select(attrs={'class': 'form-control','required':True}),
            'account_category': forms.Select(attrs={'class': 'form-control','required':True}),
        }

# class LedgerForm(forms.ModelForm):
#     party = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
#     class Meta:
#         model = LedgerMaster
#         fields = '__all__'
#         widgets = {
#             'vendor': forms.Select(attrs={'class': 'form-control','required':True}),
#             'party_type': forms.Select(attrs={'class': 'form-control'}),
#             'bank': forms.Select(attrs={'class': 'form-control'}),
#             'company_type': forms.Select(attrs={'class': 'form-control','required':True}),
#             'tally_group': forms.Select(attrs={'class': 'form-control','required':True}),
           
#             'party_address': forms.Select(attrs={'class': 'form-control'}),
#             'ledger_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
#             'under': forms.Select(attrs={'class': 'form-control','required':True}),
#             'opening_balance': forms.NumberInput(attrs={'class': 'form-control','required':True,'step':0.01}),
#             'balance_in': forms.Select(attrs={'class': 'form-control','required':True}),
#             'opening_date': forms.DateInput(attrs={'class': 'form-control','required':True,'type':'date'}),
#         }


class LedgerForm(forms.ModelForm):
    party = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = LedgerMaster
        fields = '__all__'
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'party_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'bank': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'company_type': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'tally_group': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
           
            'party_address': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'ledger_name': forms.TextInput(attrs={'class': 'form-control form-control-sm','required':True}),
            'under': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'opening_balance': forms.NumberInput(attrs={'class': 'form-control form-control-sm','required':True,'step':0.01}),
            'balance_in': forms.Select(attrs={'class': 'form-control form-control-sm','required':True}),
            'opening_date': forms.DateInput(attrs={'class': 'form-control form-control-sm','required':True,'type':'date'}),
        }

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'
        widgets = {
            'account_no': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'branch_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'beneficiary_name': forms.TextInput(attrs={'class': 'form-control'}),
            'swift_code': forms.TextInput(attrs={'class': 'form-control'}),
             'opening_balance': forms.NumberInput(attrs={'class': 'form-control form-control-sm','step':0.01}),
            'opening_in': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'opening_date': forms.DateInput(attrs={'type':'date','class': 'form-control form-control-sm'}),
          
        }
        
class UOMForm(forms.ModelForm):
    class Meta:
        model = UOM
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'short_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'decimal_places': forms.TextInput(attrs={'class': 'form-control','required':True}),
        }
        
class BatteryForm(forms.ModelForm):
    class Meta:
        model = Battery
        fields = '__all__'
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'model_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'vendor_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'battery_no': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'amount': forms.TextInput(attrs={'class': 'form-control','required':True}),
        }
        
class TyreForm(forms.ModelForm):
    class Meta:
        model = Tyre
        fields = '__all__'
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control','required':True}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'model_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'vendor_name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'tyre_no': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'amount': forms.TextInput(attrs={'class': 'form-control','required':True}),
        }
        
        
     
class BookingMasterForm(forms.ModelForm):
    class Meta:
        model = BookingMaster
        fields = '__all__'
        widgets = {
            'company_type':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'module':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'booking_no':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'booking_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'ref_no':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'weight':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'shipper':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'consignee':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'agent':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'pol':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'pod':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'fpod':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'shipping_line':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'container_size':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'no_of_container':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'cbm':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'mbl_no':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'hbl_no':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'buying_rate':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'selling_rate':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'etd':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'sales_person':forms.Select(attrs={'class':'form-control form-control-sm'}),
            
            'actual_weight':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'volume_weight':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'party_name':forms.Select(attrs={'class':'form-control form-control-sm'}),
        }
        

        
class JobForm(forms.ModelForm):
    # party = Party.objects.filter(is_active=True).all()

    def __init__(self, *args, **kwargs):
        party_queryset = Party.objects.filter(is_active=True).all()
        job = kwargs.pop('job', None)
        update = kwargs.pop('update', False)
        
        if not update:
            booking_queryset = BookingMaster.objects.filter(job_booking=None).all()
        else:
            print("I am update part")
            print(job.id)
            booking_queryset = BookingMaster.objects.filter(Q(Q(job_booking=None) | Q(job_booking=job))).all()
            
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['booking'].queryset = booking_queryset.order_by('-id')
        self.fields['account'].queryset = party_queryset
        self.fields['shipper'].queryset = party_queryset
        self.fields['consignee'].queryset = party_queryset
        self.fields['notify_party'].queryset = party_queryset
        self.fields['booking_party'].queryset = party_queryset
        self.fields['overseas_agent'].queryset = party_queryset
        self.fields['broker'].queryset = party_queryset
        self.fields['forwarder'].queryset = party_queryset
        self.fields['delivery'].queryset = party_queryset
        self.fields['importer'].queryset = party_queryset

   
    
    class Meta:
        model = JobMaster
        fields = '__all__'
        widgets = {
            
            'company_type': forms.Select(attrs={'class': 'form-control','required':True}),
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'alternate_company': forms.Select(attrs={'class': 'form-control'}),
            'inquiry':forms.Select(attrs={'class':'form-control'}),
            'job_no': forms.TextInput(attrs={'class': 'form-control','required':True,'readonly':True}),
            'move_type': forms.TextInput(attrs={'class': 'form-control'}),
            'job_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'scale_of_work': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'handling_type': forms.Select(attrs={'class': 'form-control'}),
            'freight_term': forms.Select(attrs={'class': 'form-control'}),
            'hbl_status': forms.Select(attrs={'class': 'form-control'}),
            'hbl_location': forms.Select(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control','required':True}),
            'job_status': forms.Select(attrs={'class': 'form-control'}),
            'account_address': forms.Select(attrs={'class': 'form-control'}),
            'do_no': forms.TextInput(attrs={'class': 'form-control'}),
            'isf_filed_by': forms.TextInput(attrs={'class': 'form-control'}),
            'mbl_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mbl_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'hbl_recieved_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'hbl_no': forms.TextInput(attrs={'class': 'form-control'}),
            'hbl_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            
            
            'ata_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'atd_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            
            'vessel_voy_name': forms.TextInput(attrs={'class': 'form-control'}),
            'via_no': forms.TextInput(attrs={'class': 'form-control'}),
            'rotation_no': forms.TextInput(attrs={'class': 'form-control'}),
            'vessel_voy_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'flight_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'work_scope':forms.Select(attrs={'class':'form-control'}),
            'cfs_out_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'gate_cutoff_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'document_cutoff_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'form13_cutoff_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'sob_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'fpod_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'account': forms.Select(attrs={'class': 'form-control'}),
            'line_freight': forms.Select(attrs={'class': 'form-control'}),
            'bl_type': forms.Select(attrs={'class': 'form-control'}),
            'mbl_type': forms.Select(attrs={'class': 'form-control'}),
            'status':forms.TextInput(attrs={'class':'form-control'}),
            'transipment1_eta':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'transipment1_etd':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'transipment1_vessel': forms.TextInput(attrs={'class': 'form-control'}),
            'transipment1_country': forms.TextInput(attrs={'class': 'form-control'}),
            
            'transipment2_eta':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'railout_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'transipment2_etd':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'transipment2_vessel': forms.TextInput(attrs={'class': 'form-control'}),
            'transipment2_country': forms.TextInput(attrs={'class': 'form-control'}),

            'shipper': forms.Select(attrs={'class': 'form-control'}),
            'container_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'consignee': forms.Select(attrs={'class': 'form-control'}),
            'notify_party': forms.Select(attrs={'class': 'form-control'}),
            'no_of_hbl':  forms.TextInput(attrs={'class': 'form-control'}),
            'part_bl':  forms.TextInput(attrs={'class': 'form-control'}),
            'container_no':  forms.TextInput(attrs={'class': 'form-control'}),
            'shipper_invoice_no':  forms.TextInput(attrs={'class': 'form-control'}),
            'container_type':  forms.Select(attrs={'class': 'form-control'}),
            'booking_party': forms.Select(attrs={'class': 'form-control'}),
            'overseas_agent': forms.Select(attrs={'class': 'form-control'}),
            'broker': forms.Select(attrs={'class': 'form-control'}),
            'place_of_reciept': forms.Select(attrs={'class': 'form-control'}),
            'final_destination': forms.Select(attrs={'class': 'form-control'}),
            'port_of_loading': forms.Select(attrs={'class': 'form-control'}),
            'port_of_discharge': forms.Select(attrs={'class': 'form-control'}),
            'po_no': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity_type': forms.Select(attrs={'class': 'form-control'}),
            'no_of_packages': forms.TextInput(attrs={'class': 'form-control'}),
            'packages_type': forms.TextInput(attrs={'class': 'form-control'}),
            'volume': forms.TextInput(attrs={'class': 'form-control'}),
            'gross_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'net_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'chargable_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'cbm': forms.TextInput(attrs={'class': 'form-control'}),
            'docket_no': forms.TextInput(attrs={'class': 'form-control'}),
            'awb_no': forms.TextInput(attrs={'class': 'form-control'}),
            'flight_no': forms.TextInput(attrs={'class': 'form-control'}),
            'igm_no': forms.TextInput(attrs={'class': 'form-control'}),
            'igm_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'agent_remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'awb_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'clearance': forms.Select(attrs={'class': 'form-control'}),
            'shipping_line': forms.Select(attrs={'class': 'form-control'}),
            'air_line': forms.Select(attrs={'class': 'form-control'}),
            'goods_reciept': forms.Select(attrs={'class': 'form-control'}),
            'cargo_nature': forms.Select(attrs={'class': 'form-control'}),
            'importer': forms.Select(attrs={'class': 'form-control'}),
            'forwarder': forms.Select(attrs={'class': 'form-control'}),
            'place_of_loading': forms.Select(attrs={'class': 'form-control'}),
            'place_of_loading_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'place_of_unloading': forms.Select(attrs={'class': 'form-control'}),
            'place_of_unloading_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'eway_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'owned_hire': forms.Select(attrs={'class': 'form-control'}),
            'gr_no': forms.TextInput(attrs={'class': 'form-control'}),
            'bilty_no': forms.TextInput(attrs={'class': 'form-control'}),
            'trailor_no': forms.TextInput(attrs={'class': 'form-control'}),
            'ptc_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'l_seal': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery': forms.Select(attrs={'class': 'form-control'}),
            'cfs_port_name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
            'uin': forms.TextInput(attrs={'class': 'form-control'}),
            'account_manager': forms.Select(attrs={'class': 'form-control'}),
            'cfs_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'asessable_value': forms.TextInput(attrs={'class': 'form-control'}),
            'oc_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'port_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'do_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'container_return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'shipper_invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'stuffing_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'rail_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'sailing_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'eta_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'actual_arrival_pod_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'gigm': forms.TextInput(attrs={'class': 'form-control'}),
            'ligm': forms.TextInput(attrs={'class': 'form-control'}),
            'gigm_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'ligm_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
           
            'ship_bill_no': forms.TextInput(attrs={'class': 'form-control'}),
            'ship_bill_type': forms.TextInput(attrs={'class': 'form-control'}),
            'ship_bill_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'cfs': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'entry_cont_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','require':True}, format="%Y-%m-%d"),
            'invoice_value': forms.TextInput(attrs={'class': 'form-control'}),
            'bl_type': forms.TextInput(attrs={'class': 'form-control'}),
            'bl_no': forms.TextInput(attrs={'class': 'form-control'}),
            'lc_no': forms.TextInput(attrs={'class': 'form-control'}),
            'ams_no': forms.TextInput(attrs={'class': 'form-control'}),
            'booking_no': forms.TextInput(attrs={'class': 'form-control'}),
            'container_pickup_location': forms.Select(attrs={'class': 'form-control'}),
            'container_pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','require':True}, format="%Y-%m-%d"),
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','require':True}, format="%Y-%m-%d"),
           
            'si_cut_off_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'vgm_cut_off_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'etd_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'charges': forms.TextInput(attrs={'class': 'form-control'}),
            'stuffing_type': forms.TextInput(attrs={'class': 'form-control'}),
            'shipment_type': forms.Select(attrs={'class': 'form-control'}),
            'truck_no': forms.TextInput(attrs={'class': 'form-control'}),
            'dispatch_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'imdg': forms.TextInput(attrs={'class': 'form-control'}),
            'gate_open_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'ams_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'isf_no': forms.TextInput(attrs={'class': 'form-control'}),
            'isf_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
           
        }
        
class CargoArrivalForm(forms.ModelForm):
    shipper = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    consignee = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    notify_party_2 = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    notify_party_1 = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = CargoArrivalNotice
        fields = '__all__'
        widgets = {
            
            'job': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'pod_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'fpd_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'move_type': forms.TextInput(attrs={'class': 'form-control'}),
            'vessel_voyage': forms.TextInput(attrs={'class': 'form-control'}),
            'seal_no': forms.TextInput(attrs={'class': 'form-control'}),
            'gigm': forms.TextInput(attrs={'class': 'form-control'}),
            'ligm':  forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_line': forms.Select(attrs={'class': 'form-control'}),
            'air_line': forms.Select(attrs={'class': 'form-control'}),
            'container_no':  forms.TextInput(attrs={'class': 'form-control'}),
            'company_type':forms.Select(attrs={'class':'form-control'}),
            'shipper':forms.Select(attrs={'class':'form-control'}),
            'consignee':forms.Select(attrs={'class':'form-control'}),
            
            'pol':forms.Select(attrs={'class':'form-control'}),
            'pod':forms.Select(attrs={'class':'form-control'}),
            'hbl_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'mbl_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'hbl':forms.Select(attrs={'class':'form-control'}),
            'mbl':forms.TextInput(attrs={'class':'form-control'}),
            'arrival_notice_no':forms.TextInput(attrs={'class':'form-control'}),
            'it_location':forms.Select(attrs={'class':'form-control'}),
            'final_destination':forms.Select(attrs={'class':'form-control'}),
            'it_no':forms.TextInput(attrs={'class':'form-control'}),
            'it_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'eta':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'etd':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'ams_hbl':forms.TextInput(attrs={'class':'form-control'}),
            'notify_party_1':forms.Select(attrs={'class':'form-control'}),
            'notify_party_2':forms.Select(attrs={'class':'form-control'}),
            'freight_location':forms.Select(attrs={'class':'form-control'}),
            'consignee_location':forms.Textarea(attrs={'class':'form-control'}),
            'notify_party_1_location':forms.Textarea(attrs={'class':'form-control'}),
            'notify_party_2_location':forms.Textarea(attrs={'class':'form-control'}),
            'freight_address':forms.Textarea(attrs={'class':'form-control'}),
            'firm_code':forms.TextInput(attrs={'class':'form-control'}),
            'firm_phone':forms.TextInput(attrs={'class':'form-control'}),
            'no_of_packages':forms.Textarea(attrs={'class':'form-control'}),
            'desc_of_packages':forms.Textarea(attrs={'class':'form-control'}),
            'gross_weight':forms.Textarea(attrs={'class':'form-control'}),
            'measurement':forms.Textarea(attrs={'class':'form-control'}),
            'marks':forms.Textarea(attrs={'class':'form-control'}),
           
        }
        
class DeliveryOrderForm(forms.ModelForm):
    consignee = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    hbl_options = forms.ModelMultipleChoiceField(queryset=JobHBL.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
    class Meta:
        model = DeliveryOrder
        fields = '__all__'
        widgets = {
            
            'company_type': forms.Select(attrs={'class': 'form-control'}),
            'job': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'gigm_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'ligm_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'manager_location': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_state': forms.TextInput(attrs={'class': 'form-control'}),
            'desc_of_goods': forms.TextInput(attrs={'class': 'form-control'}),
            'gigm':  forms.TextInput(attrs={'class': 'form-control'}),
            'ligm': forms.TextInput(attrs={'class': 'form-control'}),
            'container_no':  forms.TextInput(attrs={'class': 'form-control'}),
            'container_type':  forms.Select(attrs={'class': 'form-control'}),
            'weight':  forms.TextInput(attrs={'class': 'form-control'}),
            'total_packages':  forms.TextInput(attrs={'class': 'form-control'}),
            'hbl_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'mbl_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'hbl':forms.TextInput(attrs={'class':'form-control'}),
            'mbl':forms.TextInput(attrs={'class':'form-control'}),
            'consignee':forms.Select(attrs={'class':'form-control'}),
           
        }
        
class FreightCertificateForm(forms.ModelForm):
    consignee = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    hbl_options = forms.ModelMultipleChoiceField(queryset=JobHBL.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
    class Meta:
        model = FreightCertificate
        fields = '__all__'
        widgets = {
            
            'job': forms.Select(attrs={'class': 'form-control'}),
            'gross_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'cbm': forms.TextInput(attrs={'class': 'form-control'}),
            'ocean_freight': forms.TextInput(attrs={'class': 'form-control'}),
            'container_no':  forms.TextInput(attrs={'class': 'form-control'}),
            'container_type':  forms.Select(attrs={'class': 'form-control'}),
            'company_type':forms.Select(attrs={'class':'form-control'}),
            'consignee':forms.Select(attrs={'class':'form-control'}),
            'hbl_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'mbl_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'hbl':forms.TextInput(attrs={'class':'form-control'}),
            'mbl':forms.TextInput(attrs={'class':'form-control'}),
            
        }
        
class DSRForm(forms.ModelForm):
    consignee = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    shipper = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = DSR
        fields = '__all__'
        widgets = {
            
            'company_type':forms.Select(attrs={'class':'form-control','required':True}),
            'job':forms.Select(attrs={'class':'form-control','required':True}),
            'invoice':forms.TextInput(attrs={'class':'form-control'}),
            'container_inv_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            's_bill_no':forms.TextInput(attrs={'class':'form-control'}),
            'date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'egm_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'no':forms.TextInput(attrs={'class':'form-control'}),
            'pfi_no':forms.TextInput(attrs={'class':'form-control'}),
            'shipment_term':forms.TextInput(attrs={'class':'form-control'}),
            'consignee':forms.Select(attrs={'class':'form-control'}),
            'no_of_container':forms.TextInput(attrs={'class':'form-control'}),
            'pod':forms.Select(attrs={'class':'form-control'}),
            'pol':forms.Select(attrs={'class':'form-control'}),
            'fd':forms.Select(attrs={'class':'form-control'}),
            'net_qty':forms.TextInput(attrs={'class':'form-control'}),
            'desp_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'doc_rec_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'cont_hold_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'cont_release_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'rail_out_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'port_in_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'vessel_name':forms.TextInput(attrs={'class':'form-control'}),
            'vessel_sailed':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'eta_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
           
            'bl_release_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'mbl_no':forms.TextInput(attrs={'class':'form-control'}),
            'hbl_no':forms.TextInput(attrs={'class':'form-control'}),
            'bl_instr_given_to_line':forms.TextInput(attrs={'class':'form-control'}),
            'shipping_line':forms.Select(attrs={'class':'form-control'}),
            'doc_scan_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'dsr_status':forms.Select(attrs={'class':'form-control'}),
            'remarks':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'status':forms.TextInput(attrs={'class':'form-control'})
           
            
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryMaster
        fields = '__all__'
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'under': forms.Select(attrs={'class': 'form-control'}),
               
        }

class PortForm(forms.ModelForm):
    class Meta:
        model = Ports
        fields = '__all__'
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
  
               
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
           
               
        }

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = currency
        fields = '__all__'
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
           
               
        }

class ShippingLineForm(forms.ModelForm):
    class Meta:
        model = ShippingLines
        fields = '__all__'
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control','default':'Sea'}),
           
               
        }

class AirLineForm(forms.ModelForm):
    class Meta:
        model = Airlines
        fields = '__all__'
        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control','default':'Sea'}),
           
               
        }

class VGMForm(forms.ModelForm):
    shipper = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = VGMMaster
        fields = '__all__'
        widgets = {
            
            'company_type' : forms.Select(attrs={'class':'form-control'}),
            'job' : forms.Select(attrs={'class':'form-control'}),
            'shipper' : forms.Select(attrs={'class':'form-control'}),
            'shipper_licence_no' : forms.TextInput(attrs={'class':'form-control'}),
            'auth_shipper_name' : forms.TextInput(attrs={'class':'form-control'}),
            'auth_shipper_designation' : forms.TextInput(attrs={'class':'form-control'}),
            'shipper_contact' : forms.TextInput(attrs={'class':'form-control'}),
            'vgm_type' : forms.Select(attrs={'class':'form-control'}),
            'vgm_class' : forms.TextInput(attrs={'class':'form-control'}),
            'booking_cont_no' : forms.TextInput(attrs={'class':'form-control'}),
            'container_size' : forms.Select(attrs={'class':'form-control'}),
            'max_permissible_weight' : forms.TextInput(attrs={'class':'form-control'}),
            'verified_gross_mass' : forms.TextInput(attrs={'class':'form-control'}),
            'date_of_weighing' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'time_of_weighing' : forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'weighing_slip_no' : forms.TextInput(attrs={'class':'form-control'}),
            'weighbridge_register_no' : forms.TextInput(attrs={'class':'form-control'}),
            'weighbridge_address' : forms.TextInput(attrs={'class':'form-control'}),
           
               
        }
        
        
class MBLForm(forms.ModelForm):
    exporter_name = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    notify_party = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    consigned_name = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    agent_name = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    container_options = forms.ModelMultipleChoiceField(queryset=JobContainer.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
    class Meta:
        model = MBLMaster
        fields = '__all__'
        widgets = {
            
            'company_type':forms.Select(attrs={'class':'form-control'}),
            
            'mbl_no':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'shipper_board_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'mbl_Document_no':forms.TextInput(attrs={'class':'form-control'}),
            'job_no':forms.Select(attrs={'class':'form-control'}),
            'exporter_name':forms.Select(attrs={'class':'form-control'}),
            'exporter_address':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'consigned_name':forms.Select(attrs={'class':'form-control'}),
            'consigned_address':forms.Textarea(attrs={'class':'form-control','rows':4}),
            
            'bl_type':forms.Select(attrs={'class':'form-control'}),
            'notify_party':forms.Select(attrs={'class':'form-control'}),
            'notify_party_address':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'mtd_number':forms.TextInput(attrs={'class':'form-control'}),
            'shipment_ref_no':forms.TextInput(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'executed_at':forms.TextInput(attrs={'class':'form-control'}),
            'by':forms.TextInput(attrs={'class':'form-control'}),
            'movement_type':forms.TextInput(attrs={'class':'form-control'}),
            'freight_type':forms.Select(attrs={'class':'form-control'}),
            'total_weight':forms.TextInput(attrs={'class':'form-control'}),
            'total_packages':forms.TextInput(attrs={'class':'form-control'}),
            'carrier':forms.Select(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
            'freight':forms.TextInput(attrs={'class':'form-control'}),
            'no_of_o_mtd':forms.TextInput(attrs={'class':'form-control'}),
            'freight_charge_amt':forms.TextInput(attrs={'class':'form-control'}),
            'freight_payable_at':forms.TextInput(attrs={'class':'form-control'}),
            'export_references':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'forwarding_agent':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'point_and_country_of_origin':forms.TextInput(attrs={'class':'form-control'}),
            'loading_pier':forms.TextInput(attrs={'class':'form-control'}),
            'domestic_routing':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'pre_carriage_by':forms.TextInput(attrs={'class':'form-control'}),
            'ocean_vessel':forms.TextInput(attrs={'class':'form-control'}),
            'port_of_loading_export':forms.Select(attrs={'class':'form-control'}),
            'place_of_delivery':forms.Select(attrs={'class':'form-control'}),
            'place_of_receipt':forms.Select(attrs={'class':'form-control'}),
            'port_of_discharge':forms.Select(attrs={'class':'form-control'}),
            'voyage_no':forms.TextInput(attrs={'class':'form-control'}),
            'declared_value':forms.TextInput(attrs={'class':'form-control'}),
            'agent_name':forms.Select(attrs={'class':'form-control'}),
            'agent_address':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'marks_and_number':forms.Textarea(attrs={'class':'form-control'}),
            'no_of_packages':forms.Textarea(attrs={'class':'form-control'}),
            'description_of_commodities':forms.Textarea(attrs={'class':'form-control'}),
            'gross_weight':forms.Textarea(attrs={'class':'form-control'}),
            'measurement':forms.Textarea(attrs={'class':'form-control'}),
            'mbl_type':forms.Select(attrs={'class':'form-control'}),

            'flight_no':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'flight_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'departure_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','required':True}, format="%Y-%m-%d"),
            'airline':forms.Select(attrs={'class':'form-control form-control-sm'}),
            'departure_airport':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'destination_airport':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'accounting_information':forms.Textarea(attrs={'class':'form-control form-control-sm','rows':2}),
            'handling_information':forms.Textarea(attrs={'class':'form-control form-control-sm','rows':2}),
            'chargeable_weight':forms.Textarea(attrs={'class':'form-control form-control-sm'}),
            'rate_charges':forms.Textarea(attrs={'class':'form-control form-control-sm'}),
            'total_charges':forms.Textarea(attrs={'class':'form-control form-control-sm'}),
           
               
        }
        
        
class TransportBookingForm(forms.ModelForm):
    forwarder = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    shipper = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    broker = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    client = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    cha = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    buyer = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    overseas_agent = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    consignee = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = TransportBooking
        fields = '__all__'
        widgets = {
            
            'company_type':forms.Select(attrs={'class':'form-control'}),
            'booking_no':forms.TextInput(attrs={'class':'form-control','required':True}),
            'booking_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'shipping_line':forms.Select(attrs={'class':'form-control'}),
            'vessel_no':forms.TextInput(attrs={'class':'form-control'}),
            'voyage_no':forms.TextInput(attrs={'class':'form-control'}),
            'forwarder':forms.Select(attrs={'class':'form-control'}),
            'send_to_party':forms.Select(attrs={'class':'form-control'}),
            'date_of_sent':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'pickup_location':forms.Select(attrs={'class':'form-control'}),
            'booking_location':forms.Select(attrs={'class':'form-control'}),
            'stuffice_place':forms.Select(attrs={'class':'form-control'}),
            'is_hazardous':forms.Select(attrs={'class':'form-control'}),
            'class_name':forms.TextInput(attrs={'class':'form-control'}),
            'uin':forms.TextInput(attrs={'class':'form-control'}),
            'pol':forms.Select(attrs={'class':'form-control'}),
            'pod':forms.Select(attrs={'class':'form-control'}),
            'fpd':forms.Select(attrs={'class':'form-control'}),
            'shipper':forms.Select(attrs={'class':'form-control'}),
            'broker':forms.Select(attrs={'class':'form-control'}),
            'client':forms.Select(attrs={'class':'form-control'}),
            'cha':forms.Select(attrs={'class':'form-control'}),
            'buyer':forms.Select(attrs={'class':'form-control'}),
            'overseas_agent':forms.Select(attrs={'class':'form-control'}),
            'is_cig_involved':forms.Select(attrs={'class':'form-control'}),
            'is_tpt_involved':forms.Select(attrs={'class':'form-control'}),
            'is_isf':forms.Select(attrs={'class':'form-control'}),
            'sales_person':forms.TextInput(attrs={'class':'form-control'}),
            'eta_destination':forms.Select(attrs={'class':'form-control'}),
            'cs_remarks':forms.TextInput(attrs={'class':'form-control'}),
            'etd':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'no_of_container_1':forms.TextInput(attrs={'class':'form-control'}),
            'container_size_1':forms.Select(attrs={'class':'form-control'}),
            'gross_weight_1':forms.TextInput(attrs={'class':'form-control'}),
            'no_of_container_2':forms.TextInput(attrs={'class':'form-control'}),
            'container_size_2':forms.Select(attrs={'class':'form-control'}),
            'gross_weight_2':forms.TextInput(attrs={'class':'form-control'}),
            'commodity_1':forms.TextInput(attrs={'class':'form-control'}),
            'commodity_2':forms.TextInput(attrs={'class':'form-control'}),
            'trans_port_1':forms.Select(attrs={'class':'form-control'}),
            'trans_port_2':forms.Select(attrs={'class':'form-control'}),
            'eta_1':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'eta_2':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'etd_1':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'etd_2':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'conn_1':forms.TextInput(attrs={'class':'form-control'}),
            'conn_2':forms.TextInput(attrs={'class':'form-control'}),
            'vessel_1':forms.TextInput(attrs={'class':'form-control'}),
            'vessel_2':forms.TextInput(attrs={'class':'form-control'}),
            'cargo_type':forms.TextInput(attrs={'class':'form-control'}),
            'stuffing_type':forms.TextInput(attrs={'class':'form-control'}),
            'job_no':forms.Select(attrs={'class':'form-control'}),
            'isf_by':forms.TextInput(attrs={'class':'form-control'}),
            'bl_type':forms.TextInput(attrs={'class':'form-control'}),
            'term':forms.TextInput(attrs={'class':'form-control'}),
            'qty':forms.TextInput(attrs={'class':'form-control'}),
            'consignee':forms.Select(attrs={'class':'form-control'}),
               
        }
        
        

class GRForm(forms.ModelForm):
    consignee = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    consignor = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    gr_customer = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    billing_party = forms.ModelChoiceField(queryset=Party.objects.filter(is_active=True).all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = GRMaster
        fields = '__all__'
        
        widgets = {
            'company_type':forms.Select(attrs={'class':'form-control'}),
            'job':forms.Select(attrs={'class':'form-control','required':True}),
            'import_export':forms.Select(attrs={'class':'form-control'}),
            'drop_location':forms.Select(attrs={'class':'form-control'}),
            'gr_no':forms.TextInput(attrs={'class':'form-control'}),
            'seal_no':forms.TextInput(attrs={'class':'form-control'}),
            'trailor_no':forms.TextInput(attrs={'class':'form-control'}),
            'trailor_type':forms.TextInput(attrs={'class':'form-control'}),
            'fpd':forms.Select(attrs={'class':'form-control'}),
            'driver':forms.Select(attrs={'class':'form-control'}),
            'container_no':forms.TextInput(attrs={'class':'form-control'}),
            'container_type':forms.Select(attrs={'class':'form-control'}),
            'consignee':forms.Select(attrs={'class':'form-control'}),
            'consignee_address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'consignor':forms.Select(attrs={'class':'form-control'}),
            'consignor_address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'consignee_back_load':forms.TextInput(attrs={'class':'form-control'}),
            'consignee_bl_address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'consignor_back_load':forms.TextInput(attrs={'class':'form-control'}),
            'consignor_bl_address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            
            'gr_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'stuffing_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'time':forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'pickup_from':forms.Select(attrs={'class':'form-control'}),
            'person_name':forms.TextInput(attrs={'class':'form-control'}),
            'mobile_no':forms.TextInput(attrs={'class':'form-control'}),
            'remarks':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'factory_address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'job_type':forms.Select(attrs={'class':'form-control'}),
            'gross_wt':forms.TextInput(attrs={'class':'form-control'}),
            'delivery_address':forms.TextInput(attrs={'class':'form-control'}),
            'container_pickup_from':forms.TextInput(attrs={'class':'form-control'}),
            'container_pickup_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'back_loading':forms.Select(attrs={'class':'form-control'}),
            'loading_address':forms.TextInput(attrs={'class':'form-control'}),
            'unloading_address':forms.TextInput(attrs={'class':'form-control'}),
            'date_load':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'offload_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'gr_customer':forms.Select(attrs={'class':'form-control'}),
            'billing_party':forms.Select(attrs={'class':'form-control'}),
            'no_lr':forms.TextInput(attrs={'class':'form-control'}),
            'date_lr':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'bp_date':forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'commision':forms.TextInput(attrs={'class':'form-control'}),
            'advance':forms.TextInput(attrs={'class':'form-control'}),
            'rate':forms.TextInput(attrs={'class':'form-control'}),
            'cheque':forms.TextInput(attrs={'class':'form-control'}),
            'gross_wt_2':forms.TextInput(attrs={'class':'form-control'}),
            'cargo':forms.TextInput(attrs={'class':'form-control'}),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = DriverMaster
        fields = '__all__'
        widgets = {
        'driver_name':forms.TextInput(attrs={'class':'form-control'}),
        'phone_1':forms.TextInput(attrs={'class':'form-control'}),
        'phone_2':forms.TextInput(attrs={'class':'form-control'}),
        'address_1':forms.TextInput(attrs={'class':'form-control'}),
        'address_2':forms.TextInput(attrs={'class':'form-control'}),
        'address_3':forms.TextInput(attrs={'class':'form-control'}),
        'address_4':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.TextInput(attrs={'class':'form-control'}),
        'driving_licence_no':forms.TextInput(attrs={'class':'form-control'}),
        'lic_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        'account_no':forms.TextInput(attrs={'class':'form-control'}),
        'bank_name':forms.TextInput(attrs={'class':'form-control'}),
        'bank_ifsc':forms.TextInput(attrs={'class':'form-control'}),
        'bank_address':forms.TextInput(attrs={'class':'form-control'}),
        'aadhar_no':forms.TextInput(attrs={'class':'form-control'}),
        'driver_dob':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        'nominee_name':forms.TextInput(attrs={'class':'form-control'}),
        'nominee_bank':forms.TextInput(attrs={'class':'form-control'}),
        'nominee_account':forms.TextInput(attrs={'class':'form-control'}),
        'nominee_dob':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        'relation':forms.TextInput(attrs={'class':'form-control'}),
        'status':forms.TextInput(attrs={'class':'form-control'}),
        'joining_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        
        }
        
class TrailorForm(forms.ModelForm):
    class Meta:
        model = TrailorMaster
        fields = "__all__"
        widgets = {
            'invoice_no':forms.TextInput(attrs={'class':'form-control'}),
            'invoice_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'trailor_no':forms.TextInput(attrs={'class':'form-control'}),
            'registration_no':forms.TextInput(attrs={'class':'form-control'}),
            'finance_bank':forms.TextInput(attrs={'class':'form-control'}),
            'model_no':forms.TextInput(attrs={'class':'form-control'}),
           
            
            'engine_no':forms.TextInput(attrs={'class':'form-control'}),
            'rto_office':forms.TextInput(attrs={'class':'form-control'}),
            'tax_details':forms.TextInput(attrs={'class':'form-control'}),
            'valid_upto':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            
            'chasis_no':forms.TextInput(attrs={'class':'form-control'}),
            'fast_card_no':forms.TextInput(attrs={'class':'form-control'}),
            'diesel_card_no':forms.TextInput(attrs={'class':'form-control'}),
            'average':forms.TextInput(attrs={'class':'form-control'}),
          
        }
        
class RateMasterForm(forms.ModelForm):
    class Meta:
        model = RateMaster
        fields = "__all__"
        widgets = {
            'carrier':forms.Select(attrs={'class':'form-control'}),
            'ac_type':forms.Select(attrs={'class':'form-control'}),
            'size':forms.Select(attrs={'class':'form-control'}),
            'pol':forms.Select(attrs={'class':'form-control'}),
            'pod':forms.Select(attrs={'class':'form-control'}),
            'fpd':forms.Select(attrs={'class':'form-control'}),
            'from_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'to_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'ammendment':forms.TextInput(attrs={'class':'form-control'}),
            'basic_charges':forms.NumberInput(attrs={'class':'form-control','readonly':True,'step':0.01}),
            'oth_charges':forms.NumberInput(attrs={'class':'form-control','readonly':True,'step':0.01}),
            'ramp_charges':forms.NumberInput(attrs={'class':'form-control','readonly':True,'step':0.01}),
            'line_door_charges':forms.NumberInput(attrs={'class':'form-control','readonly':True,'step':0.01}),
            'trucking_charges':forms.NumberInput(attrs={'class':'form-control','readonly':True,'step':0.01}),
            'net_charges':forms.NumberInput(attrs={'class':'form-control','readonly':True,'step':0.01}),
          
        }