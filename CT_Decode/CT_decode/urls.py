from django.contrib import admin
from django.http import request
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from src import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path("", views.landing),
    path("scan", views.scan),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("login_gui", views.register_login_form, name="login"),
    path("logout", views.logout_request),
    path("dashboard/account_info", views.account_info),
    path("dashboard/account_reports", views.account_reports),
    path("about_us", views.about_us),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'src.views.handler404'