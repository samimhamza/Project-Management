from common.pusher import pusher_client
from users.models import User, Notification, UserNotification
from users.api.serializers import UserNotificationSerializer


def prepareData(request, user, data, new_project):
    data['notification']['description'] = data['notification']['description'].format(
        str(new_project.name), request.user.first_name + " " + request.user.last_name)
    pusher_client.trigger(
        u'notifications.'+str(user.id), u'share', {
            'id': data['id'],
            'seen': data['seen'],
            'notification': data['notification'],
            'created_at': data['created_at']
        })


def userNotifications(request, user, notification, new_project):
    if user.id != request.user.id:
        userNotification = UserNotification.objects.create(
            receiver=user, notification=notification, sender=request.user)
        serializer = UserNotificationSerializer(userNotification)
        prepareData(request, user, serializer.data, new_project)


def sendNotification(request, users, project_data, new_project):
    team_users = User.objects.only('id').filter(
        teams__in=project_data["teams"])
    if len(team_users) > 0 or len(users) > 0:
        notification, created = Notification.objects.get_or_create(
            title='Project Assignment')
        notification.description = '{} Project has assigned to you by {}'
        notification.save()
    for user in users:
        userNotifications(request, user, notification, new_project)
    for user in team_users:
        userNotifications(request, user, notification, new_project)
