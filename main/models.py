from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


class Area(models.Model):
    class Type:
        county = 'county'
        region = 'region'
        city_district = 'city_district'

        CHOICES = (
            (county, 'Страна'),
            (region, 'Регион'),
            (city_district, 'Город/район')
        )

    parent_area = models.ForeignKey(
        'self',
        verbose_name='Страна/Регион',
        related_name='child_areas',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField('Название', max_length=255, default='')
    type = models.CharField('Тип', choices=Type.CHOICES, max_length=255, default='region')
    hh_code = models.IntegerField('Head Hunter код', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Местность'
        verbose_name_plural = 'Местности'


class DetentionPlace(models.Model):
    area = models.ForeignKey(
        Area,
        verbose_name='Местность',
        related_name='detention_places',
        on_delete=models.DO_NOTHING,
        null=True)
    name = models.CharField('Название', max_length=100, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Место заключения'
        verbose_name_plural = 'Места заключений'


class CriminalArticle(models.Model):
    name = models.CharField('Название', max_length=100, default='')
    description = models.CharField('Описание', max_length=100, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Криминальную статью'
        verbose_name_plural = 'Криминальные статьи'


class Article(models.Model):
    title = models.CharField('Заголовок', max_length=255, default='')
    description = RichTextUploadingField('Описание', default='')
    image = models.ImageField('Обложка', upload_to='articles/')
    pub_date = models.DateField('Дата публикации', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Сатью'
        verbose_name_plural = 'Статьи'
