from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('posts.urls', namespace='posts')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
