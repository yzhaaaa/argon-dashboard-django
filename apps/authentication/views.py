# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from .models import UserCredentials
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from .models import UserCredentials, UserProfile, User
from .forms import LoginForm, SignUpFormCredentials, SignUpFormInfo
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.core.signing import TimestampSigner
from django.core.mail import send_mail
from django.urls import reverse


def login_view(request):
    msg = None

    if request.method == "POST":
        login_input = request.POST.get("email")
        password = request.POST.get("password")

        # Look up by username first, then by email
        user_cred = UserCredentials.objects.filter(
            username=login_input).first()
        if not user_cred:
            user_cred = UserCredentials.objects.filter(
                email_address=login_input).first()

        if not user_cred:
            msg = "User not found"
        elif not check_password(password, user_cred.password_hash):
            msg = "Invalid credentials"
        else:
            # Create signed token containing user_id and email
            signer = TimestampSigner()
            token = signer.sign(
                f"{user_cred.user_id}:{user_cred.email_address}")

            # Send login confirmation email
            login_link = request.build_absolute_uri(
                reverse('confirm_login', args=[token])
            )
            send_mail(
                'Login Confirmation',
                f'Click here to complete login: {login_link}',
                'no-reply@example.com',
                [user_cred.email_address],
                fail_silently=False
            )

            msg = "Check your email to complete login."
            return redirect("/")

    return render(request, "accounts/login.html", {"msg": msg})


def logout_view(request):
    request.session.flush()  # clears all session data
    return redirect('login')  # explicitly redirect to login page


def register_user_info(request):
    msg = None

    # Clear any existing session for profile_id
    request.session.pop("profile_id", None)

    if request.method == "POST":
        form = SignUpFormInfo(request.POST)
        if form.is_valid():
            # Save profile WITHOUT assigning user yet
            profile = form.save(commit=False)
            profile.created_at = timezone.now()
            profile.user = None  # Ensure no user assigned yet
            profile.save()

            # Store profile ID in session
            request.session["profile_id"] = profile.pk
            request.session.modified = True  # Force session save

            print("DEBUG: Profile saved with ID ->", profile.pk)
            print("DEBUG: Session data ->", dict(request.session))

            # Redirect to credentials registration
            return redirect("register")
        else:
            msg = "Form is not valid"
    else:
        form = SignUpFormInfo()

    return render(request, "accounts/register_info.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    profile_id = request.session.get("profile_id")
    if not profile_id:
        return redirect("register_info")

    if request.method == "POST":
        form = SignUpFormCredentials(request.POST)
        if form.is_valid():
            # Store credentials temporarily in session instead of saving immediately
            request.session['temp_user_data'] = {
                'user': {
                    'user_type_id': 2,
                    'user_status_id': 1,
                    'created_at': timezone.now().isoformat(),
                },
                'credentials': {
                    'username': form.cleaned_data['username'],
                    'password_hash': make_password(form.cleaned_data['password_hash']),
                    'email_address': form.cleaned_data['email_address'],
                    'created_at': timezone.now().isoformat(),
                },
                'profile_id': profile_id
            }

            # Generate signed token
            signer = TimestampSigner()
            token = signer.sign(form.cleaned_data['email_address'])

            # Build confirmation link
            confirmation_link = request.build_absolute_uri(
                reverse('confirm_email', args=[token])
            )

            # Send confirmation email
            send_mail(
                'Confirm your account',
                f'Click the link to confirm your email (hindi \'to scam): {confirmation_link}',
                'no-reply@example.com',
                [form.cleaned_data['email_address']],
                fail_silently=False,
            )

            messages.success(
                request, "Check your email to confirm registration.")
            return redirect("login")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpFormCredentials()

    return render(request, "accounts/register.html", {"form": form, "msg": msg})


def confirm_email(request, token):
    signer = TimestampSigner()
    try:
        # Validate token (expires after 1 hour)
        email = signer.unsign(token, max_age=3600)

        temp_data = request.session.get('temp_user_data')
        if not temp_data:
            return HttpResponse("Session expired or invalid token.")

        # Save actual User
        user = User.objects.create(**temp_data['user'])

        # Save UserCredentials
        credentials_data = temp_data['credentials']
        credentials = UserCredentials.objects.create(
            user_id=user.user_id,
            username=credentials_data['username'],
            password_hash=credentials_data['password_hash'],
            email_address=credentials_data['email_address'],
            created_at=credentials_data['created_at']
        )

        # Link UserProfile
        profile = UserProfile.objects.get(pk=temp_data['profile_id'])
        profile.user = credentials
        profile.save()

        # Clear temporary session
        del request.session['temp_user_data']

        return HttpResponse("Email confirmed! You can now log in.")

    except (BadSignature, SignatureExpired):
        return HttpResponse("Invalid or expired token.")


def confirm_login(request, token):
    signer = TimestampSigner()
    try:
        # Decode token: user_id:email
        data = signer.unsign(token, max_age=900)  # 15 minutes
        user_id, email = data.split(":")

        # Fetch user from DB
        user_cred = UserCredentials.objects.get(pk=user_id)
        if user_cred.email_address != email:
            return HttpResponse("Invalid token.")

        # Set session to mark user as logged in
        request.session['user_id'] = user_cred.user_id
        request.session['username'] = user_cred.username
        request.session.modified = True

        # Redirect to Argon dashboard
        return redirect('home')  # or '/' depending on your urls

    except (BadSignature, SignatureExpired):
        return HttpResponse("Invalid or expired token.")


def dashboard_view(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return redirect('/')
