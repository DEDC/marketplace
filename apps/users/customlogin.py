# Django
from django.contrib.auth import backends
# app user
from .models import Usuarios

class EmailAuthBackend(backends.ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/phone_number pair, then check
    a username/password pair if email failed
    """
    def authenticate(self, request, username=None, password=None, admin = None):
        """ Authenticate a user based on email address as the user name. """
        try:
            if admin is not None:
                user = Usuarios.objects.get(email = username, is_superuser = True)
            else:
                user = Usuarios.objects.get(email = username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Usuarios.DoesNotExist:
            return None