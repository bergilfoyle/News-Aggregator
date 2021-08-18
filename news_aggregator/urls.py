from django.contrib import admin
from django.urls import re_path, path, include
from django.conf.urls import url
from django.contrib.auth.forms import UserCreationForm
from news import views

def logged_in_switch_view(logged_in_view, logged_out_view):
    def inner_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return logged_in_view(request, *args, **kwargs)
        return logged_out_view(request, *args, **kwargs)
    return inner_view

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^userdetails/$', views.userdetails, name='userdetails'),
    path('admin/', admin.site.urls),
    path('', logged_in_switch_view(views.ArticleListView.as_view(), views.index), name='home'),
    path('index', logged_in_switch_view(views.ArticleListView.as_view(), views.index), name='index'),
    path('saved', views.SavedListView.as_view(), name='saved'),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^viewtopic/(?P<topicname>.+)$', views.viewtopic, name='viewtopic'),
    re_path(r'^changesaved/(?P<operation>.+)/(?P<pk>\d+)/(?P<source>.+)$', views.changesaved, name='changesaved')
]
