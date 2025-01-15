from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, TeamSerializer, TournamentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Team, Match, Tournament
from django.core.exceptions import ValidationError


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
        # Create the tournament instance, but don't save it yet
        tournament = serializer.save(host=self.request.user)

        try:
            # Explicitly call the clean method to perform validation
            tournament.full_clean()  # This will call the `clean` method
        except ValidationError as e:
            # Catch the validation error and return a 400 response
            return Response(
                {'detail': e.message_dict.get('__all__', ['Invalid data'])},
                status=status.HTTP_400_BAD_REQUEST
            )
        # If no error occurs, save the tournament
        tournament.save()
        
# class TournamentDeleteView(generics.DestroyAPIView):
#     serializer_class = TournamentSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         user = self.request.user
#         return Tournament.objects.filter(host=user)

