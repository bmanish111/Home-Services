from django.shortcuts import HttpResponse, redirect, render
from homeservice.models import Service, Employee, Appointment, Rating
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


@role_required("employee")
def appointment_completed(request, appointment_id):
    appointments = Appointment.objects.filter(employee=request.user.employee)

    # If the appointment_id is provided, approve the appointment
    if appointment_id:
        if appointments.filter(
            id=appointment_id, employee=request.user.employee
        ).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = "Completed"
            messages.success(request, "Appointment completed successfully!")
            appointment.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.error(request, "Invalid request")

    return render(request, "employee/appointments.html", {"appointments": appointments})


@role_required("employee")
def reviews(request):
    reviews = Rating.objects.filter(employee=request.user.employee)

    # destructuring the reviews because we need to change the rate to a string so that we can use it in the template to iterate over the stars
    processed_reviews = []
    for review in reviews:
        if review.rate == 1:
            rate = "a"
        elif review.rate == 2:
            rate = "aa"
        elif review.rate == 3:
            rate = "aaa"
        elif review.rate == 4:
            rate = "aaaa"
        elif review.rate == 5:
            rate = "aaaaa"

        review = {
            "rate": rate,
            "review": review.review,
            "customer": review.customer,
            "date": review.date,
        }
        processed_reviews.append(review)

    return render(request, "employee/reviews.html", {"reviews": processed_reviews})


@role_required("employee")
def profile(request):

    if (
        request.method == "POST"
        and request.POST.get("update_password") == "Update Password"
    ):
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        if not request.user.check_password(current_password):
            messages.error(request, "Invalid current password!")
        else:
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match!")
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, "Password updated successfully!")
        return redirect("employee:employee_profile")

    elif (
        request.method == "POST"
        and request.POST.get("update_profile") == "Update Profile"
    ):
        employee = Employee.objects.get(user=request.user)
        bio = request.POST.get("bio")
        previous_work = request.POST.get("previous_work")
        previous_experience = request.POST.get("previous_experience")
        messages.success(request, "Profile updated successfully!")

        employee.bio = bio
        employee.previous_work = previous_work
        employee.previous_experience = previous_experience
        employee.save()

        return redirect("employee:employee_profile")

    employee = Employee.objects.get(user=request.user)
    return render(request, "employee/profile.html", {"employee": employee})
