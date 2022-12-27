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
        name = models.CharField(max_length=100, null=True)
        username = models.EmailField(max_length=100, null=True)
        email = models.EmailField(unique=True, null=True)
        bio = models.TextField(null=True)

        avatar = models.ImageField(null=True, default="avatar.svg")

        USERNAME_FIELD = 'email'
   
        REQUIRED_FIELDS = ['name','username']


class Kebele(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kebele_name = models.CharField(help_text=_("Required"), max_length=255, unique=True)
    phone = models.CharField(max_length=20, help_text=_("Required"),null=True)
    email = models.EmailField(help_text=_("Required"))
    address = models.CharField(_("City"), max_length=150,help_text=_("Required"))
    fox_number = models.CharField(max_length=100)
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
    kebele = models.ForeignKey(Kebele, null=True, on_delete=models.CASCADE)
    admin = models.OneToOneField(User, on_delete = models.CASCADE)
    fname = models.CharField(max_length=100,null=True)
    lname = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField()
    address = models.CharField(max_length=150, null=True)
    sex = models.CharField(max_length=50)
    bio = models.TextField()
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
    kebele = models.ForeignKey(Kebele,on_delete=models.CASCADE)
    admin = models.OneToOneField(User, on_delete = models.CASCADE)

    fname = models.CharField(max_length=100,null=True)
    lname = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField()
    profile_pic = models.FileField()
    address = models.CharField( max_length=150, null=True)
    sex = models.CharField(max_length=50, null=True)
    salary = models.CharField(max_length=100,null=True)
    qualification = models.BooleanField(default=True)
    bio = models.TextField()
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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    current_status = models.CharField(max_length=100,null=True)
    death_date = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateTimeField(auto_now_add=True)
    # marital = models.Model(max_length=150, null= True)
    objects = models.Manager()

    class Meta:

        verbose_name = 'Vitalevent'
        verbose_name_plural = 'Vitalevents'

    def __str__(self):
        return self.current_status



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