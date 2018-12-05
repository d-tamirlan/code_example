from django import http
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import generic as gc
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from accounts.views import auth_check_decorator
from . import forms
from . import models


@method_decorator(auth_check_decorator(user_rel_name='applicant'), name='dispatch')
class ResumeCreate(CreateWithInlinesView):
    model = models.Resume
    inlines = (forms.JobInline, forms.EducationInline, forms.RecommendationInline)
    fields = ('name', 'skills')
    template_name = 'res_vac/resume/create.html'
    success_url = reverse_lazy('main:index')
    success_message = 'Резюме успешно создано'

    def dispatch(self, request, *args, **kwargs):
        applicant = self.request.user.applicant

        # If current applicant already have resume
        if applicant.resume:
            # Redirect him to resume update page
            return http.HttpResponseRedirect(reverse('res_vac:resume_update'))

        return super(ResumeCreate, self).dispatch(request, *args, **kwargs)

    def forms_valid(self, form, inlines):
        # bound current applicant with created resume
        form.instance.applicant = self.request.user.applicant

        response = super(ResumeCreate, self).forms_valid(form, inlines)

        messages.success(self.request, self.success_message)
        return response

    def forms_invalid(self, form, inlines):
        print('errors', form.errors)
        for inline in inlines:
            print('inline', inline.errors)
        return super().forms_invalid(form, inlines)


@method_decorator(auth_check_decorator(user_rel_name='applicant'), name='dispatch')
class ResumeUpdate(UpdateWithInlinesView):
    model = models.Resume
    inlines = (forms.JobInline, forms.EducationInline)
    fields = ('name', 'skills')
    template_name = 'res_vac/resume/create.html'
    success_url = reverse_lazy('res_vac:resume_update')
    success_message = 'Резюме успешно изменено'

    def dispatch(self, request, *args, **kwargs):
        applicant = self.request.user.applicant

        # If current applicant haven't yet resume
        if not applicant.resume:
            # Redirect him to resume create page
            return http.HttpResponseRedirect(reverse('res_vac:resume_create'))

        return super(ResumeUpdate, self).dispatch(request, *args, **kwargs)

    def get_inlines(self):
        for inline in self.inlines:
            exist_forms = inline.model.objects.filter(resume=self.object).exists()
            # if resume have objects of current inline form
            if exist_forms:
                # Remove additional empty forms
                inline.factory_kwargs['extra'] = 0
            else:
                # Add additional empty form
                inline.factory_kwargs['extra'] = 1

        return self.inlines

    def get_object(self, queryset=None):
        applicant = self.request.user.applicant

        # Return current applicant resume
        return applicant.resume

    def forms_valid(self, form, inlines):
        response = super(ResumeUpdate, self).forms_valid(form, inlines)

        # Adding success message
        messages.success(self.request, self.success_message)
        return response

    def forms_invalid(self, form, inlines):
        print('errors', form.errors)
        for inline in inlines:
            print(inline.model)
            print('inline', inline.errors)
        return super().forms_invalid(form, inlines)


class ResumeDelete(gc.DeleteView):
    model = models.Resume
    success_url = reverse_lazy('main:index')
    success_message = 'Резюме успешно удалено'

    def get(self, request, *args, **kwargs):
        # Turn off deletion confirm
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super(ResumeDelete, self).delete(request, *args, **kwargs)

        # Adding success message
        messages.success(self.request, self.success_message)

        return response

    def get_object(self, queryset=None):
        applicant = self.request.user.applicant

        # Return current applicant resume
        return applicant.resume


class ResumeDetail(gc.DetailView):
    model = models.Resume
    template_name = 'res_vac/resume/detail.html'
    context_object_name = 'resume'


class ResumeList(gc.ListView):
    model = models.Resume
    template_name = 'res_vac/resume/list.html'
    context_object_name = 'resumes'


@method_decorator(auth_check_decorator(user_rel_name='employer'), name='dispatch')
class VacancyCreate(SuccessMessageMixin, gc.CreateView):
    form_class = forms.VacancyCreate
    template_name = 'res_vac/vacancy/create.html'
    success_url = reverse_lazy('main:index')
    success_message = 'Вакансия успешно создана'

    def form_valid(self, form):
        # bound current employer with instance
        form.instance.employer = self.request.user.employer

        return super(VacancyCreate, self).form_valid(form)


@method_decorator(auth_check_decorator(user_rel_name='employer'), name='dispatch')
class VacancyUpdate(SuccessMessageMixin, gc.UpdateView):
    model = models.Vacancy
    form_class = forms.VacancyCreate
    template_name = 'res_vac/vacancy/create.html'
    success_message = 'Вакансия успешно изменена'

    def get_success_url(self):
        # show updated vacancy
        return reverse('res_vac:vacancy_update', kwargs={'pk': self.object.pk})


class VacancyDelete(gc.DeleteView):
    model = models.Vacancy
    success_url = reverse_lazy('main:index')
    success_message = 'Вакансия успешно удалена'

    def get(self, request, *args, **kwargs):
        # Turn off deletion confirm
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super(VacancyDelete, self).delete(request, *args, **kwargs)

        # Adding success message
        messages.success(self.request, self.success_message)

        return response


class VacancyDetail(gc.DetailView):
    model = models.Vacancy
    template_name = 'res_vac/vacancy/detail.html'
    context_object_name = 'vacancy'


class VacancyList(gc.ListView):
    model = models.Vacancy
    template_name = 'res_vac/vacancy/list.html'
    context_object_name = 'vacancies'
