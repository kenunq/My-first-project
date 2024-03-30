import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from support.models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = {}

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user_id = self.scope["user"].id if self.scope["user"].username else self.room_name

        # Присоединение к комнате
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        self.connected_users.get(self.room_name, set()).discard(str(self.user_id))
        await self.send_user_list()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type = text_data_json.get("type")
        message = text_data_json.get("message")
        sended_time = datetime.now().strftime("%H:%M")
        user_id = text_data_json.get("user_id")
        # self.channel_name - уникальный номер участника группы

        if type == "message":
            await self.create_message(message, user_id, sended_time)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sended_time": sended_time,
                    "user_id": user_id,
                    "username": self.scope["user"].username if self.scope["user"].username else "Anonymous",
                },
            )

            # Отправка сообщения админу (для уведомлений)
            channel_layer_admin = get_channel_layer()

            await channel_layer_admin.group_send(
                "chat_admin",
                {
                    "type": "chat_message",
                    "message": message,
                    "sended_time": sended_time,
                    "user_id": self.room_name,
                    "username": self.scope["user"].username if self.scope["user"].username else "Anonymous",
                },
            )

        # добавление польователя в список присоединенных пользователей
        if type == "connect":
            self.connected_users.setdefault(self.room_name, set()).add(str(self.user_id))
            await self.send_user_list()

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["type"],
                    "message": event["message"],
                    "sended_time": event["sended_time"],
                    "user_id": event["user_id"],
                    "username": event["username"],
                }
            )
        )

    @database_sync_to_async
    def create_message(self, body, user_id, sended_time):
        message = Message.objects.create(body=body, user_id=user_id, sended_time=sended_time)
        chat_room = ChatRoom.objects.get(slug=self.room_name)
        chat_room.messages.add(message)
        chat_room.last_message = message.body
        if chat_room.state not in ["2", "4", "3"]:
            chat_room.state = "3"
        chat_room.save()

    async def send_user_list(self):
        # Получаем список пользователей из словаря
        user_ids = list(self.connected_users.get(self.room_name, set()))

        # Отправляем обновленный список пользователей всем участникам комнаты
        await self.channel_layer.group_send(self.room_group_name, {"type": "user_list", "user_ids": user_ids})

    async def user_list(self, event):
        # Отправляем обновленный список пользователей только конкретному пользователю
        await self.send(text_data=json.dumps({"type": event["type"], "user_ids": event["user_ids"]}))


class AdminChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "admin"
        self.room_group_name = f"chat_{self.room_name}"

        # Присоединение к комнате
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        # Обработчик для сообщений типа 'chat_message'
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["type"],
                    "message": event["message"],
                    "sended_time": event["sended_time"],
                    "user_id": event["user_id"],
                    "username": event["username"],
                }
            )
        )
