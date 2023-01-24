from django.urls import path
from . import views , systemadmin, kebeleemployee,resident


urlpatterns = [
    path('', views.index),
    path('admin_home/', systemadmin.admin_home, name="admin_home"),
    path('loginPage/', views.loginPage, name="loginPage"),
    path('home/', views.home),

]
