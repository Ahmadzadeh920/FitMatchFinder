from django.db import models
from datetime import datetime

# Create your models here.
from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password and extra data.
        """
        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


# class role




# class profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser,related_name="User", on_delete=models.CASCADE)
    first_name = models.CharField()
    last_name = models.CharField()
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.user.email} Profile"
    
    @receiver(post_save, sender= CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)



class List_API_Key(models.Model):
    def generate_uuid():
        return str(uuid.uuid5(uuid.NAMESPACE_OID, datetime.now().isoformat()))
    
    profile = models.ForeignKey(Profile, related_name="Profle", on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True, default= generate_uuid , blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    is_active = models.BooleanField(default=False)
    name_service = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.key
       
    

# reset password
class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)