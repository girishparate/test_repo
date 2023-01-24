import threading
from django.shortcuts import render
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.conf import settings
from .models import LoginLogout, UserSessionModel
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from rest_framework.renderers import TemplateHTMLRenderer




request_local = threading.local()
request_branch = threading.local()
request_bms_val = threading.local()

def get_username():
    return getattr(request_local, 'request', None)

def get_branch():
    return getattr(request_branch, 'request', None)

class RequestMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # if isfunction(response, render):
        #     print("hello")
        
        if isinstance(response, Response):
            
            response.data['new_data'] = "Girish Parate is logged in"
            response._is_rendered = False 
            response.render()
            print((response.data))
      
        return response

    # def process_template_response(self, request, response):
    #    if hasattr(response, 'data'): 
    #       response.data['detail'] = 'bla-bla-bla'
    #    return response