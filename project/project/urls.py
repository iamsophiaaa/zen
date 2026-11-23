
from django.contrib import admin
from django.urls import path, include
from core.views import home, about, cart, gallery, contact, menu, order, payment, payment_confirm
from django.conf import settings
from django.conf.urls.static import static   
from django.contrib.auth import views as auth_views

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
    path('accounts/', include("accounts.urls")),
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
    ),
    name="password_reset",
),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)