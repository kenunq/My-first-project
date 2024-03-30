from django.test import TestCase
from django.urls import reverse

from user.models import User


# Create your tests here.


class TestHomePage(TestCase):
    @classmethod
    def setUp(cls):
        cls.user1_username = cls.user1_password = "user1"
        cls.user2_username = cls.user2_password = "user2"
        cls.user1_email, cls.user2_email = "user1@yandex.ru", "user2@yandex.ru"

        cls.user1 = User.objects.create_user(cls.user1_username, cls.user1_email, cls.user1_password)
        cls.user2 = User.objects.create_user(cls.user2_username, cls.user2_email, cls.user2_password)

    def test_status(self):
        response = self.client.get(reverse("home"))

        self.assertTemplateUsed(response, "HomePage/HomePage.html")
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse("home"), {"comment": ["TestComment"]})
        self.assertIn("access error", response.content.decode())  # Не авторизованный пользователь не может отправить
        # описание проблемы

        self.assertTrue(self.client.login(username=self.user1_username, password=self.user1_password))
        response = self.client.post(reverse("home"), {"comment": ["TestComment"]})
        self.assertIn("complaint sent successfully", response.content.decode())  # Описание проблемы успешно отправлено

        response = self.client.post(reverse("home"), {"comment": [""]})
        self.assertIn("complaint not sent", response.content.decode())  # Описание проблемы не было отправлено так как
        # все поля были пустые

    def test_get(self):
        response = self.client.get(reverse("home"), {"data": ["item-scaling"]})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["Content-Type"], "application/x-javascript; charset=utf-8")
        self.assertIn("Wowhead", response.content.decode())

        response = self.client.get(
            reverse("home"),
            {
                "data": ["talents"],
                "class": ["1"],
                "locale": ["8"],
                "t": ["s877LVqSDI4Awswmk4RcPCpHXhdaG2cl9Qox528t"],
                "355": [""],
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["Content-Type"], "application/x-javascript; charset=utf-8")
        self.assertIn("Wowhead", response.content.decode())
