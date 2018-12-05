from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('applicant/registration/', views.ApplicantRegistration.as_view(), name='applicant_registration'),
    path('applicant/data/', views.ApplicantData.as_view(), name='applicant_data'),

    path('employer/registration/', views.EmployerRegistration.as_view(), name='employer_registration'),
    path('employer/data/', views.EmployerData.as_view(), name='employer_data'),

    path('login/', views.Login.as_view(), name='login')
]
