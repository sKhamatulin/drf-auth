# chat/serializers.py
from rest_framework import serializers
from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Message.
    """
    class Meta:
        model = Message
        fields = ['id', 'sender_type', 'client_id', 'content', 'timestamp']


class ChatRoomSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ChatRoom.
    Включает связанные сообщения.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'user', 'b24_user_id', 'created_at', 'messages']