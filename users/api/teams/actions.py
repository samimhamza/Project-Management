from users.models import Team, TeamUser, User


# return leader of team of unserialized team parameter
def get_leader(team):
    try:
        team_leader = TeamUser.objects.values(
            "user").get(team=team, is_leader=True)
        leader = User.objects.values("id", "first_name", "last_name").get(
            pk=team_leader["user"]
        )
        return leader
    except:
        return {}


# return leader of team of serialized team_id parameter
def get_leader_by_id(id):
    try:
        team = Team.objects.only('id').get(pk=id)
        team_leader = TeamUser.objects.values(
            "user").get(team=team, is_leader=True)
        leader = User.objects.values("id", "first_name", "last_name").get(
            pk=team_leader["user"]
        )
        return leader
    except:
        return {}


# return total users of team of unserialized team parameter
def get_total(team):
    try:
        return TeamUser.objects.filter(team=team).count()
    except:
        return 0


# return total_users of team of serialized team_id parameter
def get_total_users(id):
    try:
        team = Team.objects.only('id').get(pk=id)
        return TeamUser.objects.filter(team=team).count()
    except:
        return 0
