from django.urls import path, re_path
from home.views import (
	HomeView,
	FileView,
	SoundView,
	PictureView,
)
from home import views

app_name = 'home'

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	re_path(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
	# re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
	path('view_friends', views.view_friends, name='view_friends'),
	path('files/', FileView.as_view(), name='files'),
  path('sounds/', SoundView.as_view(), name='sounds'),
  re_path(r'^my_sounds/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_sounds, name='change_sounds'),
  path('pictures/', PictureView.as_view(), name='pictures'),
  re_path(r'^my_pictures/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_pictures, name='change_pictures'),
]