from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('base', login_required(cache_per_user(60*60)(Base.as_view())),name='home'),

    path('home', login_required(Home.as_view()),name='home'),

    path('login', Login1.as_view(), name='login'),

    path('add-data', login_required(AddData.as_view()), name='add-data'),

    path('logout', login_required(Logout.as_view()), name='logout')

]