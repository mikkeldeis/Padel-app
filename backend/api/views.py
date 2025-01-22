from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, TeamSerializer, TournamentSerializer, RoundSerializer, MatchSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Team, Match, Tournament, Round
from rest_framework.exceptions import ValidationError


# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

class TeamListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(player1=user) | Team.objects.filter(player2=user)
    def perform_create(self, serializer):
        serializer.save(player1=self.request.user)

class TournamentListCreateView(generics.ListCreateAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Tournament.objects.filter(host=user)
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
class TournamentUpdateView(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]
    def perform_update(self,serializer):
        serializer.save()
        #TODO add email confirmation. 
class TournamentRetriveView(generics.RetrieveAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]
class TournamentDeleteView(generics.DestroyAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Tournament.objects.filter(host=user)


class RoundListCreateView(generics.ListCreateAPIView):
    serializer_class = RoundSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Round.objects.filter(tournament__host=user)
    def perform_create(self, serializer):
        tournament_id = self.request.data.get('tournament')
        if not tournament_id:
            raise ValidationError({"tournament": "This field is required."})
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            raise ValidationError({"tournament": "Invalid tournament ID."})
        from datetime import datetime

        start_date_str = self.request.data['start_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        # Validate that the round start date is not before the tournament start date
        if start_date < tournament.start_date:
            raise ValidationError({"start_date": "Round start date cannot be before the tournament start date."})
        serializer.save(tournament=tournament)
class MatchListCreateView(generics.ListCreateAPIView):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(Match.objects.filter(team_1=user) | Match.objects.filter(team_2=user))
    def perform_create(self, serializer):
        team_1_id = self.request.data.get('team_1')
        team_2_id = self.request.data.get('team_2')

        if not team_1_id or not team_2_id:
            raise ValidationError({"team_1": "This field is required.", "team_2": "This field is required."})
        try:
            team_1 = Team.objects.get(id=team_1_id)
        except Team.DoesNotExist:
            raise ValidationError({"team_1": "Invalid team ID."})

        try:
            team_2 = Team.objects.get(id=team_2_id)
        except Team.DoesNotExist:
            raise ValidationError({"team_2": "Invalid team ID."})

        if team_1 == team_2:
            raise ValidationError({"team_2": "Team 2 cannot be the same as Team 1."})

        # Pass objects directly to the serializer
        serializer.save(team_1=team_1, team_2=team_2)
class MatchRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    def perform_update(self, serializer):
        match = self.get_object()  # Get the Match instance
        if match.status == 'completed':
            raise ValidationError({"status": "Match is already completed."})

        # Get scores from validated data
        score1 = serializer.validated_data.get('score_team_1')
        score2 = serializer.validated_data.get('score_team_2')

        if score1 and score2:
            match.record_result(score1, score2)  # Call the model's method
        else:
            serializer.save()  # Save other fields if no scores provided
        match.save()








