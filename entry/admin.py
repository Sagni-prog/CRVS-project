from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Kebele,Resident, KebeleEmploye,FeedBackResident,LeaveReportKebele_employee,FeedBackSkebele_employee,Notification_Kebele_employee,SessionYearModel

class Usermodel(UserAdmin):
    pass

admin.site.register(User,Usermodel)
admin.site.register(Kebele)
admin.site.register(Resident)
admin.site.register(KebeleEmploye)
admin.site.register(LeaveReportKebele_employee)
admin.site.register(FeedBackResident)
admin.site.register(FeedBackSkebele_employee)
admin.site.register(SessionYearModel)
admin.site.register(Notification_Kebele_employee)
