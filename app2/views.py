from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
# from .models import User
from .models import User, UserSessionModel, LoginLogout, Attendance, Profile
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta


# Create your views here.
class Home(APIView):
    def get(self, request):
        return render(request, 'home2.html', {'ticket': 'Ticket.objects.filter(toll_hm=request.user)'})

    def post(self, request):
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        profile = Profile.objects.create(start_time=start_time, end_time=end_time)
        profile.save()
        datetime.strptime(profile.start_time, '%H:%M')
        profile.duration = datetime.strptime(profile.end_time, '%H:%M') - datetime.strptime(profile.start_time, '%H:%M')
        # print(duration)
        profile.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class Login1(APIView):
    def get(self, request):
        return render(request, 'login.html')
        
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)                
            correct_password = check_password(password, user.password)

            if correct_password:
                    logout(request)
                    login(request, user)
                           
                    # request.session.set_expiry(200)
                    attendance = 0
                    profile = Profile.objects.first()
                    start_time_job_today = datetime.combine(datetime.now().date(), profile.start_time)
                    end_time_job_today = start_time_job_today + profile.duration
                    next_day = start_time_job_today+timedelta(days=1)

                    start_time_job_today_allowed = start_time_job_today - profile.buffer_time_login
                    end_time_job_today_allowed = end_time_job_today + profile.buffer_time_logout

                    print(start_time_job_today_allowed, end_time_job_today_allowed)

                    if Attendance.objects.filter(working_date=start_time_job_today, logout_date=end_time_job_today).exists():
                        attendance = Attendance.objects.get(working_date=start_time_job_today, logout_date=end_time_job_today)

                        if (start_time_job_today_allowed < datetime.now() and end_time_job_today_allowed > datetime.now()) or (end_time_job_today < datetime.now() and next_day > datetime.now()):
                            LoginLogout.objects.create(attendance_of=attendance, login_time=datetime.now(), session_key=str(request.session.session_key)).save()
                        else:
                            pass
                    
                    else:
                        seco = timedelta(seconds=0)
                        attendance = Attendance.objects.create(working_date=start_time_job_today, logout_date=end_time_job_today, total_duration=seco)
                        attendance.save()
                        
                        if (start_time_job_today_allowed < datetime.now() and end_time_job_today_allowed > datetime.now()) or (end_time_job_today < datetime.now() and next_day > datetime.now()):
                            LoginLogout.objects.create(attendance_of=attendance, login_time=datetime.now(), session_key=str(request.session.session_key)).save()
                        else:
                            pass
                    

                    if UserSessionModel.objects.filter(user=user).exists():
                        user_session = UserSessionModel.objects.get(user=user)
                        old_session = user_session.session
                        
                        session_delete = Session.objects.get(pk=old_session.session_key)
                        session_delete.delete()

                        user_session.session = Session.objects.get(session_key=request.session.session_key)
                        user_session.save()
                    else:
                        user_session = UserSessionModel.objects.create(user=user, session=Session.objects.get(session_key=request.session.session_key))
                        user_session.save()
                       
                    response = 0
                    if self.request.GET.get('next'):
                        response = redirect(self.request.GET.get('next'))
                    else:
                        response = redirect('home')
                    response.set_cookie('name', str(request.user.username)) 
                    
                    return response
                    
            else:
                return Response({'data':"Wrong password"})
        else:
            return Response({'data':"User does not exists"})
        

class Logout(APIView):
    def get(self, request):
        loginlogout = LoginLogout.objects.get(session_key=str(request.session.session_key))
        loginlogout.logout_time = datetime.now()
        loginlogout.duration = loginlogout.logout_time - loginlogout.login_time
        loginlogout.save()

        attendance = loginlogout.attendance_of
        attendance.total_duration = attendance.total_duration + loginlogout.duration

        
        if attendance.total_duration > request.user.profile.duration:
            attendance.present = True
        elif attendance.total_duration > request.user.profile.half_day and attendance.total_duration < request.user.profile.duration:
            attendance.half_day = True
        else:
            attendance.absent = True 
        attendance.save()

        Session.objects.get(pk=loginlogout.session_key).delete()
        logout(request)

        return HttpResponseRedirect('login')