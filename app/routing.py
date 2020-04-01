from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('app/<str:room_name>/', consumers.ChatConsumer, name='chatroom'),
]


