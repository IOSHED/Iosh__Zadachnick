from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from .lib.path import user_directory_path


# Define CustomUserManager to handle user creation, validation, and authentication
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Check if email is provided
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        # Create user object and set password
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set is_staff and is_superuser to True for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Define CustomUser model that extends AbstractBaseUser
class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.TextField(max_length=255, null=True)
    surname = models.TextField(max_length=255, null=True)
    chat_id = models.CharField(max_length=50, null=True, default=None, blank=True)

    icon32 = models.ImageField(upload_to=user_directory_path, default="default/user_icon_32.png")
    icon64 = models.ImageField(upload_to=user_directory_path, default="default/user_icon_64.png")

    birthday_at = models.DateField(null=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verification = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'birthday_at']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.is_superuser

    def has_perm(self, _):
        return self.is_staff

    def has_module_perms(self, _):
        return self.is_staff
