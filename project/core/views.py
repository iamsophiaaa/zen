from django.shortcuts import render
from .models import *
import json
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about_us.html")

def menu(request, table_id):
    menu_items = MenuItem.objects.all()

    return render(request, "core/hotel_menu.html" , {"menu_items": menu_items, "table_id": table_id})

def cart(request):
    return render(request, "core/cart.html")

def gallery(request):
    return render(request, "core/gallery.html")

def contact(request):
    return render(request, "core/contact.html")

def order(request):
    cart = json.loads(request.POST.get("cart"))
    table_id = request.POST.get("table_id")
    order = Order.objects.create(table_id = table_id, total=0)
    order_total = 0

    for item in cart:
        item_id = item.get("id")
        item_name = item.get("name")
        menu_item = MenuItem.objects.get(id=item_id)
        item_total = item.get("qty")*menu_item.price
        order_item = OrderItem.objects.create(menu_item=menu_item, quantity= item.get("qty"), total = item_total, order=order)
        order_total+=order_item.total

    order.total = order_total
    order.save()
    return HttpResponse("Order Created")

    

def login(request):
    return render(request, "core/login.html")

def logout(request):
    return render(request, "core/logout.html")

