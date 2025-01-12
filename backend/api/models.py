from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
  player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_player1')
  player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_player2', null=True, blank=True)
  wins = models.IntegerField(default=0)
  losses = models.IntegerField(default=0)
  
  def __str__(self):
    if self.player2 is None:
      return f'{self.player1.username} with {self.wins} wins and {self.losses} losses'
    else:
      return f'{self.player1.username} and {self.player2.username} with {self.wins} wins and {self.losses} losses'

class Match(models.Model):
  team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team1',null=False, default=1)
  team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team2',null=False, default=2)
  winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_winner')
  loser = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_loser')
  date = models.DateTimeField(auto_now_add=True)
  score = models.CharField(max_length=100, default='0-0')

  def __str__(self):
    return f'{self.team1} vs {self.team2} with {self.winner} as the winner at {self.date} with a score of {self.score}'
