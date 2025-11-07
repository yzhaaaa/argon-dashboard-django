# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, register_user_info, logout_view, confirm_email, confirm_login, dashboard_view
from django.contrib.auth.views import LogoutView
from ..home.views import index

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('register_info/', register_user_info, name="register_info"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path('logout/', logout_view, name='logout'),
    path('confirm-email/<str:token>/', confirm_email, name='confirm_email'),
    path('confirm-login/<str:token>/', confirm_login, name='confirm_login'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
