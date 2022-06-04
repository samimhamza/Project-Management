from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from users.models import User, UserPermissionList
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from users.api.serializers import AuthUserSerializer, UserPermissionListSerializer


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
        auth_user = User.objects.filter(pk=self.user.id).first()
        data['user'] = AuthUserSerializer(auth_user).data
        try:
            permissions = UserPermissionList.objects.get(user=auth_user)
            data['permissions'] = UserPermissionListSerializer(
                permissions).data['permissions_list']

        except UserPermissionList.DoesNotExist:
            data['permissions'] = []
        return data
