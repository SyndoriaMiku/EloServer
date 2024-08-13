from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Player
from .serializers import PlayerSerializer, ResultSerializer, DrawSerializer
from .elo import calculate_elo, draw_elo
from django.db import models
from django.db.models import Q
from rest_framework.authtoken.models import Token



# Create your views here.

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def create(self, request, *args, **kwargs):
        player_id = request.data['id']
        if Player.objects.filter(id=player_id).exists():
            return Response({'error' : 'Player already exists'}, status=status.HTTP_400_BAD_REQUEST)
        response = super().create(request, *args, **kwargs)
        return response
    
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
        
class DrawView(APIView):
    def post(self, request):
        serializer = DrawSerializer(data=request.data)
        if serializer.is_valid():
            player1 = serializer.validated_data['p1']
            player2 = serializer.validated_data['p2']

            try:
                p1 = Player.objects.get(id=player1)
                p2 = Player.objects.get(id=player2)

            except Player.DoesNotExist:
                return Response({'error' : 'Player does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except p1 == p2:
                return Response({'error' : 'Duplicate ID'}, status=status.HTTP_400_BAD_REQUEST)

            #Calculate new elo
            p1_elo, p2_elo = draw_elo(p1.elo, p2.elo)

            #Update elo in database
            p1.elo = p1_elo
            p2.elo = p2_elo

            p1.save()
            p2.save()
            return Response({'message' : 'Elo updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
        
class LoginView(APIView):
    def post(self, request):
        #Get username and password from request
        username = request.data.get('username')
        password = request.data.get('password')
        
        #Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            #Successful login
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token' : 'token.key'}, status=status.HTTP_200_OK)
        else:
            #Unsuccessful login
            return Response({'error' : 'Wrong username or password'}, status=status.HTTP_400_BAD_REQUEST)