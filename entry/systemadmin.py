from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from entry.models import LeaveReportKebele_employee, SessionYearModel, SystemAdmin, User, KebeleEmploye, Resident, Kebele,FeedBackSkebele_employee, FeedBackResident
from .forms import  KebeleForm, ResidentForm,KebeleEmployForm

from django.core import serializers
import json



def admin_home(request):
    #Counting amount of all exit abjects
    all_resident_count = Resident.objects.all().count()
    all_kebele_count = Kebele.objects.all().count()
    all_kebele_employee_count = KebeleEmploye.objects.all().count()
    admin_home = SystemAdmin.objects.get(admin=request.user.id)


    # Total kebele_employe and resident in kebele

    kebele_all = Kebele.objects.all()
    kebele_list_name = []
    kebele_employee_list = []
    resident_list = []
    for kebe in kebele_all:
        kebele_employees = KebeleEmploye.objects.filter(kebele_id=kebe.id).count()
        residents= Resident.objects.filter(kebele_id=kebe.id).count()

        kebele_list_name.append(kebe.kebele_name)
        kebele_employee_list.append(kebele_employees)
        resident_list.append(residents)
    

    employee = KebeleEmploye.objects.all()
    employee_list = []
    for emplo in employee:
        employee = KebeleEmploye.objects.filter(id=emplo.id)
        employee_list.append(employee)
     

    # for Kebele employee

    kebele_employe_name_list = []
    kebele_employee_leave_list=[]

    employees = KebeleEmploye.objects.all() 
    for employe in employees:
        kebele_id = Kebele.objects.filter(id=employe.id)
        leave =  LeaveReportKebele_employee.objects.filter(id__in=kebele_id,leave_status=1).count()
        kebele_employee_leave_list.append(leave)
        kebele_employe_name_list.append(employe.fname)

    resident_name_list = []
    resident_list_in_kebele = []

    residents = Resident.objects.all()
    for resident in residents:
        kebele_id = Kebele.objects.filter(resident=resident.id)
        resident  = Resident.objects.filter(kebele_id = resident.id)
        resident_name_list.append(resident)
        resident_list_in_kebele.append(kebele_id)  



    context = {
        "all_resident_count":all_resident_count,
        "all_kebele_count":all_kebele_count,
        "all_kebele_employee_count": all_kebele_employee_count,
        "admin_home":admin_home,
        "kebele_list_name":kebele_list_name,
        "kebele_employee_list":kebele_employee_list,
        "resident_list":resident_list,
        "employee_list":employee_list,
        "kebele_employe_name_list":kebele_employe_name_list,
        "resident_name_list":resident_name_list,
        "resident_list_in_kebele":resident_list_in_kebele,
        




    }

    return render(request , "admin/home_content.html", context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_employee(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    form = KebeleEmployForm()

    context = {
        "form": form
    }
    return render(request, "admin/add_employee_template.html",context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_employee_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_employee')
    else:
        form = KebeleEmployForm(request.POST, request.FILES)
        if form.is_valid():
            fname = request.POST.GET['fname']
            lname = request.POST.GET['lname']
            username = request.POST.GET['username']
            email = request.POST.GET['email']
            password = request.POST.GET['password']
            address = request.POST.GET['address']
            kebele_id = request.POST.GET['kebele_id']
            gender = request.POST.GETa['gender']
            employee_id= request.POST.GET['employee_id']
            phone = request.POST.GET('phone')
            age = request.POST.GET('age')


            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
        

            try:
                user = User.objects.create_user(username=username, password=password, email=email, fname=fname,age=age,phone=phone,employee_id=employee_id, lname=lname, user_type=2)
                user.kebele_employee.address = address
                user.kebele_employee.gender = gender
                user.kebele_employee.profile_pic = profile_pic_url
                user.kebele_employee.ohone = phone
                user.kebele_employee.age = age


                kebele_obj = Kebele.objects.get(id=kebele_id )
                user.kebele_employee.kebele_id = kebele_obj

                employee_obj = KebeleEmploye.objects.get(id=employee_id)
                user.kebele_employee.employee_id = employee_obj
                user.save()
                messages.success(request, "Employee Added Successfully!")
                return redirect('add_employee')
            except:
                messages.error(request, "Failed to Add Employee!")
                return redirect('add_employee')


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def manage_employee(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    employees = KebeleEmploye.objects.all()
    kebele = Kebele.objects.all()
    context = {
        "employees": employees,
        'kebele': kebele
    }
    
    return render(request, "admin/manage_employee_template.html", context)


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_employee(request, employees_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    employee = KebeleEmploye.objects.get(admin=employees_id)
    form = KebeleEmployForm(request.POST, request.FILES)
    # Filling the form with Data frome Database

    form.fields['email'].initial = employee.admin.email
    form.fields['username'].initial = employee.admin.username
    form.fields['fname'].initial = employee.admin.fname
    form.fields['lname'].initial = employee.admin.lname
    form.fields['address'].initial = employee.address
    form.fields['kebele_id'].initial = employee.kebele_id.id
    form.fields['gender'].initial = employee.gender
    form.fields['session_year_id'].initial = employee.session_year_id.id
    form.fields['employee_id'].initial = employee.employee_id.id


    context = {
        "id": employees_id,
        "username": employees_id.admin.username,
        "form":form
    }


    return render(request, "admin/edit_emplooyees_template.html", context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_employee_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        kebele_employee_id = request.session.get('kebele_employee_id')
        if kebele_employee_id == None:
            return redirect('/manage_employee')

        form = KebeleEmployForm(request.POST, request.FILES)
        if form.is_valid:
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            session_year_id =form.cleaned_data['session_year_id']
            kebele_id = form.cleaned_data['kebele_id']
            gender = form.cleaned_data['gender']
            employee_id= form.cleaned_data['employee_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

        try:
            # INSERTING into user Model
            user = User.objects.get(id=kebele_employee_id)
            user.fname = fname
            user.lname = lname
            user.email = email
            user.username = username
            # user.phone = phone
            user.save()
            
            # INSERTING into Employee Model
            employee_model = KebeleEmploye.objects.get(admin=kebele_employee_id)
            employee_model.address = address
            

            kebele = Kebele.objects.get(id = kebele_id)
            employee_model.kebele_id = kebele
            
            employee = Kebele.objects.get(id = employee_id)
            employee_model.employee_id = employee

            session_year_obj = SessionYearModel.objects.get(id=session_year_id)
            employee_model.session_year_id = session_year_obj 


            employee_model.gender = gender
            if profile_pic_url != None:
                employee_model.profile_pic = profile_pic_url

            employee_model.save()

            # Delete Employee_id SESSION after the data is updated

            del request.session['kebele_employee_id']    
            

            messages.success(request, "Employee Updated Successfully.")
            return redirect('/edit_employee/'+kebele_employee_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_employee/'+kebele_employee_id)


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
            email = form.cleaned_data['email']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            kebele= form.cleaned_data['kebele']
            # resident= form.cleaned_data['resident']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']
            birth_date_year = form.cleaned_data['birth_date_year']
            death_date_year = form.cleaned_data['death_date_year']
            current_status = form.cleaned_data('current_status')
            marital = form.cleaned_data('marital')


            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

        

            try:
                user = User.objects.create_user(username=username,  email=email, fname=fname,kebele=kebele, lname=lname, user_type=3)
                user.residents.address = address

                kebele_obj = Kebele.objects.get(id=kebele)
                user.residents.kebele_id = kebele_obj

                resident_id = Resident.objects.get(id=resident_id)
                user.residents.resident_id = resident_id

                user.resident.gender = gender
                user.resident.current_status = current_status
                user.resident.marital = marital
                user.residents.birth_date_year = birth_date_year
                user.residents.death_date_year = death_date_year

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.residents.session_year_id = session_year_obj

                if profile_pic_url != None:
                    user.residents.profile_pic = profile_pic_url
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
    return render(request, 'admin/manage_resident_template.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
def edit_resident(request, resident_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    # Adding Residents ID into Session Variable
    request.session['resident_id'] = resident_id

    resident = Resident.objects.get(admin=resident_id)
    form = ResidentForm()
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
    form.fields['current_status'].initial = resident.current_status
    form.fields['marital'].initial = resident.marital

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

        form = ResidentForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            sex = form.cleaned_data['sex']
            kebele= form.cleaned_data['kebele_id']
            session_year_id = form.cleaned_data['session_year_id']
            age = form.cleaned_data['age']
            phone = form.cleaned_data['phone']
            sex = form.cleaned_data['sex']
            current_status = form.cleaned_data['current_status']
            marital = form.cleaned_data['marital']


            try:
                # First Update into User Model
                user = User.objects.get(id=resident_id)
                user.first_name = fname
                user.last_name = lname
                user.email = email
                user.username = username

                user.save()

                # Then Update Residens Table
                resident_model = Resident.objects.get(admin=resident_id)
                resident_model.address = address
                resident_model.current_status = current_status
                resident_model.marital = marital

                kebele = Kebele.objects.get(id=kebele)
                resident_model.kebele_id = kebele
                resident_model.age = age
                resident_model.phone = phone
                resident_model.sex = sex

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.residents.session_year_id = session_year_obj

                # vitalevent_obj =Vitalevent.objects.get(id=vitalevent_id)
                # resident_model.viltalevent_id = vitalevent_obj


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
    return render(request, 'admin/employee_feedback_template.html', context)


@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def employee_feedback_message_reply(request):
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




@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_kebele(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)

    form = KebeleForm()

    context = {
        'form':form
    }
    return render(request, "admin/add_kebele_template.html", context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_kebele_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_kebele')
    else:
        form = KebeleForm()
        if form.is_valid():
            email = form.cleaned_data['email']
            kebele_name = form.cleaned_data['kebele_name']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            po_number = form.cleaned_data['po_number']
      
        try:
            kebele = Kebele.objects.create_user(username=username,  email=email,kebele_name=kebele_name,po_number=po_number)
            kebele.kebele.address = address
            kebele.save()
            messages.success(request, "Kebele Added Successfully!")
            return redirect('add_kebele')
        except:
            messages.error(request, "Failed to Add Kebele!")
            return redirect('add_kebele')

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def manage_kebele(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    kebeles = Kebele.objects.all()
    context = {
        "kebeles": kebeles
    }
    return render(request, 'admin/manage_kebele_template.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_kebele(request, kebele_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    kebele = Kebele.objects.get(id=kebele_id)
    context = {
        "kebele": kebele,
        "id": kebele_id
    }
    return render(request, 'admin/edit_kebele_template.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_kebele_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        kebele_id = request.POST.get('kebele_id')
        kebele_name = request.POST.get('kebele')

        try:
            kebele = Kebele.objects.get(id=kebele_id)
            kebele.course_name = kebele_name
            kebele.save()

            messages.success(request, "Kebele Updated Successfully.")
            return redirect('/edit_course/'+kebele_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+kebele_id)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def delete_kebele(request, kebele_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    kebele = Kebele.objects.get(id=kebele_id)
    try:
        kebele.delete()
        messages.success(request, "Kebele Deleted Successfully.")
        return redirect('manage_kebele')
    except:
        messages.error(request, "Failed to Delete Kebele.")
        return redirect('manage_kebele')



@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def admin_profile(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    user = User.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'admin/admin_profile.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def admin_profile_update(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        password = request.POST.get('password')

        try:
            customuser = User.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
def kebele_employe_profile(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    pass


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
def manage_session(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "admin/manage_session_template.html", context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_session(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    return render(request, "admin/add_session_template.html")

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def add_session_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_resident')
    else:
        session_birth_date_year = request.POST.get('session_birth_date_year')
        session_death_date_year = request.POST.get('session_death_date_year')

        try:
            sessionyear = SessionYearModel(session_birth_date_year=session_birth_date_year, session_death_date_year=session_death_date_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_session(request, session_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "admin/edit_session_template.html", context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def edit_session_save(request):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_brith_date_year = request.POST.get('session_brith_date_year')
        session_death_date_year = request.POST.get('session_death_date_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_brith_date_year = session_brith_date_year
            session_year.session_death_date_year = session_death_date_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def delete_session(request, session_id):
    admin_home = SystemAdmin.objects.get(admin=request.user.id)
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')

