from django.urls import path
from . import views , systemadmin, kebeleemployee,resident


urlpatterns = [
    
    path('loginPage', views.loginPage, name="loginPage"),
    path('logoutuser/', views.logout_User, name="logoutuser"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('', views.home, name="home"),
   



                #   for Systemadmin

    path('admin_home/', systemadmin.admin_home, name="admin_home"),
    path('add_employee/', systemadmin.add_employee, name="add_employee"),
    path('add_employee_save/', systemadmin.add_employee_save, name="add_employee_save"),
    path('manage_employee/', systemadmin.manage_employee, name="manage_employee"),
    path('edit_employee/<employees_id>/', systemadmin.edit_employee, name="edit_employee"),
    path('edit_employee_save/', systemadmin.edit_employee_save, name="edit_employee_save"),
    path('delete_employee/<employee_id>/', systemadmin.delete_employee, name="delete_employee"),
    path('add_kebele/', systemadmin.add_kebele, name="add_kebele"),
    path('add_kebele_save/', systemadmin.add_kebele_save, name="add_kebele_save"),
    path('manage_kebele/', systemadmin.manage_kebele, name="manage_kebele"),
    path('edit_kebele/<kebele_id>/', systemadmin.edit_kebele, name="edit_kebele"),
    path('edit_kebele_save/', systemadmin.edit_kebele_save, name="edit_kebele_save"),
    path('delete_kebele/<kebele_id>/', systemadmin.delete_kebele, name="delete_kebele"),
    path('add_resident/', systemadmin.add_resident, name="add_resident"),
    path('add_resident_save/', systemadmin.add_resident_save, name="add_resident_save"),
    path('edit_resident/<resident_id>', systemadmin.edit_resident, name="edit_resident"),
    path('edit_ridedent_save/', systemadmin.edit_resident_save, name="edit_resident_save"),
    path('manage_resident/', systemadmin.manage_resident, name="manage_resident"),
    path('delete_resident/<resident_id>/', systemadmin.delete_resident, name="delete_resident"),
    path('check_username_exist/', systemadmin.check_username_exist, name="check_username_exist"),
    path('check_email_exist/', systemadmin.check_email_exist, name="check_email_exist"),
    path('resident_feedback_message/', systemadmin.resident_feedback_message, name="resident_feedback_message"),
    path('resident_feedback_message_reply/', systemadmin.resident_feedback_message_reply, name="resident_feedback_message_reply"),
    path('employee_feedback_message/', systemadmin.employee_feedback_message, name="employee_feedback_message"),
    path('employee_feedback_message_reply/', systemadmin.employee_feedback_message_reply, name="employee_feedback_message_reply"),
    path('employee_leave_view/', systemadmin.employee_leave_view, name="employee_leave_view"),
    path('employee_leave_approve/<leave_id>/', systemadmin.employee_leave_approve, name="employee_leave_approve"),
    path('eployee_leave_reject/<leave_id>/', systemadmin.employee_leave_reject, name="employee_leave_reject"),
    path('admin_profile/', systemadmin.admin_profile, name="admin_profile"),
    path('admin_profile_update/', systemadmin.admin_profile_update, name="admin_profile_update"),
    path('manage_session/', systemadmin.manage_session, name="manage_session"),
    path('add_session/', systemadmin.add_session, name="add_session"),
    path('add_session_save/', systemadmin.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', systemadmin.edit_session, name="edit_session"),
    path('edit_session_save/', systemadmin.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', systemadmin.delete_session, name="delete_session"),
    




    path('kebeleemployee_home/', kebeleemployee.kebeleemployee_home, name="kebeleemployee_home"),

    



]
