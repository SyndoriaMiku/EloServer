from rest_framework import serializers
from .models import Player, Match, Tournament, Stage, MatchLog

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class ResultSerializer(serializers.Serializer):
    winner = serializers.IntegerField()
    loser = serializers.IntegerField()
    
class DrawSerializer(serializers.Serializer):
    p1 = serializers.IntegerField()
    p2 = serializers.IntegerField()
    
    
class MatchSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField(required=False, allow_null=True)
    stage_type = serializers.CharField()
    round = serializers.IntegerField()
    best_of = serializers.ChoiceField(choices=[1, 3, 5])
    
    player_a_id = serializers.IntegerField()
    player_b_id = serializers.IntegerField()
    
    game_wins_a = serializers.IntegerField(default=0)
    game_wins_b = serializers.IntegerField(default=0)
    
    def validate(self, data):
        bo = data.get('best_of')
        win_needed = (bo // 2) + 1
        
        a = data.get('game_wins_a', 0)
        b = data.get('game_wins_b', 0)
        
        if a == b:
            if a != 0:
                raise serializers.ValidationError("Match cannot end in a draw")
        else:
            if a < win_needed and b < win_needed:
                raise serializers.ValidationError("No player has enough wins to finish the match")
            if a > win_needed or b > win_needed:
                raise serializers.ValidationError("Invalid game wins")
        
        return data

class BulkMatchItemSerializer(serializers.Serializer):
    round = serializers.IntegerField()
    best_of = serializers.ChoiceField(choices=[1, 3, 5])
    
    player_a_id = serializers.IntegerField()
    player_b_id = serializers.IntegerField()
    
    game_wins_a = serializers.IntegerField(default=0)
    game_wins_b = serializers.IntegerField(default=0)
    
    def validate(self, data):
        bo = data.get('best_of')
        win_needed = (bo // 2) + 1
        
        a = data.get('game_wins_a', 0)
        b = data.get('game_wins_b', 0)
        
        if a == b:
            if a != 0:
                raise serializers.ValidationError("Match cannot end in a draw")
        else:
            if a < win_needed and b < win_needed:
                raise serializers.ValidationError("No player has enough wins to finish the match")
            if a > win_needed or b > win_needed:
                raise serializers.ValidationError("Invalid game wins")
        
        return data
    
class BulkMatchSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField(required=False, allow_null=True)
    stage_type = serializers.CharField()
    matches = BulkMatchItemSerializer(many=True)
    
    def validate(self, value):
        if len(value.get('matches', [])) == 0:
            raise serializers.ValidationError("Match list cannot be empty")
        return value