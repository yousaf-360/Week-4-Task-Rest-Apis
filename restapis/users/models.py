from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    )
    
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='doctor')
    specialization = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()  
    def save(self, *args, **kwargs):
        if self.role != 'doctor':
            self.specialization = None
        
        self.update_permissions_by_role()
        super().save(*args, **kwargs)
    
    def update_permissions_by_role(self):
        if self.role == 'admin':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
    
    def __str__(self):
        return self.username
