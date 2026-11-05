
from django.contrib import admin
from django.urls import path
from core.views import *
from django.conf import settings
from django.conf.urls.static import static   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"), 
    path('about/' , about, name="about"),
    
    path('cart/' , cart, name="cart"),
    path('gallery/' , gallery, name="gallery"),
    path('contact/' , contact, name="contact"),
     path('menu/', menu, name="menu"),                            
     path('order/', order, name="order"),                            
    path('menu/tables/<int:table_id>/', menu, name="menu"), 
    
     path('login/' , login, name="login"),
    path('logout/' , logout, name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)