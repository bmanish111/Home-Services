from django.shortcuts import render, HttpResponse, redirect
from homeservice.models import Service
from django.contrib.auth import logout
from homeservice.decorators import role_required


@role_required("customer")
def home(request):
    return render(request, "customer/home.html")


@role_required("customer")
def services(request):
    services = Service.objects.all()
    return render(request, "customer/services.html", {"services": services})


@role_required("customer")
def service_details(request, slug):
    service = Service.objects.get(slug=slug)
    return render(request, "customer/service_details.html", {"service": service})
    return HttpResponse(slug)


@role_required("customer")
def customer_logout(request):
    logout(request)
    return redirect("login")

@role_required("customer")
def appointment(request):
    return render(request, "customer/appointment.html")