from django.contrib import admin
from .models import User, Service, Employee

# Register your models here.
admin.site.register(User)
admin.site.register(Service)
admin.site.register(Employee)
