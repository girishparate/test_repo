from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
# from .models import User
from .models import User, UserSessionModel, LoginLogout, Attendance, Profile, Data
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .decorator import cache_per_user
from .serializer import SampleSerializer
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin




class Base(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home2.html'
    
    def get(self, request):
        response = Response({"hello":"Hello"})
        response.data['new_data'] = "Girish Parate is logged in"
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response._is_rendered = False 
        response.render()
        return response

# Create your views here.
class Home(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home2.html'

    def get(self, request):
        
        return Response({"hello":"Naatak nhi"})

    def post(self, request):
        profile = Profile.objects.create(image=request.FILES.get('image'), user=request.user)
        profile.save()
        print(profile)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class Login1(APIView):
    def get(self, request):
        return render(request, 'login.html')
        
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        if User.objects.filter(username=email).exists():
            user = User.objects.get(username=email)                
            correct_password = check_password(password, user.password)

            if correct_password:
                    
                    response = 0
              
                    login(request, user)
                        

                    
                    response = Response({'home':"present"})

                    return response
                       
                    # response = 0
                    # if self.request.GET.get('next'):
                    #     response = redirect(self.request.GET.get('next'))
                    # else:
                    #     response = redirect('home')
                    # response.set_cookie('name', str(request.user.username)) 
                    
                    # return response
                    
            else:
                return Response({'data':"Wrong password"})
        else:
            return Response({'data':"User does not exists"})
        

class Logout(APIView):
    def get(self, request):        
        logout(request)

        return HttpResponseRedirect('login')


class AddData(APIView):
    # permission_required = ("app2.view_data", "app2.add_data")
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home2.html'
    parser_classes = [DjangoModelPermissions]

    # @method_decorator(permission_required('app2.view_data'))
    def get(self, request):
        print(request.user.has_perm("app2.add_data"))
        data = {'data':Data.objects.all()}
        return Response(data)

    
    def post(self, request):
        serializer = SampleSerializer(data=request.data)
        if serializer.is_valid():
            saved_serializer = serializer.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])