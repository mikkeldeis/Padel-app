from django.urls import path, include
from . import views

# 
urlpatterns = [
    path('teams/', views.TeamListCreateView.as_view(), name="team-list-create"),
    path('tournaments/', views.TournamentListCreateView.as_view(), name="tournament-list-create"),
    path('tournaments/<int:pk>/', views.TournamentRetriveView.as_view(), name="tournament-retrieve"),
    path('tournaments/update/<int:pk>/', views.TournamentUpdateView.as_view(), name="tournament-update"),
    path('tournaments/delete/<int:pk>/', views.TournamentDeleteView.as_view(), name="tournament-delete"),
    path('rounds/', views.RoundListCreateView.as_view(), name="round-list-create"),
    path('match/', views.MatchListCreateView.as_view(), name="match-list-create"),
    path('match/<int:pk>/', views.MatchRetrieveUpdateView.as_view(), name="match-retrieve-update"),
]
