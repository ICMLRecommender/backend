from django.conf.urls import url, include

from icml_backend import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^author$', views.AuthorView.as_view(), name='author'),
    url(r'^paper$', views.PaperView.as_view(), name='paper'),
    url(r'^comment$', views.CommentView.as_view(), name='comment'),
    url(r'^like$', views.LikeView.as_view(), name='like'),
]