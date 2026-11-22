
from django.contrib import admin
from django.urls import path, include
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
     path('payment/', payment, name="payment"),   
     path('payment/confirm', payment_confirm, name="payment_confirm"),   

    path('menu/tables/<int:table_id>/', menu, name="menu"), 
    path('accounts/', include("accounts.urls"))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)