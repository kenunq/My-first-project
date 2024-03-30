from django.test import TestCase
from django.urls import reverse

from services.models import MentorModel


# Create your tests here.


class TestServicesPage(TestCase):
    @classmethod
    def setUp(cls):
        cls.data = {
            "type": "Test",
            "server": "Test",
            "fraction": "Test",
            "class": "Test",
            "mentor": "Kenun",
            "username": "Test",
            "communication": "Test",
            "comment": "Test",
        }

        MentorModel.objects.create(name="Kenun", telegram_id=1740864511)

    def test_status(self):
        response = self.client.get(reverse("services:services"))
        self.assertEquals(response.status_code, 200)  # страница успешно отобразилась

    def test_send_message(self):
        response = self.client.post(reverse("services:services"), self.data, "application/json; utf-8")
        self.assertIn("message sent successfully", response.content.decode())  # Сообщение успешно отправилось

    def test_success_send_message_page(self):
        response = self.client.get(reverse("services:success_add"))
        self.assertEquals(response.status_code, 302)  # Пользователь перенаправляется на страницу создания записи

        response = self.client.post(reverse("services:services"), self.data, "application/json; utf-8")
        self.assertIn("message sent successfully", response.content.decode())  # Сообщение успешно отправилось

        response = self.client.get(reverse("services:success_add"))
        self.assertEquals(response.status_code, 200)  # Страница с успешным отправлением успешно отобразилась

        response = self.client.get(reverse("services:success_add"))
        self.assertEquals(response.status_code, 302)  # При повторном заходе на страницу пользователь перенаправляется
