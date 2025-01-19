from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Match, Team, Tournament, Round
from datetime import date

User = get_user_model()

class MatchTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.force_authenticate(user=self.user1)
        self.team1 = Team.objects.create(player1=self.user1)
        self.team2 = Team.objects.create(player1=self.user2)

    # test of match/
    def test_create_match(self):
        response = self.client.post('/api/match/', {'team_1': self.team1.id, 'team_2': self.team2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(Match.objects.get().team_1, self.team1)
        self.assertEqual(Match.objects.get().team_2, self.team2)
    def test_create_match_same_team(self):
        response = self.client.post('/api/match/', {'team_1': self.team1.id, 'team_2': self.team1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Match.objects.count(), 0)
    def test_create_match_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/match/', {'team_1': self.team1.id, 'team_2': self.team2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Match.objects.count(), 0)
    def test_create_match_no_team(self):
        response = self.client.post('/api/match/', {'team_1': self.team1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Match.objects.count(), 0)
    def test_match_in_bracket_tournament(self):
        self.tournament = Tournament.objects.create(host=self.user1, start_date=date(2022, 1, 1), end_date=date(2022, 1, 2), name='Tournament 1', tournament_type='BRACKET')
        self.round = Round.objects.create(tournament=self.tournament, round_number=1, start_date=date(2022, 1, 1))
        response = self.client.post('/api/match/', {'team_1': self.team1.id, 'team_2': self.team2.id, 'round': self.round.id, 'tournament': self.tournament.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(Match.objects.get().round, self.round)
        self.assertEqual(Match.objects.get().tournament, self.tournament)
    def test_match_in_bracket_tournament_no_round(self):
        self.tournament = Tournament.objects.create(host=self.user1, start_date=date(2022, 1, 1), end_date=date(2022, 1, 2), name='Tournament 1', tournament_type='BRACKET')
        response = self.client.post('/api/match/', {'team_1': self.team1.id, 'team_2': self.team2.id, 'tournament': self.tournament.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Match.objects.count(), 0)
    def test_match_in_americano_no_round(self):
        self.tournament = Tournament.objects.create(host=self.user1, start_date=date(2022, 1, 1), end_date=date(2022, 1, 2), name='Tournament 1', tournament_type='AMERICANO')
        response = self.client.post('/api/match/', {'team_1': self.team1.id, 'team_2': self.team2.id, 'tournament': self.tournament.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertIsNone(Match.objects.get().round)
        self.assertEqual(Match.objects.get().tournament, self.tournament)
    def test_match_in_americano_with_round(self):
        self.tournament = Tournament.objects.create(host=self.user1, start_date=date(2022, 1, 1), end_date=date(2022, 1, 2), name='Tournament 1', tournament_type='AMERICANO')
        self.round = Round.objects.create(tournament=self.tournament, round_number=1, start_date=date(2022, 1, 1))
        response = self.client.post('/api/match/', {'team_1': self.team1.id, 'team_2': self.team2.id, 'round': self.round.id, 'tournament': self.tournament.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Match.objects.count(), 0)

    # test of match/<int:pk>/
    def test_update_score_and_find_winner(self):
        match = Match.objects.create(team_1=self.team1, team_2=self.team2)
        response = self.client.patch(f'/api/match/{match.id}/', {'score_team_1': [6,1,5], 'score_team_2': [5,6,6]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        match.refresh_from_db()
        self.assertEqual(match.status, 'Completed')
        self.assertEqual(match.score_team_1, [6,1,5])
        self.assertEqual(match.score_team_2, [5,6,6])
        self.assertEqual(match.winner, self.team2)

  

