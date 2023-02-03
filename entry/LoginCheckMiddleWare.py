from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
       
        user = request.user

        #Check whether the user is logged in or not
        
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "entry.auth.User":
                    pass
                elif modulename == "entry.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("login_register")
            
            elif user.user_type == "3":
                if modulename == "entry.kebeleemployee":
                    pass
                elif modulename == "entry.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("login_register")
            
            elif user.user_type == "2":
                if modulename == "entry.resident":
                    pass
                elif modulename == "entry.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("login_register")

            else:
                return redirect("login_register")

        else:
            if request.path == reverse("login_register") or request.path == reverse("login_register"):
                pass
            else:
                return redirect("login_register")
