from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import CharField


class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, name, school, class_number, city, mobile, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, school=school, class_number=class_number, city=city, mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password):

        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    school = models.CharField(max_length=255)
    class_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email





