from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's built-in `AbstractUser`.
    
    This model includes additional fields and methods to handle user roles, 
    permissions, and specialization. It provides role-based permissions and 
    manages the specialization field based on the user's role.
    """
    
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    )
    
    role = models.CharField(
        max_length=7,
        choices=ROLE_CHOICES,
        default='doctor',
        help_text='Defines the role of the user (admin, doctor, patient).'
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Specialization of the doctor. Null if the user is not a doctor.'
    )

    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        """
        Override the save method to update the `specialization` field and
        set permissions based on the user role before saving the instance.
        """
        if self.role != 'doctor':
            self.specialization = None
        
        self.update_permissions_by_role()
        super().save(*args, **kwargs)
    
    def update_permissions_by_role(self):
        """
        Update the user's permissions based on their role.
        """
        if self.role == 'admin':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
    
    def __str__(self):
        """
        Return a string representation of the user.
        """
        return self.username
