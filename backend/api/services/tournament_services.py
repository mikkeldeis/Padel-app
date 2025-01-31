import random
from ..models import Tournament, Team
from django.utils import timezone

def create_teams_Americano(tournament):
  participants = list(tournament.participants.all())
  random.shuffle(participants)
  team_size = tournament.team_size
  while len(participants) >= team_size:
    team = Team.objects.create(player1=participants.pop(), player2=participants.pop() if team_size == 2 else None)
    tournament.teams.add(team)
  tournament.save()


