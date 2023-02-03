from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Kebele,Resident, KebeleEmployee,FeedBackResident,LeaveReportKebele_employee,FeedBackSkebele_employee,Notification_Kebele_employee,Brith,Death,VitalEvant,Marriage

class Usermodel(UserAdmin):
    list_display= ('username','first_name','last_name','email')
    search_fields= ('first_name','username','user_type')
    list_per_page= 10

class ResidentAdmin(admin.ModelAdmin):
    list_display= ('fname','address','kebele', 'phone','gender','avatar', 'created_at','updated_at')
    search_fields= ('fname','username','phone','email')
    list_per_page= 10


class KebeleEmployeeAdmin(admin.ModelAdmin):
    list_display= ('first_name','last_name','address',  'created_at','updated_at')
    search_fields= ('first_name','last_name')
    list_per_page= 10

class KebeleAdmin(admin.ModelAdmin):
    list_display= ('kebele_name','email','address', 'po_number', 'created_at','updated_at')
    search_fields= ('kebele_name','email','address','po_number')
    list_per_page= 10



admin.site.register(User,Usermodel)
admin.site.register(Kebele,KebeleAdmin)
admin.site.register(Resident,ResidentAdmin)
admin.site.register(KebeleEmployee,KebeleEmployeeAdmin)
admin.site.register(LeaveReportKebele_employee)
admin.site.register(FeedBackResident)
admin.site.register(FeedBackSkebele_employee)
admin.site.register(Notification_Kebele_employee)
admin.site.register(Brith)
admin.site.register(Death)
admin.site.register(VitalEvant)
admin.site.register(Marriage)
