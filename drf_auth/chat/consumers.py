# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.room_group_name = f'chat_{self.chat_room_id}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщения от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_type = text_data_json['sender_type']
        client_id = text_data_json['client_id']  # Используем client_id из CustomUser

        # Сохраняем сообщение в базе данных
        chat_room = await ChatRoom.objects.aget(id=self.chat_room_id)
        await Message.objects.acreate(
            chat_room=chat_room,
            sender_type=sender_type,
            client_id=client_id,
            content=message
        )

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_type': sender_type,
                'client_id': client_id,
            }
        )

    # Получение сообщения из группы
    async def chat_message(self, event):
        message = event['message']
        sender_type = event['sender_type']
        client_id = event['client_id']

        # Отправляем сообщение обратно в WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_type': sender_type,
            'client_id': client_id,
        }))