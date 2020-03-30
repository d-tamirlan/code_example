from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.Applicant)
class ApplicantAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': (
            'first_name', 'last_name', 'patronymic', 'phone', 'email', 'birth_date', 'gender', 'photo'
        )}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.Employer)
class EmployerAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'phone', 'email', 'about')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.Sentence)
class SentenceAdmin(admin.ModelAdmin):
    pass
