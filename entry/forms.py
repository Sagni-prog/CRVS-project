from multiprocessing import AuthenticationError
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from django import forms 
from django.forms import Form
from entry.models import Resident, KebeleEmploye,Kebele, SessionYearModel,User

class DateInput(forms.DateInput):
    input_type = "date"



class UserCreationFrom(UserCreationForm):
    class Mate:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']



class UserLoginForm(AuthenticationError):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))



class KebeleForm(forms.Form):
    # class Meta:
    #     model = Kebele
    #     fields = ['kebele_name', 'phone', 'email', 'address','po_number']
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    fname = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    lname = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    po_number = forms.CharField(label="Post Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))


class ResidentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    fname = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    lname = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Kebele
    try:
        kebele = Kebele.objects.all()
        kebele_list = []
        for kebele in kebele:
            single_kebele = (kebele.id, kebele.kebele_name)
            kebele_list.append(single_kebele)
    except:
        kebele_list = []

    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_birth_date_year)+" to "+str(session_year.session_death_date_year))
            session_year_list.append(single_session_year)
    except:
        session_year_list = []


    try:
        resident = Resident.objects.all()
        resident_list = []

        for resident in resident:
            single_resident = (resident.id,resident.resident_name)
            resident_list.append[single_resident]
    except:
        resident_list=[]         


    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    current_status_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    marital_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    
    kebele = forms.ChoiceField(label="Kebele", choices=kebele_list, widget=forms.Select(attrs={"class":"form-control"}))
    resident = forms.ChoiceField(label="Resident", choices=kebele_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    birth_date_year = forms.DateField(label="birth_date",  widget=DateInput(attrs={"class":"form-control"}))
    death_date_year = forms.DateField(label="death_date", widget=DateInput(attrs={"class":"form-control"}))
    current_status = forms.ChoiceField(label="current_status_list", choices=current_status_list, widget=forms.Select(attrs={"class":"form-control"}))
    marital = forms.ChoiceField(label="Gender", choices=marital_list, widget=forms.Select(attrs={"class":"form-control"}))
       




class EditResidentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    fname = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    lname = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Kebele
    try:
        kebele = Kebele.objects.all()
        kebele_list = []
        for kebele in kebele:
            single_kebele = (kebele.id, kebele.kebele_name)
            kebele_list.append(single_kebele)
    except:
        kebele_list = []

    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_birth_date_year)+" to "+str(session_year.session_death_date_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []

    
    try:
        resident = Resident.objects.all()
        resident_list = []

        for resident in resident:
            single_resident = (resident.id,resident.resident_name)
            resident_list.append[single_resident]
    except:
        resident_list=[]      




    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    current_status_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    marital_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    
    kebele_id = forms.ChoiceField(label="Course", choices=kebele_list, widget=forms.Select(attrs={"class":"form-control"}))
    resident_id = forms.ChoiceField(label="Resident", choices=kebele_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_birth_date_year = forms.DateField(label="ession_birth_date",widget=DateInput(attrs={"class":"form-control"}))
    session_death_date_year = forms.DateField(label="session_death_date",widget=DateInput(attrs={"class":"form-control"}))
    current_status = forms.ChoiceField(label="Gender", choices=current_status_list, widget=forms.Select(attrs={"class":"form-control"}))
    marital = forms.ChoiceField(label="Gender", choices=marital_list, widget=forms.Select(attrs={"class":"form-control"}))
     

class KebeleEmployForm(forms.Form):
    # class Meta:
    #     model = KebeleEmploye
    #     fields = ['fname', 'lname','age','phone', 'email', 'address','sex'] 

    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    fname = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    lname = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    

    try:
        kebele = Kebele.objects.all()
        kebele_list = []
        for kebele in kebele:
            single_kebele = (kebele.id, kebele.kebele_name)
            kebele_list.append(single_kebele)
    except:
        kebele_list = []
    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []
          
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    current_status_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    marital_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    
    kebele = forms.ChoiceField(label="Kebele", choices=kebele_list, widget=forms.Select(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))    
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    age = forms.CharField(label="Age", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone = forms.CharField(label="Phone", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditKebeleEmployForm(forms.Form):
    # class Meta:
    #     model = KebeleEmploye
    #     fields = ['fname', 'lname','age','phone', 'email', 'address','sex'] 

    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    fname = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    lname = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    

    try:
        kebele = Kebele.objects.all()
        kebele_list = []
        for kebele in kebele:
            single_kebele = (kebele.id, kebele.kebele_name)
            kebele_list.append(single_kebele)
    except:
        kebele_list = []
    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []
    
    try:
        employee = KebeleEmploye.objects.all()
        employee_list = []

        for employee in employee:
            single_employee = (employee.id,employee.employee_name)
            employee_list.append[single_employee]
    except:
        employee_list=[]        
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    current_status_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    marital_list = (
        ('Yes','YES'),
        ('NO','NO')
    )
    
    kebele_id = forms.ChoiceField(label="Kebele", choices=kebele_list, widget=forms.Select(attrs={"class":"form-control"}))
    employee_id = forms.ChoiceField(label="Kebele", choices=employee_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))        