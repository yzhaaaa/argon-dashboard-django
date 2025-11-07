# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.authentication.models import UserCredentials, UserProfile
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


# @login_required(login_url="/login/")
def index(request):
    if not request.session.get('user_id'):
        return redirect('login')  # Redirect if not logged in

    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    if not request.session.get('user_id'):
        return redirect('login')  # Redirect if not logged in

    context = {}
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


# def profile_view(request):
#     # Redirect if not logged in
#     if not request.user.is_authenticated:
#         return redirect('login')

#     # Get the currently logged-in user credentials
#     user_id = request.session.get('user_id')
#     creds = None
#     profile = None

#     if user_id:
#         creds = UserCredentials.objects.filter(pk=user_id).first()
#         if creds:
#             profile = UserProfile.objects.filter(user=creds).first()

#     context = {
#         'segment': 'profile',
#         'creds': creds,
#         'profile': profile,
#     }
#     return render(request, 'home/profile.html', context)
