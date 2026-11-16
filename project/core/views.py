from django.shortcuts import render
from .models import *
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.
def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about_us.html")

def menu(request, table_id=None):
    if table_id is not None:
        request.session["table_id"] = table_id      # new scan: remember it
    else:
        table_id = request.session.get("table_id")  # plain /menu/: use the saved one

    menu_items = MenuItem.objects.all()
    return render(
        request,
        "core/hotel_menu.html",
        {"menu_items": menu_items, "table_id": table_id},
    )

def cart(request):
    table_id = request.session["table_id"]
    return render(request, "core/cart.html", {"table_id": table_id})

def gallery(request):
    return render(request, "core/gallery.html")

def contact(request):
    return render(request, "core/contact.html")

def order(request):
    if request.method == "POST":
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
        order_ids = request.session.get('order_ids', [])
        order_ids.append(order.id)
        request.session['order_ids']= order_ids
        
        return JsonResponse({
            'order_id': order.id
        })
    else:
        table_id = request.session['table_id']
        orders = Order.objects.filter(id__in = request.session.get('order_ids'))
        return render(request, "core/order.html", {"table_id":table_id, "orders":orders})

    

