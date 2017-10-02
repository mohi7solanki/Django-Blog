from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='index'),
    url(r'^create/$', views.post_create, name='create'),
    url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete),
]