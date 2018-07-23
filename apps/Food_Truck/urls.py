from django.conf.urls import url
from . import views

urlpatterns =[
	url(r'^$', views.home),
	url(r'login/$', views.login),
	url(r'create/$', views.create),
	url(r'create_truck/$', views.create_truck),
	url(r'dashboard/$', views.dashboard),
]