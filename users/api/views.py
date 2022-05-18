from rest_framework import generics, permissions, status
from users.api.serializers import (
    UserSerializer,
    TeamSerializer,
    TeamUserSerializer,
    NotificationSerializer,
    UserNoteSerializer,
    ReminderSerializer,
    HolidaySerializer,
)
from users.models import User, Team, TeamUser, UserNote, Reminder, Holiday, Notification
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data
            first_name = data["first_name"]
            last_name = data["last_name"]
            username = data["username"]
            email = data["email"]
            password = data["password"]
            re_password = data["re_password"]
            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(username=username, email=email).exists():
                        user = User.objects.create_user(
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                            email=email,
                            password=password,
                            created_by=request.user.id,
                            updated_by=request.user.id,
                        )
                        user.save()
                        if User.objects.filter(username=username).exists():
                            return Response(
                                {"success": "Account Successfully Created"},
                                status=status.HTTP_201_CREATED,
                            )
                        else:
                            return Response(
                                {
                                    "error": "Something went wrong when registering account"
                                },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            )
                    else:
                        return Response(
                            {"error": "User Already Exists"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"error": "Password must be at least 8 characters in length"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"error": "Something went wrong while trying to register account"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# User CRUD
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True)
    serializer_class = UserSerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(created_by=request.user.id)
                request.data.update(updated_by=request.user.id)
        except:
            request.data.update(created_by=request.user.id)
            request.data.update(updated_by=request.user.id)
        return self.create(request, *args, **kwargs)


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(updated_by=request.user.id)
                request.data.update(updated_at=datetime.datetime.now())
        except:
            request.data.update(updated_by=request.user.id)
            request.data.update(updated_at=datetime.datetime.now())
        return self.update(request, *args, **kwargs)


# end of User CRUD

# Team CRUD
class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.filter(deleted_at__isnull=True)
    serializer_class = TeamSerializer
    # paginate_by = 10

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     try:
    #         if not request.data._mutable:
    #             request.data._mutable = True
    #             request.data.update(created_by=request.user.id)
    #             request.data.update(updated_by=request.user.id)
    #     except:
    #         request.data.update(created_by=request.user.id)
    #         request.data.update(updated_by=request.user.id)
    #     return self.create(request, *args, **kwargs)


class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.filter(deleted_at__isnull=True)
    serializer_class = TeamSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     try:
    #         if not request.data._mutable:
    #             request.data._mutable = True
    #             request.data.update(updated_by=request.user.id)
    #             request.data.update(updated_at=datetime.datetime.now())
    #     except:
    #         request.data.update(updated_by=request.user.id)
    #         request.data.update(updated_at=datetime.datetime.now())
    #     return self.update(request, *args, **kwargs)


# end of Team CRUD

# TeamUser CRUD
class TeamUserListCreateAPIView(generics.ListCreateAPIView):
    queryset = TeamUser.objects.all()
    serializer_class = TeamUserSerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TeamUserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamUser.objects.all()
    serializer_class = TeamUserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# end of TeamUser CRUD

# UserNote CRUD
class UserNoteListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserNote.objects.all()
    serializer_class = UserNoteSerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(user=request.user.id)
        except:
            request.data.update(user=request.user.id)
        return self.create(request, *args, **kwargs)


class UserNoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserNote.objects.all()
    serializer_class = UserNoteSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(updated_at=datetime.datetime.now())
        except:
            request.data.update(updated_at=datetime.datetime.now())
        return self.update(request, *args, **kwargs)


# end of UserNote CRUD
# Reminder CRUD
class ReminderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(user=request.user.id)
        except:
            request.data.update(user=request.user.id)
        return self.create(request, *args, **kwargs)


class ReminderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
                request.data.update(updated_at=datetime.datetime.now())
        except:
            request.data.update(updated_at=datetime.datetime.now())
        return self.update(request, *args, **kwargs)


# end of Reminder CRUD
# Notification CRUD
class NotificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NotificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# end of Notification CRUD
# Holiday CRUD
class HolidayListCreateAPIView(generics.ListCreateAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class HolidayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# end of Holiday CRUD
