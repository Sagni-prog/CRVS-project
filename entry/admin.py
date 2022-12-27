from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Kebele,Resident, Vitalevent,KebeleEmploye

class Usermodel(UserAdmin):
    pass

admin.site.register(User,Usermodel)
admin.site.register(Kebele)
admin.site.register(Resident)
admin.site.register(Vitalevent)
admin.site.register(KebeleEmploye)
