from django.conf.urls import url
from django.contrib import admin
from . views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    addlike,
    addcomment,
)

urlpatterns = [
    url(r'^$', 'blog.views.post_list'),
    url(r'^create/$', 'blog.views.post_create'),
    url(r'^(?P<id>\d+)/$', 'blog.views.post_detail', name='detail'),
    url(r'^(?P<id>\d+)/edit/$', 'blog.views.post_update', name='update'),
    url(r'^delete/$', 'blog.views.post_delete'),
    url(r'^(?P<id>\d+)/addlike/$', addlike, name='addlike'),
    url(r'^addcomment/(?P<id>\d+)/$', addcomment, name='addcomment'),
]
