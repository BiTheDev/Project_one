from django.conf.urls import url
from . import views

urlpatterns =[
	url(r'^$', views.home),
	url(r'login/$', views.login),
	url(r'create/$', views.create),
	url(r'register/$', views.register),
	url(r'create_truck/$', views.create_truck),
	url(r'dashboard/$', views.dashboard),
	url(r'logout/$', views.logout),
	url(r'shopping_list$', views.buy_menu),
	url(r'tools/$', views.tools),
	url(r'add_ingredient$', views.add_ingredient),
	url(r'add_product$', views.add_product),
	url(r'buy_ingredient$', views.buy_ingredient),
	url(r'cook$', views.cook),
	url(r'make_food$', views.make_food),
	url(r'sell$', views.sell),
]