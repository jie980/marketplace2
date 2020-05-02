from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Room
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Join room group
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'app_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # Send message to room group
        userOne = self.scope['user']
        try:
            Room.objects.get(userOne=userOne, userTwo=self.room_name)
        except Exception as e:
            try:
                Room.objects.get(userOne=self.room_name, userTwo=userOne)
            except Exception as e:
                print(e)
                room = Room.objects.create(userOne=userOne, userTwo=self.room_name)
                room.content = ''
                room.save()
            else:
                room = Room.objects.get(userOne=self.room_name, userTwo=userOne)
                room.save()
        else:
            room = Room.objects.get(userOne=userOne, userTwo=self.room_name)
            room.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': room.content + '\n'
            }
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # self.send(text_data="Start chatting with the seller!")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userOne = self.scope['user']
        # add time and user to the message
        cur_time = datetime.now().strftime("%A, %b %d, %Y %I:%M:%S %p")
        message = '(' + cur_time + ') ' + str(userOne) + ': ' + message + '\n'
        # check again just to make sure
        try:
            Room.objects.get(userOne=self.scope['user'], userTwo=self.room_name)
        except Exception:
            try:
                Room.objects.get(userOne=self.room_name, userTwo=self.scope['user'])
            except Exception:
                room = Room.objects.create(userOne=userOne, userTwo=self.room_name)
                room.content = message
                room.save()
            else:
                room = Room.objects.get(userOne=self.room_name, userTwo=self.scope['user'])
                room.content += message
                room.save()
        else:
            room = Room.objects.get(userOne=self.scope['user'], userTwo=self.room_name)
            room.content += message
            room.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': message
            }
        )
    # Receive message from room group
    def chat_message(self, message):
        self.send(text_data=json.dumps(message))

