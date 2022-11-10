from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from .decorator import cache_per_user


urlpatterns = [
    path('home', login_required(cache_per_user(30)(Home.as_view())),name='home'),

    path('login', Login1.as_view(), name='login'),

    path('logout', login_required(Logout.as_view()), name='logout')

]