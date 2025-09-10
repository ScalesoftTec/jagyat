from hr import models
from django import forms


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':3})
        }

class DesignationForm(forms.ModelForm):
    class Meta:
        model = models.Designation
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':3})
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'from_date': forms.DateInput(attrs={'type':'date','class': 'form-control','required':True}),
            'to_date': forms.DateInput(attrs={'type':'date','class': 'form-control','required':True}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':3,'required':True})
        }

class LeaveStatusForm(forms.ModelForm):
    class Meta:
        model = models.LeaveStatus
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':3})
        }

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = models.LeaveType
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':3})
        }

class LeaveForm(forms.ModelForm):
    class Meta:
        model = models.Leave
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control','required':True}),
            'leave_type': forms.Select(attrs={'class': 'form-control','required':True}),
            'leave_status': forms.Select(attrs={'class': 'form-control','required':True}),
            'from_date': forms.DateInput(attrs={'class': 'form-control','type':'date','required':True}),
            'to_date': forms.DateInput(attrs={'class': 'form-control','type':'date','required':True}),
            'no_of_days': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':3})
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = '__all__'
        widgets = {
            'company_type': forms.Select(attrs={'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control','rows':3}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':3})
        }