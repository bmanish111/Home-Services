from django.contrib import admin
from .models import User, Service, Employee, Appointment, Inquiry

# Register your models here.
admin.site.register(User)
admin.site.register(Service)
admin.site.register(Employee)
admin.site.register(Appointment)
admin.site.register(Inquiry)
