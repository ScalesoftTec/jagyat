from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Logistic
# Create your models here.



class UserAccount(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_account")
    profile_photo = models.ImageField(null=True,blank=True)
    is_sea_export = models.BooleanField(default=False)
    is_sea_import = models.BooleanField(default=False)
    is_air_export = models.BooleanField(default=False)
    is_air_import = models.BooleanField(default=False)
    is_finance = models.BooleanField(default=False)
    can_view_bills=models.BooleanField(default=False)
    is_crm = models.BooleanField(default=False)
    is_bi = models.BooleanField(default=False)
    is_transportation = models.BooleanField(default=False)
    is_operations = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    is_special_access = models.BooleanField(default=False)
    can_report = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    see_global_data = models.BooleanField(default=False)
    create_global_data = models.BooleanField(default=False)
    also_handle_other_work = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    handle_masters = models.BooleanField(default=False)
    is_invoice_reversal = models.BooleanField(default=False, help_text = "Check it to give permission of Convert E-invoice to Performa")

    office = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,related_name="emp_office")
    
    def __str__(self) -> str:
        return f'{self.user.username}'
    


class DocumentHandler(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='document_handler')
    company_type = models.ForeignKey(Logistic,on_delete=models.CASCADE,null=True,blank=True,related_name='handler_company')
    is_sea_ex_job = models.BooleanField(default=False)
    is_sea_im_job = models.BooleanField(default=False)
    is_air_im_job = models.BooleanField(default=False)
    is_air_ex_job = models.BooleanField(default=False)
    is_transport_job = models.BooleanField(default=False)
    is_rec_invoice = models.BooleanField(default=False)
    
   
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        verbose_name = 'Document Handler'
        verbose_name_plural = 'Document Handlers'    

       
