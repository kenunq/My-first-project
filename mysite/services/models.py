from django.conf import settings
from django.db import models

from user.models import User


# Create your models here.


class ServicesModel(models.Model):
    type = models.CharField(max_length=64, verbose_name="Тип услуги")
    server = models.CharField(max_length=64, verbose_name="Сервер")
    fraction = models.CharField(max_length=32, verbose_name="Сторона")
    class_name = models.CharField(max_length=32, verbose_name="Класс")
    mentor = models.CharField(max_length=32, verbose_name="Ментор")
    communication = models.CharField(max_length=32, verbose_name="Способ связи")
    username = models.CharField(max_length=64, verbose_name="Имя пользователя")
    comment = models.CharField(max_length=264, null=True, verbose_name="Дополнительный комментарий")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Создатель услуги")
    time_of_create = models.DateTimeField(verbose_name="Время создания услуги")

    def __str__(self):
        return "Услуга: " + str(self.id)

    class Meta:
        verbose_name = "Услуге"
        verbose_name_plural = "Услуги"


class TypeModel(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название услуги")

    class Meta:
        verbose_name = "Тип услуги"
        verbose_name_plural = "Типы услуги"


class ServerModel(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название сервера")

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Серверы"


class FractionModel(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название фракции")

    class Meta:
        verbose_name = "Фракцию"
        verbose_name_plural = "Фракции"


class ClassModel(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название класса")

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"


class MentorModel(models.Model):
    name = models.CharField(max_length=64, verbose_name="Никнейм ментора")
    telegram_id = models.IntegerField()

    class Meta:
        verbose_name = "Ментора"
        verbose_name_plural = "Менторы"


class CommunicationModel(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название способа связи")

    class Meta:
        verbose_name = "Способ связи"
        verbose_name_plural = "Способы связи"
