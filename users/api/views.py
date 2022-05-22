from rest_framework import viewsets, status
from users.api.serializers import (
    UserSerializer,
    NotificationSerializer,
    ReminderSerializer,
    HolidaySerializer,
    UserWithProfileSerializer,
)
from users.models import User, Reminder, Holiday, Notification
from common.custom import CustomPageNumberPagination
from common.actions import withTrashed, trashList, restore, delete
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted_at__isnull=True).order_by("-created_at")
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {}

    def list(self, request):
        queryset = self.get_queryset()
        if request.GET.get("items_per_page") == "-1":
            serializer = UserWithProfileSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, pk=None):
        return delete(self, request, User)

    @action(detail=False, methods=["get"])
    def all(self, request):
        serializer = withTrashed(self, User, order_by="-created_at")
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, User)

    # for multi restore
    @action(detail=False, methods=["get"])
    def restore(self, request, pk=None):
        return restore(self, request, User)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    pagination_class = CustomPageNumberPagination


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = CustomPageNumberPagination


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all().order_by("-created_at")
    serializer_class = ReminderSerializer
    pagination_class = CustomPageNumberPagination

    def destroy(self, request, pk=None):
        data = request.data
        if data:
            reminders = Reminder.objects.filter(pk__in=data["ids"])
            for reminder in reminders:
                reminder.delete()
        else:
            reminder = self.get_object()
            reminder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class RegisterView(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         try:
#             data = request.data
#             first_name = data["first_name"]
#             last_name = data["last_name"]
#             username = data["username"]
#             email = data["email"]
#             password = data["password"]
#             re_password = data["re_password"]
#             if password == re_password:
#                 if len(password) >= 8:
#                     if not User.objects.filter(username=username, email=email).exists():
#                         user = User.objects.create_user(
#                             first_name=first_name,
#                             last_name=last_name,
#                             username=username,
#                             email=email,
#                             password=password,
#                             created_by=request.user.id,
#                             updated_by=request.user.id,
#                         )
#                         user.save()
#                         if User.objects.filter(username=username).exists():
#                             return Response(
#                                 {"success": "Account Successfully Created"},
#                                 status=status.HTTP_201_CREATED,
#                             )
#                         else:
#                             return Response(
#                                 {
#                                     "error": "Something went wrong when registering account"
#                                 },
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             )
#                     else:
#                         return Response(
#                             {"error": "User Already Exists"},
#                             status=status.HTTP_400_BAD_REQUEST,
#                         )
#                 else:
#                     return Response(
#                         {"error": "Password must be at least 8 characters in length"},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             else:
#                 return Response(
#                     {"error": "Passwords do not match"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except:
#             return Response(
#                 {"error": "Something went wrong while trying to register account"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
