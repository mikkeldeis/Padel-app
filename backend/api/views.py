from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, TeamSerializer, TournamentSerializer, RoundSerializer
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

    
# class TournamentDeleteView(generics.DestroyAPIView):
#     serializer_class = TournamentSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         user = self.request.user
#         return Tournament.objects.filter(host=user)

