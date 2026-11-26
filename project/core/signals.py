from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, Payment

@receiver(post_save, sender = Order)
def create_order_payment(sender, instance, created, **kwargs):
    order = instance
    payment, created = Payment.objects.get_or_create(
        order = order,
        defaults = {
            "amount" : order.total * 100,
        }
    )

