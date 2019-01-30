from django.conf.urls import url, include

from . import views

urlpatterns = [
	url(r'^hello', views.hello, name='login'),
	url(r'^script_list$', views.script_list_view, name = 'script_list'),
	url(r'^start_script', views.start_script_view, name= 'start_script'),
]