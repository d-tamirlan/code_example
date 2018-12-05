from django import http
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, reverse
from django.views import generic as gc
from . import forms
from . import models
from res_vac import models as res_vac_models


def auth_check_decorator(view_func=None, user_rel_name='', msg='Необходимо войти для доступа в личный кабинет'):
    """ Check user on authenticated

        :param view_func - decorated func, None when other params sent
        :param user_rel_name - user related name, can be 'applicant' or 'employer'
        :param msg - message for showing when user is not authenticated
    """

    if view_func is None:
        return lambda func: auth_check_decorator(func, user_rel_name=user_rel_name, msg=msg)

    def decorated_func(request, *args, **kwargs):
        user = request.user

        # if user is not authenticated
        if not hasattr(user, user_rel_name):
            # show info message
            messages.info(request, msg)
            # redirect to login page
            return http.HttpResponseRedirect(reverse('accounts:login'))

        return view_func(request, *args, **kwargs)

    return decorated_func


class BaseRegistration(gc.CreateView):
    """ Base registration class for Applicant and Employer"""
    template_name = 'accounts/registration.html'

    # custom attr
    group_name = ''

    def form_valid(self, form):
        response = super(BaseRegistration, self).form_valid(form)

        # add applicant to applicants group
        group, created = Group.objects.get_or_create(name=self.group_name, defaults={'name': self.group_name})
        self.object.groups.add(group.pk)
        self.object.save()

        return response


class ApplicantRegistration(BaseRegistration):
    """ Applicant registration """

    form_class = forms.ApplicantRegistration
    success_url = reverse_lazy('accounts:applicant_data')

    group_name = 'Соискатели'


class EmployerRegistration(BaseRegistration):
    """ Employer registration """

    form_class = forms.EmployerRegistration
    success_url = reverse_lazy('accounts:employer_data')

    group_name = 'Работодатели'


class Login(auth_views.LoginView):
    """ User authenticate """

    form_class = forms.LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        super(Login, self).form_valid(form)

        if hasattr(self.request.user, 'applicant'):
            return http.HttpResponseRedirect(reverse('accounts:applicant_data'))

        elif hasattr(self.request.user, 'employer'):
            return http.HttpResponseRedirect(reverse('accounts:employer_data'))

        else:
            return http.HttpResponseRedirect(reverse('main:index'))


@method_decorator(auth_check_decorator(user_rel_name='applicant'), name='dispatch')
class ApplicantIndex(gc.ListView):
    """ Show index page of user profile """

    model = res_vac_models.Vacancy
    template_name = 'accounts/applicant/data.html'

    def get_queryset(self):
        vacancies = super(ApplicantIndex, self).get_queryset()
        applicant = self.request.user.applicant
        vacancies = vacancies.filter(area=applicant.living_area)
        vacancies = vacancies.filter(specialization__in=applicant.specializations)
        vacancies = vacancies.filter(experience__lte=applicant.experience['years'])

        return vacancies[:10]


@method_decorator(auth_check_decorator(user_rel_name='applicant'), name='dispatch')
class ApplicantData(SuccessMessageMixin, gc.UpdateView):
    """ Updating applicant accounts data """

    model = models.Applicant
    template_name = 'accounts/applicant/data.html'
    form_class = forms.ApplicantData
    success_url = reverse_lazy('accounts:applicant_data')
    success_message = 'Ваши данные успешно изменены'

    def get_object(self, queryset=None):
        return self.request.user.applicant


@method_decorator(auth_check_decorator(user_rel_name='employer'), name='dispatch')
class EmployerData(SuccessMessageMixin, gc.UpdateView):
    """ Updating employer accounts data """

    model = models.Employer
    template_name = 'accounts/employer/data.html'
    form_class = forms.EmployerData
    success_url = reverse_lazy('accounts:employer_data')
    success_message = 'Ваши данные успешно изменены'

    def get_object(self, queryset=None):
        return self.request.user.employer
