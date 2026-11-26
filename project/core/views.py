from django.shortcuts import render, redirect
from .models import *
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import requests
from django.urls import reverse
from django.conf import settings
from .services import LoyaltyPoints
from accounts.models import Wallet
from decimal import Decimal

from django.db import transaction


# Create your views here.
def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about_us.html")


def menu(request, table_id=None):
    if table_id is not None:
        request.session["table_id"] = table_id      # new scan: remember it
    else:
        table_id = request.session.get("table_id")  # plain /menu/: use saved one

    menu_items = MenuItem.objects.all()
    return render(
        request,
        "core/hotel_menu.html",
        {"menu_items": menu_items, "table_id": table_id},
    )


def cart(request):
    table_id = request.session.get("table_id")      # no KeyError if missing
    return render(request, "core/cart.html", {"table_id": table_id})


def order(request):
    if request.method == "POST":
        # Parse the cart safely
        try:
            cart_data = json.loads(request.POST.get("cart", "[]"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid cart"}, status=400)

        if not cart_data:
            return JsonResponse({"error": "Cart is empty"}, status=400)

        # Prefer the session's table; fall back to what the form sent
        table_id = request.session.get("table_id") or request.POST.get("table_id")
        if not table_id or table_id in ("None", "null", ""):
            return JsonResponse({"error": "No table selected"}, status=400)

        try:
            with transaction.atomic():
                new_order = Order.objects.create(table_id=table_id, total=0)
                order_total = Decimal("0")

                for item in cart_data:
                    qty = int(item.get("qty", 0))
                    if qty < 1:
                        continue
                    menu_item = MenuItem.objects.get(id=item.get("id"))
                    item_total = menu_item.price * qty
                    OrderItem.objects.create(
                        order=new_order,
                        menu_item=menu_item,
                        quantity=qty,
                        total=item_total,
                    )
                    order_total += item_total

                new_order.total = order_total
                new_order.save()
        except (MenuItem.DoesNotExist, ValueError, TypeError):
            return JsonResponse({"error": "Invalid item in cart"}, status=400)

        order_ids = request.session.get("order_ids", [])
        order_ids.append(new_order.id)
        request.session["order_ids"] = order_ids

        return JsonResponse({"order_id": new_order.id, "orders_count": len(order_ids),})

    # GET
    table_id = request.session.get("table_id")
    orders = Order.objects.filter(
        id__in=request.session.get("order_ids", [])
    ).order_by("-created_at")
    return render(request, "core/order.html", {"table_id": table_id, "orders": orders})
def gallery(request):
    return render(request, "core/gallery.html")

def contact(request):
    return render(request, "core/contact.html")


def payment(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
       

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, "Payment initiation failed")
            return redirect('order')
        use_points = request.POST.get('use-points')
        if use_points:
            wallet = request.user.wallet
            paisa = LoyaltyPoints.calculate_paisa(wallet.loyalty_points)
            wallet.loyalty_points = 0
            wallet.save()

        else:
            paisa = 0

        payment, created = Payment.objects.get_or_create(
            order = order,
            defaults = {
                "amount": order.total * 100- paisa,
                
            }
        )
        url = "https://dev.khalti.com/api/v2/epayment/initiate/"
        return_url = request.build_absolute_uri(reverse('payment_confirm'))
        print(return_url)
        payload = json.dumps({
            "return_url": return_url,
            "website_url": "https://example.com/",
            "amount": str(payment.amount),
            "purchase_order_id": str(payment.id),
            "purchase_order_name": "test",
            "customer_info": {
            "name": "Ram Bahadur",
            "email": "test@khalti.com",
            "phone": "9800000001"
            }
        })
        headers = {
            'Authorization': f'key {settings.KHALTI_SECRET_KEY} ',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        payment.pidx = data.get('pidx')
        payment.save()

        return redirect(data.get('payment_url'))
       
def payment_confirm(request):
    print("payment done, lets confirm it")
    url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    payload = json.dumps({
        "pidx": request.GET.get('pidx')
        
    })
    headers = {
        'Authorization': f'key {settings.KHALTI_SECRET_KEY} ',
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    amount = data.get('total_amount')
    status = data.get('status')
    pidx  = data.get('pidx')
    
    try: 
        payment = Payment.objects.get(pidx = pidx )
    except Payment.DoesNotExist:
        messages.error(request, "Payment reference doesn't exist. Please contact administrator" )

    else:
        if status == "Completed"  and amount == payment.amount:
            payment.status = Payment.STATUS.COMPLETE
            payment.save()
            messages.success(request, "Payment successful for order")
            points = LoyaltyPoints.calculate(payment)
            wallet , created = Wallet.objects.get_or_create(
                user = request.user,
                )
            wallet.loyalty_points += points
            wallet.save()
            messages.success(request, f"{points} loyalty points added to wallet")
            return redirect('order')
        
