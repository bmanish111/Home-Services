from django.shortcuts import HttpResponse, redirect, render
from homeservice.models import Service, Employee, Appointment
from homeservice.decorators import role_required
from django.contrib import messages


@role_required("employee")
def register(request):
    service = Service.objects.all()
    if Employee.objects.filter(user=request.user).exists():
        employee = Employee.objects.filter(user=request.user)
        status = "Pending"
        if request.user.is_account_verified:
            status = "Approved"
        return render(
            request,
            "employee/complete_profile.html",
            {"employee": employee, "status": status},
        )
        return HttpResponse("You have already submitted your documents")

    if request.method == "POST":
        job_title = request.POST.get("job_title")
        experience = request.POST.get("experience")
        bio = request.POST.get("bio")
        id_type = request.POST.get("id_type")
        id_image = request.FILES["id_image"]
        print(job_title, experience, bio, id_type, id_image)

        employee = Employee(
            user=request.user,
            job_title=job_title,
            experience=experience,
            bio=bio,
            id_type=id_type,
            id_image=id_image,
            is_doc_uploaded=True,
        )
        employee.save()

        return HttpResponse("Profile Updated! Wait for approval")

    return render(request, "employee/complete_profile.html", {"service": service})


@role_required("employee")
def home(request):
    appointments = Appointment.objects.filter(
        employee=request.user.employee, status="Pending"
    )
    return render(request, "employee/home.html", {"appointments": appointments})


@role_required("employee")
def appointment(request, appointment_id=None):
    appointments = Appointment.objects.filter(employee=request.user.employee)

    # If the appointment_id is provided, approve the appointment
    if appointment_id:
        if appointments.filter(
            id=appointment_id, employee=request.user.employee
        ).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = "Approved"
            messages.success(request, "Appointment approved successfully!")
            appointment.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.error(request, "Invalid request")

    return render(request, "employee/appointments.html", {"appointments": appointments})
