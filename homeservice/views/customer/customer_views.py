from django.shortcuts import render, HttpResponse, redirect
from homeservice.models import Service, Appointment, Employee, Rating
from django.contrib.auth import logout
from homeservice.decorators import role_required
from django.contrib import messages
from django.http import HttpResponseNotAllowed


@role_required("customer")
def home(request):
    appointments = Appointment.objects.filter(customer=request.user)[:5]
    # True if there are more than 5 appointments so that the "View More" button will be displayed
    view_more = Appointment.objects.filter(customer=request.user).count() > 5
    return render(
        request,
        "customer/home.html",
        {"appointments": appointments, "view_more": view_more},
    )


@role_required("customer")
def services(request):
    services = Service.objects.all()
    return render(request, "customer/services.html", {"services": services})


@role_required("customer")
def service_details(request, slug):
    service = Service.objects.get(slug=slug)
    employees = Employee.objects.filter(job_title=service.pk)
    return render(
        request,
        "customer/service_details.html",
        {"service": service, "employees": employees},
    )


@role_required("customer")
def customer_logout(request):
    logout(request)
    return redirect("login")


@role_required("customer")
def appointment(request, service_id=None, employee_id=None):

    if request.method == "POST":
        print(request.POST)
        employee = Employee.objects.get(id=request.POST["employee"])
        service = Service.objects.get(id=request.POST["service"])
        date = request.POST["date_time"].split("T")[0]
        time = request.POST["date_time"].split("T")[1]
        problem = request.POST["problem"]
        appointment = Appointment(
            customer=request.user,
            employee=employee,
            service=service,
            date=date,
            time=time,
            problem=problem,
        )
        appointment.save()
        messages.success(request, "Appointment booked successfully!")
        return redirect("customer:customer_appointments")

    service = Service.objects.get(id=service_id)
    employee = Employee.objects.get(id=employee_id)
    return render(
        request, "customer/appointment.html", {"service": service, "employee": employee}
    )


@role_required("customer")
def myappointment(request):
    appointments = Appointment.objects.filter(customer=request.user)
    # True if there are more than 5 appointments so that the "View More" button will be displayed
    # view_more = Appointment.objects.filter(customer=request.user).count() > 5
    return render(
        request,
        "customer/my_appointments.html",
        {"appointments": appointments},
    )


def cancel_appointment(request, appointment_id):
    # if request.method == "POST":
    appointment = Appointment.objects.get(id=appointment_id)
    if (
        appointment
        and appointment.customer == request.user
        and appointment.status == "Pending"
    ):
        appointment.delete()
        messages.success(request, "Appointment cancelled successfully!")
        return redirect("customer:customer_appointments")
    else:
        messages.error(request, "Invalid request, Cannot cancel appointment!")
        return redirect("customer:customer_appointments")


@role_required("customer")
def customer_profile(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        if not request.user.check_password(current_password):
            messages.error(request, "Invalid current password!")
            print("Invalid current password!")
        else:
            if new_password != confirm_password:
                print("Passwords do not match!")
                messages.error(request, "Passwords do not match!")
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, "Password updated successfully!")
                print("Password updated successfully!")
        return redirect("customer:customer_profile")
    return render(request, "customer/update_profile.html")


@role_required("customer")
def rating(request):
    if request.method == "POST":
        rating = request.POST["rating"]
        review = request.POST["review"]
        employee = Employee.objects.get(id=request.POST["employee"])
        if Appointment.objects.filter(
            customer=request.user, employee=employee, status="Completed"
        ).exists():
            print("Completed appointment found!")
            if Rating.objects.filter(customer=request.user, employee=employee).exists():
                messages.error(request, "You have already rated this employee!")
                print("You have already rated this employee!")

            else:
                print("rating saved successfully!")
                messages.success(request, "Rating submitted successfully!")
                rating = Rating(
                    customer=request.user,
                    employee=employee,
                    rate=rating,
                    review=review,
                )
                rating.save()
        else:
            print(
                "Sorry you cannot rate, beacuse you have not completed appointment with the serviceman!"
            )
            messages.error(
                request,
                "Sorry you cannot rate, beacuse you have not completed appointment with the serviceman!",
            )
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return HttpResponseNotAllowed("Method Not Allowed!")
