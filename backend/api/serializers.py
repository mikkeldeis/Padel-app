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
  def update(self, instance, validated_data):
    start_date = validated_data.get('start_date', instance.start_date)
    end_date = validated_data.get('end_date', instance.end_date)
    if start_date >= end_date:
        raise serializers.ValidationError(
            {"start_date": "Start date must be before the end date."}
        )
    instance.start_date = start_date
    instance.end_date = end_date
    instance.name = validated_data.get('name', instance.name)
    instance.tournament_type = validated_data.get('tournament_type', instance.tournament_type)
    instance.save()
    return instance

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
#     fields = ["id","round","team_1","team_2","date","status","score_team_1","score_team_2","winner"]
#     extra_kwargs = {
#         "winner": {"read_only": True},
#         "score_team_1": {"required": False},
#         "score_team_2": {"required": False},
#     }
#   def create(self, validated_data):
#     match = Match.objects.create(**validated_data)
#     return match
#   def validate(self, data):
#     team_1 = data.get('team_1')
#     team_2 = data.get('team_2')
#     if team_1 == team_2:
#         raise serializers.ValidationError(
#             {"team_2": "Team 2 cannot be the same as Team 1."}
#         )
#     return data
#   def update(self, instance, validated_data):
    # instance.score_team_1 = validated_data.get('score_team_1', instance.score_team_1)
    # instance.score_team_2 = validated_data.get('score_team_2', instance.score_team_2)
    # instance.winner = validated_data.get('winner', instance.winner)
    # instance.save()
    # return instance
  



  

    