from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    doctor = models.ForeignKey(User, related_name="doctor_appointment", on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name="patient_appointment", on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('doctor', 'scheduled_at')
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
    
    def clean(self):
        super().clean()
        if self.doctor.role != 'doctor':
            raise ValidationError({'doctor': 'The selected user is not a doctor.'})
        if self.patient.role != 'patient':
            raise ValidationError({'patient': 'The selected user is not a patient.'})

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Appointment for {self.patient.username} with Dr. {self.doctor.username}'
