
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Kebele,KebeleEmploye, Resident,  User,FeedBackResident,FeedBackSkebele_employee

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




def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Kebele.objects.filter(
        Q(kebele_name__icontains=q) |
        Q(phone__icontains=q) |
        Q(address__icontains=q)
    )

    topics = KebeleEmploye.objects.all()[0:5]
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count}
    return render(request, 'base/home.html', context)
    return render(request, 'index.html')




def loginPage(request):
    page = 'login'

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
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('kebelemployee_home')
            elif user_type == '3':
                return redirect('index')   
            else:
                messages.error(request, "Invalid Login!")
                return redirect('loginPage')

        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('loginPage')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)




def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_User(request):
    logout(request)
    return redirect('loginPage')


# def registerPage(request):
#     form = MyUserCreationForm()
#     if request.method == 'POST':
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.is_active = False
#             user.save()
#             login(request, user)
#             messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

#             # Welcome Email
#             subject = "Welcome to Debo E-learning!!"
#             message = "Hello " + str(user.name) + "!! \n" + "Welcome to Debo E-learning\nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You"        
#             from_email = settings.EMAIL_HOST_USER
#             to_list = [user.email]
#             send_mail(subject, message, from_email, to_list, fail_silently=True)


#             # Email Address Confirmation Email
#             current_site = get_current_site(request)
#             email_subject = "Confirm your Email @ Debo E-learneing!!"
#             message2 = render_to_string('email_confirmation.html',{
#                 'name': user.name,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': generate_token.make_token(user)
#                 })

#             email = EmailMessage(
#                 email_subject,
#                 message2,
#                 settings.EMAIL_HOST_USER,
#                 [user.email],
#                 )
#             email.fail_silently = True
#             email.send()
#             return redirect('home')
               
#         else:
#             messages.error(request, 'An error occurred during registration')

#     return render(request, 'base/login_register.html', {'form': form})

                
# def activate(request,uidb64,token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError,ValueError,OverflowError,User.DoesNotExist):
#         user = None

#     if user is not None and generate_token.check_token(user,token):
#         user.is_active = True
#         user.save()
#         login(request,user)
#         messages.success(request, "Your Account has been activated!!")
#         return redirect('home')
#     else:
#         return render(request,'activation_failed.html')
