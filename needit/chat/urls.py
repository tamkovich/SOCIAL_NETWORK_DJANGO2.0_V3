from django.urls import path, re_path
from chat.views import ChatView

app_name = 'chat'

urlpatterns = [
	re_path(r'^(?P<room_name>[^/]+)/$', ChatView.as_view(), name='chat'),
]