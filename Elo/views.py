from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Player
from .serializers import PlayerSerializer, ResultSerializer
from .elo import calculate_elo
from django.db import models
from django.db.models import Q



# Create your views here.

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def create(self, request, *args, **kwargs):
        player_id = request.data['id']
        if Player.objects.filter(id=player_id).exists():
            return Response({'error' : 'Player already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
class ResultView(APIView):
    def post(self, request):
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            winner = serializer.validated_data['winner']
            loser = serializer.validated_data['loser']
            
            try:
                winner = Player.objects.get(id=winner)
                loser = Player.objects.get(id=loser)
            except Player.DoesNotExist:
                return Response({'error' : 'Player does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except winner == loser:
                return Response({'error' : 'Duplicate ID'}, status=status.HTTP_400_BAD_REQUEST)
            
            #Calculate new elo
            winner_elo, loser_elo = calculate_elo(winner.elo, loser.elo)
            
            #Update elo in database
            winner.elo = winner_elo
            loser.elo = loser_elo
            winner.save()
            loser.save()
            
            return Response({'message' : 'Elo updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetNewIDView(APIView):
    def get(self, request):
        max_id = Player.objects.all().aggregate(models.Max('id'))['id__max']
        
        #If no players exist, return 1
        max_id = max_id if max_id is not None else 0
        
        next_id = max_id + 1
        return Response({'id' : next_id})
    
class PlayerFilterView(generics.ListAPIView):
    serializer_class = PlayerSerializer
    
    def get_queryset(self):
        queryset = self.request.query_params.get('query', '')
        
        players = Player.objects.filter(Q(id__icontains=queryset) | Q(name__icontains=queryset))
        return players
        
                