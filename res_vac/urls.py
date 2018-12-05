from django.urls import path, include
from . import views


app_name = 'res_vac'

urlpatterns = [
    path('resume/', include([
        path('create/', views.ResumeCreate.as_view(), name='resume_create'),
        path('update/', views.ResumeUpdate.as_view(), name='resume_update'),
        path('delete/', views.ResumeDelete.as_view(), name='resume_delete'),
        path('<int:pk>/', views.ResumeDetail.as_view(), name='resume_detail'),
        path('list/', views.ResumeList.as_view(), name='resume_list'),
    ])),
    path('vacancy/', include([
        path('create/', views.VacancyCreate.as_view(), name='vacancy_create'),
        path('update/<int:pk>/', views.VacancyUpdate.as_view(), name='vacancy_update'),
        path('delete/<int:pk>/', views.VacancyDelete.as_view(), name='vacancy_delete'),
        path('<int:pk>/', views.VacancyDetail.as_view(), name='vacancy_detail'),
        path('list/', views.VacancyList.as_view(), name='vacancy_list'),
    ]))
]
