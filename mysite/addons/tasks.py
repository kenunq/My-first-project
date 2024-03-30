from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from addons.models import Order


@shared_task
def clear_orders():
    Order.objects.filter(status=False, created_at__lte=timezone.now() - timedelta(hours=1)).delete()
