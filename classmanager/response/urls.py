from django.urls import path
from .views import add_location, success_view
from response import views

app_name = 'response'

urlpatterns =[
    path('success/', success_view, name='success_url'),
    path('add_location/', add_location, name='add_location'),
    path('signup/',views.SignUp,name="signup"),
    path('signup/rescue_signup/',views.RescueSignUp,name="RescueSignUp"),
    path('signup/agency_signup/',views.AgencySignUp,name="AgencySignUp"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('rescue/<int:pk>/',views.RescueDetailView.as_view(),name="rescue_detail"),
    path('agency/<int:pk>/',views.AgencyDetailView.as_view(),name="agency_detail"),
    path('update/rescue/<int:pk>/',views.RescueUpdateView,name="rescue_update"),
    path('update/agency/<int:pk>/',views.AgencyUpdateView,name="agency_update"),
    path('rescue/<int:pk>/enter_marks',views.add_marks,name="enter_marks"),
    path('rescue/<int:pk>/marks_list',views.rescue_marks_list,name="rescue_marks_list"),
    path('marks/<int:pk>/update',views.update_marks,name="update_marks"),
    path('rescue/<int:pk>/add',views.add_rescue.as_view(),name="add_rescue"),
    path('rescue_added/',views.rescue_added,name="rescue_added"),
    path('rescues_list/',views.rescues_list,name="rescues_list"),
    path('agencys_list/',views.agencys_list,name="agencys_list"),
    path('agency/class_rescues_list',views.class_rescues_list,name="class_rescue_list"),
    path('rescue/<int:pk>/all_marks',views.RescueAllMarksList.as_view(),name="all_marks_list"),
    path('rescue/<int:pk>/message',views.write_message,name="write_message"),
    path('agency/<int:pk>/messages_list',views.messages_list,name="messages_list"),
    path('agency/write_notice',views.add_notice,name="write_notice"),
    path('rescue/<int:pk>/class_notice',views.class_notice,name="class_notice"),
    path('upload_assignment/',views.upload_assignment,name="upload_assignment"),
    path('class_assignment/',views.class_assignment,name="class_assignment"),
    path('assignment_list/',views.assignment_list,name="assignment_list"),
    path('update_assignment/<int:id>/',views.update_assignment,name="update_assignment"),
    path('assignment_delete/<int:id>/',views.assignment_delete,name="assignment_delete"),
    path('submit_assignment/<int:id>/',views.submit_assignment,name="submit_assignment"),
    path('submit_list/',views.submit_list,name="submit_list"),
    path('change_password/',views.change_password,name="change_password"),
]
