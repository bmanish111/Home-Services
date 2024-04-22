from django.urls import path, include
from . import admin_views as views

app_name = "admin_dashboard"

urlpatterns = [
    path("", views.home, name="admin_home"),
    path("employee/create", views.employee, name="employee_create"),
    path("employee", views.employee_list, name="employee"),
    path("employee/<int:employee_id>/edit", views.employee_edit, name="employee_edit"),
    path("employee/<int:employee_id>/delete", views.employee_delete, name="employee_delete"),
    path(
        "employee/application", views.employee_application, name="employee_application"
    ),
    path(
        "employee/application/<int:employee_id>",
        views.employee_application,
        name="employee_application",
    ),
    path(
        "employee/application/<int:employee_id>/verify",
        views.employee_verification,
        name="employee_verification",
    ),
]
