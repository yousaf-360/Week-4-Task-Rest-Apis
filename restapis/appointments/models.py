from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    """
    Model representing an appointment between a doctor and a patient.
    """
    doctor = models.ForeignKey(User, related_name="doctor_appointment", on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name="patient_appointment", on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """
        Meta options for the `Appointment` model.
        """
        unique_together = ('doctor', 'scheduled_at')
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
    
    def clean(self):
        """
        Validate the appointment data to ensure that the `doctor` and `patient` 
        have appropriate roles.

        Raises:
            ValidationError: If the selected doctor is not a doctor or 
            if the selected patient is not a patient.
        """
        super().clean()
        if self.doctor.role != 'doctor':
            raise ValidationError({'doctor': 'The selected user is not a doctor.'})
        if self.patient.role != 'patient':
            raise ValidationError({'patient': 'The selected user is not a patient.'})

    def save(self, *args, **kwargs):
        """
        Override the save method to perform custom validation before saving the instance.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.clean()  
        super().save(*args, **kwargs)
    
    def __str__(self):
        """
        Return a string representation of the appointment.

        Returns:
            str: A string representing the appointment, including patient and doctor usernames.
        """
        return f'Appointment for {self.patient.username} with Dr. {self.doctor.username}'
