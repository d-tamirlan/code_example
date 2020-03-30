from django import forms
from extra_views import InlineFormSetFactory
from . import models


class JobInline(InlineFormSetFactory):
    model = models.Job
    fields = ('detention_place', 'position', 'start_date', 'end_date', 'place', 'description')
    factory_kwargs = {'extra': 1}


class EducationInline(InlineFormSetFactory):
    model = models.Education
    fields = ('institution', 'level', 'specialization', 'start_date', 'end_date')
    factory_kwargs = {'extra': 1}


class RecommendationInline(InlineFormSetFactory):
    model = models.Recommendation
    fields = ('description', 'scan')
    factory_kwargs = {'extra': 1}


class VacancyCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VacancyCreate, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Vacancy
        fields = ('name', 'specialization', 'area', 'salary_from', 'salary_to', 'description')
