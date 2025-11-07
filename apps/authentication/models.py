# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Authentications(models.Model):
    authentication_id = models.AutoField(primary_key=True)
    user_credential_id = models.IntegerField()
    access_token = models.CharField(max_length=50)
    token_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'authentications'


class Provider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'provider'


class TwoFactorAuth(models.Model):
    # Field renamed because it wasn't a valid Python identifier.
    number_2fa_id = models.AutoField(db_column='2fa_id', primary_key=True)
    user_id = models.IntegerField()
    method = models.CharField(max_length=50)
    secret_key = models.CharField(max_length=50)
    is_active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'two_factor_auth'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_type_id = models.IntegerField(blank=True, null=True)
    user_status_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'


class UserAgreement(models.Model):
    agreement_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    terms_version = models.CharField(max_length=50)
    agreed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_agreement'


class UserCredentials(models.Model):
    user_credential_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    provider_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    email_address = models.CharField(max_length=50)
    verified = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    password_expires_at = models.DateTimeField(blank=True, null=True)
    failed_attempts = models.IntegerField(blank=True, null=True)
    last_failed_at = models.DateTimeField(blank=True, null=True)
    is_locked = models.IntegerField(blank=True, null=True)
    lock_expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_credentials'


class UserProfile(models.Model):
    user_profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        UserCredentials,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_profile'


class UserSessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    device_id = models.IntegerField()
    token = models.CharField(max_length=50)
    is_persistent = models.IntegerField()
    ip_address = models.CharField(max_length=50)
    ip_location = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_sessions'


class UserStatus(models.Model):
    user_status_id = models.AutoField(primary_key=True)
    user_status_name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'user_status'


class UserType(models.Model):
    user_type_id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50)
    session_policy_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user_type'
