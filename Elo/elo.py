from decimal import Decimal
def calculate_elo(winner_elo, loser_elo, k=20):
    winner_expected = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    loser_expected = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))
    
    winner_elo = winner_elo + k * (1 - winner_expected)
    loser_elo = loser_elo + k * (0 - loser_expected)
    
    return winner_elo, loser_elo

def draw_elo(player1_elo, player2_elo, k=20):
    p1_expected = 1 / (1 + 10 ** ((player2_elo - player1_elo) / 400))
    p2_expected = 1 / (1 + 10 ** ((player1_elo - player2_elo) / 400))
    result= Decimal("0.5")

    player1_elo = player1_elo + k * (result - p1_expected)
    player2_elo = player2_elo + k * (result - p2_expected)

    return player1_elo, player2_elo