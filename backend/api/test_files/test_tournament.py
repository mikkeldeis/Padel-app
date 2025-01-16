from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Tournament, Team
from datetime import date

User = get_user_model()

class TournamentTests(TestCase):

  def setUp(self):
    self.client = APIClient()
    self.host = User.objects.create_user(username='host', password='password')
    self.client.force_authenticate(user=self.host)
  def test_create_tournament_bracket(self):
      response = self.client.post(
          '/api/tournaments/',
          {'start_date': '2022-01-01', 'end_date': '2022-01-02', 'name': 'Tournament 1', 'tournament_type': 'BRACKET'},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Tournament.objects.count(), 1)
      tournament = Tournament.objects.get()
      self.assertEqual(tournament.start_date, date(2022, 1, 1)) 
      self.assertEqual(tournament.end_date, date(2022, 1, 2))   
      self.assertEqual(tournament.name, 'Tournament 1')
      self.assertIsNone(tournament.winner)
      self.assertEqual(tournament.tournament_type, 'BRACKET')
  def test_create_tournament_Americano(self):
      response = self.client.post(
          '/api/tournaments/',
          {'start_date': '2022-01-01', 'end_date': '2022-01-02', 'name': 'Tournament 1', 'tournament_type': 'AMERICANO'},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Tournament.objects.count(), 1)
      tournament = Tournament.objects.get()
      self.assertEqual(tournament.start_date, date(2022, 1, 1)) 
      self.assertEqual(tournament.end_date, date(2022, 1, 2))   
      self.assertEqual(tournament.name, 'Tournament 1')
      self.assertIsNone(tournament.winner)
      self.assertEqual(tournament.tournament_type, 'AMERICANO')
  def test_create_tournament_invalid_dates(self):
          # Invalid start_date and end_date (start_date is after end_date)
          response = self.client.post(
              '/api/tournaments/',
              {'start_date': '2022-01-02', 'end_date': '2022-01-01', 'name': 'Tournament 1', 'tournament_type': 'BRACKET'},
              format='json'
          )
          self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
          self.assertEqual(Tournament.objects.count(), 0)
          self.assertIn('start_date', response.data)  
          self.assertEqual(response.data['start_date'][0], 'Start date must be before the end date.') 
  def test_create_tournament_unauthenticated(self):
      self.client.force_authenticate(user=None)
      response = self.client.post(
          '/api/tournaments/',
          {'start_date': '2022-01-01', 'end_date': '2022-01-02', 'name': 'Tournament 1', 'tournament_type': 'BRACKET'},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
      self.assertEqual(Tournament.objects.count(), 0)
  
