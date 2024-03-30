from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from CharPage.models import CharModel
from user.models import User


# Create your tests here.


class TestTalents(TestCase):
    @classmethod
    def setUp(cls):
        cls.create_talent = {
            "name": "Test",
            "url": "http://127.0.0.1:8000/talents/#L",
            "class": "../static/img/classes/warrior.jpg",
            "spec": "../static/img/Talents/trees/warrior_1.jpg",
        }

        cls.deltalent = {"deltalent_id": "1"}

        cls.user1_username = cls.user1_password = "user1"
        cls.user2_username = cls.user2_password = "user2"
        cls.user1_email, cls.user2_email = "user1@yandex.ru", "user2@yandex.ru"

        cls.user1 = User.objects.create_user(cls.user1_username, cls.user1_email, cls.user1_password)
        cls.user2 = User.objects.create_user(cls.user2_username, cls.user2_email, cls.user2_password)

        cls.room_id = "8d87df22-0506-4445-b143-dcb59713cb08"
        CharModel.objects.create(
            room_id=cls.room_id,
            creator=cls.user1,
            last_update_time=timezone.now(),
            allow_edit=False,
            creating=False,
            race="1",
            gender="1",
            items="",
            face="0,0,0,0,0",
        )

        cls.create_talent_with_char = {
            "name": "q",
            "url": "http://127.0.0.1:8000/talents/#L",
            "class": "../static/img/classes/warrior.jpg",
            "spec": "../static/img/Talents/trees/warrior_1.jpg",
            "char": cls.room_id,
        }

    def test_status(self):
        response = self.client.get(reverse("talants"))
        self.assertEquals(response.status_code, 200)

    def test_create_talent(self):
        response = self.client.post(reverse("talants"), self.create_talent, "application/json")
        self.assertIn("access error", response.content.decode())  # Не авторизированный пользователь не может
        # создать таланты

        self.assertTrue(self.client.login(username=self.user1_username, password=self.user1_password))
        response = self.client.post(reverse("talants"), self.create_talent, "application/json")
        self.assertIn("talents successfully saved", response.content.decode())  # Таланты успешно созданны

        response = self.client.post(reverse("talants"), self.create_talent_with_char, "application/json")
        self.assertIn(
            "talents are successfully saved and tied to the character",
            response.content.decode(),
        )  # Таланты
        # успешно созданы и привязаны к персонажу

        response = self.client.post(reverse("talants"), self.create_talent_with_char, "application/json")
        self.assertIn(
            "talents are successfully saved and tied to the character",
            response.content.decode(),
        )  # Таланты
        # успешно созданы и привязаны к персонажу

        response = self.client.post(reverse("talants"), self.create_talent_with_char, "application/json")
        self.assertIn("the character has too many talents", response.content.decode())  # Персонаж имеет слишком много
        # талантов

        response = self.client.post(reverse("talants"), self.deltalent, "application/json")
        self.assertIn("data was successfully talent deleted", response.content.decode())  # Таланты успешно удалены
