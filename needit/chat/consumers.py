# home/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from home.models import AllMsg
from chat.models import Message
from django.contrib.auth.models import User
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        chat_type, fpk, lpk = self.scope['url_route']['kwargs']['room_name'].split('-')
        self.room_name = chat_type+'-'
        self.room_name += fpk+'-'+lpk if lpk>fpk else lpk+'-'+fpk

        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        pk = text_data_json['pk']
        Message.objects.create(
            content=message,
            id_user=pk,
            room_name=self.room_name,
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'pk': pk
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        pk = event['pk']
        msg_date = datetime.datetime.now()
        msg_date = str(msg_date)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'msg_date': msg_date,
            'message': message,
            'pk': pk,
            
        }))