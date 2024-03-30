import hashlib

from django.conf import settings
from django.core.cache import cache
from django.db.models import Count
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from addons.models import Addon, AddonCategory, Order
from common.mixin.views import TitleMixin


# Create your views here.


class AddonsView(TitleMixin, ListView):
    """Представление обрабатывающее страницу товаров с аддонами."""

    model = Addon
    template_name = "addons/addons_shop.html"
    title = "Магазин аддонов"

    # paginate_by = 4
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        if category_id:
            cache.clear()

        filter = self.request.GET.get("filter")

        if filter:
            list_filter = {"price": "price", "-price": "-price", "popular": "name"}

            return (
                queryset.filter(category__id=category_id, is_published=True).order_by(list_filter.get(filter, ""))
                if category_id
                else queryset.filter(is_published=True).order_by(list_filter.get(filter, ""))
            )

        return (
            queryset.filter(category__id=category_id, is_published=True)
            if category_id
            else queryset.filter(is_published=True)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        user = self.request.user

        if user.is_authenticated:
            context["paid_addons"] = Addon.objects.filter(order__user=user, order__status=True)

        categories = cache.get("categories")

        if not categories:
            # возвращаем только те категории, которые используются
            context["categories"] = AddonCategory.objects.annotate(one=Count("a_category")).filter(one__gt=0)
            cache.set("categories", context["categories"], 30)
        else:
            context["categories"] = categories
        return context


class AddonPageView(TemplateView):
    """Представление обрабатывающее страницу товара(аддона)."""

    template_name = "addons/addon_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["addon"] = Addon.objects.filter(slug=kwargs["addon_slug"])[0]

        user = self.request.user
        if user.is_authenticated:
            context["paid"] = Order.objects.filter(user=user, addon=context["addon"], status=True).exists()

        context["title"] = context["addon"].name

        if self.request.user.is_authenticated:
            currency = "RUB"
            order = Order.objects.create(user=self.request.user, addon=context["addon"])
            sign = hashlib.md5(
                f'{settings.MERCHANT_ID}:{context["addon"].price}:{settings.SECRET_WORD}:{currency}:{order.id}'.encode()
            ).hexdigest()
            context["payment_url"] = (
                f'https://pay.kassa.shop/?m={settings.MERCHANT_ID}&oa={context["addon"].price}&s={sign}&currency={currency}&o={order.id}'
            )

        return context


def payment_alerts(request):
    if request.GET.get("MERCHANT_ID") == settings.MERCHANT_ID:
        order = Order.objects.get(id=request.GET.get("MERCHANT_ORDER_ID"))

        amount = request.GET.get("AMOUNT")

        if order.addon.price == int(amount):
            order.status = True

            order.save()

        return HttpResponse("YES")

    return HttpResponse("NO")


class PaymentSuccess(TitleMixin, TemplateView):
    template_name = "addons/payment_success.html"
    title = "Успех!"


class PaymentFailed(TitleMixin, TemplateView):
    template_name = "addons/payment_failed.html"
    title = "Неудача!"
