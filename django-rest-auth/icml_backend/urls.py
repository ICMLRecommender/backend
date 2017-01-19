from django.conf.urls import url, include

from icml_backend import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]