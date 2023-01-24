
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Kebele,KebeleEmploye, Resident, Vitalevent, User,FeedBackResident,FeedBackSkebele_employee

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from cbtp import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token




def index(request):
    return render(request, 'index.html')




def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                #return HttpResponse("admin Login")
                return redirect('admin')
            elif user_type == '2':
                return redirect('kebelemployee_home')
            elif user_type == '3':
                return redirect('home')   
            else:
                messages.error(request, "Invalid Login!")
                return redirect('home')

        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('home')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)




def home(request):
    return render(request, 'index.html')
