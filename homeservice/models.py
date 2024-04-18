from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from django.utils.text import slugify

# from tinymce.models import HTMLField


class CustomUserManager(BaseUserManager):

    def _create_user(
        self, email, fullname, address, phone, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Email is required")
        if not fullname:
            raise ValueError("Full Name is required")
        if not address:
            raise ValueError("Address is required")
        if not phone:
            raise ValueError("Phone is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email, fullname=fullname, address=address, phone=phone, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, fullname, address, phone, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, fullname, address, phone, **extra_fields)

    def create_superuser(self, email, fullname, address, phone, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self._create_user(email, fullname, address, phone, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    ROLE_CHOICES = [
        ("employee", "Employee"),
        ("customer", "Customer"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")
    is_account_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "address", "phone"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    experience = models.IntegerField()
    bio = models.TextField()
    is_doc_uploaded = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    ID_TYPE_CHOICES = [
        ("passport", "Passport"),
        ("driving_license", "Driving License"),
        ("national_id", "National ID"),
        # Add more choices as needed
    ]

    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)

    id_image = models.ImageField(upload_to="Documents/", null=True, blank=True)

    # def add_employee(self, user):
    #     if not user.is_superuser:
    #         self.user = user
    #         self.save()
    #     else:
    #         raise ValueError("You can't add super users as employees")

    def __str__(self):
        return self.user.fullname


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="service_images/")
    slug = models.SlugField(unique=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="employee"
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    problem = models.TextField()

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.customer.fullname} - {self.employee.user.fullname} - {self.service.name}"


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.name    