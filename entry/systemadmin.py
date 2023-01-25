from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from entry.models import LeaveReportKebele_employee, SystemAdmin, User, KebeleEmploye, Resident, Kebele,FeedBackSkebele_employee, FeedBackResident, Vitalevent
from .forms import EditResidentForm, KebeleForm, ResidentForm,KebeleEmployForm

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
    kebele_employee_attendance_leave_list=[]

    employees = KebeleEmploye.objects.all() 
    for employe in employees:
        resident = Resident.objects.filter(employe_id=employe.admin.id).count()
        leave =  LeaveReportKebele_employee.object.filter(employe_id=employe.id,leave_status=1).count()
        kebele_employee_attendance_leave_list.append(leave)
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

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_employee(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    return render(request, "admin/add_employee_template.html")

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_employee_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        age = request.POST.get('age')
        phone = request.POST.GET('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.create_user(username=username, password=password, email=email, fname=fname, lname=lname,age=age,phone=phone, user_type=2)
            user.kebele_employee.address = address
            user.save()
            messages.success(request, "Employee Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_employee')


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def manage_employee(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    employees = KebeleEmploye.objects.all()
    context = {
        "eployees": employees
    }
    return render(request, "admin/manage_employee_template.html", context)


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_employee(request, employees_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    employees = KebeleEmploye.objects.get(admin=employees_id)

    context = {
        "employee": employees,
        "id": employees_id
    }
    return render(request, "admin/edit_eployees_template.html", context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_employee_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employees_id = request.POST.get('employee_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        try:
            # INSERTING into user Model
            user = User.objects.get(id=employees_id)
            user.fname = fname
            user.lname = lname
            user.email = email
            user.username = username
            user.phone = phone
            user.save()
            
            # INSERTING into Employee Model
            employee_model = KebeleEmploye.objects.get(admin=employees_id)
            employee_model.address = address
            employee_model.save()

            messages.success(request, "Employee Updated Successfully.")
            return redirect('/edit_employee/'+employees_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_employee/'+employees_id)


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def delete_employee(request, employee_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    employee = KebeleEmploye.objects.get(admin=employee_id)
    try:
        employee.delete()
        messages.success(request, "Employee Deleted Successfully.")
        return redirect('manage_employee')
    except:
        messages.error(request, "Failed to Delete Employee.")
        return redirect('manage_employee')



@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_resident(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    form = ResidentForm()
    context = {
        "form": form
    }
    return render(request, 'admin/add_resident_template.html', context)



@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_resident_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_resident')
    else:
        form = ResidentForm(request.POST, request.FILES)

        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            kebele_id= form.cleaned_data['kebele_id']
            vitalevent_id= form.cleaned_data['vitalevent_id']
            age = form.cleaned_data['age']
            phone = form.cleaned_data['phone']
            sex = form.cleaned_data['sex']


            try:
                user = User.objects.create_user(username=username, age=age, email=email, fname=fname,kebele_id=kebele_id,vitalevent_id=vitalevent_id, lname=lname,phone=phone,sex=sex, user_type=3)
                user.residents.address = address

                kebele_obj = Kebele.objects.get(id=kebele_id)
                user.residents.kebele_id = kebele_obj

                vitalevent_obj =Vitalevent.objects.get(id=vitalevent_id)
                user.residents.session_year_id = vitalevent_obj

                user.sresidents.sex = sex
                user.save()
                messages.success(request, "Residents Added Successfully!")
                return redirect('add_resident')
            except:
                messages.error(request, "Failed to Add Resident!")
                return redirect('add_resident')
        else:
            return redirect('add_resident')

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def manage_resident(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    residents = Resident.objects.all()
    context = {
        "residents": residents
    }
    return render(request, 'admin/manage_student_template.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
def edit_resident(request, resident_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    # Adding Residents ID into Session Variable
    request.session['resident_id'] = resident_id

    resident = Resident.objects.get(admin=resident_id)
    form = EditResidentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = resident.admin.email
    form.fields['username'].initial = resident.admin.username
    form.fields['fname'].initial = resident.admin.fname
    form.fields['lname'].initial = resident.admin.lname
    form.fields['address'].initial = resident.address
    form.fields['age'].initial = resident.age
    form.fields['phone'].initial = resident.phone
    form.fields['kebele_id'].initial = resident.kebele_id.id
    form.fields['sex'].initial = resident.sex
    form.fields['vitalevent_id'].initial = resident.vitalevent_id.id

    context = {
        "id": resident_id,
        "username": resident.admin.username,
        "form": form
    }
    return render(request, "admin/edit_resident_template.html", context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_resident_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        resident_id = request.session.get('resident_id')
        if resident_id == None:
            return redirect('/manage_resident')    

        form = EditResidentForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            sex = form.cleaned_data['sex']
            kebele_id= form.cleaned_data['kebele_id']
            vitalevent_id= form.cleaned_data['vitalevent_id']
            age = form.cleaned_data['age']
            phone = form.cleaned_data['phone']
            sex = form.cleaned_data['sex']


            try:
                # First Update into User Model
                user = User.objects.get(id=resident_id)
                user.fname = fname
                user.lname = lname
                user.email = email
                user.username = username

                user.save()

                # Then Update Residens Table
                resident_model = Resident.objects.get(admin=resident_id)
                resident_model.address = address

                kebele = Kebele.objects.get(id=kebele_id)
                resident_model.kebele_id = kebele

                vitalevent_obj =Vitalevent.objects.get(id=vitalevent_id)
                resident_model.viltalevent_id = vitalevent_obj
                resident_model.age = age
                resident_model.phone = phone

                resident_model.sex = sex
                resident_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['resident_id']

                messages.success(request, "Resident Updated Successfully!")
                return redirect('/edit_resident/'+resident_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_resident/'+resident_id)
        else:
            return redirect('/edit_resident/'+resident_id)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def delete_resident(request, student_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    resident = Resident.objects.get(admin=student_id)
    try:
        resident.delete()
        messages.success(request, "Resident Deleted Successfully.")
        return redirect('manage_resident')
    except:
        messages.error(request, "Failed to Delete Resident.")
        return redirect('manage_resident')

@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def check_email_exist(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    email = request.POST.get("email")
    user_obj = User.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def check_username_exist(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    username = request.POST.get("username")
    user_obj = User.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def resident_feedback_message(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    feedbacks = FeedBackResident.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin/resident_feedback_template.html', context)


@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def resident_feedback_message_reply(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackResident.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def employee_feedback_message(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    feedbacks = FeedBackSkebele_employee.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/employee_feedback_template.html', context)


@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def staff_feedback_message_reply(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackSkebele_employee.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")



@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def employee_leave_view(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    leaves = LeaveReportKebele_employee.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'admin/employee_leave_view.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def employee_leave_approve(request, leave_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    leave = LeaveReportKebele_employee.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('employee_leave_view')

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def employee_leave_reject(request, leave_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    leave = LeaveReportKebele_employee.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('employee_leave_view')        