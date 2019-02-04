from django.conf.urls import url, include

from . import views

urlpatterns = [
	url(r'^main', views.main, name='login'),
	url(r'^x', views.main2, name='login'),
	url(r'^script_list$', views.script_list_view, name = 'script_list'),
	url(r'^start_script$', views.start_script_view, name= 'start_script'),
	url(r'^process_list$', views.process_list_view, name ='process_list'),
]