from audioop import reverse
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, User
from django.core.files.storage import FileSystemStorage



class User(AbstractUser):
        user_type_data = ((1,"Systemadmin"),(2,"Resident"), (3,"KebeleEmployee"))
        user_type = models.CharField(default=1,choices=user_type_data, max_length=10)
        first_name = models.CharField(max_length=100, null=True, blank=False)
        username = models.CharField(max_length=100, null=True,blank=False)
        email = models.EmailField(unique=True, null=True)
        is_resident = models.BooleanField(default=False)
        is_systemadmin = models.BooleanField(default=False)
        is_KebeleEmployee = models.BooleanField(default=False)


       

        avatar = models.ImageField(null=True, default="avatar.svg")

        USERNAME_FIELD = 'email'
   
        REQUIRED_FIELDS = ['first_name','username']
  



        




class Kebele(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    kebele_name = models.CharField(help_text=_("Required"), max_length=255, unique=True, blank=False)
    phone = models.CharField(max_length=20, help_text=_("Required"),null=True,blank=False)
    email = models.EmailField(help_text=_("Required"),blank=False, null=True)
    address = models.CharField(_("City"), max_length=150,help_text=_("Required"), null=True,blank=False)
    po_number = models.CharField(max_length=100,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    class Meta:
        verbose_name = _("Kebele")
        verbose_name_plural = _("Kebeles")

    def __str__(self):
        return self.kebele_name




class SystemAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()





CHOICES = (
    ("singel", "singel"),
    ("married", "married"),

)

GENDER = (
    ("Male","Male"),
    ("Faleme","Famele"),
    ("No","No"),
)




class Resident(models.Model):
    id = models.AutoField(primary_key=True)
    kebele = models.ForeignKey(Kebele, null=True,on_delete = models.CASCADE)
    admin = models.OneToOneField(User, on_delete = models.CASCADE)
    fname = models.CharField(max_length=50,null=True)
    age = models.IntegerField(default=0)
    phone = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=150, null=True)
    gender = models.CharField(max_length=50,choices=GENDER)
    current_status = models.CharField(max_length=50, blank=False, choices=CHOICES)
    marital_status =models.IntegerField(default=0)
    avatar = models.ImageField(null=True, default="avatar.svg",height_field=50, width_field=50) 
    is_resident = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    objects = models.Manager()


    class Meta:
        verbose_name = _("Resident")
        verbose_name_plural = _("Residents")


    def __str__(self):
        return self.fname    




class FeedBackResident(models.Model):
    id = models.AutoField(primary_key=True)
    resident_id = models.ForeignKey(Resident, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()




class KebeleEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    admin = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.TextField()
    is_employee = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    


    class Meta:

        verbose_name = 'KebeleEmployee'
        verbose_name_plural = 'KebeleEmployees'


    def __str__(self):
        return self.first_name    




class LeaveReportKebele_employee(models.Model):
    id = models.AutoField(primary_key=True)
    kebele_employee_id = models.ForeignKey(KebeleEmployee, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.leave_message[0:50]




class FeedBackSkebele_employee(models.Model):
    id = models.AutoField(primary_key=True)
    KebeleEmploye_id = models.ForeignKey(KebeleEmployee, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.feedback[0:10]




class Notification_Kebele_employee(models.Model):
    id = models.AutoField(primary_key=True)
    kebeleEmploye_id = models.ForeignKey(KebeleEmployee, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    def __str__(self):
        return self.message[0:10]        




class VitalEvant(models.Model):
    id = models.AutoField(primary_key=True)
    Kebele = models.OneToOneField(Kebele, related_name="kebeless", on_delete=models.CASCADE)  
    resident = models.OneToOneField(Resident,related_name="reisdent", on_delete=models.CASCADE)  
    is_resident = models.BooleanField(default=False)
    brith_date = models.DateTimeField(auto_now=True)
    death_date =models.DateTimeField(auto_now=True)
    record_date =models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  
    



class Marriage(models.Model):
    id =  models.AutoField(primary_key=True)
    residenr = models.OneToOneField(Resident,related_name='residents',on_delete=models.CASCADE)
    kebele = models.OneToOneField(Kebele, related_name="kebeles",on_delete=models.CASCADE)
    marital_status = models.CharField(max_length=100, default=False,choices=CHOICES)
    brith_date = models.DateTimeField(auto_now=True)
    marriage_date = models.DateTimeField(auto_now=True)
    given_by = models.ForeignKey(KebeleEmployee,null=True,on_delete= models.CASCADE)
    is_resident = models.BooleanField(default=False)
    record_date =models.DateTimeField(auto_now=True)
    objects = models.Manager()






class Death(models.Model):
    id =  models.AutoField(primary_key=True)
    residenr = models.OneToOneField(Resident,related_name='resident',on_delete=models.CASCADE)
    kebele = models.OneToOneField(Kebele, related_name="kebelesa",on_delete=models.CASCADE)
    marital_status = models.CharField(max_length=10, choices=CHOICES)
    death_date = models.DateTimeField(auto_now=True)
    given_by = models.ForeignKey(KebeleEmployee,null=True,on_delete= models.CASCADE)
    is_resident = models.BooleanField(default=False)
    record_date =models.DateTimeField(auto_now=True)
    objects = models.Manager()





class Brith(models.Model):
    id =  models.AutoField(primary_key=True)
    residenr = models.OneToOneField(Resident,related_name='residentssa',on_delete=models.CASCADE)
    kebele = models.ForeignKey(Kebele, related_name="kebelessss",on_delete=models.CASCADE)
    marital_status = models.CharField(max_length=100, default=False,choices=CHOICES)
    brith_date = models.DateTimeField(auto_now=True)
    given_by = models.ForeignKey(KebeleEmployee,null=True,on_delete= models.CASCADE)
    is_resident = models.BooleanField(default=False)
    record_date =models.DateTimeField(auto_now=True)
    objects = models.Manager()





#Creating Django Signals

@receiver(post_save, sender=User)
# Now Creating a Function which will automatically insert data in Residents, kebele_ emp 
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            SystemAdmin.objects.create(admin=instance)
        if instance.user_type == 2:
            Resident.objects.create(admin=instance)
        if instance.user_type == 3:
            KebeleEmployee.objects.create(admin=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.systemadmin.save()
    if instance.user_type == 2:
        instance.resident.save()
    if instance.user_type == 3:
        instance.kebeleEmployee.save()