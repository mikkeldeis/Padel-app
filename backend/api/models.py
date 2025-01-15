from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

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
  ]
  host = models.ForeignKey(User, on_delete=models.CASCADE)
  start_date = models.DateField(null=True, blank=True)
  end_date = models.DateField(null=True, blank=True)
  name = models.CharField(max_length=100)
  winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tournament_winner', null=True, blank=True)
  tournament_type = models.CharField(max_length=10, choices=TOURNAMENT_TYPES, default='BRACKET')
  def __str__(self):
    return f'{self.name} hosted by {self.host.username}'
  def clean(self):
        # Custom validation: ensure start_date is before end_date
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
               raise ValidationError({'__all__': ['Start date must be before the end date.']})
  
class Round(models.Model):
  tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  round_number = models.IntegerField()
  start_date = models.DateField()

  def __str__(self):
    return f'Round {self.round_number} of {self.tournament.name}'


class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    round = models.ForeignKey('Round', related_name='matches', on_delete=models.CASCADE, null=True, blank=True)
    team_1 = models.ForeignKey('Team', related_name='team_1_matches', on_delete=models.CASCADE, null=True, blank=True)
    team_2 = models.ForeignKey('Team', related_name='team_2_matches', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    # Store scores as arrays of integers
    score_team_1 = ArrayField(models.IntegerField(), blank=True, null=True)  # [6, 5, 6]
    score_team_2 = ArrayField(models.IntegerField(), blank=True, null=True)  # [4, 7, 3]
    
    winner = models.ForeignKey('Team', related_name='won_matches', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} at {self.date}"

    def record_result(self, score_team_1, score_team_2):
        """ Record the final result after the match is done. """
        self.score_team_1 = score_team_1
        self.score_team_2 = score_team_2
        self.status = 'completed'
        # Determine the winner based on scores
        self.winner = self.team_1 if self._get_winner(score_team_1) else self.team_2
        self.save()

    def _get_winner(self, score_team_1):
        """ Helper function to calculate the winner based on set scores. """
        team_1_sets_won, team_2_sets_won = 0, 0
        for set_team_1, set_team_2 in zip(self.score_team_1, self.score_team_2):
            if set_team_1 > set_team_2:
                team_1_sets_won += 1
            else:
                team_2_sets_won += 1
        return team_1_sets_won > team_2_sets_won



  
