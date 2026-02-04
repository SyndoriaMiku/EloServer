from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from .match import finish_match
from .models import Player, Match, Tournament, Stage
from .serializers import PlayerSerializer, DrawSerializer, MatchSerializer, BulkMatchSerializer
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
    
class MatchResultView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        
        serializer = MatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        player_a = Player.objects.get(id=data['player_a_id'])
        player_b = Player.objects.get(id=data['player_b_id'])
        
        tournament = None
        if data.get('tournament_id'):
            tournament = Tournament.objects.get(id=data['tournament_id'])
        
        stage = Stage.objects.filter(tournament=tournament, stage_type=data['stage_type']).first()
        if not stage:
            # Auto-create stage for non-tournament matches
            stage = Stage.objects.create(
                tournament=tournament,
                name=f"Casual {data['stage_type'].upper()}",
                stage_type=data['stage_type']
            )
            
        match = Match.objects.create(
            tournament=tournament,
            stage=stage,
            round=data['round'],
            best_of=data['best_of'],
            player_a=player_a,
            player_b=player_b,
            game_wins_a=data['game_wins_a'],
            game_wins_b=data['game_wins_b'],
            status='pending'
        )
        
        finish_match(match)
        
        return Response(
            {'message' : 'Match result processed successfully'},
            status=status.HTTP_201_CREATED
        )
           
    
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = DrawSerializer(data=request.data)
        if serializer.is_valid():
            player1 = serializer.validated_data['p1']
            player2 = serializer.validated_data['p2']

            if player1 == player2:
                return Response({'error' : 'Duplicate ID'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                p1 = Player.objects.get(id=player1)
                p2 = Player.objects.get(id=player2)

            except Player.DoesNotExist:
                return Response({'error' : 'Player does not exist'}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({'token' : token.key}, status=status.HTTP_200_OK)
        else:
            #Unsuccessful login
            return Response({'error' : 'Wrong username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
class BulkMatchView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = BulkMatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        tournament = None
        if data.get('tournament_id'):
            tournament = Tournament.objects.get(id=data['tournament_id'])
        
        stage = Stage.objects.filter(tournament=tournament, stage_type=data['stage_type']).first()
        if not stage:
            # Auto-create stage for non-tournament matches
            stage = Stage.objects.create(
                tournament=tournament,
                name=f"Casual {data['stage_type'].upper()}",
                stage_type=data['stage_type']
            )
        
        created_matches = []
        with transaction.atomic():
            for item in data['matches']:
                player_a = Player.objects.get(id=item['player_a_id'])
                player_b = Player.objects.get(id=item['player_b_id'])
                
                has_result = item.get('game_wins_a', 0) > 0 or item.get('game_wins_b', 0) > 0
                
                match = Match.objects.create(
                    tournament=tournament,
                    stage=stage,
                    round=item['round'],
                    best_of=item['best_of'],
                    player_a=player_a,
                    player_b=player_b,
                    game_wins_a=item.get('game_wins_a', 0),
                    game_wins_b=item.get('game_wins_b', 0),
                    status='pending'
                )
                
                if has_result:
                    finish_match(match)
                
                created_matches.append(match)
                
        return Response(
            {'message' : f'{len(created_matches)} matches created successfully'},
            status=status.HTTP_201_CREATED
        )