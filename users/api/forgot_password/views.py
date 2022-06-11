from rest_framework import generics
from users.models import User, PasswordReset
from .serializers import PasswordResetSerializer, PasswordResetUserSerializer
from users.api.serializers import UserSerializer
from rest_framework.response import Response
import django.utils.timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import environ
env = environ.Env()
environ.Env.read_env()


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
        htmly = get_template('email.html')
        resetUrl = "http://localhost:3000/auth/reset_password/" + \
            str(password_reset.id) + "/"
        baseUrl = "http: // localhost: 3000/"
        context = {'baseUrl': baseUrl, 'resetUrl': resetUrl}
        subject, from_email, to = 'Password Reset Link', env(
            'EMAIL'), user.email
        html_content = htmly.render(context)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return Response({'success': "Reset Link has sent to your email. Please check your email!"}, status=201)


class ForgotPasswordRetrieveAPIView(generics.RetrieveAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        password_reset = self.get_object()
        diff = django.utils.timezone.now() - password_reset.created_at
        if diff.total_seconds() < 1200:
            serializer = PasswordResetUserSerializer(password_reset)
            return Response(serializer.data)
        else:
            return Response({"error": "Access expired please try again"}, status=403)


class ChangePasswordAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.get(pk=data['id'])
        except User.DoesNotExist:
            return Response({"error": 'No such user with provided email!'}, status=404)
        user.set_password(data["password"])
        user.save()
        passwrod_resets = PasswordReset.objects.filter(user=user)
        passwrod_resets.delete()
        return Response({'success': "Password Successfully changed!"}, status=201)
