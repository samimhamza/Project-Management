from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from users.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

    def validate(self, attrs):
        userName = attrs.get("username")
        password = attrs.get("password")

        if validateEmail(userName) is False:
            try:
                user = User.objects.get(username=userName)
                if user.check_password(password):
                    attrs['username'] = user.username
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    'No such user with provided credentials'.title())
        else:
            try:
                user = User.objects.get(email=userName)
                if user.check_password(password):
                    attrs['username'] = user.username
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    'No such user with provided credentials'.title())

        data = super().validate(attrs)
        return data
