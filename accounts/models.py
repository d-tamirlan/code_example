from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from dateutil.relativedelta import relativedelta
from main import models as main_models


class Applicant(User):
    class Gender:
        male = 'male'
        female = 'female'
        CHOICES = (
            (male, 'Мужской'),
            (female, 'Женский')
        )

    user = models.OneToOneField(
        User,
        parent_link=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    citizenship = models.ForeignKey(
        main_models.Area,
        verbose_name='Гражданство',
        related_name="citizenship_applicants",
        limit_choices_to={'type': 'country'},
        on_delete=models.DO_NOTHING,
        null=True
    )
    living_area = models.ForeignKey(
        main_models.Area,
        verbose_name='Место проживания',
        related_name="applicants",
        limit_choices_to={'type': 'city/district'},
        on_delete=models.DO_NOTHING,
        null=True
    )
    patronymic = models.CharField('Отчество', max_length=100, default='', blank=True)
    phone = PhoneNumberField('Номер телефона', default='', blank=True)
    gender = models.CharField('Пол', max_length=100, choices=Gender.CHOICES)
    photo = models.ImageField('Фото', upload_to="applicants/", blank=True)
    birth_date = models.DateField('Дата рождения', default=timezone.now)
    about = models.TextField('Обо мне', max_length=5000, default='', blank=True)

    @property
    def resume(self):
        """ Return user resume, in the current case, it can be only one """
        return self.resumes.first()

    @property
    def specializations(self):
        """ Return user specialization from educations """
        return self.resume.educations.values_list('specialization', flat=True)

    @property
    def experience(self):
        """ Return user experience counted from jobs """
        jobs = self.resume.jobs.all()
        years = [relativedelta(job.end_date, job.start_date).years for job in jobs]

        months = [
            # count months between begin end_date year and end_date date
            relativedelta(
                job.end_date,
                job.end_date.replace(month=1, day=1)  # get start of year
            ).months for job in jobs
        ]

        months_sum = sum(months)
        years_sum = sum(years) + int(months_sum / 12)

        return {'years': years_sum, 'months': months_sum % 12}

    def clean(self):
        super(Applicant, self).clean()
        if self.email:
            self.username = self.email
        else:
            self.username = self.phone

    class Meta:
        verbose_name = 'Соискателя'
        verbose_name_plural = 'Соискатели'


class Employer(User):
    user = models.OneToOneField(
        User,
        parent_link=True,
        verbose_name='Пользователь',
        related_name='employer',
        on_delete=models.CASCADE,
    )
    phone = PhoneNumberField('Номер телефона', default='')
    about = models.TextField('О компании', max_length=5000, default='')

    def clean(self):
        super(Employer, self).clean()
        if self.email:
            self.username = self.email
        else:
            self.username = self.phone

    class Meta:
        verbose_name = 'Работодателя'
        verbose_name_plural = 'Работодатели'


class Sentence(models.Model):
    class Type:
        conditional = 'conditional'
        penalty = 'penalty'
        liberty_deprivation = 'liberty_deprivation'

        CHOICES = (
            ('conditional', 'Условно'),
            ('penalty', 'Штраф'),
            ('liberty_deprivation', 'Лишение свободы')
        )
    articles = models.ManyToManyField(
        main_models.CriminalArticle,
        verbose_name='Статьи',
        related_name='sentences'
    )
    place = models.ForeignKey(
        main_models.DetentionPlace,
        verbose_name='Место заключения',
        related_name='sentences',
        on_delete=models.DO_NOTHING,
        null=True
    )
    type = models.CharField('Тип', choices=Type.CHOICES, max_length=100, default='')
    start_date = models.DateField('Дата начала', default=timezone.now)
    end_date = models.DateField('Дата окончания', default=timezone.now)

    def __str__(self):
        return 'Приговор'

    class Meta:
        verbose_name = 'Приговор'
        verbose_name_plural = 'Приговоры'
