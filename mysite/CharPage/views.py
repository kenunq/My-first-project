import json
from datetime import datetime, timedelta
from os.path import exists
from pathlib import Path
from typing import Any
from uuid import uuid4

import requests
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.handlers.asgi import ASGIRequest
from django.db import connection
from django.db.models import QuerySet
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic.base import TemplateView, View

from CharPage.models import CharModel
from common.mixin.views import TitleMixin
from talants.models import TalentsModel
from user.models import User


RACES = {
    1: ["Человек", "race_human"],
    2: ["Орк", "race_orc"],
    3: ["Дворф", "race_dwarf"],
    4: ["Ночной эльф", "race_nightelf"],
    5: ["Нежить", "race_scourge"],
    6: ["Таурен", "race_tauren"],
    7: ["Гном", "race_gnome"],
    8: ["Тролль", "race_trol"],
    9: ["Гоблин", "race_goblin"],
    10: ["Эльф крови", "race_bloodelf"],
    11: ["Дреней", "race_draenei"],
}
GENDERS = {0: "male", 1: "female"}

PROFFESIONS = {
    1: ["Ювелирное дело", "Jewelcrafting"],
    2: ["Инженерное дело", "Engineering"],
    3: ["Кузнечное дело", "Blacksmithing"],
    4: ["Портняжное дело", "Tailoring"],
    5: ["Кожевничество", "Leatherworking"],
    6: ["Травничество", "Herbalism"],
    7: ["Наложение чар", "Enchanting"],
    8: ["Алхимия", "Alchemy"],
    9: ["Начертание", "Inscription"],
    10: ["Горное дело", "Mining"],
    11: ["Снятие шкур", "Skinning"],
}


class ZamimgProxyView(View):
    """Проксирует запрос к zamimg API через этот сервер,
    т.к. zamimg сервер не установил Cross-Origin Resource Sharing заголовки,
    для возможности отправки запроса со стороны клиента используя JavaScript.
    https://developer.mozilla.org/ru/docs/Web/HTTP/CORS
    И кэширует файлы локально для уменьшения количества запросов к zamimg API."""

    _cache_timeout = 60 * 60 * 24 * 182

    @method_decorator(cache_page(_cache_timeout))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        modelviewer_path: str = kwargs.get("modelviewer_path")

        # Костыль для частичной работы "Нагрудников" на wrath патче
        if modelviewer_path.startswith("wrath/meta/armor/5/"):
            file_name = modelviewer_path.rsplit("/", 1)[-1]
            modelviewer_path = f"live/meta/armor/5/{file_name}"

        STATIC_ROOT = settings.BASE_DIR / "static"
        full_path = f"{STATIC_ROOT}/CharPage/json/modelviewer/{modelviewer_path}"

        if not exists(full_path):
            headers_get = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
            }
            print("---------------------------------------------------")
            zamimg_url = f"https://wow.zamimg.com/modelviewer/{modelviewer_path}"
            zamimg_url = f"https://kenundev.ru/api/modelviewer/{modelviewer_path}"

            response = requests.get(zamimg_url, headers=headers_get, timeout=5)

            path_to_file, file_name = full_path.rsplit("/", maxsplit=1)
            path_obj = Path(path_to_file)
            path_obj.mkdir(parents=True, exist_ok=True)

            with open(f"{path_to_file}/{file_name}", "wb+") as file:
                file.write(response.content)
            return HttpResponse(response.content)

        with open(full_path, "rb") as file:
            return HttpResponse(file.read())


class CharPageView(View):
    """Представление которое генерирует uuid4\
    и использует его для создания уникального url адреса для примерочной страницы."""

    def get(self, request, *args, **kwargs):
        return redirect("char_page_room", uuid4())


class UniqueCharPageView(TitleMixin, TemplateView):
    """Представление обрабатывающее примерочную страницу."""

    template_name = "index.html"
    title = "Персонаж"
    time_delta = timedelta(days=365)

    def _time_checking(self):
        """Обновляет время для текущей комнаты и
        проверяет все остальные комнаты на предмет устаревания
        для последующего удаления."""

        current_datetime = self.timezone_now
        self.dressing_room.update(last_update_time=current_datetime)

        dressing_rooms = CharModel.objects.all().only("creator", "last_update_time")

        for room in dressing_rooms:
            if current_datetime - self.time_delta >= room.last_update_time:
                # Если пользователь не прикреплён к модели удаляем модель
                if not room.creator:
                    room.delete()

    def _get_my_saved_rooms(self, creator: dict[str, str | User]) -> tuple[list[dict[str, str | int | bool]], QuerySet]:
        """Создание даты для отображения списка созданных комнат у текущего пользователя."""
        dressing_rooms = CharModel.objects.filter(creator=creator)
        my_saved_rooms = []

        for room in dressing_rooms:
            my_saved_rooms.append(
                self.create_my_saved_rooms(
                    room.last_update_time,
                    room.room_id,
                    room.allow_edit,
                    room.race,
                    room.gender,
                )
            )

        if not self.dressing_room:
            my_saved_rooms.append(self.create_my_saved_rooms(self.timezone_now, self.room_id))

        my_saved_rooms.sort(
            key=lambda room: datetime.strptime(room["last_update_time"], "%d-%m-%Y %H:%M:%S"),
            reverse=True,
        )
        return my_saved_rooms, dressing_rooms

    def create_my_saved_rooms(
        self,
        last_update_time: datetime,
        room_id: str,
        allow_edit: bool = False,
        race: int = 1,
        gender: int = 1,
    ) -> dict[str, Any]:
        return {
            "room_id": room_id,
            "allow_edit": allow_edit,
            "race": race,
            "gender": gender,
            "last_update_time": timezone.localtime(last_update_time).strftime("%d-%m-%Y %H:%M:%S"),
        }

    def create_character_data(
        self,
        allow_edit: bool = False,
        race: int = 1,
        gender: int = 1,
        items: str = "",
        face: str = "0,0,0,0,0",
    ) -> dict[str, Any]:
        return {
            "room_creator": self.is_room_creator,
            "allow_edit": allow_edit,
            "race": race,
            "gender": gender,
            "items": items,
            "face": face,
        }

    def get_context_data(self, *, object_list=None, **kwargs):
        """Создаёт запись в БД с новой страницей и добавляет character_data в контекст шаблона."""

        context = super().get_context_data(**kwargs)
        self.timezone_now = timezone.now()
        self.room_id = str(kwargs.get("room_id"))  # <class 'uuid.UUID'>
        self.dressing_room = CharModel.objects.filter(room_id=self.room_id)

        # Если эта комната записана в БД
        if self.dressing_room:
            self.creator_id = self.dressing_room[0].creator
            if self.creator_id is None:
                self.is_room_creator = True
            else:
                self.is_room_creator = self.creator_id == self.request.user

            context["creating"] = getattr(self.dressing_room[0], "creating")
            context["class"] = getattr(self.dressing_room[0], "char_class").lower()
            context["race"] = RACES[getattr(self.dressing_room[0], "race")][0]
            context["is_creator"] = self.is_room_creator
            context["race_image"] = (
                f"../static/img/rass/{GENDERS[getattr(self.dressing_room[0], 'gender')]}/{RACES[getattr(self.dressing_room[0], 'race')][1]}.jpg"
            )
            context["name"] = getattr(self.dressing_room[0], "char_name")
            if eval(getattr(self.dressing_room[0], "proffesions"))[0] == 0:
                if eval(getattr(self.dressing_room[0], "proffesions"))[1] == 0:
                    pass
                else:
                    context["proffesion1_icon"] = (
                        f"../static/img/Professions/large/{PROFFESIONS[eval(getattr(self.dressing_room[0], 'proffesions'))[1]][1]}.jpg"
                    )
                    context["proffesion1"] = PROFFESIONS[eval(getattr(self.dressing_room[0], "proffesions"))[1]][0]
            else:
                context["proffesion1_icon"] = (
                    f"../static/img/Professions/large/{PROFFESIONS[eval(getattr(self.dressing_room[0], 'proffesions'))[0]][1]}.jpg"
                )
                context["proffesion1"] = PROFFESIONS[eval(getattr(self.dressing_room[0], "proffesions"))[0]][0]
                if not eval(getattr(self.dressing_room[0], "proffesions"))[1] == 0:
                    context["proffesion2_icon"] = (
                        f"../static/img/Professions/large/{PROFFESIONS[eval(getattr(self.dressing_room[0], 'proffesions'))[1]][1]}.jpg"
                    )
                    context["proffesion2"] = PROFFESIONS[eval(getattr(self.dressing_room[0], "proffesions"))[1]][0]

            context["talents"] = self.dressing_room[0].talents.all()
            if not self.request.user.is_anonymous:
                context["talents_all"] = reversed(TalentsModel.objects.filter(creator=self.request.user))
                context["user_chars"] = reversed(CharModel.objects.filter(creator=self.request.user, creating=True))

            self._time_checking()

            object_room = self.dressing_room[0]
            character_data = self.create_character_data(
                object_room.allow_edit,
                object_room.race,
                object_room.gender,
                object_room.items,
                object_room.face,
            )

        else:
            self.is_room_creator = True

            default_create_config = {
                "room_id": self.room_id,
                "allow_edit": False,
                "last_update_time": self.timezone_now,
                "race": 1,
                "gender": 1,
                "items": "",
                "face": "0,0,0,0,0",
            }

            if not self.request.user.is_anonymous:
                default_create_config["creator"] = self.request.user

            self.dressing_room.create(**default_create_config)

            character_data = self.create_character_data()

            current_room = CharModel.objects.filter(room_id=self.room_id)
            context["creating"] = getattr(current_room[0], "creating")

        context.update({"character_data": json.dumps(character_data)})

        return context

    def render_to_response(self, context, **response_kwargs):
        if not context["creating"]:
            return redirect("createchar", self.room_id)
        return super(UniqueCharPageView, self).render_to_response(context, **response_kwargs)

    def post(self, request: ASGIRequest, *args, **kwargs) -> JsonResponse:
        """Получает character_data с фронта и на её основе обновляет запись в БД."""

        room_id = str(kwargs.get("room_id"))

        self.dressing_room = CharModel.objects.filter(room_id=room_id)

        creator_id = self.dressing_room[0].creator

        if creator_id is None:
            self.is_room_creator = True
        else:
            self.is_room_creator = creator_id == self.request.user

        if not self.dressing_room:
            raise Http404

        data: dict = json.loads(request.body)
        if self.is_room_creator:
            if data.get("talent_id"):
                if self.dressing_room[0].talents.count() < 2:
                    talent = TalentsModel.objects.get(id=int(data["talent_id"]))
                    talent.charmodel_set.add(self.dressing_room[0])
                    return JsonResponse({"status": "data was successfully update talent"})

            if data.get("deltalent_id"):
                if self.dressing_room[0].talents.count() > 0:
                    talent = TalentsModel.objects.get(id=int(data["deltalent_id"]))
                    talent.charmodel_set.remove(self.dressing_room[0])
                    return JsonResponse({"status": "data was successfully delete talent"})

            self.dressing_room.update(**data)

            return JsonResponse({"status": "data was successfully saved"})

        if creator_id is None:
            self.dressing_room.update(**data)

            return JsonResponse({"status": "data was successfully saved"})

        return JsonResponse({"status": "access error"})


class CreateCharView(TitleMixin, TemplateView):
    """Представление обрабатывающее страницу создания персонажа."""

    template_name = "create_char.html"
    title = "Создание персонажа"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.room_id = self.kwargs["room_id"]
        current_room = CharModel.objects.get(room_id=self.kwargs["room_id"])
        context["creating"] = getattr(current_room, "creating")

        return context

    def render_to_response(self, context, **response_kwargs):
        room_id = str(context["room_id"])
        dressing_room = CharModel.objects.filter(room_id=room_id)

        # Если персонаж создан перенаправляем на страницу с персонажем
        if context["creating"]:
            return redirect("char_page_room", self.room_id)
        # Иначе если создатель существует и не равен текущему пользователю - запрещаем доступ к странице
        if dressing_room[0].creator != self.request.user and dressing_room[0].creator != None:
            raise PermissionDenied()

        return super(CreateCharView, self).render_to_response(context, **response_kwargs)

    def post(self, request: ASGIRequest, *args, **kwargs):
        data: dict = json.loads(request.body)

        current_room = CharModel.objects.get(room_id=self.kwargs["room_id"])
        setattr(current_room, "char_name", data["Name"])
        setattr(current_room, "proffesions", str(data["Proffesions"]))
        setattr(current_room, "gender", data["Gender"])
        setattr(current_room, "race", data["Race"])
        setattr(current_room, "char_class", data["Class"])
        setattr(current_room, "face", ",".join(map(str, data["Face_options"])))
        setattr(current_room, "creating", True)
        current_room.save()

        return JsonResponse({"status": "data was successfully saved"})


class CharListPageView(TitleMixin, TemplateView):
    """Представление обрабатывающее страницу с персонажами пользователя"""

    template_name = "char_list_page.html"
    title = "Мои персонажи"

    def get_context_data(self, **kwargs):
        context = super(CharListPageView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context["all_chars"] = list(reversed(CharModel.objects.filter(creator=self.request.user, creating=True)))

        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_anonymous:
            return redirect("char")

        return super(CharListPageView, self).render_to_response(context, **response_kwargs)

    def post(self, request: ASGIRequest, *args, **kwargs):
        data: dict = json.loads(request.body)

        if data.get("delchar_id"):
            char_id = data.get("delchar_id")
            obj_char = CharModel.objects.get(room_id=char_id)
            # Если пользователь является создателем персонажа
            if self.request.user == obj_char.creator:
                obj_char.delete()
                messages.success(self.request, "Персонаж успешно удален.")
                return JsonResponse({"status": "The character has been successfully deleted"})
            else:
                return JsonResponse({"status": "access error"})
