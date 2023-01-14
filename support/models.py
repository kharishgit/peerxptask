from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User,on_delete=models.CASCADE)

class UserManager(BaseUserManager):
    def create_user(self, email_or_phone, password=None, **extra_fields):
        if not email_or_phone:
            raise ValueError('Users must have an email or phone number')
        user = self.model(email_or_phone=email_or_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_or_phone, password,**extra_fields):
        user = self.create_user(email_or_phone, password,**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    role_choices = [('admin', 'admin'), ('local user', 'local user')]
    role = models.CharField(max_length=20, choices=role_choices, default='local user')
    email_or_phone = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=30)
    # username=models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default= False)

    objects = UserManager()

    USERNAME_FIELD = 'email_or_phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email_or_phone

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    priority = models.CharField(max_length=12)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    status_choices = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tickets')

