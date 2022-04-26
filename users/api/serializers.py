from rest_framework import serializers
from users.models import User, Team, UserNote, Reminder, Holiday, Notification, TeamUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamUser
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    # team_users = TeamUserSerializer(many=True)

    class Meta:
        model = Team
        fields = "__all__"


class UserNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNote
        fields = "__all__"


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = "__all__"


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
