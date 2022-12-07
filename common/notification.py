from common.pusher import pusher_client
from users.models import Notification, UserNotification
from users.api.serializers import UserNotificationSerializer


def prepareData(user, data):
    returnObj = {
        'id': data['id'],
        'seen': data['seen'],
        'notification': data['notification'],
        'created_at': data['created_at'],
    }
    if data['description'] is not None:
        returnObj['description'] = data['description']
    if data['instance_id'] is not None:
        returnObj['instance_id'] = data['instance_id']
    if data['model_name'] is not None:
        returnObj['model_name'] = data['model_name']
    pusher_client.trigger(
        u'notifications.'+str(user.id), u'share', returnObj)


def userNotifications(request, user, notification, data):
    if user.id != request.user.id:
        userNotification = UserNotification.objects.create(
            receiver=user,
            notification=notification,
            sender=request.user
        )
        if 'description' in data.keys():
            userNotification.description = data['description']
        if 'model_name' in data.keys():
            userNotification.model_name = data['model_name']
        if 'instance_id' in data.keys():
            userNotification.instance_id = data['instance_id']
        userNotification.save()
        serializer = UserNotificationSerializer(userNotification)
        prepareData(user, serializer.data)


def sendNotification(request, users, data, team_users=[]):
    if len(team_users) > 0 or len(users) > 0:
        notification, created = Notification.objects.get_or_create(
            title=data['title'])
        if "notification_description" in data.keys():
            notification.description = data['notification_description']
        if 'icon' in data.keys():
            notification.icon = data['icon']
        if 'type' in data.keys():
            notification.type = data['type']
        notification.save()
    for user in users:
        userNotifications(request, user, notification, data)
    for user in team_users:
        userNotifications(request, user, notification, data)
