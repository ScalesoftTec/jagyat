from django import forms
from crm.models import Inquiry,Lead,Event,sales_person_party


class EventForm(forms.ModelForm):
    def __init__(self,user,*args,**kwargs):
       
        print('--user',user)
        super (EventForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['customer'].queryset = sales_person_party.objects.filter(sales_person=user)

    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'company_type':forms.Select(attrs={'class':'form-control','required':True}),
          
            'user':forms.Select(attrs={'class':'form-control','required':True}),
            'title':forms.TextInput(attrs={'class':'form-control','required':True}),
            'customer':forms.Select(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','required':True,'rows':2}),
            "start": forms.DateInput(
                attrs={"type": "datetime-local", "class": "form-control",'required':True},
                format="%Y-%m-%dT%H:%M",
            ),
            "end": forms.DateInput(
                attrs={"type": "datetime-local", "class": "form-control",'required':True},
                format="%Y-%m-%dT%H:%M",
            ),
            'status':forms.Select(attrs={'class':'form-control','required':True}),
            'manager_remarks':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'remarks':forms.Textarea(attrs={'class':'form-control','rows':2}),
        }


class sales_person_party_Form(forms.ModelForm):
    class Meta:
        model = sales_person_party
        fields = "__all__"
        widgets = {

            'party_name':forms.TextInput(attrs={'class':'form-control'}), 
            'party_short':forms.TextInput(attrs={'class':'form-control'}), 
            'contact_person':forms.TextInput(attrs={'class':'form-control'}), 
            'contact_number':forms.TextInput(attrs={'class':'form-control'}), 
            'contact_email':forms.TextInput(attrs={'class':'form-control'}), 
            'states':forms.Select(attrs={'class':'form-control','required':True}),
            'address1':forms.TextInput(attrs={'class':'form-control','maxlength':'30'}),
            'address2':forms.TextInput(attrs={'class':'form-control','maxlength':'30'}),
            'address3':forms.TextInput(attrs={'class':'form-control','maxlength':'30'}),
           
        }


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets = {
            'company_type':forms.Select(attrs={'class':'form-control'}), 
            'sales_person':forms.TextInput(attrs={'class':'form-control'}), 
            'manager_remarks':forms.Textarea(attrs={'class':'form-control','rows':2,'cols':2}), 
            'status':forms.Select(attrs={'class':'form-control'}),
        }


class InquiryForm(forms.ModelForm):
    def __init__(self,user,*args,**kwargs):
        # print('--user',user)
        super (InquiryForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['customer'].queryset = sales_person_party.objects.filter(sales_person=user)
        
    class Meta:
        model = Inquiry
        fields = '__all__'
        widgets = {
            'quotation_no':forms.TextInput(attrs={'class':'form-control','required':True}),
            'date_of_inquiry':forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'customer':forms.Select(attrs={'class':'form-control','required':True}),
           
            'company_type':forms.Select(attrs={'class':'form-control','required':True}),
            'shipping_line':forms.Select(attrs={'class':'form-control'}),
            'airline':forms.Select(attrs={'class':'form-control'}),
            'valid_from':forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'valid_till':forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'pol':forms.Select(attrs={'class':'form-control','required':True}),
            'pod':forms.Select(attrs={'class':'form-control','required':True}),
            'origin':forms.Select(attrs={'class':'form-control','required':True}),
            'destination':forms.Select(attrs={'class':'form-control','required':True}),
            'priority':forms.Select(attrs={'class':'form-control'}),
            'freght_terms':forms.Select(attrs={'class':'form-control'}),
            'work_scope':forms.Select(attrs={'class':'form-control'}),
            'module':forms.Select(attrs={'class':'form-control','required':True}),
            'gross':forms.TextInput(attrs={'class':'form-control'}),
            'detention_at_origin':forms.TextInput(attrs={'class':'form-control'}),
            'detention_at_pod':forms.TextInput(attrs={'class':'form-control'}),
            'routing':forms.TextInput(attrs={'class':'form-control'}),
            'vessel_schedule':forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required':True}, format="%Y-%m-%d"),
            'container_type':forms.Select(attrs={'class':'form-control'}),
            'commodity':forms.TextInput(attrs={'class':'form-control','required':True}),
            'commodity_type':forms.TextInput(attrs={'class':'form-control'}),
            'total_packages':forms.TextInput(attrs={'class':'form-control'}),
            'total_packages_type':forms.TextInput(attrs={'class':'form-control'}),
            'gross_amount':forms.TextInput(attrs={'class':'form-control','required':True}),
            'gst_amount':forms.TextInput(attrs={'class':'form-control','required':True}),
            'advance_amount':forms.TextInput(attrs={'class':'form-control','required':True}),
            'net_amount':forms.TextInput(attrs={'class':'form-control','required':True}),
            'profit_amount':forms.TextInput(attrs={'class':'form-control','required':True}),
            'remark':forms.TextInput(attrs={'class':'form-control'}),
            'client_status':forms.Select(attrs={'class':'form-control'}),
            
        }