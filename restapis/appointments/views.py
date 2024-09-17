from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.utils.dateparse import parse_date
from django.utils.dateformat import format
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.role == 'admin':
            appointments = Appointment.objects.all()
        elif request.user.role == 'doctor':
            appointments = Appointment.objects.filter(doctor=request.user)
        else:
            return Response({'detail': 'Not authorized to view appointments'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AppointmentSerializer(appointments, many=True, context={'request': request})
        return Response(serializer.data)

class AppointmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        appointment = super().get_object()
        if self.request.user.role == 'doctor' and appointment.doctor != self.request.user:
            raise PermissionDenied("You do not have permission to view this appointment.")
        return appointment

class AppointmentSummaryAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to access this resource.")
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        doctor_name = request.query_params.get('doctor_name', '')

        if not start_date:
            return Response({'detail': 'Start date is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = parse_date(start_date)
            if end_date:
                end_date = parse_date(end_date)
        except ValueError:
            return Response({'detail': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if start_date:
            if end_date and start_date > end_date:
                return Response({'detail': 'Start date must be before end date.'}, status=status.HTTP_400_BAD_REQUEST)

            filters = {'scheduled_at__date__gte': start_date}
            if end_date:
                filters['scheduled_at__date__lte'] = end_date
            if doctor_name:
                filters['doctor__username__icontains'] = doctor_name

            appointments = Appointment.objects.filter(**filters)

            summary = (
                appointments
                .values('scheduled_at__date')
                .annotate(count=Count('id'))
                .order_by('scheduled_at__date')
            )
            
            data = []
            for entry in summary:
                date_str = format(entry['scheduled_at__date'], 'Y-m-d')
                count = entry['count']
                day_appointments = appointments.filter(scheduled_at__date=entry['scheduled_at__date'])
                
                serializer = self.get_serializer(day_appointments, many=True, context={'request': request})
                appointment_urls = [appt['url'] for appt in serializer.data]
                
                data.append({
                    'date': date_str,
                    'count': count,
                    'appointments_url': appointment_urls
                })
            
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Start date is required.'}, status=status.HTTP_400_BAD_REQUEST)