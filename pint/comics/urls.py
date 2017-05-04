from django.conf.urls import url, include
from comics import views
from django.contrib.auth import views as auth_views
from comics import views as rview



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^register/', rview.register, name='register'),
]
