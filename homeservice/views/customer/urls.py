from django.urls import path
from . import customer_views

# app_name = "customer"

urlpatterns = [
    path("", customer_views.home, name="customer_home"),
    path("home", customer_views.home, name="customer_home"),
]
