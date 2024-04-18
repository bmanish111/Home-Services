from django.urls import path
from homeservice import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("about", views.about, name="about"),
    path("service", views.service, name="service"),
    path("contact", views.contact, name="contact"),

    # Authentication
    path("login", views.login_page, name="login"),
    path("signup", views.register_page, name="signup"),
    path("logout", views.logout_user, name="logout"),
]
