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
    url(r'^comic/', views.comic, name = 'comic'),
    url(r'^author/', views.author, name = 'auhor'),
    url(r'^character/', views.character, name = 'character'),
    #url(r'^(?P<product_id>\d+)/$',views.detail, name='detail'),
]
