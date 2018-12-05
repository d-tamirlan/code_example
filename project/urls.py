from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('main.urls', namespace='main')),
    path('', include('res_vac.urls', namespace='res_vac')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
