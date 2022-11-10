import threading
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth import logout

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
        try:
            if request.user.is_authenticated:
                if request.session.has_key('last_login'):
                    print("alkdj")
            else:
                response = Response(
                                        {"detail": "This action is not authorized"},
                                        content_type="application/json",
                                        status=status.HTTP_401_UNAUTHORIZED,
                                    )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response()
        except:
            pass
        return self.get_response(request)

    def process_exception(self, request, exception):
        request_local.request = None
        request_branch.request = None

    def process_template_response(self, request, response):
        request_local.request = None
        request_branch.request = None
        return response
