from django.urls import path
from .views import LoginAPIView, UserListAPIView, UserDetailAPIView, UserCreateAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
]
