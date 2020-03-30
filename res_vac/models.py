from django.db import models
from django.utils import timezone
from accounts import models as accounts_models
from main import models as main_models


class Skill(models.Model):
    name = models.CharField('Название', max_length=100, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class Specialization(models.Model):
    prof_area = models.CharField('Профессиональная область', max_length=255, default='')
    name = models.CharField('Название', max_length=100, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Vacancy(models.Model):
    employer = models.ForeignKey(
        accounts_models.Employer,
        verbose_name='Работодатель',
        related_name='vacancies',
        on_delete=models.CASCADE,
        null=True
    )
    area = models.ForeignKey(
        main_models.Area,
        verbose_name='Район/Город',
        related_name='vacancies',
        on_delete=models.DO_NOTHING,
        null=True
    )
    name = models.CharField('Название', max_length=200, default='')
    specialization = models.ForeignKey(
        Specialization,
        verbose_name='Специальность',
        related_name='vacancies',
        on_delete=models.SET_NULL,
        null=True
    )
    experience = models.PositiveIntegerField('Опыт', default=0)
    salary_from = models.IntegerField('Зарплата от', default=0)
    salary_to = models.IntegerField('Зарплата до', default=0)
    description = models.TextField('Описание', max_length=5000, default='')
    active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вакансию'
        verbose_name_plural = 'Вакансии'


class Resume(models.Model):
    applicant = models.ForeignKey(
        accounts_models.Applicant,
        verbose_name='Соискатель',
        related_name='resumes',
        on_delete=models.CASCADE,
        null=True
    )
    skills = models.ManyToManyField(
        Skill,
        verbose_name='Навыки',
        related_name='resumes',
    )
    name = models.CharField('Название', max_length=255, default='')
    active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'


class Job(models.Model):
    resume = models.ForeignKey(
        Resume,
        verbose_name='Резюме',
        related_name='jobs',
        on_delete=models.CASCADE,
        null=True
    )
    detention_place = models.ForeignKey(
        main_models.DetentionPlace,
        verbose_name='Место заключения',
        on_delete=models.DO_NOTHING,
        help_text="Поле заполняется, если человек работал на месте заключения",
        null=True,
        blank=True
    )
    position = models.CharField('Должность', max_length=100, default='')
    start_date = models.DateField('Дата начала', default=timezone.now)
    end_date = models.DateField('Дата окончания', default=timezone.now)
    place = models.CharField('Место работы', max_length=200, default='')
    description = models.TextField('Описание', max_length=1000, default='')

    def __str__(self):
        return self.place

    class Meta:
        verbose_name = 'Место работы'
        verbose_name_plural = 'Места работы'


class Education(models.Model):
    class Level:
        gen_elementary = 'gen_elementary'
        gen_basic = 'gen_basic'
        spec_secondary = 'spec_secondary'
        higher = 'higher'

        CHOICES = (
            (gen_elementary, 'Начальное общее'),
            (gen_basic, 'Основное общее'),
            (spec_secondary, 'Среднее специальное'),
            (higher, 'Высшее образование')
        )
    specialization = models.ForeignKey(
        Specialization,
        verbose_name='Специальность',
        related_name='educations',
        on_delete=models.SET_NULL,
        null=True
    )
    resume = models.ForeignKey(
        Resume,
        verbose_name='Резюме',
        related_name='educations',
        on_delete=models.CASCADE,
        null=True
    )
    institution = models.CharField('Учебное заведение', max_length=200, default='')
    level = models.CharField('Уровень образования', max_length=100, choices=Level.CHOICES, null=True)
    start_date = models.DateField('Дата начала', default=timezone.now)
    end_date = models.DateField('Дата окончания', default=timezone.now)

    def __str__(self):
        return self.institution

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образования'


class Recommendation(models.Model):
    resume = models.ForeignKey(
        Resume,
        verbose_name='Резюме',
        related_name='recommendations',
        on_delete=models.CASCADE,
        null=True
    )
    description = models.CharField('Описание', max_length=1000, default='')
    scan = models.FileField('Скан', upload_to="recommendations/", blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Рекомендацию'
        verbose_name_plural = 'Рекомендации'
