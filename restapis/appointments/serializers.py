from rest_framework import serializers
from .models import Appointment
from django.urls import reverse

class AppointmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'scheduled_at', 'created_at', 'updated_at', 'url']
        read_only_fields = ['created_at', 'updated_at']

    def get_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(reverse('appointment-detail', args=[obj.id]))
        return None

    def validate(self, data):
        doctor = data.get('doctor')
        patient = data.get('patient')

        if doctor and doctor.role != 'doctor':
            raise serializers.ValidationError({'doctor': 'The selected user is not a doctor.'})
        if patient and patient.role != 'patient':
            raise serializers.ValidationError({'patient': 'The selected user is not a patient.'})

        return data
