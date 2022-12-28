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
        user_type_data = ((1,"Resident"), (2,"KebeleEmploye"))
        user_type = models.CharField(default=1,choices=user_type_data, max_length=10)
        name = models.CharField(max_length=100, null=True, blank=False)
        username = models.CharField(max_length=100, null=True,blank=False)
        email = models.EmailField(unique=True, null=True)
        bio = models.TextField(null=True)

        avatar = models.ImageField(null=True, default="avatar.svg")

        USERNAME_FIELD = 'email'
   
        REQUIRED_FIELDS = ['name','username']


class Kebele(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    kebele_name = models.CharField(help_text=_("Required"), max_length=255, unique=True, blank=False)
    phone = models.CharField(max_length=20, help_text=_("Required"),null=True,blank=False)
    email = models.EmailField(help_text=_("Required"),blank=False, null=True)
    address = models.CharField(_("City"), max_length=150,help_text=_("Required"), null=True,blank=False)
    fox_number = models.CharField(max_length=100,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    class Meta:
        verbose_name = _("Kebele")
        verbose_name_plural = _("Kebeles")

    def __str__(self):
        return self.kebele_name
    


class Resident(models.Model):
    id = models.AutoField(primary_key=True)
    kebele = models.OneToOneField(Kebele, null=True, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, null=True,on_delete = models.CASCADE)
    fname = models.CharField(max_length=100,null=True)
    lname = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100,null=True,)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=150, null=True)
    sex = models.CharField(max_length=50)
    bio = models.TextField(null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("Resident")
        verbose_name_plural = _("Residents")

    def __str__(self):
        return self.fname


class KebeleEmploye(models.Model):
    id = models.AutoField(primary_key=True)
    kebele = models.ForeignKey(Kebele, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Resident, null=True, on_delete=models.RESTRICT)
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

class Vitalevent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Resident, null=True,  related_name="users", on_delete=models.RESTRICT)
    kebele= models.ForeignKey(Kebele, null=True, related_name="kebeles", on_delete=models.RESTRICT)
    residents = models.ForeignKey(Resident, null=True, on_delete=models.CASCADE)
    current_status = models.CharField(max_length=100,null=True,blank=True)
    death_date = models.CharField(max_length=100,null=True,blank=True)
    birth_date = models.CharField(max_length=100,null=True,blank=True)
    marital = models.CharField(max_length=150, null= True)
    objects = models.Manager()

    class Meta:

        verbose_name = 'Vitalevent'
        verbose_name_plural = 'Vitalevents'
    def __init__(self,current_status, birht_date,user,kebele,residents,death_date,marital,id):
        self.current_status = current_status
        self.birth_date = birht_date
        self.user = user
        self.kebele = kebele
        self.residents = residents
        self.marital = marital
        self.death_date = death_date
        self.birth_date = id
    #  def __getstate__   

    def __str__(self):
        return str(self.current_status)



@receiver(post_save, sender=User)
# Now Creating a Function which will automatically insert data in Residents, kebele_ emp 
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Resident.objects.create(admin=instance)
        if instance.user_type == 2:
            KebeleEmploye.objects.create(admin=instance, kebele=Kebele.objects.get(id=1), address="", profile_pic="", sex="")
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.resident.save()
    if instance.user_type == 2:
        instance.kebeleEmploye.save()