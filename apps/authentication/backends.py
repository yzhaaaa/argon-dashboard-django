# # apps/authentication/backends.py
# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.models import AnonymousUser
# from .models import UserCredentials
# from django.contrib.auth.hashers import check_password


# class CustomAuthBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = UserCredentials.objects.get(username=username)
#             if user and check_password(password, user.password_hash):
#                 return user  # This object will be request.user
#         except UserCredentials.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return UserCredentials.objects.get(pk=user_id)
#         except UserCredentials.DoesNotExist:
#             return None


# class UserCredentialsBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = UserCredentials.objects.get(username=username)
#             if check_password(password, user.password_hash):
#                 return user  # Note: user must implement is_authenticated
#         except UserCredentials.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return UserCredentials.objects.get(pk=user_id)
#         except UserCredentials.DoesNotExist:
#             return None
