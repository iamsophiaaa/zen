from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about_us.html")

def menu(request):
    return render(request, "core/hotel_menu.html")