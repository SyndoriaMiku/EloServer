from .models import Match, Player, MatchLog
from .elo import calculate_elo, match_score

def finish_match(match: Match):
    if match.status == 'completed':
        raise ValueError("Match is already completed.")
    
    win_needed = (match.best_of // 2) + 1
    if match.game_wins_a >= win_needed:
        match.winner = match.player_a
    elif match.game_wins_b >= win_needed:
        match.winner = match.player_b
    else:
        raise ValueError("Match cannot be finished yet; no player has enough wins.")
    
    match.status = 'completed'
    match.save()
    
    #Elo processing
    player_a = match.player_a
    player_b = match.player_b
    
    elo_a_before = player_a.elo
    elo_b_before = player_b.elo
    
    score_a = match_score(match.game_wins_a, match.game_wins_b, match.best_of)

    new_elo_a, new_elo_b = calculate_elo(
        player_a.elo,
        player_b.elo,
        score_a,
        match.tournament.k_factor if match.tournament else 20
    )
    
    MatchLog.objects.create(
        match=match,
        player_a=player_a,
        player_b=player_b,
        elo_a_before=elo_a_before,
        elo_b_before=elo_b_before,
        score_a=score_a,
        best_of=match.best_of,
        stage_type=match.stage.stage_type,
    )
    
    #Update player Elo ratings
    player_a.elo = new_elo_a
    player_b.elo = new_elo_b
    player_a.save()
    player_b.save()
    