from rest_framework import serializers
from .models import Player

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
    