import json

from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from common.mixin.views import TitleMixin
from services.models import (
    ClassModel,
    CommunicationModel,
    FractionModel,
    MentorModel,
    ServerModel,
    ServicesModel,
    TypeModel,
)

from .tasks import send_telegram_message


# Create your views here.


class ServicesView(TitleMixin, TemplateView):
    """Представление обрабатывающее страницу записи на услуги."""

    template_name = "services/appointment_page.html"
    title = "Заказать услугу"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["types"] = TypeModel.objects.all()

        context["servers"] = ServerModel.objects.all()

        context["fractions"] = FractionModel.objects.all()

        context["classes"] = ClassModel.objects.all()

        context["mentors"] = MentorModel.objects.all()

        context["communications"] = CommunicationModel.objects.all()

        return context

    def post(self, request: ASGIRequest, *args, **kwargs):
        data: dict = json.loads(request.body)
        creator = self.request.user if not self.request.user.is_anonymous else None

        comment = data.get("comment", "")
        telegram_id = MentorModel.objects.get(name=data["mentor"]).telegram_id

        bids = ServicesModel.objects.create(
            type=data["type"],
            server=data["server"],
            fraction=data["fraction"],
            class_name=data["class"],
            mentor=data["mentor"],
            communication=data["communication"],
            username=data["username"],
            comment=comment,
            creator=creator,
            time_of_create=timezone.now(),
        )
        bids.save()

        # messages.success(request, data['mentor'])
        request.session["mentor"] = data["mentor"]

        # send_message_zapis(telegram_id, data)
        send_telegram_message.delay(telegram_id, data)

        return JsonResponse({"status": "message sent successfully"})


class SuccessAddView(TitleMixin, TemplateView):
    """Представление обрабатывающее страницу успешного записи на услугу."""

    template_name = "services/success_add.html"
    title = "Успех!"

    def render_to_response(self, context, **response_kwargs):
        if not context.get("mentor"):
            return redirect(reverse("services:services"))

        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get("mentor"):
            context["mentor"] = self.request.session["mentor"]
            del self.request.session["mentor"]

        return context
