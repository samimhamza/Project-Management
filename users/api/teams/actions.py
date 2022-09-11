from users.models import Team, TeamUser, User
from users.api.serializers import UserWithProfileSerializer


def get_leader(team, request):
    try:
        team_leader = TeamUser.objects.values(
            "user").get(team=team, is_leader=True)
    except TeamUser.DoesNotExist:
        return {}
    leader = User.objects.get(pk=team_leader["user"])
    serializer = UserWithProfileSerializer(
        instance=leader, context={"request": request})
    return serializer.data


# return leader of team of serialized team_id parameter
def get_leader_by_id(id, request):
    team = Team.objects.only('id').get(pk=id)
    try:
        team_leader = TeamUser.objects.values(
            "user").get(team=team, is_leader=True)
    except TeamUser.DoesNotExist:
        return {}
    leader = User.objects.get(pk=team_leader["user"])
    serializer = UserWithProfileSerializer(
        instance=leader, context={"request": request})
    return serializer.data


# return total users of team of unserialized team parameter
def get_total(team):
    try:
        return TeamUser.objects.filter(team=team).count()
    except:
        return 0


# return total_members of team of serialized team_id parameter
def get_total_users(id):
    try:
        team = Team.objects.only('id').get(pk=id)
        return TeamUser.objects.filter(team=team).count()
    except:
        return 0
