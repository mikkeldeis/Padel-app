from rest_framework import serializers
from .models import User, Team, Match, Tournament, Round

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id","username","password"]
    extra_kwargs = {"password": {"write_only": True}}
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user
  
class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = ["id","player1","player2","wins","losses"]
    extra_kwargs = {
          "player1": {"read_only": True},
          "wins": {"read_only": True},    # Default to 0
          "losses": {"read_only": True}
    }
  def validate(self, data):
    player1 = self.context['request'].user  # player1 is the logged-in user
    player2 = data.get('player2')  # player2 is the user to be added to the team
    # Check if player2 is the same as player1
    if player2 == player1:
        raise serializers.ValidationError(
            {"player2": "Player2 cannot be the same as Player1."}
        )
    return data
  def create(self, validated_data):
    validated_data['player1'] = self.context['request'].user
    return Team.objects.create(**validated_data)
class TournamentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tournament
    fields = ["id","host","start_date","end_date","name","winner","tournament_type"]
    extra_kwargs = {"host": {"read_only": True}, "winner": {"read_only": True}}
  def create(self, validated_data):
    validated_data['host'] = self.context['request'].user
    return Tournament.objects.create(**validated_data)
  def validate(self, data):
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if start_date >= end_date:
        raise serializers.ValidationError(
            {"start_date": "Start date must be before the end date."}
        )
    return data

class RoundSerializer(serializers.ModelSerializer):
  class Meta:
    model = Round
    fields = ["id","tournament","round_number","start_date"]
    extra_kwargs = {"tournament": {"read_only": True}}
  def create(self, validated_data):
    round = Round.objects.create(**validated_data)
    return round

  

# class MatchSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Match
#     fields = ["id","team1","team2","played_at","team1_score","team2_score","team1_set_scores","team2_set_scores","winner"]
#     extra_kwargs = {"team1": {"read_only": True}, "team2": {"read_only": True}, "played_at": {"read_only": True}, "team1_score": {"read_only": True}, "team2_score": {"read_only": True}, "team1_set_scores": {"read_only": True}, "team2_set_scores": {"read_only": True}, "winner": {"read_only": True}}
#   def create(self, validated_data):
#     match = Match.objects.create(**validated_data)
#     return match



  

    