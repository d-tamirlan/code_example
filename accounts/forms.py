from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from phonenumber_field.phonenumber import to_python

from . import models


class BaseRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(BaseRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['title'] = 'В формате +7ХХХ ХХХ ХХ ХХ'

    def clean_email(self):
        """ Unique email validation """
        if User.objects.filter(email__iexact=self.cleaned_data['email']).exclude(email='').exists():
            raise forms.ValidationError('Аккаунт с таки почтовым адресом уже существует. Используйте другой.')
        return self.cleaned_data['email']

    def clean_phone(self):
        """ Unique phone validation """
        exist_applicant = models.Applicant.objects.filter(phone=self.cleaned_data['phone']).exclude(phone='').exists()
        exist_employer = models.Employer.objects.filter(phone=self.cleaned_data['phone']).exclude(phone='').exists()
        if exist_applicant or exist_employer:
            raise forms.ValidationError('Аккаунт с таким номером уже существует. Используйте другой.')
        return self.cleaned_data['phone']

    def clean(self):
        cleaned_data = super(BaseRegistrationForm, self).clean()

        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if email == '' and phone == '':
            self.add_error('email', 'Вы должны заполнить хотябы одно из этих полей')
            self.add_error('phone', 'Вы должны заполнить хотябы одно из этих полей')

        return cleaned_data


class ApplicantRegistration(BaseRegistrationForm):
    class Meta:
        model = models.Applicant
        fields = ('email', 'phone')


class EmployerRegistration(BaseRegistrationForm):
    class Meta:
        model = models.Employer
        fields = ('email', 'phone')


class LoginForm(AuthenticationForm):

    def clean_username(self):
        """ Find user and return his username

            Applicant can auth by email or phone, so we try find user by email or phone
            if we found him we return his username for future auth
        """
        username = to_python(self.cleaned_data['username'])

        applicant = models.Applicant.objects.filter(Q(email=username) | Q(phone=username)).first()

        if applicant is not None:
            return applicant.username

        employer = models.Employer.objects.filter(Q(email=username) | Q(phone=username)).first()

        if employer is not None:
            return employer.username

        return self.cleaned_data['username']


class ApplicantData(forms.ModelForm):
    class Meta:
        model = models.Applicant
        fields = ('first_name', 'last_name', 'patronymic', 'gender', 'photo', 'birth_date',
                  'citizenship', 'living_area', 'about')


class EmployerData(forms.ModelForm):
    class Meta:
        model = models.Employer
        fields = ('first_name', 'about', 'phone', 'email')
