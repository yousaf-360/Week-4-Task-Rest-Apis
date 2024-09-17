from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import APIException
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token

class LoginAPIView(APIView):
    """
    Handles user login and token generation.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username:
            raise ValidationError('Username not given')
        if not password:
            raise ValidationError('Password not given')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.role == 'patient':
                return Response(
                    {'non_field_errors': ['Patients cannot log in.']},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'non_field_errors': ['Invalid credentials']},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserListAPIView(generics.ListCreateAPIView):
    """
    Lists and creates users (doctors and patients).
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

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to create this resource.")
        serializer.save()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to access this resource.")
        return super().get_object()

    def put(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to update this resource.")
        serializer.save()

    def delete(self, request, *args, **kwargs):
        try:
            if self.request.user.role != 'admin':
                raise PermissionDenied("You do not have permission to delete this resource.")
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
class UserCreateAPIView(generics.CreateAPIView):
    """
    Create a new user (doctor or patient).
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have permission to create this resource.")
        serializer.save()