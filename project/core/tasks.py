
from celery import shared_task
from .services import analyze_popular_items
@shared_task(schedule=0)
def update_popular_menu_items():
    analyze_popular_items()
    print("updated")

