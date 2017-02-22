from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^request_reset_password/$', views.request_reset_password, name='request_reset_password'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
]
