from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib.sessions.models import Session


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    duration = models.DurationField(default=timedelta)
    half_day = models.DurationField(null=True)
    buffer_time_login = models.DurationField(null=True)
    buffer_time_logout = models.DurationField(null=True)

    def __str__(self) -> str:
        return str(self.start_time)

# Create your models here.
class Ticket(models.Model):
    toll_hm = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class UserSessionModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)


class Attendance(models.Model):
    working_date = models.DateTimeField(null=True)
    logout_date = models.DateTimeField(null=True)
    total_duration = models.DurationField(null=True, blank=True)
    present = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)
    half_day = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.working_date)

class LoginLogout(models.Model):
    attendance_of = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    session_key = models.TextField()


