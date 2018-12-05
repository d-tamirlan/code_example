from django.contrib import admin
from . import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Area)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DetentionPlace)
class DetentionPlaceAdmin(admin.ModelAdmin):
    pass
