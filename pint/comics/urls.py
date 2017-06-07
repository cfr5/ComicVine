from django.conf.urls import url, include
from comics import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/comics/'}),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^register/', views.register, name='register'),
    url(r'^account/', views.account, name='account'),
    url(r'^shops/', views.shops, name='shops'),
    url(r'^statistics/', views.statistics, name='statistics'),
    url(r'^comic/(?P<comic_id>\d+)/$',views.comic, name='comic'),
    url(r'^author/(?P<author_id>\d+)/$',views.author, name='author'),
    url(r'^character/(?P<character_id>\d+)/$',views.character, name='character'),
]
