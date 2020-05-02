from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/app/<str:room_name>/', consumers.ChatConsumer),
]


