from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Team

User = get_user_model()

class TeamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.force_authenticate(user=self.user1)

    def test_create_single_player_team(self):
      response = self.client.post(
          '/api/teams/',
          {'player2': None},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Team.objects.count(), 1)
      self.assertEqual(Team.objects.get().player1, self.user1)
      self.assertIsNone(Team.objects.get().player2)
      self.assertEqual(Team.objects.get().wins, 0)  # Assert default value
      self.assertEqual(Team.objects.get().losses, 0)  # Assert default value
    def test_create_double_team(self):
      response = self.client.post(
          '/api/teams/',
          {'player2': self.user2.id},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Team.objects.count(), 1)
      self.assertEqual(Team.objects.get().player1, self.user1)
      self.assertEqual(Team.objects.get().player2, self.user2)
      self.assertEqual(Team.objects.get().wins, 0)
      self.assertEqual(Team.objects.get().losses, 0)  # Assert default value
    def test_create_double_team_same_player(self):
      response = self.client.post(
          '/api/teams/',
          {'player2': self.user1.id},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      self.assertEqual(Team.objects.count(), 0)
    def test_get_teams(self):
      response = self.client.get('/api/teams/')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data, [])
      team = Team.objects.create(player1=self.user1)
      response = self.client.get('/api/teams/')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data, [{'id': team.id, 'player1': self.user1.id, 'player2': None, 'wins': 0, 'losses': 0}])
    def test_get_teams_with_player2(self):
      team = Team.objects.create(player1=self.user1, player2=self.user2)
      response = self.client.get('/api/teams/')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data, [{'id': team.id, 'player1': self.user1.id, 'player2': self.user2.id, 'wins': 0, 'losses': 0}])

       
