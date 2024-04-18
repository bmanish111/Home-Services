from django.urls import path
from . import customer_views

app_name = "customer"

urlpatterns = [
    path("", customer_views.home, name="customer_home"),
    path("home", customer_views.home, name="customer_home"),
    path("service/", customer_views.services, name="customer_service"),
    path(
        "service/<slug:slug>",
        customer_views.service_details,
        name="customer_service_details",
    ),
    path("appointment", customer_views.appointment, name="customer_appointment"),
    path("logout", customer_views.customer_logout, name="customer_logout"),
]
