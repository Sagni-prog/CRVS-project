from multiprocessing import AuthenticationError
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from django import forms 
from django.forms import Form
from entry.models import Resident, KebeleEmploye,Vitalevent,Kebele,User



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



class KebeleForm(ModelForm):
    class Meta:
        model = Kebele
        fields = ['kebele_name', 'phone', 'email', 'address','po_number']



class ResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = ['fname', 'lname', 'email','address','age','phone','sex']        


class EditResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = ['fname', 'lname', 'email','address','age','phone','sex']
class EditResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = ['fname', 'lname', 'email','address','age','phone','sex'] 

class KebeleEmployForm(ModelForm):
    class Meta:
        model = KebeleEmploye
        fields = ['fname', 'lname','age','phone', 'email', 'address','sex'] 
        