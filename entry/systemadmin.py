from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from entry.models import SystemAdmin, User, KebeleEmploye, Resident, Kebele,FeedBackSkebele_employee, FeedBackResident
from .forms import KebeleForm, ResidentForm,KebeleEmployForm

from django.core import serializers
import json



def admin_home(request):
    #Counting amount of all exit abjects
    all_resident_count = Resident.objects.all().count()
    kebele_count = Kebele.objects.all().count()
    kebele_employee_count = KebeleEmploye.objects.all().count()
    admin_home = SystemAdmin.objects.get(admin=request.user.id)


    # Total kebele_employe and resident in kebele

    kebele_all = Kebele.objects.all()
    kebele_list_name = []
    kebele_employee_list = []
    resident_list = []
    for kebe in kebele_all:
        kebele_employees = KebeleEmploye.objects.filter(kebe_id=kebe.id).count()
        residents= Resident.objects.filter(kebe_id=kebe.id).count()

        kebele_list_name.append(kebe.kebe_name)
        kebele_employee_list.append(kebele_employees)
        resident_list.append(residents)
    

    employee = KebeleEmploye.objects.all()
    employee_list = []
    resident_list_in_kebele = []
    for emplo in employee:
        kebele = KebeleEmploye.objects.filter(id=emplo.kebe_id.id).count()
        resident_count = Resident.objects.filter(kebe_id=kebele.id).count()
        employee_list.append(emplo.emplo_name)
        resident_list_in_kebele.append(resident_count)

    # for Kebele employee

    kebele_employe_name_list = []

    employees = KebeleEmploye.objects.all() 
    for employe in employees:
        resident = Resident.objects.filter(employe_id=employe.admin.id).count()
        kebele_employe_name_list.append(employe.admin.fname)

        
   # for resident

    resident_vitalevent = []
    resident_name_list = []
    resident_alls = Resident.objects.all()
    for residents in resident_alls:
        resident = Resident.objects.filter(residents_id=residents.id).count()
        vitalevent = vitalevent.object.filter(resident_id = resident.id).count()
        resident_name_list.append(residents.admin.fname)
        resident_vitalevent.append(vitalevent)


    context = {
        "all_resident_count":all_resident_count,
        "kebele_count":kebele_count,
        "kebele_employee_count": kebele_employee_count,
        "admin_home":admin_home,
        "kebele_list_name":kebele_list_name,
        "kebele_employee_list":kebele_employee_list,
        "resident_list":resident_list,
        "employee_list":employee_list,
        "resident_list_in_kebele":resident_list_in_kebele,
        "kebele_employe_name_list":kebele_employe_name_list,
        "resident_vitalevent":resident_vitalevent,
        "resident_name_list":resident_name_list,


    }

    return render(request , "admin/home_content.html", context)

