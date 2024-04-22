from django.urls import path, include
from . import admin_views as views

app_name = "admin_dashboard"

urlpatterns = [
    path("", views.home, name="admin_home"),
    path("employee", views.employee, name="employee_create"),
]
