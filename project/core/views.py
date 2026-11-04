from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about_us.html")

def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, "core/hotel_menu.html" , {"menu_items": menu_items})

def cart(request):
    return render(request, "core/cart.html")

def gallery(request):
    return render(request, "core/gallery.html")

def contact(request):
    return render(request, "core/contact.html")

def login(request):
    return render(request, "core/login.html")

def logout(request):
    return render(request, "core/logout.html")

