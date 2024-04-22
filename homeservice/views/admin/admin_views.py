from django.shortcuts import render, HttpResponse, redirect
import secrets
import string
from .employee_form import MyForm
from django.contrib.auth import get_user_model

User = get_user_model()

from homeservice.models import Employee, Service
from django.contrib import messages
from django.db.models import Q


def home(request):
    return render(request, "admin/dashboard.html")


# create employee
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
                # is_account_verified=True,
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
            if employee:
                user.is_account_verified = True
                user.save()
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


# view employee
def employee_list(request):
    if request.method == "POST":
        search_text = request.POST.get("search")
        print("search_text=", search_text)
        employees = Employee.objects.filter(
            Q(is_verified=True)
            & (
                Q(user__fullname__istartswith=search_text)
                | Q(user__email__istartswith=search_text)
                | Q(user__phone__istartswith=search_text)
                | Q(user__address__istartswith=search_text)
                | Q(user__email__iexact=search_text)
            )
        )
        return render(
            request,
            "admin/employee.html",
            {"employees": employees, "search_text": search_text},
        )

    employees = Employee.objects.filter(is_verified=True)
    return render(request, "admin/employee.html", {"employees": employees})


# employee application
def employee_application(request, employee_id=None):
    if employee_id:
        employee = Employee.objects.get(id=employee_id)
        # return HttpResponse(employee.user.fullname)
        return render(
            request, "admin/employee_verification.html", {"employee": employee}
        )

    employees = Employee.objects.filter(is_verified=False)
    return render(
        request, "admin/employee_applications_list.html", {"employees": employees}
    )


# view employee application
# def employee_application(request, employee_id):
#     employee = Employee.objects.get(id=employee_id)
#     return HttpResponse(employee.user.fullname)
#     # return render(request, "admin/employee_application.html", {"employee": employee})


# employee verification
def employee_verification(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.method == "POST":
        employee.is_verified = True
        employee.save()
        employee.user.is_account_verified = True
        employee.user.save()
        messages.success(request, "Employee verified successfully")
        return redirect("admin_dashboard:employee_application")
