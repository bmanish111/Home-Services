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
    path("appointment/", customer_views.appointment, name="customer_appointment"),
    path(
        "appointment/<int:service_id>/<int:employee_id>",
        customer_views.appointment,
        name="customer_appointment",
    ),
    path("myappointment", customer_views.myappointment, name="customer_appointments"),
    path("appointment/<int:appointment_id>", customer_views.cancel_appointment, name="cancel_appointment"),
    path("profile", customer_views.customer_profile, name="customer_profile"),
    path("logout", customer_views.customer_logout, name="customer_logout"),
]
