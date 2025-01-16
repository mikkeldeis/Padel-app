from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Tournament, Team, Round
from datetime import date

User = get_user_model()

class RoundTests(TestCase):
  
  def setUp(self):
    self.client = APIClient()
    self.host = User.objects.create_user(username='host', password='password')
    self.client.force_authenticate(user=self.host)
    self.tournament = Tournament.objects.create(host=self.host, start_date=date(2022, 1, 1), end_date=date(2022, 1, 2), name='Tournament 1', tournament_type='BRACKET')
  def test_create_round(self):
      response = self.client.post(
          '/api/rounds/',
          {'tournament': self.tournament.id, 'round_number': 1, 'start_date': '2022-01-01'},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Round.objects.count(), 1)
      round = Round.objects.get()
      self.assertEqual(round.tournament, self.tournament)
      self.assertEqual(round.round_number, 1)
      self.assertEqual(round.start_date, date(2022, 1, 1))
  def test_create_round_invalid_dates(self):
          # Invalid start_date (start_date is before tournament start_date)
          response = self.client.post(
              '/api/rounds/',
              {'tournament': self.tournament.id, 'round_number': 1, 'start_date': '2021-12-31'},
              format='json'
          )
          self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
          self.assertEqual(Round.objects.count(), 0)
          self.assertIn('start_date', response.data)  
          self.assertIn('Round start date cannot be before the tournament start date.', response.data['start_date'])
  def test_create_round_unauthenticated(self):
      self.client.force_authenticate(user=None)
      response = self.client.post(
          '/api/rounds/',
          {'tournament': self.tournament.id, 'round_number': 1, 'start_date': '2022-01-01'},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
      self.assertEqual(Round.objects.count(), 0)
  