from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from CharPage.models import CharModel
from user.models import User


# Create your tests here.


class TestCharpage(TestCase):
    @classmethod
    def setUp(cls):
        cls.user1_username = cls.user1_password = "user1"
        cls.user2_username = cls.user2_password = "user2"
        cls.user1_email, cls.user2_email = "user1@yandex.ru", "user2@yandex.ru"

        cls.room_id = "8d87df22-0506-4445-b143-dcb59713cb08"
        cls.create_char_data = {
            "Face_options": [0, 0, 0, 0, 0],
            "Proffesions": [0, 0],
            "Name": "TestChar",
            "Class": "Разбойник",
            "Race": 1,
            "Gender": 1,
        }
        cls.update_char_data = {
            "allow_edit": False,
            "race": 1,
            "gender": 1,
            "items": "1,117575,50605,0,inv_helmet_158",
            "face": "0,0,0,0,0",
        }
        cls.delate_char_data = {"delchar_id": cls.room_id}

        cls.user1 = User.objects.create_user(cls.user1_username, cls.user1_email, cls.user1_password)
        cls.user2 = User.objects.create_user(cls.user2_username, cls.user2_email, cls.user2_password)

    def test_redirect_on_open_charlist_anonymous(self):
        response = self.client.get(reverse("char_list"))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/char/")

    def test_redirect_on_open_charlist_authenticated(self):
        self.assertTrue(self.client.login(username=self.user1_username, password=self.user1_password))
        response = self.client.get(reverse("char_list"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "char_list_page.html")

    def test_create_char(self):
        CharModel.objects.create(
            room_id=self.room_id,
            creator=self.user1,
            last_update_time=timezone.now(),
            allow_edit=False,
            creating=False,
            race="1",
            gender="1",
            items="",
            face="0,0,0,0,0",
        )

        response = self.client.get(reverse("createchar", args=(self.room_id,)))
        self.assertEquals(response.status_code, 403)  # PermissionDenied

        self.assertTrue(self.client.login(username=self.user1_username, password=self.user1_password))
        response = self.client.get(reverse("createchar", args=(self.room_id,)))
        self.assertEquals(response.status_code, 200)  # страница с созданием персонажа успешно отобразилась

        response = self.client.get(reverse("char_page_room", args=(self.room_id,)))
        self.assertEquals(response.status_code, 302)  # страница с персонажем успешно отобразилась

        response = self.client.post(
            reverse("createchar", args=(self.room_id,)),
            self.create_char_data,
            "application/json",
        )
        self.assertIn("data was successfully saved", response.content.decode())  # персонаж успешно создался

        response = self.client.get(reverse("char_list"))
        self.assertIn("TestChar", response.content.decode())  # созданный персонаж отобразился в списке персонажей

        response = self.client.get(reverse("char_page_room", args=(self.room_id,)))
        self.assertEquals(response.status_code, 200)  # страница с персонажем успешно отобразилась
        self.assertEquals("TestChar", response.context_data["name"])
        self.assertEquals(True, response.context_data["is_creator"])  # пользователь является создателем комнаты
        self.assertIn("Добавить таланты", response.content.decode())  # Создатель может добавить таланты персонажу

        response = self.client.get(reverse("createchar", args=(self.room_id,)))
        self.assertEquals(response.status_code, 302)  # Созданному персонажу нельзя изменить внешность

        response = self.client.post(
            reverse("char_page_room", args=(self.room_id,)),
            self.update_char_data,
            "application/json",
        )
        self.assertIn("data was successfully saved", response.content.decode())  # конфигурация персонажа обновилась

        self.client.logout()

        response = self.client.get(reverse("char_page_room", args=(self.room_id,)))
        self.assertEquals(response.status_code, 200)  # страница с персонажем успешно отобразилась
        self.assertEquals(
            False, response.context_data["is_creator"]
        )  # анонимный пользователь не является создателем комнаты
        self.assertNotIn(
            "Добавить таланты", response.content.decode()
        )  # анонимный пользователь не может добавить таланты персонажу
        response = self.client.post(
            reverse("char_page_room", args=(self.room_id,)),
            self.update_char_data,
            "application/json",
        )
        self.assertNotIn("data was successfully saved", response.content.decode())  # конфигурация персонажа не
        # обновилась

        self.assertTrue(self.client.login(username=self.user2_username, password=self.user2_password))
        response = self.client.get(reverse("char_page_room", args=(self.room_id,)))
        self.assertEquals(response.status_code, 200)  # страница с персонажем успешно отобразилась
        self.assertEquals(
            False, response.context_data["is_creator"]
        )  # другой пользователь не является создателем комнаты
        self.assertNotIn(
            "Добавить таланты", response.content.decode()
        )  # другой пользователь не может добавить таланты персонажу
        response = self.client.post(
            reverse("char_page_room", args=(self.room_id,)),
            self.update_char_data,
            "application/json",
        )
        self.assertNotIn("data was successfully saved", response.content.decode())  # конфигурация персонажа не
        # обновилась
        response = self.client.post(reverse("char_list"), self.delate_char_data, "application/json")
        self.assertIn("access error", response.content.decode())  # Не создатель персонажа не может удалить персонажа

        self.client.logout()

        self.assertTrue(self.client.login(username=self.user1_username, password=self.user1_password))
        response = self.client.post(reverse("char_list"), self.delate_char_data, "application/json")
        self.assertIn("The character has been successfully deleted", response.content.decode())  # Персонаж удалился
