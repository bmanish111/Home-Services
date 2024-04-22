from django.shortcuts import render, HttpResponse, redirect
import secrets
import string
from .employee_form import MyForm
from django.contrib.auth import get_user_model

User = get_user_model()

from homeservice.models import Employee, Service
from django.contrib import messages


def home(request):
    return render(request, "admin/dashboard.html")


def employee(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        job_title = request.POST.get("service")
        experience = request.POST.get("experience")
        bio = request.POST.get("bio")
        previous_work = request.POST.get("previous_work")
        previous_experience = request.POST.get("previous_experience")

        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(8))

        print("password=", password)
        form = MyForm(request.POST, request.FILES)

        if form.is_valid():
            print
            user = User.objects.create_user(
                email=email,
                fullname=fullname,
                address=address,
                phone=phone,
                profile_pic=request.FILES["profile_pic"],
                role="employee",
                is_account_verified=True,
            )
            user.set_password(password)
            print("user created successfully")
            employee = Employee.objects.create(
                user=user,
                job_title=job_title,
                experience=experience,
                bio=bio,
                previous_work=previous_work,
                previous_experience=previous_experience,
                id_type=request.POST.get("id_type"),
                id_image=request.FILES["picture_of_id"],
                is_verified=True,
                is_doc_uploaded=True,
            )
            print("employee created successfully")
            messages.success(request, "Employee added successfully")
            return redirect("admin_dashboard:employee_create")
        else:
            services = Service.objects.all()
            return render(
                request,
                "admin/employee_create.html",
                {"form": form, "services": services},
            )

    services = Service.objects.all()
    return render(request, "admin/employee_create.html", {"services": services})
