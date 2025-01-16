from django.urls import path, include
from . import views

urlpatterns = [
    path('teams/', views.TeamListCreateView.as_view(), name="team-list-create"),
    path('tournaments/', views.TournamentListCreateView.as_view(), name="tournament-list-create"),
    path('rounds/', views.RoundListCreateView.as_view(), name="round-list-create"),
    # path('tournaments/delete/<int:pk>/', views.TournamentDeleteView.as_view(), name="tournament-delete"),
]
