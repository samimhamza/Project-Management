from rest_framework import generics
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


class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.filter(deleted_at__isnull=True)
    serializer_class = TeamSerializer

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
