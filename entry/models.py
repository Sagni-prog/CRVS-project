from audioop import reverse
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _



class AccountManager(BaseUserManager):
    def create_superuser(self, email, name, password, **other_fields):
        user_type_data = ((1,"Resident", (2,"Kebele_employee")))
        user_type = models.CharField(default=1,choices=user_type_data, max_length=10)
        other_fields.setdefault('is_residents', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_residents') is not True:
            raise ValueError('Superuser must be assigned to is_residents=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)

    @receiver(post_save, sender='User')
    def create_user(self, sender,instance, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,**other_fields)
        user.set_password(password)
        if instance.user_type == 1:
            residents.object.create(residents=instance)
        if instance.user_type == 2:
            residents.object.create(Kebele_employee=instance)
                
    @receiver(post_save, sender='User')
    def save_user(self, sender,instance, email, name, password, **other_fields):
        if instance.user_type == 1:
            instance.residents.save()
        if instance.user_type == 2:
            instance.Kebele_employee.save()    

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    age = models.IntegerField(max_length=150)
    sex = models.CharField(_("Male/Fale/Both"), max_length=150)
    email = models.EmailField(unique=True,null=False)
    mobile = models.CharField(max_length=20, blank=True)
    address = models.CharField(_("Town/City/State"), max_length=150)
    bio = models.TextField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_residents = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_kebele_employee = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    objects = AccountManager()
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
   
    REQUIRED_FIELDS = []


    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'



    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'a@a.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name     



class Address(models.Model):
    """
    Address
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=("User"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full name"),max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'address'
        verbose_name_plural = 'addresss'

        def __str__(self) -> str:
            return "Address"



class kebele(models.Model):
    user = models.ForeignKey(User , on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("kebele"), help_text=_("Required"), max_length=255, unique=True)
    email = models.EmailField()
    address = models.CharField(_("Town/City/State"), max_length=150)
    is_active = models.BooleanField(default=True)
    fox_number = models.CharField(max_length=100)



    

    class Meta:
        verbose_name = _("kebele")
        verbose_name_plural = _("kebeles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kebele_detail", kwargs={"pk": self.pk})



class residents(models.Model):
    pass



class Kebele_employee(models.Model):
    pass