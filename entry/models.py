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
        user_type_data = ((1,"Systemadmin"),(2,"Resident"), (3,"KebeleEmploye"))
        user_type = models.CharField(default=1,choices=user_type_data, max_length=10)
        name = models.CharField(max_length=100, null=True, blank=False)
        username = models.CharField(max_length=100, null=True,blank=False)
        email = models.EmailField(unique=True, null=True)
        bio = models.TextField(null=True)

        avatar = models.ImageField(null=True, default="avatar.svg")

        USERNAME_FIELD = 'email'
   
        REQUIRED_FIELDS = ['name','username']






        
class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_birth_date_year = models.DateField()
    session_death_date_year = models.DateField()
    objects = models.Manager()



class Kebele(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
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



class Resident(models.Model):
    id = models.AutoField(primary_key=True)
    kebele = models.ForeignKey(Kebele, null=True,on_delete = models.CASCADE)
    admin = models.ForeignKey(User, null=True,on_delete = models.CASCADE)
    fname = models.CharField(max_length=100,null=True)
    lname = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100,null=True,)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=150, null=True)
    sex = models.CharField(max_length=50)
    current_status = models.CharField(max_length=100,null=True,blank=True)
    marital = models.CharField(max_length=150, null= True)
    death_date = models.ForeignKey(SessionYearModel,null=True, related_name='death', on_delete=models.CASCADE)
    birth_date = models.ForeignKey(SessionYearModel, null=True, related_name="birth", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(null=True,)
    
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

class KebeleEmploye(models.Model):
    id = models.AutoField(primary_key=True)
    kebele = models.ForeignKey(Kebele, null=True, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    fname = models.CharField(max_length=100,null=True, blank=False)
    lname = models.CharField(max_length=100, null=True,blank=False)
    age = models.CharField(max_length=100,null=True,blank=False)
    phone = models.CharField(max_length=20,null=True, blank=False)
    email = models.EmailField(null=True)
    profile_pic = models.FileField(null=True)
    address = models.CharField( max_length=150, null=True,blank=False)
    sex = models.CharField(max_length=50, null=True, blank=False)
    salary = models.CharField(max_length=100,null=True,blank=False)
    qualification = models.BooleanField(default=True, blank=False)
    bio = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:

        verbose_name = 'KebeleEmploye'
        verbose_name_plural = 'KebeleEmployes'


    def __str__(self):
        return self.fname    

class LeaveReportKebele_employee(models.Model):
    id = models.AutoField(primary_key=True)
    kebele_employee_id = models.ForeignKey(KebeleEmploye, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackSkebele_employee(models.Model):
    id = models.AutoField(primary_key=True)
    KebeleEmploye_id = models.ForeignKey(KebeleEmploye, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Notification_Kebele_employee(models.Model):
    id = models.AutoField(primary_key=True)
    kebeleEmploye_id = models.ForeignKey(KebeleEmploye, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()        


        




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
            KebeleEmploye.objects.create(admin=instance, kebele=Kebele.objects.get(id=1), address="", profile_pic="", sex="")
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.systemadmin.save()
    if instance.user_type == 2:
        instance.resident.save()
    if instance.user_type == 3:
        instance.kebeleEmploye.save()