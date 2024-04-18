from django.shortcuts import render, HttpResponse, redirect
from .forms import MyForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

User = get_user_model()


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
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)
        if user:
            if user.role == "customer":
                login(request, user)
                # return HttpResponse("Customer Home")
                return redirect("customer_home")
            elif user.role == "employee":
                login(request, user)
                if not request.user.is_account_verified:
                    # Employee need to verify their account
                    return HttpResponse(
                        "Login Successful, You are a Employee but need to upload your documents"
                    )
                else:
                    return HttpResponse(request, "Login Successful, You are a Employee")
            elif user.role == "admin":
                print("Invalid Email or Password")
                messages.error(request, "Invalid Email or Password")
                print("admin_home")
        else:
            messages.error(request, "Invalid Email or Password")
            redirect("login")
    return render(request, "login.html")


def register_page(request):
    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        address = request.POST["address"]
        contact = request.POST["contact"]
        is_employee = request.POST["is_employee"]
        profile_pic = request.FILES["profile_pic"]
        password = request.POST["password1"]

        form = MyForm(request.POST, request.FILES)

        if form.is_valid():
            if is_employee == "True":
                user = User.objects.create_user(
                    email=email,
                    fullname=name,
                    address=address,
                    phone=contact,
                    profile_pic=profile_pic,
                    role="employee",
                )
                message = "Employee registered successfully"
                messages.success(request, "Employee registered successfully")
            else:
                user = User.objects.create_user(
                    email=email,
                    fullname=name,
                    address=address,
                    phone=contact,
                    profile_pic=profile_pic,
                )
                message = "Customer registered successfully"
                messages.success(request, "Customer registered successfully")
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            return render(request, "register.html", {"form": form})

    return render(request, "register.html")


def logout_user(request):
    logout(request)
    return redirect("login")
