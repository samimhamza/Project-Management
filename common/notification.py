from common.pusher import pusher_client
from users.models import User, Notification, UserNotification
from users.api.serializers import UserNotificationSerializer
import json


def prepareData(user, data):
    pusher_client.trigger(
        u'notifications.'+str(user.id), u'share', {
            'sender': data['sender'],
            'receiver': data['receiver'],
            'notification': data['notification'],
            'created_at': data['created_at']
        })


def userNotifications(request, user, notification):
    if user.id != request.user.id:
        userNotification = UserNotification.objects.create(
            receiver=user, notification=notification, sender=request.user)
        serializer = UserNotificationSerializer(userNotification)
        prepareData(user, serializer.data)


def sendNotification(request, users, project_data):
    team_users = User.objects.only('id').filter(
        teams__in=project_data["teams"])
    if len(team_users) > 0 or len(users) > 0:
        notification, created = Notification.objects.get_or_create(
            title='New Project Assignment')
        notification.description = 'New Project Has been assigned to you!'
        notification.save()
    for user in users:
        userNotifications(request, user, notification)
    for user in team_users:
        userNotifications(request, user, notification)
