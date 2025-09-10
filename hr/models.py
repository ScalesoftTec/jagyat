from django.db import models
from masters.models import LogFolder,State,Country,City
from dashboard.models import Logistic
from django.contrib.auth.models import User
from accounting.models import Vendor
# Create your models here.

class Department(LogFolder):
    name = models.CharField(max_length=120,null=True,blank=True)
    title = models.CharField(max_length=120,null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return self.name
    
class Designation(LogFolder):
    name = models.CharField(max_length=120,null=True,blank=True)
    title = models.CharField(max_length=120,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name

CHOOSE_GENDER = (
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
)

class Employee(LogFolder):
    company_type = models.ForeignKey(Logistic,on_delete=models.SET_NULL,null=True,blank=True,related_name='employee_company')
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,blank=True,related_name='employee_vendor')
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='employee_user')
    role = models.ForeignKey(Designation,on_delete=models.SET_NULL,null=True,blank=True,related_name='employee_role')
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True,related_name='employee_department')
    name =  models.CharField(max_length=120,null=True,blank=True)
    gender = models.CharField(max_length=20,choices=CHOOSE_GENDER)
    email =  models.CharField(max_length=180,null=True,blank=True)
    contact_no =  models.CharField(max_length=30,null=True,blank=True)
    dob =  models.DateField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,null=True,related_name='employee_state')
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,related_name='employee_country')
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True,related_name='employee_city')
    description = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.role})'
    
    
class Event(LogFolder):
    title = models.CharField(max_length=200,null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.title

class LeaveStatus(LogFolder):
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.title

class LeaveType(LogFolder):
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.title


class Leave(LogFolder):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name='leave_employee')
    leave_type = models.ForeignKey(LeaveType,on_delete=models.SET_NULL,null=True,blank=True,related_name='employee_leave_type')
    leave_status = models.ForeignKey(LeaveStatus,on_delete=models.SET_NULL,null=True,blank=True,related_name='employee_leave_status')
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    no_of_days = models.IntegerField(default=0)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return f'{self.employee} ({self.leave_type} - {self.leave_status})'