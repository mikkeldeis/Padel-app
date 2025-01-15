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
  def test_create_tournament(self):
      response = self.client.post(
          '/api/tournaments/',
          {'start_date': '2022-01-01', 'end_date': '2022-01-02', 'name': 'Tournament 1', 'tournament_type': 'BRACKET'},
          format='json'
      )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Tournament.objects.count(), 1)

      # Get the tournament that was created
      tournament = Tournament.objects.get()

      # Check if the start_date is correct
      self.assertEqual(tournament.start_date, date(2022, 1, 1))  # compare with datetime.date object
      self.assertEqual(tournament.end_date, date(2022, 1, 2))    # compare with datetime.date object
      self.assertEqual(tournament.name, 'Tournament 1')
      self.assertIsNone(tournament.winner)
      self.assertEqual(tournament.tournament_type, 'BRACKET')
  def test_create_tournament_invalid_dates(self):
          # Invalid start_date and end_date (start_date is after end_date)
          response = self.client.post(
              '/api/tournaments/',
              {'start_date': '2022-01-02', 'end_date': '2022-01-01', 'name': 'Tournament 1', 'tournament_type': 'BRACKET'},
              format='json'
          )
          self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # It should return a 400 Bad Request
          self.assertEqual(Tournament.objects.count(), 0)  # Tournament should not be created
          self.assertIn('start_date', response.data)  # The field 'start_date' should have an error
          self.assertEqual(response.data['start_date'][0], 'Start date must be before the end date.')  # Correct error message
