from django.db import models
from django.contrib.auth.models import User


class Match(models.Model):
  SINGLE = 'S'
  DOUBLE = 'D'
  MATCH_TYPE_CHOICES = [
    (SINGLE, 'Single'),
    (DOUBLE, 'Double'),
  ]

  match_type = models.CharField(
    max_length=1,
    choices=MATCH_TYPE_CHOICES,
    default=SINGLE,
  )
  player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1')
  player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2')
  player3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player3', null=True, blank=True)
  player4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player4', null=True, blank=True)
  player1_score = models.IntegerField()
  player2_score = models.IntegerField()
  player3_score = models.IntegerField(null=True, blank=True)
  player4_score = models.IntegerField(null=True, blank=True)
  date = models.DateTimeField(auto_now_add=True)
  winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner')
  loser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loser')

  def __str__(self):
    return f"{self.player1} vs {self.player2} on {self.date}"
