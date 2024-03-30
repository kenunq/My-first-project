import mimetypes
import uuid

from decouple import config
from django.conf import settings
from django.core.exceptions import BadRequest, PermissionDenied
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from proxy.views import proxy_view

from common.mixin.views import TitleMixin
from HomePage.tasks import send_problem_message


class HomePageView(TitleMixin, TemplateView):
    """Представление обрабатывающее главную страницу."""

    template_name = "HomePage/HomePage.html"
    title = "Главная страница"

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        id_class = request.GET.get("class")

        if request.GET.get("data") == "talents":
            return HttpResponse(
                open(
                    f"./static/js/javascript/data-class={id_class}.js",
                    "r",
                    encoding="utf-8",
                ),
                content_type="application/x-javascript; charset=utf-8",
            )

        if request.GET.get("data") == "item-scaling":
            return HttpResponse(
                open("./static/js/javascript/data-item-scaling.js", "r", encoding="utf-8"),
                content_type="application/x-javascript; charset=utf-8",
            )

        return resp

    def post(self, request: ASGIRequest, *args, **kwargs):
        if self.request.user.is_anonymous:
            return JsonResponse({"status": "access error"})

        if request.FILES:
            # Заполняем словарь нужными данными, так как селери не принимает файлы
            files = {}
            for file in request.FILES:
                files[request.FILES[file].name] = [
                    request.FILES[file].read(),
                    mimetypes.guess_type(request.FILES[file].name)[0],
                ]
        else:
            files = None

        text = request.POST.get("comment", "")

        if files or text != "":
            send_problem_message.delay(files, text)
            return JsonResponse({"status": "complaint sent successfully"})

        return JsonResponse({"status": "complaint not sent"})

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        if self.request.user.is_anonymous and not self.request.COOKIES.get("userID"):
            response.set_cookie(key="userID", value=uuid.uuid4(), domain=settings.PARENT_DOMAIN)

        if not self.request.COOKIES.get("ctrEnterWidget"):
            response.set_cookie(key="ctrEnterWidget", value="close", domain=settings.PARENT_DOMAIN)

        return response


def bad_request(request: ASGIRequest, exception: BadRequest) -> HttpResponse:
    """Обработка ошибки 400"""

    error_msg = "Сервер не смог распознать запрос."
    if type(exception) is BadRequest and str(exception):
        error_msg = str(exception)

    return render(
        request=request,
        template_name="error/error_page.html",
        status=400,
        context={"code": 400, "title": "Неверный запрос", "error_msg": error_msg},
    )


def permission_denied(request: ASGIRequest, exception: BadRequest) -> HttpResponse:
    """Обработка ошибки 403"""

    error_msg = "Доступ к данной странице запрещен."
    if type(exception) is BadRequest and str(exception):
        error_msg = str(exception)

    return render(
        request=request,
        template_name="error/error_page.html",
        status=403,
        context={"code": 403, "title": "Доступ запрещен", "error_msg": error_msg},
    )


def page_not_found(request: ASGIRequest, exception: BadRequest) -> HttpResponse:
    """Обработка ошибки 404"""

    error_msg = "Страница не существует или была перемещена на другой адрес."
    if type(exception) is BadRequest and str(exception):
        error_msg = str(exception)

    return render(
        request=request,
        template_name="error/error_page.html",
        status=404,
        context={"code": 404, "title": "Страница не найдена", "error_msg": error_msg},
    )


def server_error(request: ASGIRequest) -> HttpResponse:
    """Обработка ошибки 500"""

    error_msg = "Cервер столкнулся с неожиданной ошибкой, администрация уже работает над этим."

    return render(
        request=request,
        template_name="error/error_page.html",
        status=500,
        context={"code": 500, "title": "Ошибка сервера", "error_msg": error_msg},
    )


@csrf_exempt
def flower_proxy_view(request: ASGIRequest, path: str) -> HttpResponse:
    """Представление позволяющее открывать панель flower
    как обычную страницу django (только для супер пользователя)."""

    if not request.user.is_superuser:
        raise PermissionDenied
    return proxy_view(
        request,
        f"http://{config('CELERY_FLOWER_ADDRESS')}:{config('CELERY_FLOWER_PORT')}/{config('CELERY_FLOWER_URL_PREFIX')}/{path}",
        {},
    )
