from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import permission_classes, authentication_classes
from users.models import User, PasswordReset


@authentication_classes([])
@permission_classes([])
def index(request):
    user = User.objects.filter()[0]
    password_reset = PasswordReset.objects.filter(user=user).last()
    resetUrl = "http://localhost:3000/auth/reset_password/" + \
        str(password_reset.id) + "/"
    baseUrl = "http: // localhost: 3000/"

    template = loader.get_template('email.html')
    context = {'baseUrl': baseUrl, 'resetUrl': resetUrl}
    return HttpResponse(template.render(context, request))
