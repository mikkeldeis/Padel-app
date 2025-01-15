# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from api.models import Match, Team

# User = get_user_model()

# class MatchTests(TestCase):
#   def setUp(self):
#     self.client = APIClient()
#     self.user1 = User.objects.create_user(username='user1', password='password')
#     self.user2 = User.objects.create_user(username='user2', password='password')
#     self.client.force_authenticate(user=self.user1)
#     self.team1 = Team.objects.create(player1=self.user1)
#     self.team2 = Team.objects.create(player1=self.user2)
#   def test_create_match(self):
#     response = self.client.post(
#       '/api/matches/',
#       {'team1': self.team1.id, 'team2': self.team2.id},
#       format='json'
#     )
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     self.assertEqual(Match.objects.count(), 1)
#     self.assertEqual(Match.objects.get().team1, self.team1)
#     self.assertEqual(Match.objects.get().team2, self.team2)
#     self.assertIsNone(Match.objects.get().winner)
#     self.assertIsNone(Match.objects.get().loser)
#     self.assertIsNone(Match.objects.get().date)