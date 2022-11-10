from django.contrib import admin
from .models import *

class LoginLogoutAdmin(admin.StackedInline):
    model = LoginLogout

class AttendanceAdmin(admin.ModelAdmin):
    inlines = [LoginLogoutAdmin]


# Register your models here.
admin.site.register(Ticket)
admin.site.register(Profile)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(UserSessionModel)
