from channels.db import database_sync_to_async
from channels.testing import ChannelsLiveServerTestCase, WebsocketCommunicator
from django.test import TestCase
from django.urls import reverse

from support.consumers import AdminChatConsumer, ChatConsumer
from support.models import ChatRoom
from user.models import User


# Create your tests here.


class TestSupportPage(TestCase):
    @classmethod
    def setUp(cls):
        cls.user1_username = cls.user1_password = "user1"
        cls.user2_username = cls.user2_password = "user2"
        cls.user1_email, cls.user2_email = "user1@yandex.ru", "user2@yandex.ru"

        cls.user1 = User.objects.create_user(cls.user1_username, cls.user1_email, cls.user1_password)
        cls.user2 = User.objects.create_user(cls.user2_username, cls.user2_email, cls.user2_password, is_superuser=True)

    def test_support_status_anonym(self):
        self.client.get(reverse("home"))  # устанавливаем куки для входа в комнату анонимным пользователем
        response = self.client.get(reverse("support:chat"))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse("support:admin-chat"))
        self.assertEquals(response.status_code, 302)  # анонимного пользователя не пустит на страницу чата админа

    def test_support_status_auth(self):
        self.assertTrue(self.client.login(username=self.user1_username, password=self.user1_password))
        response = self.client.get(reverse("support:chat"))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse("support:admin-chat"))
        self.assertEquals(response.status_code, 302)  # обычного пользователя не пустит на страницу чата админа

    def test_support_status_admin(self):
        self.assertTrue(self.client.login(username=self.user2_username, password=self.user2_password))
        response = self.client.get(reverse("support:chat"))
        self.assertEquals(response.status_code, 302)  # админа перенаправит на страницу чата админа

        response = self.client.get(reverse("support:admin-chat"))
        self.assertEquals(response.status_code, 200)

        ChatRoom.objects.create(user=self.user1, slug=self.user1.id)
        response = self.client.get(reverse("support:admin-chat") + f"?user-id={self.user1.id}")
        self.assertEquals(response.status_code, 200)  # страница чата с пользователем успешно отобразилась

    def test_status_admin_chat_post(self):
        ChatRoom.objects.create(user=self.user1, slug=self.user1.id)
        self.assertEquals(ChatRoom.objects.get(slug=self.user1.id).state, "3")
        self.assertTrue(self.client.login(username=self.user2_username, password=self.user2_password))
        response = self.client.post(
            reverse("support:admin-chat") + f"?user-id={self.user1.id}",
            {"change_state": "2"},
            "application/json",
        )
        self.assertIn('status changed successfully"', response.content.decode())  # статус чата успешно поменялся
        self.assertEquals(ChatRoom.objects.get(slug=self.user1.id).state, "2")


class ChatConsumerTest(ChannelsLiveServerTestCase):
    async def connect_and_authenticate(self, communicator):
        # Соединяемся с WebSocket
        connected, subprotocol = await communicator.connect()

        # В Django Channels аутентификация уже выполняется автоматически для WebSocket соединений
        # Поэтому нет необходимости в явной аутентификации через communicator.scope['user']

        return connected, subprotocol

    async def test_chat_consumer(self):
        user1 = await self.create_user(username="user1", password="password1")
        user2 = await self.create_user(username="user2", password="password2", admin=True)

        await self.create_chatroom(user1)

        communicator_user1 = WebsocketCommunicator(ChatConsumer.as_asgi(), f"ws/support/chat/{user1.id}/")
        communicator_user2 = WebsocketCommunicator(ChatConsumer.as_asgi(), f"ws/support/chat/{user1.id}/")
        communicator_admin = WebsocketCommunicator(AdminChatConsumer.as_asgi(), "ws/support/chat/admin/")
        communicator_user1.scope["url_route"] = {"kwargs": {"user_id": user1.id}}
        communicator_user1.scope["user"] = user1
        communicator_user2.scope["url_route"] = {"kwargs": {"user_id": user1.id}}
        communicator_user2.scope["user"] = user2

        # Подключаем обоих пользователей к своим комнатам
        connected_user1, _ = await self.connect_and_authenticate(communicator_user1)
        connected_user2, _ = await self.connect_and_authenticate(communicator_user2)
        connected_admin, _ = await self.connect_and_authenticate(communicator_admin)

        self.assertTrue(connected_user1)
        self.assertTrue(connected_user2)
        self.assertTrue(connected_admin)

        # отправляем сообщение о подключении первого пользователя
        await communicator_user1.send_json_to({"type": "connect"})

        # Получаем сообщение, о том, кто находится в комнате
        response_user2 = await communicator_user2.receive_json_from()
        self.assertEqual(response_user2["type"], "user_list")
        self.assertEqual(response_user2["user_ids"], [str(user1.id)])

        # Отправляем сообщение от user1
        message_content = "Hello, user2!"
        await communicator_user1.send_json_to({"type": "message", "message": message_content, "user_id": str(user1.id)})

        # принимаем сообщение у админа
        response_admin = await communicator_admin.receive_json_from()

        self.assertEqual(response_admin["type"], "chat_message")
        self.assertEqual(response_admin["message"], message_content)
        self.assertEqual(response_admin["user_id"], user1.id)
        self.assertEqual(response_admin["username"], "user1")

        # Получаем сообщение user2
        response_user2 = await communicator_user2.receive_json_from()

        self.assertEqual(response_user2["type"], "chat_message")
        self.assertEqual(response_user2["message"], message_content)
        self.assertEqual(response_user2["user_id"], str(user1.id))
        self.assertEqual(response_user2["username"], "user1")

        # Закрываем соединение для первого пользователя
        await communicator_user1.disconnect()

        # Получаем сообщение, о том, кто находится в комнате
        response_user2 = await communicator_user2.receive_json_from()
        self.assertEqual(response_user2["type"], "user_list")

        # Закрываем соединение для второго пользователя и админа
        await communicator_user2.disconnect()
        await communicator_admin.disconnect()

    @database_sync_to_async
    def create_user(self, username, password, admin=False):
        return User.objects.create_user(username=username, password=password, is_superuser=admin)

    @database_sync_to_async
    def create_chatroom(self, user):
        return ChatRoom.objects.create(user=user, slug=user.id)
