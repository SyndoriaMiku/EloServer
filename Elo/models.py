from django.db import models
from decimal import Decimal

# Create your models here.

class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    elo = models.DecimalField(default=500.0, decimal_places=1, max_digits=6)
    point = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Tournament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    k_factor = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('upcoming', 'Upcoming'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed')
        ],
        default='upcoming'
    )
    
class Stage(models.Model):
    STAGE_TYPES = [
        ('sw', 'Swiss'),
        ('se', 'Single Elimination'),
        ('rr', 'Round Robin'),
    ]
    tournament = models.ForeignKey(
        Tournament,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    stage_type = models.CharField(max_length=2, choices=STAGE_TYPES)
    
    round_count = models.IntegerField(default=0, null=True, blank=True)
    advance_count = models.IntegerField(default=0, null=True, blank=True)
    
    
class Match(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        null=True, blank=True,
        on_delete=models.SET_NULL)
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE)
    
    player_a = models.ForeignKey(Player, related_name='player_a', null=True, blank=True, on_delete=models.SET_NULL)
    player_b = models.ForeignKey(Player, related_name='player_b', null=True, blank=True, on_delete=models.SET_NULL)
    
    best_of = models.IntegerField(choices=[(1, 'BO1'), (3, 'BO3'), (5, 'BO5')], default=3)
    
    game_wins_a = models.IntegerField(default=0)
    game_wins_b = models.IntegerField(default=0)
    
    @property
    def score_a(self):
        return self.game_wins_a
    
    @property
    def score_b(self):
        return self.game_wins_b
    
    winner = models.ForeignKey(
        Player,
        related_name='match_winner',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    round = models.IntegerField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed')
        ],
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MatchLog(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE)
    
    player_a = models.ForeignKey(
        Player,
        related_name='log_player_a',
        null=True, blank=True,
        on_delete=models.SET_NULL)
    player_b = models.ForeignKey(
        Player,
        related_name='log_player_b',
        null=True, blank=True,
        on_delete=models.SET_NULL)
    
    elo_a_before = models.DecimalField(decimal_places=1, max_digits=6)
    elo_b_before = models.DecimalField(decimal_places=1, max_digits=6)
    
    score_a = models.DecimalField(decimal_places=2, max_digits=3)
    best_of = models.IntegerField()
    stage_type = models.CharField(max_length=2)
    
    created_at = models.DateTimeField(auto_now_add=True)