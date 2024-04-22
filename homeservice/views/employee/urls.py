from django.urls import path
from . import employee_views

app_name = "employee"

urlpatterns = [
    path("register/", employee_views.register, name="employee_register"),
    path("home/", employee_views.home, name="employee_home"),
    path("appointment/", employee_views.appointment, name="employee_appointment"),
    path(
        "appointment/<int:appointment_id>",
        employee_views.appointment,
        name="employee_appointment",
    ),
]
