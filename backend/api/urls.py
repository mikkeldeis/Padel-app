from django.urls import path, include
from . import views

urlpatterns = [
    path('teams/', views.TeamListCreateView.as_view(), name="team-list-create"),
    path('tournaments/', views.TournamentListCreateView.as_view(), name="tournament-list-create"),
    # path('tournaments/', views.TournamentListCreateView.as_view(), name="tournament-list"),
    # path('tournaments/delete/<int:pk>/', views.TournamentDeleteView.as_view(), name="tournament-delete"),
]
