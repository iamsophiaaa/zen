class LoyaltyPoints:
    POINTS_TO_PAISA = 1/10
    @staticmethod
    def calculate(payment):
        return int(payment. amount/100)


    @staticmethod
    def calculate_paisa(points):
        return int(points*LoyaltyPoints.POINTS_TO_PAISA)


def analyze_popular_items(days=1):
    from .models import OrderItem, MenuItem
    from django.db import transaction
    from django.db.models import Sum
    from django.utils import timezone
    from datetime import timedelta

    date_from = timezone.now() - timedelta(days=days)

    popular_item_ids = list(
        OrderItem.objects
        .filter(order__created_at__gte=date_from)
        .values('menu_item')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')
        .values_list('menu_item', flat=True)[:3]
    )

    with transaction.atomic():
        MenuItem.objects.update(is_popular=False)  # reset all first
        MenuItem.objects.filter(id__in=popular_item_ids).update(is_popular=True)

    return popular_item_ids