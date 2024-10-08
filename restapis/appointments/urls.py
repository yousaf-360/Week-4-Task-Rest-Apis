from django.urls import path
from .views import AppointmentListAPIView, AppointmentCreateAPIView,AppointmentDetailAPIView, AppointmentSummaryAPIView

urlpatterns = [
     path('appointments/', AppointmentListAPIView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetailAPIView.as_view(), name='appointment-detail'),
    path('appointments/summary/', AppointmentSummaryAPIView.as_view(), name='appointment-summary'),
    path('appointments/create/', AppointmentCreateAPIView.as_view(), name='appointment-create'),
]
