from django.conf.urls import patterns, include, url
from django.contrib import admin
from . views import (
   login,
   logout,
)


urlpatterns = [
    url(r'^login/', 'loginsys.views.login', name='login'),
    url(r'^logout/', 'loginsys.views.logout', name='logout'),
]
