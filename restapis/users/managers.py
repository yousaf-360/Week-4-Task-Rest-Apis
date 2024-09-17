from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the `CustomUser` model.

    This manager provides methods for creating superusers and regular users 
    with email normalization and password hashing.
    """
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser with the given username, email, and password.

        A superuser is a user with admin privileges. This method sets the 
        `is_staff` and `is_superuser` flags to True and assigns the 'admin' 
        role to the user. It also ensures that an email is provided.

        Args:
            username (str): The username for the superuser.
            email (str, optional): The email address for the superuser. Must be provided.
            password (str, optional): The password for the superuser.
            **extra_fields: Additional fields to set on the user.

        Returns:
            CustomUser: The created superuser instance.

        Raises:
            ValueError: If no email is provided.
        """
        if not email:
            raise ValueError('Superusers must have an email address.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin' 
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user with the given username, email, and password.

        This method ensures that an email is provided and handles password 
        hashing. It does not set `is_staff` or `is_superuser` flags.

        Args:
            username (str): The username for the user.
            email (str, optional): The email address for the user. Must be provided.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields to set on the user.

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValueError: If no email is provided.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
