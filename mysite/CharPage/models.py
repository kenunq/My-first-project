from django.db import models
from django.urls import reverse

from talants.models import TalentsModel
from user.models import User


# Create your models here.


class CharModel(models.Model):
    """#### Модель создающая поля для хранения настроек персонажа на странице Примерочная."""

    RACES = {
        1: "Human",
        2: "Orc",
        3: "Dwarf",
        4: "Nightelf",
        5: "Scourge",
        6: "Tauren",
        7: "Gnome",
        8: "Troll",
        9: "Goblin",
        10: "Bloodelf",
        11: "Draenei",
        12: "Felorc",
        13: "Naga_",
        14: "Broken",
        15: "Skeleton",
        16: "Vrykul",
        17: "Tuskarr",
        18: "Foresttroll",
        19: "Taunka",
        20: "Northrendskeleton",
        21: "Icetroll",
        22: "Worgen",
        # 23: "Gilnean",
        24: "Pandaren",
        # 25: "Pandarena",
        # 26: "Pandarenh",
        27: "Nightborne",
        28: "Highmountaintauren",
        29: "Voidelf",
        30: "Lightforgeddraenei",
        31: "Zandalaritroll",
        32: "Kultiran",
        33: "Thinhuman",
        34: "Darkirondwarf",
        35: "Vulpera",
        36: "Magharorc",
        37: "Mechagnome",
    }

    RACES_WITHOUT_ICON = (
        12,  # "Felorc"
        13,  # "Naga_"
        14,  # "Broken"
        15,  # "Skeleton"
        16,  # "Vrykul"
        17,  # "Tuskarr"
        18,  # "Foresttroll"
        19,  # "Taunka"
        20,  # "Northrendskeleton"
        21,  # "Icetroll"
        # 23, # "Gilnean"
        # 25, # "Pandarena"
        # 26, # "Pandarenh"
        33,  # "Thinhuman"
    )

    GENDERS = {0: "Male", 1: "Female"}

    DEFAULT_ICON_URL = "https://wow.zamimg.com/images/wow/icons/large/"

    room_id = models.CharField(max_length=45, verbose_name="Id комнаты")

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Создатель комнаты")

    last_update_time = models.DateTimeField(verbose_name="Время последнего изменения")

    allow_edit = models.BooleanField(verbose_name="Разрешить редактирование")

    creating = models.BooleanField(verbose_name="Персонаж создан?", default=False)

    char_name = models.CharField(max_length=32, verbose_name="Имя персонажа", default="")

    proffesions = models.CharField(max_length=32, verbose_name="Профессии", default="[0,0]")

    talents = models.ManyToManyField(TalentsModel, verbose_name="Привязанные таланты")

    char_class = models.CharField(max_length=32, verbose_name="Класс персонажа", default="")

    race = models.IntegerField(verbose_name="Раса")

    gender = models.IntegerField(verbose_name="Пол")

    items = models.CharField(max_length=1024, verbose_name="Экипировка", blank=True)

    face = models.CharField(max_length=150, verbose_name="Внешность")

    class Meta:
        verbose_name = "Персонажу"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        return "Комната: " + self.room_id

    def get_absolute_url(self):
        return reverse("char", kwargs={"room_id": self.room_id})
