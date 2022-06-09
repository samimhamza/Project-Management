from rest_framework import generics
from users.models import User, PasswordReset
from .serializers import PasswordResetSerializer
from rest_framework.response import Response
import django.utils.timezone
from django.core.mail import send_mail


class ForgotPasswordCreateAPIView(generics.CreateAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response({"error": 'No such user with provided email!'}, status=404)
        password_reset = PasswordReset.objects.create(user=user)
        return Response({'success': "Reset Link has sent to your email. Please check your email!"}, status=201)


class ForgotPasswordRetrieveAPIView(generics.RetrieveAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        password_reset = self.get_object()
        diff = django.utils.timezone.now() - password_reset.created_at
        if diff.total_seconds() < 300:
            return Response({'success': ""})
        else:
            return Response({"error": "Access expired please try again"})
