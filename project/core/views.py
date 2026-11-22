from django.shortcuts import render, redirect
from .models import *
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import requests
from django.urls import reverse


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
        orders = Order.objects.filter(id__in = request.session.get('order_ids')).order_by('-created_at')
        return render(request, "core/order.html", {"table_id":table_id, "orders":orders})

    

def payment(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, "Payment initiation failed")
            return redirect('order')

        payment, created = Payment.objects.get_or_create(
            order = order,
            defaults = {
                "amount": order.total * 100
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
            'Authorization': 'key ',
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
        'Authorization': 'key ',
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

    return redirect('order')
        
