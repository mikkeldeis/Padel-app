from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import JSONField

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

class Tournament(models.Model):
  TOURNAMENT_TYPES = [
    ('BRACKET', 'Bracket'),
    ('AMERICANO', 'Americano'),
    ('LEAGUE', 'League')
  ]
  host = models.ForeignKey(User, on_delete=models.CASCADE)
  start_date = models.DateField(null=True, blank=True)
  end_date = models.DateField(null=True, blank=True)
  name = models.CharField(max_length=100)
  winner = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
  tournament_type = models.CharField(max_length=10, choices=TOURNAMENT_TYPES, default='BRACKET')
  def __str__(self):
    return f'{self.name} hosted by {self.host.username}'
  
class Round(models.Model):
  tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  round_number = models.IntegerField()
  start_date = models.DateField()

  def __str__(self):
    return f'Round {self.round_number} of {self.tournament.name}'

class Match(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    round = models.ForeignKey('Round', related_name='matches', on_delete=models.CASCADE, null=True, blank=True)
    tournament = models.ForeignKey('Tournament', related_name='matches', on_delete=models.CASCADE, null=True, blank=True)
    team_1 = models.ForeignKey('Team', related_name='team_1_matches', on_delete=models.CASCADE, null=True, blank=True)
    team_2 = models.ForeignKey('Team', related_name='team_2_matches', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    # Store scores as arrays of integers
    score_team_1 = JSONField(blank=True, null=True)  # Store scores as JSON
    score_team_2 = JSONField(blank=True, null=True)
    
    winner = models.ForeignKey('Team', related_name='won_matches', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} at {self.date}"
    def record_result(self, score_team_1, score_team_2):
      """ Record the final result after the match is done. """
      self.score_team_1 = score_team_1
      self.score_team_2 = score_team_2
      self.status = 'Completed'
      # Determine the winner based on scores
      self.winner = self.determine_winner()
      self.save()

    def determine_winner(self):
      """ Determine the winner based on set scores. """
      if not self.score_team_1 or not self.score_team_2:
            return None
      team_1_sets_won = sum(1 for set_team_1, set_team_2 in zip(self.score_team_1, self.score_team_2) if set_team_1 > set_team_2)
      team_2_sets_won = len(self.score_team_1) - team_1_sets_won
      return self.team_1 if team_1_sets_won > team_2_sets_won else self.team_2
  
  


  
