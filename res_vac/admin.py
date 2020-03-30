from django.contrib import admin
from . import models


class InlineJob(admin.StackedInline):
    model = models.Job
    extra = 0


class InlineEducation(admin.TabularInline):
    model = models.Education
    extra = 0


@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    inlines = (InlineJob, InlineEducation)


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    pass
