from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username:
            raise ValidationError('Username not given')
        if not password:
            raise ValidationError('Password not given')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            raise ValidationError('Invalid credentials')



class UserListAPIView(generics.ListAPIView):
    """
    List users (doctors and patients). Only accessible by admin.
    Can be filtered by role using the 'role' query parameter.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to view this resource.")
        
        role = self.request.query_params.get('role', None)
        queryset = CustomUser.objects.all()

        if role:
            if role not in ['doctor', 'patient']:
                raise ValidationError("Invalid role specified.")
            queryset = queryset.filter(role=role)
        
        return queryset

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single user. Only accessible by admin.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to access this resource.")
        return super().get_object()

    def put(self, request, *args, **kwargs):
        """
        Override the update method to return the updated user data.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_update(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to update this resource.")
        serializer.save()

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to return a status code.
        """
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserCreateAPIView(generics.CreateAPIView):
    """
    Create a new user (doctor or patient). Only accessible by admin.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to create this resource.")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
