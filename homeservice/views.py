from django.shortcuts import render, HttpResponse


# Create your views here.
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def service(request):
    return render(request, "services.html")


def contact(request):
    return render(request, "contact.html")


def login_page(request):
    return render(request, "login.html")
